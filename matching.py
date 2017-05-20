#!/usr/bin/env python

import argparse
import csv
import pprint

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

def matching(members, pos):
    matches = {}
    for key in list(members.keys()):
        if key in pos:
            matches[members[key]['MEMBER NUMBER']] = { 'pos': pos[key], 'member': members[key] }
    return matches

def possible_match(matches, key):
    if key in matches:
        pos = matches[key]['pos']
        member = matches[key]['member']
        return [key, pos['ID'], pos['NAME'],
                member['FIRST NAME'] + ' ' + member['LAST NAME']]
    else:
        return ['','','','']

with open(args.members, newline='') as members_file:
    with open(args.pos, newline='') as pos_file:
        members_reader = csv.DictReader(members_file)
        pos_reader = csv.DictReader(pos_file, delimiter='\t')
        members = { member_key(m): m for m in members_reader }
        pos = { pos_key(p) : p for p in pos_reader }
        matches = matching(members, pos)
        nonmatching_members = [key for key in list(members.keys())
                               if key not in pos]
        nonmatching_pos = [key for key in list(pos.keys())
                           if key not in members]
        with open(args.output, 'w', newline='') as outfile:
            out = csv.writer(outfile)
            keys = sorted(matches.keys())
            max_key = keys[-1]
            out.writerow(['MEMBER NUMBER', 'POS ID', 'POS NAME', 'MEMBER NAME'])
            [out.writerow(possible_match(matches, str(i)))
             for i in range(1, int(max_key)+1)]
            out.writerow(['Non matching'])
            out.writerow(['MEMBER NUMBER', 'FIRST NAME', 'LAST NAME'])
            [out.writerow([members[key]['MEMBER NUMBER'],
                          members[key]['FIRST NAME'],
                           members[key]['LAST NAME']]) for key
                          in nonmatching_members]
        print("Non matching: ", len(nonmatching_members))
        print("Matching: ", len(matches))
