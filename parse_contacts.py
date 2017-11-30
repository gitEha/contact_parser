import sys
import os
import re
import json

class ParseContacts():
    '''
    A class that takes in an input of area codes and text and parses out contact addresses (emails, phone numbers)
    from the given text.

    Arguments:
    area_codes -- A dict of country names, area codes, and country codes.

    text -- A string of text to parse the contacts from
    '''
    def __init__(self, area_codes, text):
        self.area_codes = area_codes
        self.text = text
        self.numbers = self.find_numbers_from_text(self.text, area_codes)
        self.emails = self.find_emails(self.text)
        self.contacts = {'Phone_numbers': self.numbers, 'Emails': self.emails }

    def find_numbers_from_text(self, text, area_codes):
        '''
        Takes in an input string and parses out all the phone numbers it finds.
        Arguments:
        text -- A string of text to parse phone numbers from.
        Returns:
        numbers -- A list containing the numbers found.
        '''
        numbers_to_process = []
        pattern = re.compile(
            r'(?:\b|[\+])\d{1,4}[-. ]?\d{2,4}(?:[-. ]?\d{1,4}\b)+')

        to_strip = str.maketrans("", "", " -.")
        for n in pattern.findall(text):
            numbers_to_process.append(n.translate(to_strip)) 
        print(numbers_to_process)
        numbers = self.find_area_code_matches(numbers_to_process, area_codes)
        return numbers

    @staticmethod
    def find_area_code_matches(numbers, area_codes):
        '''
        Takes in phone numbers and area codes and returns a list of dicts of details about a given number.
        if a given number doesn't find an area code to match it, it just gets added with the extra details being empty.

        Arguments:
        numbers -- A list of phone numbers in strings

        area_codes -- A dict of area codes and their corresponding country and country code.

        Returns:
        number_list -- A list containing dictionaries filled with detailed, formatted, sorted details for
                       each given phone number.
        '''

        number_list = []

        for number in numbers:
            for country in area_codes['countryCodes']:
                pattern = re.compile('\\' + country['dialling_code'])                
                for match in pattern.findall(number):
                    bracketed_num = number.replace(match, '(' + match + ')')
                    number_list.append({'number': bracketed_num, 'match': match,
                                        'country': country['country_name'], 'country_code': country['country_code']})
                    # So we could check if the number is already in the list for non-matched numbers
                    number = bracketed_num

            if number not in [x['number'] for x in number_list]:
                number_list.append(
                    {'number': number, 'match': '', 'country': '', 'country_code': ''})

        number_list = sorted(
            number_list, key=lambda k: len(k['number']), reverse=True)

        return number_list

    @staticmethod
    def find_emails(text):
        '''
        Find all the emails in the text.

        Arguments:
        text -- A string of text containing text to parse emails from.

        Returns:
        emails -- a list containing found emails from the input text.
        '''
        pattern = re.compile(r'[^\s@]+@[^@.]+[.][a-zA-Z]{1,10}')
        emails = pattern.findall(text)

        return emails


AREA_CODES = json.load(
    open(os.path.dirname(sys.argv[0]) + '/area_codes.json'))


TEXT = '''To contact us you can use our phone number: +372 5959 6129, +372 53546329
	or you can use our landline 65656660, if you cant reach any of those, try the help like 1188, or our friend's phone 56565550.
	The US line is +1-555-123-4567.
    
    If you prefer to contact us via email, you can contact us at andrus.rähnik@mail.ee, as well as емаил-аддрс@яндекс.c, or at मराठी@yahoo.com'''

FoundContacts = ParseContacts(AREA_CODES, TEXT)

[print(i) for i in [x for x in FoundContacts.contacts['Phone_numbers']]]
print(FoundContacts.contacts['Emails'])
