from openpyxl import Workbook

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
    best_paradigm_matches1 = {}

    for base_word, paradigms in words_with_paradigms.items():
        best_paradigm = None
        max_match_count = 0
        best_paradigm_details = None  # To store the best paradigm with its details (match count, difference)
        best_matching_words = []

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

            # Check if all inflectional words match (difference == 0)
            if difference == 0 and match_count > 0:
                # If this paradigm has more matches, select it
                if match_count > max_match_count:
                    max_match_count = match_count
                    best_paradigm = paradigm
                    best_matching_words = matches
                    best_paradigm_details = (paradigm, difference, match_count)

            # Step 2: Select paradigm with the least difference, but only if match_count is > 0
            elif match_count > 0 and (
                (best_paradigm_details is None) or
                (difference < best_paradigm_details[1]) or
                (difference == best_paradigm_details[1] and inflectional_count > max_match_count)
            ):
                max_match_count = match_count
                best_paradigm = paradigm
                best_matching_words = matches
                best_paradigm_details = (paradigm, difference, match_count)

        # Store the best paradigm with its matches for the base word
        best_paradigm_matches[base_word] = {
            "Paradigm": best_paradigm,
            "Matching Words": best_matching_words,
            "All Inflectional Words": paradigms.get(best_paradigm, [])
        }
        # Step 3: Store the best paradigm for the base word, only if match_count > 0
        if best_paradigm and max_match_count > 0:
            best_paradigm_matches1[base_word] = best_paradigm_details
        else:
            best_paradigm_matches1[base_word] = (None, 0, 0)

    # # Save the results to an .xlsx file
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Best Paradigm Matches"
    sheet.append(["Base Word", "Paradigm", "Matching Words", "All Inflectional Words"])

    for base_word, details in best_paradigm_matches.items():
        paradigm = details["Paradigm"]
        matching_words = ', '.join(details["Matching Words"])
        inflectional_words = ', '.join(details["All Inflectional Words"])
        # Append data to the sheet
        sheet.append([base_word, paradigm, matching_words, inflectional_words])

    # Save the workbook
    workbook.save("best_paradigm_matches.xlsx")
    print("Data saved to best_paradigm_matches.xlsx")

    

    return best_paradigm_matches1,best_paradigm_matches
