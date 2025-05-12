# Generate ADIDO template

Create `index-adido-template.html` as a copy of `index-htmx.html`.

## Step 1 of the app should be kept.
No need to load `TDI GI Pipeline` data.

Additional data readings: Once metadata is loaded, read the following additional sheets:
- Adhoc Data-In
- Adhoc Data-Out
into a new data structure - `adhoc_data`.

Column mapping to local object `adhoc_data_item`:
```json
{
  "Status": "status",
  "Team Requesting": "team_requesting",
  "Sub-Team requesting": "sub_team_requesting",
  "Also requested by other LOB?": "also_requested_by_other_lob",
  "New/Existing Initiative": "initiative_status",
  "File Name": "file_name",
  "Data Out Purpose": "data_out_purpose",
  "Type of Data Out": "data_out_type",
  "Frequency": "frequency",
  "Process Name": "process_name",
  "Recipient (Internal/External)": "recipient",
  "Recipient Name": "recipient_name",
  "Contain PII?": "contains_pii",
  "If External - Please specify 3rd party": "external_third_party",
  "Is the Recipient from another AZ": "recipient_from_another_az",
  "Will it be used in Use-cases?": "used_in_usecases",
  "Usecase SME": "usecase_sme",
  "Impact": "impact",
  "File Type": "file_type",
  "Retention Code (EDGO) (If not sure, please check with the Data Steward)": "retention_code",
  "Retention Period": "retention_period",
  "Impacted Jurisdiction Country (refer to EDC for correct name)": "jurisdiction_country",
  "Impacted Jurisdiction Province (refer to EDC for correct name)": "jurisdiction_province"
}
```
Add one more column (at first position): `data_source` with value "data_in" or "data_out" based on the source sheet name.


## Step 2
Rreplace existing Step 2 and its functionality with the completely new functionality.
New Step 2 would be to load a "ADIDO Metadata Template.xlsx" (aka `adido_template`) excel file.
UI: Card title: "Step 2", info box: "Load ADIDO Metadata Template files", button: "Load ADIDO Template".
Place at the same position as old Step 2 card. Simply replaces old Step 2.

## Step 3
New Step 3 would be to select files from `adido_metadata` list and fill out the `adido_template` based on the selected files.

UI: 
- Card title: "Step 3"
- info box: "Select files to generate ADIDO template"
- Table: list of report files from `adido_data` with checkboxes (columns: Selection, Source, File Name)
- Submit button: "Generate ADIDO template" (placed below the table, centered)
Card is placed below Step1 and 2, and takes whole width. 

Submit button produces two lists:

### `tpl_fields` - List of fields
This list is the `adido_metadata` list filtered to keep only `report_file` that user selected.
```python
_ = ["report_file", "field_name", "business_description", "classification", "pci", "pi", "treatment"]
```
This list is then ingested into `adido_template` excel file on the `Field Metadata` sheet at cell `A6`.

### `tpl_files` - List of files
For each `report_file` user selected, get matching record from `adhoc_data` whose `file_name` match user's selection.
New list contains calculated values and has following columns:
- file_name - from `adhoc_data`
- file_type - from `adhoc_data`
- business_description - from `adhoc_data`
- classification - calculated based on highest classification of all fields in the file (same file_name). Order: Critical > Restricted > Confidential > Internal > Public
- pci - calculated based on highest pci value of all fields in the file (same file_name). If any field has pci = yes, then file has pci = yes
- pi - calculated based on highest pi value of all fields in the file (same file_name). If any field has pi = yes, then file has pi = yes
- retention_code - from `adhoc_data`
- retention_period - from `adhoc_data`
- jurisdiction_country - from `adhoc_data`
- jurisdiction_province - from `adhoc_data`
- delimiter - always empty
- line_length - always empty

This list is then ingested into `adido_template` excel file on the `File Metadata` sheet at cell `A4`.


Once both lists are generated, `adido_template` is saved to user's local disk.

