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
        '''
        조건(condition)에 따라 html 태그를 포함할지 안할지를 선택하고
        html 문서 안에 숫자와 영어를 분리해서 반환한다.
        만약 html 태그를 포함하지 않을 경우 문서 중간에
        <body>
            <테스트입니다.
        </body>
        이런 텍스트가 나올 경우 "<" 가 열려있고 스택에 담겨있기 때문에 그 밑에 글자들은 포함되지 않는다.
        :param text: html 문서
        :return: html 문서안에 영어와 숫자 배열
        '''
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
        '''
        알파벳과 숫자 배열을 알파벳이 앞에 나오게 하나씩 짝지어서 이어진 문자열을 반환한다.
        '''
        return ''.join([item for items in zip_longest(alphabet, decimal) for item in items if item is not None])

    def divide_text(self, text):
        '''
        주어진 출력묶음단위에 따라 문자열을 잘라 몫과 나머지를 반환한다.
        '''
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
