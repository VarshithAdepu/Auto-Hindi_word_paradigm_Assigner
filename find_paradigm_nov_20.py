from find_paradigm import *
import os
import json

words_with_paradigms = {}

# Function to categorize the values based on their category
def categorize_value(value):
    if '__adj' in value:
        return 'adjective'
    elif '__n' in value:
        return 'noun'
    elif '__v' in value:
        return 'verb'
    elif '__sh' in value:
        return 'shashthi'
    elif '__vj' in value:
        return 'verbal adjective'
    elif '__vn' in value:
        return 'verbal noun'
    elif '__p' in value:
        return 'pronoun'
    elif 'parsarg' in value:
        return 'parsarg'
    elif 'regular__adj-noun' in value:
        return 'adjective-noun'
    else:
        return 'unknown'

# Initialize an empty dictionary
output_data = {}

# Read data from the file and process it
with open('/home/user/varsh/dataset_hi/pradigm_nov_20/extracted_values.txt', 'r') as file:
    for line in file:
        key, value = line.strip().split(": ")
        # Add the key-value pair to the dictionary with categorization
        output_data[key] = categorize_value(value)

# Print the dictionary in the required format
print(output_data)

# Dictionary to store results in the required format
words_with_categories = output_data

# Iterate over each word and find matching paradigms
for word, category in words_with_categories.items():
    paradefs = locals().get(category + 's', [])
    matching_paradigms = []
    
    for paradef in paradefs:
        paradef_name = paradef.split('"')[1]
        if match_last_character(word, paradef_name):
            matching_paradigms.append(paradef_name)
    
    words_with_paradigms[word] = matching_paradigms

try:
    inflectional_words_dict = generate_inflectional_words_for_dict('/home/user/varsh/dataset_hi/pradigm_nov_20/apertium_hn_LC.dix', words_with_paradigms)

    # Write results in the required format
    output = {}
    if inflectional_words_dict:
        for base_word, paradigms_dict in inflectional_words_dict.items():
            output[base_word] = {}
            for paradigm, inflectional_words in paradigms_dict.items():
                base_list = []
                inflectional_words_in_wx = [convert_to_hindi(word) for word in inflectional_words]
                if inflectional_words_in_wx:
                    output[base_word][paradigm] = inflectional_words_in_wx
                else:
                    base_list.append(convert_to_hindi(base_word))
                    output[base_word][paradigm] = base_list

    # Write the output to a file
    output_file_path = '/home/user/varsh/dataset_hi/pradigm_nov_20/output_inflectional_words.json'
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)

    # Load the Hindi monolingual corpus from split files
    corpus_dir = '/home/user/varsh/dataset_hi/split_parts'
    monolingual_corpus = set()

    # Process each split file in the directory
    for filename in sorted(os.listdir(corpus_dir)):
        if filename.startswith("part_"):  # Ensure we're reading split files
            filepath = os.path.join(corpus_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    words = line.split()
                    monolingual_corpus.update(words)

    json_output = json.dumps(output, ensure_ascii=False, indent=4)
    parsed_output = json.loads(json_output)

    # Run the function and print the results
    best_matches = find_best_matching_paradigm(parsed_output, monolingual_corpus)

    best_matches_file = '/home/user/varsh/dataset_hi/pradigm_nov_20/best_matches_output_0.txt'
    with open(best_matches_file, 'w', encoding='utf-8') as f:
        for base_word, (paradigm,difference, match_count) in best_matches.items():
            if paradigm:
                f.write(f"{base_word}: {paradigm}(Match Count: {match_count}, Difference: {difference})\n")
            else:
                f.write(f"{base_word}: No matching paradigm found\n")

except NameError:
    print("The function 'generate_inflectional_words_for_dict' is not defined. Please check the import or function implementation.")

