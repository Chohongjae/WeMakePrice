import string
from itertools import zip_longest

import requests


class Parser:
    def __init__(self, url, condition, count):
        self.url = url
        self.condition = condition
        self.count = count

    def get_html(self):
        return requests.get(self.url).text

    def distribute_text(self, text):
        stack = []
        alphabet = []
        decimal = []

        if self.condition == 'exclude_html_tag':
            for i in text:
                if i == '<':
                    stack.append(i)
                elif i == '>' and stack:
                    stack.pop()
                elif not stack:
                    if i.isdecimal():
                        decimal.append(i)
                    elif i in string.ascii_letters:
                        alphabet.append(i)
        else:
            for i in text:
                if i.isdecimal():
                    decimal.append(i)
                elif i in string.ascii_letters:
                    alphabet.append(i)
        return alphabet, decimal

    @staticmethod
    def merge_each_items(alphabet, decimal):
        return ''.join([item for items in zip_longest(alphabet, decimal) for item in items if item is not None])

    def divide_text(self, text):
        length = len(text)
        if length < self.count:
            quotient = ''
            remainder = text
        elif length == self.count:
            quotient = text
            remainder = ''
        else:
            quotient = text[:(length // self.count) * self.count]
            if quotient == text:
                remainder = ''
            else:
                remainder = text[-(length % self.count):]

        return quotient, remainder
