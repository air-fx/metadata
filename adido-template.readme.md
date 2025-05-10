# ADIDO Template Generator

## Overview

The ADIDO Template Generator is a web-based tool that helps users generate ADIDO (Adhoc Data In/Data Out) templates for data governance and compliance. It automates the process of collecting metadata about data fields and files, and populates standardized templates with this information.

## Features

- Load metadata from Excel files containing ADIDO Metadata and Adhoc Data sheets
- Use a built-in default ADIDO template or load your own custom template
- Select specific files to include in the template generation
- Filter the file list to quickly find relevant files
- Validate data quality with warning notifications for invalid values
- Generate completed ADIDO templates ready for submission

## How to Use

### Step 1: Load Use Case File

1. Click the "Browse" button in the Step 1 card
2. Select an Excel (.xlsx) file containing:
   - ADIDO Metadata sheet: Contains field-level metadata
   - Adhoc Data-In sheet: Contains information about incoming data files
   - Adhoc Data-Out sheet: Contains information about outgoing data files
3. The application will display the number of records loaded from each sheet

### Step 2: Load ADIDO Template

1. Either:
   - Click "Use Default Template" to use the built-in template, or
   - Select "Or use custom" to upload your own ADIDO Template Excel file (.xlsx)
2. Enter the AZ Name in the text field provided (this will be included in the generated template)
3. The template must contain:
   - Field Metadata sheet: Will be populated with field-level information
   - File Metadata sheet: Will be populated with file-level information
4. A success message will appear when the template is loaded

### Step 3: Select Files for ADIDO

1. Browse the list of files from the Adhoc Data sheets
2. Use the filter box to search for specific files (requires at least 2 characters)
3. Click on rows or checkboxes to select files for inclusion in the template
4. Selected files will appear in the "Selected Files" panel

### Step 4: Generate ADIDO Template

1. Review your selected files in the "Selected Files" panel
2. Click "Generate ADIDO template" to create the populated template
3. The application will:
   - Extract field metadata for the selected files
   - Calculate file-level metadata based on the fields
   - Populate the template with this information
   - Save the completed template to your device

## Technical Details

### Technology Stack

- **Frontend**: HTML, CSS, JavaScript
- **Libraries**:
  - Alpine.js (v3.13.0): For reactive data binding and UI state management
  - XLSX-Populate (v1.21.0): For Excel file handling
  - Pico CSS (v1.5.10): For basic styling

### Data Models

#### ADIDO Metadata Schema

Required fields in the Excel file:
- `File Name`: Report name (Source)
- `Field Name`: Field name (Source Field Name)
- `Business Description`: Description of the field
- `Classification`: Security classification
- `PCI`: PCI-DSS status (boolean)
- `PI`: Personal Information status (boolean)
- `Data Treatment`: Required data treatment

Internal object schema:
```javascript
{
  report_file: string,  // Source
  field_name: string,   // Source Field Name
  business_description: string,
  classification: string,
  pi: boolean,
  pci: boolean,
  treatment: string
}
```

#### Adhoc Data Schema

Required fields in the Excel file:
- `Status`: Current status of the request
- `Team Requesting`: Team that requested the data
- `Sub-Team requesting`: Sub-team that requested the data
- `Also requested by other LOB?`: Whether other lines of business requested the data
- `New/Existing Initiative`: Whether this is a new or existing initiative
- `File Name`: Name of the file
- `Data Out Purpose`: Purpose of the data output
- `Type of Data Out`: Type of data output
- `Frequency`: Frequency of data transfer
- `Process Name`: Name of the process
- `Recipient`: Recipient of the data
- `Recipient Name`: Name of the recipient
- `Contain PII?`: Whether the data contains PII
- `If External - Please specify 3rd party`: Third party details if external
- `is the Recipient from another AZ`: Whether recipient is from another AZ
- `Will it be used in Use-cases?`: Whether data will be used in use cases
- `Usecase SME`: Subject matter expert for the use case
- `Impact`: Impact of the data

Internal object schema (with data_source added):
```javascript
{
  data_source: string,  // 'data_in' or 'data_out'
  status: string,
  team_requesting: string,
  sub_team_requesting: string,
  also_requested_by_other_lob: string,
  initiative_status: string,
  file_name: string,
  data_out_purpose: string,
  data_out_type: string,
  frequency: string,
  process_name: string,
  recipient: string,
  recipient_name: string,
  contains_pii: string,
  external_third_party: string,
  recipient_from_another_az: string,
  used_in_usecases: string,
  usecase_sme: string,
  impact: string,
  // ... additional fields as per mapping
}
```

