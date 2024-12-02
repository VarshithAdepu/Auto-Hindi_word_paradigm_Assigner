import re

# Sample data (based on the example provided)
# words_with_paradigms = {
#     'Pasala': {
#         'rAw/a__n': ['वेधन', 'वेधनें', 'वेधनों'],
#         'BIda/__n': ['वेधन'],
#         'Gar/a__n': ['वेधन', 'वेधनों'],
#         'Karc/a__n': ['वेधन', 'वेधने', 'वेधनों']
#     }
# }

# words_with_paradigms = {
#     "Pasala": {
#         "rAw/a__n": [
#             "फसलों",
#             "फसल",
#             "फसलें"
#         ],
#         "BIda/__n": [],
#         "Gar/a__n": [
#             "फसलों",
#             "फसल"
#         ],
#         "Karc/a__n": [
#             "फसलों",
#             "फसले",
#             "फसल"
#         ]
#     }
# }


# Function to find matches in corpus and determine best matching paradigm
# def find_best_matching_paradigm(words_with_paradigms, corpus):
#     '''words_with_paradigms = {
#         "Pasala": {
#             "rAw/a__n": [
#                 "फसलों",
#                 "फसल",
#                 "फसलें"
#             ],
#             "BIda/__n": [],
#             "Gar/a__n": [
#                 "फसलों",
#                 "फसल"
#             ],
#             "Karc/a__n": [
#                 "फसलों",
#                 "फसले",
#                 "फसल"
#             ]
#         }
#     }'''
#     print(words_with_paradigms,'llllllllllllll')
#     # Dictionary to store the paradigm with most matches for each base word
#     best_paradigm_matches = {}

#     for base_word, paradigms in words_with_paradigms.items():
#         max_matches = 0
#         best_paradigm = None

#         # Iterate through each paradigm and its inflectional words
#         for paradigm, words in paradigms.items():
#             # Count matches in corpus for the current paradigm
#             match_count = sum(1 for word in words if word in corpus)

#             print(f"Inflectional words for base '{base_word}' using paradigm '{paradigm}':")
#             print(f"Words in paradigm: {words}")
#             print(f"Matching words in corpus: {[word for word in words if word in corpus]}")
#             # print(f"Match count: {match_count}")

#             # Update the best matching paradigm if this has more matches
#             if match_count > max_matches:
#                 max_matches = match_count
#                 best_paradigm = paradigm

#         # Store the best paradigm for the base word
#         best_paradigm_matches[base_word] = (best_paradigm, max_matches)
#     print(best_paradigm_matches,'best')
#     return best_paradigm_matches

# =====================================================================
# nov 20 2024
# def find_best_matching_paradigm(words_with_paradigms, corpus):
#     """
#     Function to find the best matching paradigm based on specific criteria.
#     Args:
#         words_with_paradigms: Dictionary mapping base words to their paradigms and inflectional words.
#         corpus: Set or list of words to compare against the paradigms.
#     Returns:
#         Dictionary mapping base words to their best matching paradigm and additional details.
#     """
#     # Dictionary to store the best paradigm for each base word
#     best_paradigm_matches = {}

#     for base_word, paradigms in words_with_paradigms.items():
#         best_paradigm = None
#         min_difference = float('inf')
#         max_matches = 0

#         for paradigm, words in paradigms.items():
#             # Count matches in corpus for the current paradigm
#             matches = [word for word in words if word in corpus]
#             match_count = len(matches)
#             inflectional_count = len(words)
#             difference = inflectional_count - match_count

#             print(f"Base Word: {base_word}")
#             print(f"Paradigm: {paradigm}")
#             print(f"Words in Paradigm: {words}")
#             print(f"Matches in Corpus: {matches}")
#             print(f"Match Count: {match_count}, Difference: {difference}")

#             # Step 1: Check if all inflectional words match
#             if difference == 0:  # All words match
#                 best_paradigm = paradigm
#                 print(f"All words matched for paradigm '{paradigm}'. Selected!")
#                 break  # Select this paradigm immediately
            
#             # Step 2: Select paradigm with the least difference
#             if difference < min_difference or (difference == min_difference and inflectional_count > max_matches):
#                 min_difference = difference
#                 max_matches = inflectional_count
#                 best_paradigm = paradigm
#                 print(f"Paradigm '{paradigm}' has least difference so far. Provisional selection.")

#         # Step 3: Store the best paradigm for the base word
#         best_paradigm_matches[base_word] = (best_paradigm, min_difference, max_matches)

#     print("Final Best Paradigm Matches:", best_paradigm_matches)
#     return best_paradigm_matches

# =======================================
# duplicates
def find_best_matching_paradigm(words_with_paradigms, corpus):
    """
    Function to find the best matching paradigm based on specific criteria.
    Args:
        words_with_paradigms: Dictionary mapping base words to their paradigms and inflectional words.
        corpus: Set or list of words to compare against the paradigms.
    Returns:
        Dictionary mapping base words to their best matching paradigm and additional details.
    """
    # Dictionary to store the best paradigm for each base word
    best_paradigm_matches = {}

    for base_word, paradigms in words_with_paradigms.items():
        best_paradigm = None
        max_match_count = 0
        best_paradigm_details = None  # To store the best paradigm with its details (match count, difference)

        for paradigm, words in paradigms.items():
            # Track match results for individual words
            word_match_status = {}
            matches = []
            
            # Count matches in corpus for the current paradigm
            for word in words:
                # If the word has already been encountered, use its previous match result
                if word in word_match_status:
                    if word_match_status[word]:  # If it matched previously
                        matches.append(word)
                else:
                    # Check corpus and store match result
                    is_match = word in corpus
                    word_match_status[word] = is_match
                    if is_match:
                        matches.append(word)

            match_count = len(matches)
            inflectional_count = len(words)  # Count all occurrences, including duplicates
            difference = inflectional_count - match_count

            print(f"Base Word: {base_word}")
            print(f"Paradigm: {paradigm}")
            print(f"Words in Paradigm: {words}")
            print(f"Matches in Corpus: {matches}")
            print(f"Match Count: {match_count}, Difference: {difference}")

            # Check if all inflectional words match (difference == 0)
            if difference == 0 and match_count > 0:
                # If this paradigm has more matches, select it
                if match_count > max_match_count:
                    max_match_count = match_count
                    best_paradigm = paradigm
                    best_paradigm_details = (paradigm, difference, match_count)
                print(f"Paradigm '{paradigm}' matches all inflectional words and has {match_count} matches. Selected as provisional best.")

            # Step 2: Select paradigm with the least difference, but only if match_count is > 0
            elif match_count > 0 and (
                (best_paradigm_details is None) or
                (difference < best_paradigm_details[1]) or
                (difference == best_paradigm_details[1] and inflectional_count > max_match_count)
            ):
                max_match_count = match_count
                best_paradigm = paradigm
                best_paradigm_details = (paradigm, difference, match_count)
                print(f"Paradigm '{paradigm}' has least difference so far and non-zero matches. Provisional selection.")

        # Step 3: Store the best paradigm for the base word, only if match_count > 0
        if best_paradigm and max_match_count > 0:
            best_paradigm_matches[base_word] = best_paradigm_details
        else:
            best_paradigm_matches[base_word] = (None, 0, 0)

    print("Final Best Paradigm Matches:", best_paradigm_matches)
    return best_paradigm_matches
