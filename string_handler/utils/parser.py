import string
from itertools import zip_longest

import requests


class Parser:
    def __init__(self, url):
        self.url = url

    def get_html(self):
        return requests.get(self.url).text

    @staticmethod
    def distribute_text(text, condition):
        stack = []
        alphabet = []
        decimal = []

        if condition == 'exclude_html_tag':
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
