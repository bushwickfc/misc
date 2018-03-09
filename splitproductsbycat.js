// These scripts contain utilities to manage Inventory.

var MAIN_PRODUCT_SHEET = "master";

// Creates a separate tab for each category name in the main sheet/tab.
function createSubSheets() {
  var categoryNames = [];
  var lastCategory = "";
  var lastChange = 2;
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var ms = ss.getSheetByName(MAIN_PRODUCT_SHEET);
  var lastRow = ms.getLastRow();
  var lastCol = String.fromCharCode(65+ms.getLastColumn());
  console.log("Last Row " + lastRow);
  console.log("Last Col " + lastCol);
  var values = ms.getRange("A2:A"+lastRow).getValues();
  for (var i = 2; i <= lastRow; i++) {
    var j = Math.round(i);
    // Values is offset by header row and 1-based indexing
    // It's a single-item list
    var value = values[j-2][0];
    if (lastCategory == "") {
      lastCategory = value;
      lastChange = 2;
    } else if (lastCategory != value && value != "") {
      // Use the old category first
      categoryNames.push(lastCategory);
      ss.insertSheet(lastCategory);
      console.log("Inserted new category: " + lastCategory);
      var ns = ss.getActiveSheet();
      var bodyTargetRange = ss.getRange(ns.getName()+"!A2"+":"+lastCol+(j - lastChange + 2));
      var headerTargetRange = ss.getRange(ns.getName()+"!A1:"+lastCol+"1");
      ms.getRange("A"+lastChange+":"+lastCol+(j-1)).copyTo(bodyTargetRange);
      ms.getRange("A1:"+lastCol+"1").copyTo(headerTargetRange);
      // Last, update the category and last change for next change.
      lastCategory = value;
      lastChange = j; // Update the row of the last category change
    }
  }
}

function deleteSheets() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheets = ss.getSheets();
  for (var i = 0; i < sheets.length; i++) {
    if (sheets[i].getName() != MAIN_PRODUCT_SHEET) {
      ss.deleteSheet(sheets[i]);
    }
  }
}