### Default Template Implementation

The application includes a built-in default ADIDO template that is embedded as a base64-encoded string. This provides users with a convenient option while still allowing them to upload custom templates.

#### How the Default Template Works:

1. The Excel template file is converted to a base64 string using a Python script:

   [xlsx2base64.py](src/xlsx2base64.py)
   ```python
   import base64

   # Path to Excel template file
   fname = "../data/ADIDO Metadata Template_base64"
   excel_file_path = f'{fname}.xlsx'
   
   # Read the Excel file in binary mode
   with open(excel_file_path, 'rb') as file:
       excel_data = file.read()
   
   # Convert to base64
   base64_encoded = base64.b64encode(excel_data)
   
   # Convert bytes to string for easier handling
   base64_string = base64_encoded.decode('utf-8')
   
   # Print to console
   print(base64_string)
   
   # Optionally save to a file
   with open(f"{fname}_base64.txt", 'w') as output_file:
       output_file.write(base64_string)
   
   print(f"Base64 encoding complete. Output saved to {fname}_base64.txt")
   ```

2. The base64 string is stored in the application code
3. When the user clicks "Use Default Template", the application:
   - Converts the base64 string back to binary
   - Loads it using XLSX-Populate
   - Processes it the same way as an uploaded template

### Template Generation Process

1. **Field Metadata Generation**:
   - Set the AZ Name in cell B3 of the Field Metadata sheet
   - Filter `adido_metadata` to include only fields from selected files
   - Extract the following properties: report_file, field_name, business_description, classification, pci, pi, treatment
   - Write this data to the Field Metadata sheet starting at cell A6

2. **File Metadata Generation**:
   - For each selected file, find matching record in `adhoc_data`
   - Calculate aggregated values:
     - `classification`: Highest classification of all fields in the file (Critical > Restricted > Confidential > Internal > Public)
     - `pci`: Yes if any field has pci = yes
     - `pi`: Yes if any field has pi = yes
   - Extract file-level properties: file_name, file_type, business_description, etc.
   - Write this data to the File Metadata sheet starting at cell A4

### Validation

The application validates:
- PI values: Must be one of Yes, No, True, False, 1, 0 (case insensitive)
- PCI values: Must be one of Yes, No, True, False, 1, 0 (case insensitive)
- Classification values: Must be one of Critical, Restricted, Confidential, Internal, Public (case sensitive)

Validation warnings are displayed in a modal dialog when issues are found.

### Known Limitations

1. **Browser Compatibility**:
   - Requires a modern browser with JavaScript enabled
   - May not work on older browsers or mobile devices with limited capabilities

2. **File Size Limitations**:
   - Large Excel files (>10MB) may cause performance issues
   - Processing time increases with the number of records
   - The embedded default template increases the initial page load size

3. **Template Requirements**:
   - ADIDO Template must have specific sheet names and cell positions
   - Field Metadata must be written starting at cell `A6`
   - File Metadata must be written starting at cell `A4`
   - Custom templates must follow the same structure as the default template

4. **Data Quality**:
   - The application validates some data quality issues but cannot detect all problems
   - Missing or malformed data in the source files may lead to incomplete templates

5. **Security Considerations**:
   - All processing happens client-side; no data is sent to any server
   - File access is limited to what the browser allows through the file input element

### Implementation Notes for Developers

1. **Adding New Validation Rules**:
   - Add validation logic to the `mapAdidoMetadataToInternalSchema` or `mapAdhocDataToInternalSchema` functions
   - Push new warning objects to the `validationWarnings` array

2. **Modifying Template Generation**:
   - The `generateADIDOTemplate` function handles the template population logic
   - Modify the cell references if the template format changes

3. **Updating the Default Template**:
   - Create a new Excel template file
   - Run the Python script to convert it to base64
   - Replace the `defaultTemplateBase64` value in the code
   - Consider adding a version comment to track template changes

4. **UI Customization**:
   - The application uses Alpine.js for reactivity
   - Most UI elements can be customized by modifying the HTML and CSS
   - The grid layout can be adjusted to change the card positioning

5. **Testing Considerations**:
   - Test with various Excel file formats and sizes
   - Verify template generation with different combinations of selected files
   - Check validation with both valid and invalid data
   - Test on different browsers and screen sizes
   - Test both the default template and custom uploaded templates
