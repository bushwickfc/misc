#!/usr/bin/env python

import argparse
import csv
import pprint

import editdistance

parser = argparse.ArgumentParser()

parser.add_argument("members", help="members db csv")
parser.add_argument("pos", help="pos tsv")
parser.add_argument("output", help="output csv")

args = parser.parse_args()

pp = pprint.PrettyPrinter(indent=4)

def member_key(m):
    return (m['FIRST NAME'] + m['LAST NAME']).lower().replace(" ", "")

def pos_key(p):
    return (p['FIRSTNAME'] + p['LASTNAME']).replace(" ", "").lower()

def pos_key_alternative(p):
    return p['NAME'].split("//")[0].replace(" ","").lower()

def matching(members, pos, pos_alt):
    matches = {}
    for key in list(members.keys()):
        if key in pos:
            matches[members[key]['MEMBER NUMBER']] = { 'pos': pos[key], 'member': members[key] }
        elif key in pos_alt:
            matches[members[key]['MEMBER NUMBER']] = { 'pos': pos_alt[key], 'member': members[key] }
    return matches

def possible_match(matches, key):
    if key in matches:
        pos = matches[key]['pos']
        member = matches[key]['member']
        return [key, pos['ID'],
                member['FIRST NAME'] + ' ' + member['LAST NAME'],
                pos['FIRSTNAME'] + pos['LASTNAME']]
    else:
        return ['','','','']

def find_distance(non_matching, pos, distance):
    keys = pos.keys()
    for i in range(1, distance+1):
        found = next((key for key in keys if editdistance.eval(non_matching, key) <= i), None)
        if found:
          return found

with open(args.members, newline='') as members_file:
    with open(args.pos, newline='') as pos_file:
        members_reader = csv.DictReader(members_file)
        pos_reader = list(csv.DictReader(pos_file, delimiter='\t'))
        members = { member_key(m): m for m in members_reader }
        pos = { pos_key(p) : p for p in pos_reader }
        pos_alt = { pos_key_alternative(p) : p for p in pos_reader }
        matches = matching(members, pos, pos_alt)
        nonmatching_members = [key for key in list(members.keys())
                               if key not in pos]
        nonmatching_pos = [key for key in list(pos.keys())
                           if key not in members]
        with open(args.output, 'w', newline='') as outfile:
            out = csv.writer(outfile)
            keys = sorted(map(int, matches.keys()))
            max_key = keys[-1]
            out.writerow(['MEMBER NUMBER', 'POS ID','MEMBER NAME', 'POS NAME'])
            [out.writerow(possible_match(matches, str(i)))
             for i in range(1, int(max_key)+1)]
            out.writerow(['Non matching'])
            out.writerow(['MEMBER NUMBER', 'FIRST NAME', 'LAST NAME'])
            [out.writerow([members[key]['MEMBER NUMBER'],
                          members[key]['FIRST NAME'],
                           members[key]['LAST NAME']]) for key
                          in nonmatching_members]
        l_matches = [x for x in [(key, find_distance(key, pos, 3))
                     for key in nonmatching_members] if x[1]]
        def print_l_match(m_key, p_key):
            m = members[m_key]
            p = pos[p_key]
            print(m['MEMBER NUMBER'], p['ID'],
                  m['FIRST NAME'] + ' ' + m['LAST NAME'],
                  p['FIRSTNAME'] + ' ' + p['LASTNAME'])
        [print_l_match(m_key, p_key) for (m_key, p_key) in l_matches]
        print("Non matching:", len(nonmatching_members) - len(l_matches))
        print("Matching:", len(matches))
        print("L Matches:", len(l_matches))
