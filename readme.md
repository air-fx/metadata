# Overview

This app is a web interface that helps classify data extraction fields.

User inputs a list of field names they are going to output in their report (data extraction).

Web-page finds matches by field name and display its classification.

There are 2 csv files that contain metadata:
1. already_requested_metadata.csv - contains fields that are already requested by users. This file has higher priority than metadata.csv. This list contains previously requested report name, field name and field's metadata (classification).
2. metadata.csv - contains all fields in the system along with the table name it can be found in. 

Once user entered field names, the app will search for field name matches and display the results.
Results table should contain following columns:
- Source - existing report name (if found in already_requested_metadata.csv) or table name if found in tables list (metadata.csv). 
- Field name
- Classification
- PI
- PCI
- Treatment
- button: Auto - that's the default behaviour when system looks for this field in the existing reports, and if not found - in the tables list.
- button: Search

Search button opens a popup with 2 input fields for a quick filter and a table with 10 rows and a scrolling (if required) displays results.
Input fields are:
- Field name
- Source - source can be a report name (if found in already_requested_metadata.csv) or table name if found in tables list (metadata.csv). 

Results table should contain following columns:
- Source (report name or table name where the field was found)
- Field name
- Classification
- PI
- PCI
- Treatment
- button: Select -- clicking on this button will select the field and fill in the main results table, then automatically close the popup.


User can select fields from the dropdown and export the results.
Export button offers to download a csv with selected fields from the screen (should be the same structure as metadata.csv file).