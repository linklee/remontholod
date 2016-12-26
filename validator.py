import re


class Validator(object):

    @staticmethod
    def required(text):
        if not text or len(text) <= 0:
            return False
        return True

    @staticmethod
    def phone(text):
        if Validator.required:
            match = re.match(r'^\s*(?:\+?(\d{1,3}))?([-. (]*(\d{3})[-. )]*)?((\d{3})[-. ]*(\d{2,4})(?:[-.x ]*(\d+))?)\s*$', text)
            return match

    @staticmethod
    def email(text):
        if Validator.required:
            match = re.match(r'[^@]+@[^@]+\.[^@]+', text)
            return match

    @staticmethod
    def length(text, length):
        if len(text) >= length:
            return True
        return False