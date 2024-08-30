import sys

# Braille alphabet dictionary separated by case
braille_dicts = {
    'lower': {
        'a': 'O.....', 'b': 'O.O...', 'c': 'OO....', 'd': 'OO.O..', 'e': 'O..O..',
        'f': 'OOO...', 'g': 'OOOO..', 'h': 'O.OO..', 'i': '.OO...', 'j': '.OOO..',
        'k': 'O...O.', 'l': 'O.O.O.', 'm': 'OO..O.', 'n': 'OO.OO.', 'o': 'O..OO.',
        'p': 'OOO.O.', 'q': 'OOOOO.', 'r': 'O.OOO.', 's': '.OO.O.', 't': '.OOOO.',
        'u': 'O...OO', 'v': 'O.O.OO', 'w': '.OOO.O', 'x': 'OO..OO', 'y': 'OO.OOO',
        'z': 'O..OOO'
    },
    'upper': {
        'A': 'O.....', 'B': 'O.O...', 'C': 'OO....', 'D': 'OO.O..', 'E': 'O..O..',
        'F': 'OOO...', 'G': 'OOOO..', 'H': 'O.OO..', 'I': '.OO...', 'J': '.OOO..',
        'K': 'O...O.', 'L': 'O.O.O.', 'M': 'OO..O.', 'N': 'OO.OO.', 'O': 'O..OO.',
        'P': 'OOO.O.', 'Q': 'OOOOO.', 'R': 'O.OOO.', 'S': '.OO.O.', 'T': '.OOOO.',
        'U': 'O...OO', 'V': 'O.O.OO', 'W': '.OOO.O', 'X': 'OO..OO', 'Y': 'OO.OOO',
        'Z': 'O..OOO'
    },
    'numbers': {
        '1': 'O.....', '2': 'O.O...', '3': 'OO....', '4': 'OO.O..', '5': 'O..O..',
        '6': 'OOO...', '7': 'OOOO..', '8': 'O.OO..', '9': '.OO...', '0': '.OOO..'
    },
    'punctuation': {
        'CAPITAL': '.....O', 'SPACE': '......',
        '.': '..OO.O', ',': '..O...', '?': '..O.OO', '!': '..OO.O', ':': '..OO..',
        ';': '..O.O.', '-': '....OO', '/': '.O..O.', '(': 'O.O..O', ')': '.O.OO.',
        'DECIMAL': '.O...O', 'NUMBER': '.O.OOO'
    }
}

# Reverse lookup tables for decoding Braille
english_dicts = {
    'lower': {v: k for k, v in braille_dicts['lower'].items()},
    'upper': {v: k for k, v in braille_dicts['upper'].items()},
    'numbers': {v: k for k, v in braille_dicts['numbers'].items()},
    'punctuation': {v: k for k, v in braille_dicts['punctuation'].items()},
}

def translate_to_braille(text):
    """
    Translates a given English text into Braille.

    Args:
        text (str): The English text to be translated into Braille.

    Returns:
        str: A string representing the Braille translation of the input text.
    """
    result = []
    number_mode = False
    
    for char in text:
        if char.isupper():
            result.append(braille_dicts['punctuation']['CAPITAL'])
            result.append(braille_dicts['upper'][char])
            number_mode = False
        elif char.isdigit():
            if not number_mode:
                result.append(braille_dicts['punctuation']['NUMBER'])
                number_mode = True
            result.append(braille_dicts['numbers'][char])
        elif char == ' ':
            result.append(braille_dicts['punctuation']['SPACE'])
            number_mode = False
        elif char in braille_dicts['punctuation']:
            result.append(braille_dicts['punctuation'][char])
            number_mode = False
        else:
            result.append(braille_dicts['lower'][char])
            number_mode = False
    
    return ''.join(result)

def translate_to_english(braille):
    """
    Translates a given Braille text into English.

    Args:
        braille (str): The Braille text to be translated into English.

    Returns:
        str: A string representing the English translation of the input Braille text.
    """
    result = []
    i = 0
    capital_mode = False
    number_mode = False

    while i < len(braille):
        symbol = braille[i:i+6]

        if symbol == braille_dicts['punctuation']['CAPITAL']:
            capital_mode = True
        elif symbol == braille_dicts['punctuation']['NUMBER']:
            number_mode = True
        elif symbol == braille_dicts['punctuation']['SPACE']:
            result.append(' ')
            number_mode = False
        else:
            if number_mode and symbol in english_dicts['numbers']:
                char = english_dicts['numbers'][symbol]
            elif capital_mode and symbol in english_dicts['upper']:
                char = english_dicts['upper'][symbol]
                capital_mode = False
            elif symbol in english_dicts['lower']:
                char = english_dicts['lower'][symbol]
            elif symbol in english_dicts['punctuation']:
                char = english_dicts['punctuation'][symbol]
            else:
                char = ''
            result.append(char)
            if number_mode and symbol not in english_dicts['numbers']:
                number_mode = False

        i += 6

    return ''.join(result)

def main():
    """
    The main function that serves as the entry point for the script.
    It takes command-line input, determines if the input is English or Braille, 
    and then prints the translation.
    """
    if len(sys.argv) < 2:
        print("Please provide the text to translate as an argument.")
        return

    input_text = " ".join(sys.argv[1:])

    if all(char in ['O', '.'] for char in input_text):
        print(translate_to_english(input_text))
    else:
        print(translate_to_braille(input_text))

if __name__ == "__main__":
    main()
