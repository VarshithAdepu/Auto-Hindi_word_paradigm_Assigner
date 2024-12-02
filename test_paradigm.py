import xml.etree.ElementTree as ET

# Path to the Apertium dictionary file
file_path = "apertium_hn_LC.dix"

# Dictionary to store extracted 'lm' attributes with their corresponding paradigms
extracted_lm_values = {}

# Load and parse the XML file
try:
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Debugging: Print the root and first few elements
    print("Root:", root.tag)  # Print the root tag to confirm correct parsing

    # Extract 'lm' values and their corresponding 'n' paradigms from 'par'
    for element in root.findall('.//e'):  # Make sure to look at all 'e' elements, including nested ones
        lm_value = element.get('lm')
        par_element = element.find('par')
        
        if par_element is not None:
            # Get the paradigm from 'n' attribute of 'par' tag
            paradigm = par_element.get('n')
            if lm_value and paradigm:
                extracted_lm_values[lm_value] = paradigm

    # Output the extracted lm values with their paradigms
    print("Extracted 'lm' values with their paradigms:", extracted_lm_values)

    # Optional: Write to a file
    with open("extracted_values.txt", "w") as file:
        for lm_value, paradigm in extracted_lm_values.items():
            file.write(f"{lm_value}: {paradigm}\n")

except ET.ParseError:
    print("Error: Could not parse the XML file.")
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
