# Data Extraction Field Classifier

## Overview

This application provides a web interface that helps classify data extraction fields. It allows users to input field names they plan to include in their reports and automatically finds metadata for these fields, including their classification, PI/PCI status, and data treatment requirements.

## Features

- Load metadata from Excel file (ADIDO and Pipeline info)
- Enter field names to be classified
- Automatic matching of field names against existing metadata
- Manual search functionality for finding specific fields
- Export results as CSV
- Copy results as a formatted table

## How to Use

### Step 1: Load Metadata File

The application requires a single Excel file with two sheets:

1. Click "Browse" to select and upload an Excel file from your local system
2. The Excel file must contain two sheets:
   - **ADIDO Metadata**: Contains fields that have been previously requested by users (higher priority)
   - **TDI GI Pipeline**: Contains all fields in the system along with their table information
3. A status indicator will show the loading progress and result

### Step 2: Enter Field Names

Enter one field name per line in the text area. These are the fields you want to classify.

### Step 3: Process Fields

Click "Process Fields" to search for matches in the metadata. The system will:
1. First check in the "ADIDO Metadata" sheet (higher priority)
2. If not found, check in the "TDI GI Pipeline" sheet
3. Display results in a table

### Step 4: Review and Refine Results

For each field, you can:
- Use "Auto" mode (default) to use the automatically found match
- Use "Search" to manually find a different field that better matches your needs
- View detailed information including classification, PI/PCI status, and treatment requirements

### Step 5: Export Results

- Click "Export Results" to download a CSV file with the classified fields (includes Field Name, Business Description, Classification, PI, PCI, and Treatment)
- Click "Copy as Table" to copy the results as a formatted table that can be pasted into other applications (without headers)

## Technical Documentation

### File Structure

- `index-htmx.html`: Main application file containing HTML, CSS, and JavaScript

### Technologies Used

- **Alpine.js**: For reactive data binding and UI state management
- **SheetJS**: For Excel file handling
- **HTML/CSS/JavaScript**: Core web technologies
- **No server-side dependencies**: The application runs entirely in the browser

### Data Models

#### Already Requested Metadata Schema

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

#### General Metadata Schema

Required fields in the Excel file:
- `table_path`: Path to the table
- `Object Type`: Type of object (e.g., "field", "table")
- `Name`: Field name
- `Business Description`: Description of the field
- `Security Classification`: Security classification
- `PCI-DSS`: PCI-DSS status (boolean)
- `PI`: Personal Information status (boolean)
- `Data Treatment`: Required data treatment

Internal object schema:
```javascript
{
  object_type: string,
  field_name: string,   // Source Field Name
  business_description: string,
  classification: string,
  pi: boolean,
  pci: boolean,
  treatment: string,
  table_path: string,   // Source
  table_name: string    // Extracted from table_path
}
```

### Results Schema

```javascript
{
  fieldName: string,    // Original field name entered by user
  noMatch: boolean,     // Whether a match was found
  matchingFields: [     // Array of matching fields (if found)
    {
      source: string,   // Report name or table name
      name: string,     // Field name
      business_description: string,
      classification: string,
      pi: boolean,
      pci: boolean,
      treatment: string,
      table_path: string,
      from_source: string  // 'already_requested' or 'metadata'
    }
  ],
  currentField: object, // Currently selected field from matchingFields
  mode: string          // 'auto' or 'manual'
}
```

### Key Functions

- `loadMetadataFile(event)`: Loads and processes an Excel file containing metadata from the user's local system
- `processExcelFile(buffer)`: Processes the Excel file buffer, extracts data from both required sheets, and converts it to the internal data format
- `processFields()`: Analyzes the entered field names against metadata and finds matches, with options to use only Pipeline data
- `updateSearchResults()`: Filters metadata based on search criteria in the search modal
- `setAutoMode(index)`: Reverts a field to using the automatically found match
- `openSearch(index)`: Opens the search modal for manually finding a field match
- `selectField(field)`: Selects a field from the search results and applies it to the current field
- `exportResults()`: Exports the results as a CSV file with Field Name, Business Description, Classification, PCI, PI, and Treatment
- `copyAsTable()`: Copies the results as a formatted table that can be pasted into other applications
- `truncateDescription(text, maxLength)`: Helper function to truncate long descriptions for display while preserving full text in tooltips

### UI Components

- **Main Results Table**: Displays the matched fields with their metadata
- **Search Modal**: Allows searching for specific fields
- **File Inputs**: For loading metadata files
- **Field Names Textarea**: For entering field names to classify

### Customization

#### Styling

The application uses responsive CSS with media queries to adapt to different screen sizes. Custom styles can be added to the `<style>` section in the HTML file.

#### Data Sources

To use different data sources:
1. Prepare Excel files with the required columns
2. The Excel file must contain two sheets:
   - **ADIDO Metadata**: Contains fields that have been previously requested by users
   - **TDI GI Pipeline**: Contains all fields in the system along with their table information
3. Use the file browser to upload your Excel file
4. If you want to prioritize table-based metadata, use the "Use Pipeline data only" checkbox

##### ADIDO Metadata Sheet Requirements

The ADIDO Metadata sheet must contain the following columns:
- `File Name`: Report name (Source)
- `Field Name`: Field name (Source Field Name)
- `Business Description`: Description of the field
- `Classification`: Security classification
- `PCI`: PCI-DSS status
- `PI`: Personal Information status
- `Data Treatment`: Required data treatment

##### TDI GI Pipeline Sheet Requirements

The TDI GI Pipeline sheet must contain the following columns:
- `table_path`: Path to the table
- `Object Type`: Type of object (e.g., "field", "table")
- `Name`: Field name
- `Business Description`: Description of the field
- `Security Classification`: Security classification
- `PCI-DSS`: PCI-DSS status
- `PI`: Personal Information status
- `Data Treatment`: Required data treatment

## Maintenance and Troubleshooting

### Common Issues

1. **Metadata not loading**: Check that Excel files have the correct sheet names and required columns
2. **Fields not matching**: Verify that field names match exactly (case-insensitive)
3. **Boolean values not displaying correctly**: Ensure PI/PCI values are properly formatted in the Excel files

### Adding Features

To add new features:
1. Modify the Alpine.js data model in the `app()` function
2. Update the HTML templates as needed
3. Add any new CSS styles to the `<style>` section

### Performance Considerations

- Large Excel files may cause performance issues in the browser
- Consider limiting the size of metadata files or implementing pagination for large result sets

## Browser Compatibility

The application has been tested and works in:
- Chrome (latest)
- Firefox (latest)
- Edge (latest)
- Safari (latest)

Older browsers or browsers without JavaScript enabled are not supported.