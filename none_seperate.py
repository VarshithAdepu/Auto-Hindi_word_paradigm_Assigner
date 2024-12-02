# Open input and output files
with open('non_matches1_original.txt', 'r', encoding='utf-8') as infile, \
     open('none_predictions.txt', 'w', encoding='utf-8') as none_file, \
     open('other_predictions.txt', 'w', encoding='utf-8') as other_file:
    
    # Process each line
    for line in infile:
        # Check if 'None' is in the prediction part of the line
        if "None" in line:
            none_file.write(line)   # Write to None predictions file
        else:
            other_file.write(line)  # Write to other predictions file

# # Read input from file, process, and overwrite with modified content
# with open('other_predictions.txt', 'r', encoding='utf-8') as file:
#     lines = file.readlines()

# # Process each line to remove the predicted part
# modified_lines = []
# for line in lines:
#     # Split by ' - ' and take only the original part
#     modified_line = line.split(' - ')[0].strip()
#     modified_lines.append(modified_line)

# # Write modified lines back to the same file
# with open('other_predictions.txt', 'w', encoding='utf-8') as file:
#     for line in modified_lines:
#         file.write(line + '\n')

# print("File updated successfully.")
