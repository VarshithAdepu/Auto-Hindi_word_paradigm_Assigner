def extract_and_store_words_from_file(input_file, output_file):
    """
    Extract words before ':' from the input file and save them to a .txt file.

    Args:
    - input_file (str): Path to the input file containing words and their tags.
    - output_file (str): Path to the .txt file where extracted words will be stored.

    Returns:
    - None
    """
    try:
        # Read the input file
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Extract words before ':'
        words = [line.split(':')[0].strip() for line in lines if ':' in line]

        # Write the extracted words to the output file
        with open(output_file, 'w', encoding='utf-8') as file:
            for word in words:
                file.write(word + '\n')

        print(f"Extracted words have been saved to {output_file}")

    except FileNotFoundError:
        print(f"Error: The file {input_file} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_file = "extracted_values.txt"  # Replace with your input file path
output_file = "extracted_words.txt"  # Replace with your desired output file path
extract_and_store_words_from_file(input_file, output_file)
