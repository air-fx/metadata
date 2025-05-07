# Overview

This app is a web interface that helps classify data extraction fields.

User inputs a list of field names they are going to output in their report (data extraction).

Web-page finds matches by field name and display its classification.

There are 2 csv files that contain fields metadata:

1. `already_requested_metadata` - contains fields that are already requested by users.
File is in excel format. Data sheet name: `ADIDO Metadata`.
This file has higher priority than `metadata` list. 
This list contains previously requested report name, field name and field's metadata (classification).
File schema (required fields only, there are more on the sheet):
- File Name
- Field Name
- Business Description
- Classification
- PCI
- PI
- Data Treatment
Use following schema for internal objects:
- report_file  -- consider that it's a Source
- field_name  -- consider that it's a Source Field Name
- classification
- pi
- pci
- treatment

2. `metadata` - contains all fields in the system along with the table name it can be found in.
That's an excel file. Data sheet name: `TDI GI Pipeline`.
File schema (required fields only, there are more on the sheet):
- table_path
- Object Type
- Name 
- Business Description
- Security Classification
- PCI-DSS
- PI
- Data Treatment
Use following schema for internal objects:
- table_path -- consider that it's a Source
- objet_type
- field_name -- consider that it's a Source Field Name
- classification
- pi
- pci
- treatment

Once user entered field names, the app will search for field name matches and display the results.
Results table should contain following columns:
- Source - existing report name (if found in already_requested_metadata.csv) or table name if found in tables list (metadata.csv).
- Source Field Name -- initially the same value as Field Name. However if user selected different field from the Quick Search Popup, this column will be updated with the selected field name.
- Field Name
- Classification
- PCI
- PI
- Treatment
- button: Auto - that's the default behaviour when system looks for this field in the existing reports, and if not found - in the tables list.
- button: Search

Search button opens a popup with 2 input fields for a quick filter and a table with 10 rows and a scrolling (if required) displays results.
Input fields are:
- Field Name
- Source - source can be a report name (if found in already_requested_metadata.csv) or table name if found in tables list (metadata.csv). 

Popup results table should contain following columns:
- Source (report name or table name where the field was found)
- Field Name
- Classification
- PCI
- PI
- Treatment
- button: Select -- clicking on this button will select the field and fill in the main results table, then automatically close the popup.


User can select fields from the dropdown and export the results.
Export button offers to download a csv with selected fields from the screen (should be the same structure as metadata.csv file).

