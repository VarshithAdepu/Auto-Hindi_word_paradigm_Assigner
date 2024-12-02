# File paths for the input and output files
file2_path = 'best_matches_output_0.txt'  # Replace with your actual file path
file1_path = 'extracted_values.txt'  # Replace with your actual file path
matches_output_path = 'matches1.txt'
non_matches_output_path = 'non_matches1_original.txt'

# Function to read file and create a dictionary from it
def read_file_to_dict(file_path):
    data = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            term, definition = line.strip().split(':', 1)
            data[term.strip()] = definition.strip()
    return data

# Read both files into dictionaries
data1 = read_file_to_dict(file1_path)
data2 = read_file_to_dict(file2_path)

# Prepare lists for matches and non-matches
matches = []
non_matches = []

# Check for matching and non-matching entries
for term in data1:
    if term in data2 and data1[term] == data2[term]:
        matches.append(f"{term}: {data1[term]}")
    else:
        # Show value from both files if not matching, or 'None' if term not in file2
        # non_matches.append(f"{term}: {data1[term]} (original) - {data2.get(term, 'None')} (predicted)")
        non_matches.append(f"{term}: {data2.get(term, 'None')}")
        # non_matches.append(f"{term}: {data1[term]}")

# Write matches to a file
with open(matches_output_path, 'w', encoding='utf-8') as matches_file:
    matches_file.write("Matching Entries:\n")
    matches_file.write("\n".join(matches))

# Write non-matches to a file
with open(non_matches_output_path, 'w', encoding='utf-8') as non_matches_file:
    non_matches_file.write("Non-Matching Entries:\n")
    non_matches_file.write("\n".join(non_matches))

print("Comparison complete. Check 'matches.txt' and 'non_matches.txt' for results.")
