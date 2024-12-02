# no duplicates
import xml.etree.ElementTree as ET

def generate_inflectional_words_for_dict(file_path, words_with_paradigms):
    try:
        print(words_with_paradigms,'ppppf')
        tree = ET.parse(file_path)
        root = tree.getroot()

        pardefs = root.find('pardefs')
        if pardefs is None:
            print("No <pardefs> element found.")
            return None
        
        results = {}

        for base_word, paradigms in words_with_paradigms.items():
            results[base_word] = {}
            for paradigm_name in paradigms:
                suffix = paradigm_name.split('/')[1].split('__')[0]
                paradigm_found = False
                for pardef in pardefs.findall('pardef'):
                    if pardef.attrib['n'] == paradigm_name:
                        paradigm_found = True
                        inflectional_forms = set()
                        for e in pardef.findall('e'):
                            l_element = e.find('.//l')
                            l_value = l_element.text if l_element is not None and l_element.text else ""

                            if l_value and suffix:
                                base_word1 = base_word[:-len(suffix)]
                                inflected_word = base_word1 + l_value
                                inflectional_forms.add(inflected_word)
                            elif l_value:
                                inflected_word = base_word + l_value
                                inflectional_forms.add(inflected_word)

                        results[base_word][paradigm_name] = list(inflectional_forms)
                        break

                if not paradigm_found:
                    results[base_word][paradigm_name] = []

        return results

    except ET.ParseError as e:
        print(f"Failed to parse XML file: {e}")
        return None
# =======================================================================
# duplicates
# import xml.etree.ElementTree as ET

# def generate_inflectional_words_for_dict(file_path, words_with_paradigms):
#     try:
#         print(words_with_paradigms,'ppppf2')
#         tree = ET.parse(file_path)
#         root = tree.getroot()

#         pardefs = root.find('pardefs')
#         if pardefs is None:
#             print("No <pardefs> element found.")
#             return None
        
#         results = {}

#         for base_word, paradigms in words_with_paradigms.items():
#             results[base_word] = {}
#             for paradigm_name in paradigms:
#                 suffix = paradigm_name.split('/')[1].split('__')[0]
#                 paradigm_found = False
#                 for pardef in pardefs.findall('pardef'):
#                     if pardef.attrib['n'] == paradigm_name:
#                         paradigm_found = True
#                         inflectional_forms = []  # Use list to allow duplicates
#                         for e in pardef.findall('e'):
#                             l_element = e.find('.//l')
#                             l_value = l_element.text if l_element is not None and l_element.text else ""

#                             if l_value and suffix:
#                                 base_word1 = base_word[:-len(suffix)]
#                                 inflected_word = base_word1 + l_value
#                                 inflectional_forms.append(inflected_word)  # Append to list
#                             elif l_value:
#                                 inflected_word = base_word + l_value
#                                 inflectional_forms.append(inflected_word)  # Append to list

#                         results[base_word][paradigm_name] = inflectional_forms
#                         break

#                 if not paradigm_found:
#                     results[base_word][paradigm_name] = []

#         return results

#     except ET.ParseError as e:
#         print(f"Failed to parse XML file: {e}")
#         return None
