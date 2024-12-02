import re
import json
from xml_tree_new import generate_inflectional_words_for_dict  # Ensure this function exists in xml_tree_new
from wxconv import WXC
# from common_v4_non_mask import convert_to_hindi
# Lists of paradigms for different word categories
nouns = [
    '<pardef n="kAl/A__n">',
    '<pardef n="rAw/a__n">',
    '<pardef n="BIda/__n">',
    '<pardef n="ASA/__n">',
    '<pardef n="gudiy/A__n">',
    '<pardef n="IrRyA/__n">',
    '<pardef n="Apawwi/__n">',
    '<pardef n="SAnwi/__n">',
    '<pardef n="ladak/I__n">',
    '<pardef n="AjAxI/__n">',
    '<pardef n="qwu/__n">',
    '<pardef n="vAyu/__n">',
    '<pardef n="bah/U__n">',
    '<pardef n="bAlU/__n">',
    '<pardef n="lO/__n">',
    '<pardef n="sarasoM/__n">',
    '<pardef n="mAz/__n">',
    '<pardef n="Gar/a__n">',
    '<pardef n="Karc/a__n">',
    '<pardef n="kroXa/__n">',
    '<pardef n="ladak/A__n">',
    '<pardef n="rAjA/__n">',
    '<pardef n="loh/A__n">',
    '<pardef n="viXAwA/__n">',
    '<pardef n="kavi/__n">',
    '<pardef n="Axam/I__n">',
    '<pardef n="pAnI/__n">',
    '<pardef n="Sawru/__n">',
    '<pardef n="katu/__n">',
    '<pardef n="Al/U__n">',
    '<pardef n="lahU/__n">',
    '<pardef n="ku/Az__n">',
    '<pardef n="redio/__n">',
    '<pardef n="geh/Uz__n">',
    '<pardef n="BARAvix/__n">',
    '<pardef n="calaciwr/a__n">',
    '<pardef n="pIdZ/A__n">'
]
verbs = [
    '<pardef n="KA/__v">',
    '<pardef n="k/ara__v">',
    '<pardef n="l/e__v">',
    '<pardef n="h/o__v">',
    '<pardef n="p/I__v">',
    '<pardef n="C/U__v">',
    '<pardef n="so/__v">',
    '<pardef n="h/E__v">',
    '<pardef n="uT/a__v">',
    '<pardef n="xiK/a__v">',
    '<pardef n="k/ara__v">',
    '<pardef n="W/A__v">',
    '<pardef n="/jA__v">'
]
pronouns = [
    '<pardef n="kyA/__p">',
    '<pardef n="vahAz/__p">',
    '<pardef n="kaba/__p">',
    '<pardef n="Apan/A__p">',
    '<pardef n="/yaha__p">',
    '<pardef n="j/o__p">',
    '<pardef n="k/Ona__p">',
    '<pardef n="k/oI__p">',
    '<pardef n="/vaha__p">',
    '<pardef n="w/U__p">',
    '<pardef n="Apa/__p">',
    '<pardef n="saba/__p">',
    '<pardef n="/mEM__p">'
]
adjectives = [
    '<pardef n="xo/__adj">',
    '<pardef n="wIn/a__adj">',
    '<pardef n="anek/a__adj">',
    '<pardef n="amIra/__adj">',
    '<pardef n="bAlikA/__adj">',
    '<pardef n="bAlaka/__adj">',
    '<pardef n="ajAwI/__adj">',
    '<pardef n="kAl/A__adj">',
    '<pardef n="jyAx/A__adj">'
]

def convert_to_hindi(word):
    if '_' in word:
        word=word.replace('_',' ')
    # print(word,'llllllll')
    wx = WXC(order='wx2utf', lang='hin')
    # wx1 = WXC(order='utf2wx', lang='hin')
    hindi_text_list = wx.convert(word)
    # print(hindi_text_list,'klklklkl')
    return hindi_text_list

# Function to match the last characters of a word with the suffix from the paradigm
def match_last_character(word, paradef):
    try:
        suffix = paradef.split('/')[1].split('__')[0]
        suffix2 = paradef.split('/')[0][-1]
        if word.endswith(suffix) and suffix:
            return word[:-len(suffix)]
        elif word.endswith(suffix2) and suffix2:
            return word.endswith(suffix2)
    except IndexError:
        # Handle any malformed paradigms gracefully
        return False

# Dictionary of words with their categories
words_with_categories = {
    'Pasala': 'noun',
}

# Dictionary to store results in the required format
words_with_paradigms = {}

# Iterate over each word and find matching paradigms
for word, category in words_with_categories.items():
    paradefs = locals().get(category + 's', [])
    # print(paradefs,'klkl')
    matching_paradigms = []
    
    for paradef in paradefs:
        # Extract the name from the <pardef> tag
        paradef_name = paradef.split('"')[1]
        if match_last_character(word, paradef_name):
            matching_paradigms.append(paradef_name)
    
    # Store the matching paradigms for the word in the dictionary
    words_with_paradigms[word] = matching_paradigms

# Check if the 'generate_inflectional_words_for_dict' function exists before using it
try:
    inflectional_words_dict = generate_inflectional_words_for_dict('apertium_hn_LC.dix', words_with_paradigms)

    output_file = 'inflectional_words_output.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        if inflectional_words_dict:
            for base_word, paradigms_dict in inflectional_words_dict.items():
                for paradigm, inflectional_words in paradigms_dict.items():
                    f.write(f"\nInflectional words for base '{base_word}' using paradigm '{paradigm}':\n")
                    print(f"Inflectional words for base '{base_word}' using paradigm '{paradigm}':")
                    if inflectional_words:
                        print(inflectional_words,'vkvk')
                        # f.write(', '.join(inflectional_words) + '\n')
                        # print(inflectional_words)
                        # Convert each word to WX notation
                        inflectional_words_in_wx = [convert_to_hindi(word) for word in inflectional_words]  # Apply WX conversion here
                        f.write(', '.join(inflectional_words_in_wx) + '\n')
                        # print(inflectional_words_in_wx,'klklkl')
                    else:
                        f.write(f"No inflectional words found for {convert_to_hindi(base_word)}\n")
                        print(f"No inflectional words found for {base_word}\n")
        else:
            f.write("No inflectional words generated.\n")
    print(f"Output successfully stored in '{output_file}'.")

except NameError:
    print("The function 'generate_inflectional_words_for_dict' is not defined. Please check the import or function implementation.")
