import subprocess

def check_words_in_file(words, file_path):
    """Check if each word in the list is present in the file using shell commands.
    If a word starts with '#', remove '#', check if the word is present in the file, 
    then replace '#' with '*' if not found, or leave as is if found.
    This ensures that only whole words are matched, and matching is case-sensitive.
    """
    processed_words = []
    
    for word in words:
        original_word = word
        if word.startswith('#'):
            word_to_check = word[1:]  # Remove '#' for checking
        else:
            word_to_check = word  # If there's no '#', use the word as is
        
        # Use the -w flag to match whole words only and make sure it's case-sensitive
        command = f"grep -qw '{word_to_check}' {file_path}"
        
        # Run the grep command
        result = subprocess.run(command, shell=True)
        
        # If grep returns a non-zero exit status, the word is not found
        if result.returncode != 0:
            if original_word.startswith('#'):
                processed_words.append(f"*{word_to_check}")  # Add * in front if not found
            else:
                processed_words.append(word_to_check)  # Leave the word as is if not found and doesn't have #
        else:
            processed_words.append(original_word)  # Keep the original word if found
    
    return processed_words

# List of words to check
words_to_check = ['#sWalamaNdala', '#pramuKa', '#nirmANakArI', '#wawva', '#silIkA', 'ci', '#elyUmIniyama', 'ela', 'hE']

# Path to the file (assuming the file is 'hi_expand_lc.txt')
file_path = 'repository/hi_expanded_LC'

# Check the words and mark the missing ones with * if they had #
processed_words = check_words_in_file(words_to_check, file_path)

# Print the processed words
print('Processed Words:', ' '.join(processed_words))





# import re

# data = "^sWalamaNdala<cat:n><case:o><gen:f><num:s>$ ^pramuKa<cat:adj><case:d><gen:m><num:s>$ ^nirmANakArI<cat:adj><case:d><gen:m><num:s>$ ^wawva<cat:n><case:d><gen:m><num:s>$ ^silIkA<cat:n><case:d><gen:f><num:s>$ ci ^elyUmIniyama<cat:n><case:d><gen:m><num:s>$ ela ^hE<cat:v><gen:m><num:s><per:a><tam:hE>$"

# # Use regular expression to extract words between ^ and <
# words = re.findall(r'\^([^\^<]+)<', data)

# print(words)