# from find_paradigm import *
import os
import json
from xml_tree import generate_inflectional_words_for_dict
from finding_inflectional_words_in_corpus import find_best_matching_paradigm
# from xlsx_store import find_best_matching_paradigm
from wxconv import WXC
words_with_paradigms = {}

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
    wx = WXC(order='wx2utf', lang='hin')
    return wx.convert(word)

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
        return False

# Dictionary of words with their categories
words_with_categories = {}

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
# with open('/home/user/varsh/dataset_hi/pradigm_nov_21/other_predictions.txt', 'r') as file:
#     for line in file:
#         key, value = line.strip().split(": ")
#         # Add the key-value pair to the dictionary with categorization
#         output_data[key] = categorize_value(value)

# # Print the dictionary in the required format
# print(output_data)

# Dictionary to store results in the required format
# words_with_categories = output_data
words_with_categories = {'vAyumaNdala': 'noun', 'hAnikAraka': 'adjective', 'parAbEMganI': 'adjective', 'cakrIya': 'adjective', 'mahawva': 'noun', 'oYksIjana': 'noun', 'dAi': 'noun', 'jalavARpa': 'noun', 'XUlakaNa': 'noun', 'Sahiwa': 'adjective', 'xvanxva': 'noun', 'avaSoRiwa': 'noun', 'janwu': 'noun', 'xvanda': 'noun', 'gEsIya': 'adjective', 'svarUpa': 'noun', 'varRaNa': 'noun', 'vARpowsarjana': 'noun', 'XUlakaNA': 'noun', 'saMGanana': 'noun', 'awi': 'adjective', 'oYksAida': 'noun', 'heightmeas': 'noun', 'viRuvawa': 'noun', 'saMvahanIya': 'adjective', 'kaBI': 'noun', 'SAnwa': 'noun', 'kRoBamaNdala': 'noun', 'kRoBasImA': 'noun', 'widthmeas': 'noun', 'uparI': 'adjective', 'maNdala': 'noun', 'samawApamaNdala': 'noun', 'maXyamaNdala': 'noun', 'maNDala': 'noun', 'moTAI': 'noun', 'spatial': 'noun', 'vixyuwa': 'adjective', 'AveSiwa': 'adjective', 'compound': 'adjective', 'AyanamaNdala': 'noun', 'anwima': 'adjective', 'gurUwvAkarRaNa': 'noun', 'Ayana': 'noun', 'kim': 'adjective', 'cakraNa': 'noun', 'AksAIda': 'noun', 'BOjana': 'noun', 'kArbohAidreta': 'noun', 'rupa': 'noun', 'kArbanIkaraNa': 'noun', 'jalaBaNdAra': 'noun', 'wawva': 'noun', 'nAitreta': 'noun', 'sWAnAMwariwa': 'noun', 'sAMsa': 'noun', 'bahirmaNdala': 'noun', 'sabI': 'noun', 'sambaMXI': 'adjective', 'anwara': 'noun', 'AreKa': 'noun'}

{ 'samBava': 'noun', 'awi': 'adjective', 'kim': 'adjective', 'lohA': 'unknown', 'Upara': 'adjective', 'compound': 'adjective', 'nIce': 'noun', 'BaNdAra': 'noun'} 
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
    inflectional_words_dict = generate_inflectional_words_for_dict('/home/user/varsh/dataset_hi/pradigm_nov_21/apertium_hn_LC.dix', words_with_paradigms)

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
    output_file_path = '/home/user/varsh/dataset_hi/pradigm_nov_21/output_inflectional_words.json'
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
    print(parsed_output)
    # Run the function and print the results
    best_matches = find_best_matching_paradigm(parsed_output, monolingual_corpus)

    best_matches_file = '/home/user/varsh/dataset_hi/pradigm_nov_21/best_matches_output_0.txt'
    with open(best_matches_file, 'w', encoding='utf-8') as f:
        for base_word, (paradigm,difference, match_count) in best_matches.items():
            if paradigm:
                f.write(f"{base_word}: {paradigm}(Match Count: {match_count}, Difference: {difference})\n")
            else:
                f.write(f"{base_word}: No matching paradigm found\n")

except NameError:
    print("The function 'generate_inflectional_words_for_dict' is not defined. Please check the import or function implementation.")

