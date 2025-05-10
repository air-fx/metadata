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