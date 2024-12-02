# import xml.etree.ElementTree as ET

# # Function to get inflectional words for a dictionary of words with lists of paradigms
# def generate_inflectional_words_for_dict(file_path, words_with_paradigms):
#     print(words_with_paradigms,'kkk')
#     try:
#         # Parse the .dix file
#         tree = ET.parse(file_path)
#         root = tree.getroot()

#         # Check the root tag
#         print(f"Root tag: {root.tag}")  # Debugging output

#         # Access the <pardefs> child to find <pardef>
#         pardefs = root.find('pardefs')
#         if pardefs is None:
#             print("No <pardefs> element found.")
#             return None
        
#         # Create a dictionary to store results
#         results = {}

#         # Iterate over the dictionary of words and their corresponding paradigms
#         for base_word, paradigms in words_with_paradigms.items():
#             results[base_word] = {}
#             for paradigm_name in paradigms:
#                 print(f"Processing base word '{base_word}' with paradigm '{paradigm_name}'")  # Debugging output

#                 # Check if the paradigm exists
#                 paradigm_found = False
#                 for pardef in pardefs.findall('pardef'):
#                     if pardef.attrib['n'] == paradigm_name:
#                         paradigm_found = True
#                         inflectional_forms = []
#                         for e in pardef.findall('e'):
#                             l_element = e.find('.//l')
#                             l_value = l_element.text if l_element is not None and l_element.text else ""

#                             # Avoid concatenating NoneType
#                             if l_value:  # Only append if l_value is not empty
#                                 inflected_word = base_word + l_value
#                                 inflectional_forms.append(inflected_word)

#                         # Store the inflected forms for the specific paradigm
#                         results[base_word][paradigm_name] = inflectional_forms
#                         break

#                 if not paradigm_found:
#                     print(f"Paradigm '{paradigm_name}' not found for base word '{base_word}'")
#                     results[base_word][paradigm_name] = []

#         return results

#     except ET.ParseError as e:
#         print(f"Failed to parse XML file: {e}")
#         return None



# # Input dictionary of words with paradigms

# # # Generate inflectional words
# # inflectional_words_dict = generate_inflectional_words_for_dict(file_path, words_with_paradigms)
# # if inflectional_words_dict:
# #     for base_word, paradigms_dict in inflectional_words_dict.items():
# #         for paradigm, inflectional_words in paradigms_dict.items():
# #             print(f"\nInflectional words for base '{base_word}' using paradigm '{paradigm}':")
# #             if inflectional_words:
# #                 print(inflectional_words)
# #             else:
# #                 print("No inflectional words found for", base_word)

# ==========================================================================================================
# without duplicates

import xml.etree.ElementTree as ET

# Function to get inflectional words for a dictionary of words with lists of paradigms
def generate_inflectional_words_for_dict(file_path, words_with_paradigms):
    print(words_with_paradigms, 'kkk')
    try:
        # Parse the .dix file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Check the root tag
        print(f"Root tag: {root.tag}")  # Debugging output

        # Access the <pardefs> child to find <pardef>
        pardefs = root.find('pardefs')
        if pardefs is None:
            print("No <pardefs> element found.")
            return None
        
        # Create a dictionary to store results
        results = {}

        # Iterate over the dictionary of words and their corresponding paradigms
        for base_word, paradigms in words_with_paradigms.items():
            results[base_word] = {}
            for paradigm_name in paradigms:
                # print(f"Processing base word '{base_word}' with paradigm '{paradigm_name}'")  # Debugging output
                # print(paradigm_name,'paraa')
                suffix = paradigm_name.split('/')[1].split('__')[0]
                # Check if the paradigm exists
                paradigm_found = False
                for pardef in pardefs.findall('pardef'):
                    if pardef.attrib['n'] == paradigm_name:
                        paradigm_found = True
                        inflectional_forms = set()  # Use a set to avoid duplicates
                        for e in pardef.findall('e'):
                            l_element = e.find('.//l')
                            l_value = l_element.text if l_element is not None and l_element.text else ""

                            # Avoid concatenating NoneType
                            if l_value and suffix:  # Only add if l_value is not empty
                                base_word1 = base_word[:-len(suffix)]
                                # print(base_word1,'word')
                                inflected_word = base_word1 + l_value
                                inflectional_forms.add(inflected_word)  # Add to set
                            elif l_value:
                                inflected_word = base_word + l_value
                                inflectional_forms.add(inflected_word)  # Add to set

                        # Store the inflected forms as a list to maintain JSON format
                        results[base_word][paradigm_name] = list(inflectional_forms)
                        break

                if not paradigm_found:
                    print(f"Paradigm '{paradigm_name}' not found for base word '{base_word}'")
                    results[base_word][paradigm_name] = []

        return results

    except ET.ParseError as e:
        print(f"Failed to parse XML file: {e}")
        return None
