from openpyxl import Workbook
import json
import os
# output_file_path = 'output_inflectional_words.json'
# with open(output_file_path, 'w', encoding='utf-8') as f:
#     json.dump(output, f, ensure_ascii=False, indent=4)

#     # Load the Hindi monolingual corpus as a set for fast membership checking
#     corpus_file = 'HINDI_TREEBANK_SENTENCES'
#     with open(corpus_file, 'r', encoding='utf-8') as f:
#         monolingual_corpus = set(f.read().split())

#     json_output = json.dumps(output, ensure_ascii=False, indent=4)
#     parsed_output = json.loads(json_output)

def find_best_matching_paradigm(words_with_paradigms, corpus):
    # Dictionary to store the paradigm with most matches for each base word
    best_paradigm_matches = {}

    for base_word, paradigms in words_with_paradigms.items():
        max_matches = 0
        best_paradigm = None
        best_matching_words = []

        # Iterate through each paradigm and its inflectional words
        for paradigm, words in paradigms.items():
            # Count matches in corpus for the current paradigm
            matching_words = [word for word in words if word in corpus]
            match_count = len(matching_words)

            # Update the best matching paradigm if this has more matches
            if match_count > max_matches:
                max_matches = match_count
                best_paradigm = paradigm
                best_matching_words = matching_words

        # Store the best paradigm with its matches for the base word
        # best_paradigm_matches[base_word] = (best_paradigm, best_matching_words)
        best_paradigm_matches[base_word] = (best_paradigm, words)

    # Save the results to an .xlsx file
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Best Paradigm Matches"
    sheet.append(["Base Word", "Paradigm", "Inflectional Words"])

    for base_word, (paradigm, inflectional_words) in best_paradigm_matches.items():
        # Convert list of inflectional words to a comma-separated string
        inflectional_words_str = ', '.join(inflectional_words)
        # Append data to the sheet
        sheet.append([base_word, paradigm, inflectional_words_str])

    # Save the workbook
    workbook.save("best_paradigm_matches11.xlsx")
    print("Data saved to best_paradigm_matches.xlsx")

    return best_paradigm_matches
