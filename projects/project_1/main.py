from morse_data import data
from art import logo
import os


class MorseCodeConverter:
    def __init__(self):
        self.clear_screen()
        print(logo)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def convert_to_morse(self, message):
        morse_message = ''
        for english_char in message:
            if english_char == ' ':
                morse_message += '  '
            else:
                for morse in data:
                    if english_char.lower() == morse['letter']:
                        morse_message += morse['morse'] + ' '
        print(morse_message)

    def convert_to_english(self, message):
        english_message = ''
        morse_list = message.split('   ')
        for word in morse_list:
            morse_chars = word.split(' ')
            for morse_char in morse_chars:
                found = False
                for morse in data:
                    if morse_char == morse['morse']:
                        english_message += morse['letter']
                        found = True
                        break
                if not found:
                    english_message += '?'
            english_message += ' '
        print(english_message)

    def run(self):
        continue_loop = True

        while continue_loop:
            conversion_option = input('What type of conversion would you like? (Type number)\n'
                                      '1. Morse code to English\n'
                                      '2. English to Morse code\n')

            if conversion_option == '1':
                self.clear_screen()
                print(logo)
                user_message = input('What message would you like in English?\n')
                self.convert_to_english(user_message)
            elif conversion_option == '2':
                self.clear_screen()
                print(logo)
                user_message = input('What message would you like in Morse Code?\n')
                self.convert_to_morse(user_message)
            else:
                self.clear_screen()
                print(logo)
                print('You have chosen an option that doesn\'t exist. Please select again.')
                continue

            another_conversion = input('Would you like to convert another option? (Type \'Yes\' or \'No\')\n')

            if another_conversion.lower() == 'no':
                continue_loop = False
            elif another_conversion.lower() == 'yes':
                self.clear_screen()
                print(logo)
            else:
                self.clear_screen()
                print(logo)
                print('You have chosen an option that doesn\'t exist. Thanks for using the translator!')
                continue_loop = False

if __name__ == "__main__":
    converter = MorseCodeConverter()
    converter.run()
