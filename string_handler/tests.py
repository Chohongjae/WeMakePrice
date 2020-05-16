from pprint import pprint

from django.shortcuts import resolve_url
from django.test import TestCase


class StringHandlerTest(TestCase):
    def setUp(self) -> None:
        self.url = resolve_url('string_handler:handler')

    def test_main_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'string_handler/index.html')

    def test_fail_handler_invalid_url(self):
        '''
        Url에 scheme이 없기 때문에 실패를 의도한다.
        '''
        data = {
            'url': 'www.front.wemakeprice.com/main?utm_source=google&utm_medium=cpc&utm_campaign=null&utm_term=%EC%9C%84%EB%A9%94%ED%94%84%2E&utm_content=wemake&gclid=Cj0KCQjwnv71BRCOARIsAIkxW9FYigrgZN9FzQJ7X3_wXRnMrpbbGjpcV2gHYgEro7Dv14mj_gA29UoaApaYEALw_wcB',
            'type': 'include_html_tag',
            'count': 2
        }
        response = self.client.post(self.url, data, format='json')
        pprint(response.json())
        self.assertEqual(response.status_code, 400)

    def test_fail_handler_invalid_type(self):
        '''
        type이 올바르지 않기 때문에 실패를 의도한다.
        '''
        data = {
            'url': 'https://front.wemakeprice.com/main?utm_source=google&utm_medium=cpc&utm_campaign=null&utm_term=%EC%9C%84%EB%A9%94%ED%94%84%2E&utm_content=wemake&gclid=Cj0KCQjwnv71BRCOARIsAIkxW9FYigrgZN9FzQJ7X3_wXRnMrpbbGjpcV2gHYgEro7Dv14mj_gA29UoaApaYEALw_wcB',
            'type': 'test',
            'count': 2
        }
        response = self.client.post(self.url, data, format='json')
        pprint(response.json())
        self.assertEqual(response.status_code, 400)

    def test_fail_handler_invalid_count(self):
        '''
        1보다 작은 count를 입력했기 때문에 때문에 실패를 의도한다.
        '''
        data = {
            'url': 'https://front.wemakeprice.com/main?utm_source=google&utm_medium=cpc&utm_campaign=null&utm_term=%EC%9C%84%EB%A9%94%ED%94%84%2E&utm_content=wemake&gclid=Cj0KCQjwnv71BRCOARIsAIkxW9FYigrgZN9FzQJ7X3_wXRnMrpbbGjpcV2gHYgEro7Dv14mj_gA29UoaApaYEALw_wcB',
            'type': 'include_html_tag',
            'count': 0
        }
        response = self.client.post(self.url, data, format='json')
        pprint(response.json())
        self.assertEqual(response.status_code, 400)

    def test_success_handler(self):
        '''
        모두 유효한 값으로 성공을 의도한다.
        '''
        data = {
            'url': 'https://front.wemakeprice.com/main?utm_source=google&utm_medium=cpc&utm_campaign=null&utm_term=%EC%9C%84%EB%A9%94%ED%94%84%2E&utm_content=wemake&gclid=Cj0KCQjwnv71BRCOARIsAIkxW9FYigrgZN9FzQJ7X3_wXRnMrpbbGjpcV2gHYgEro7Dv14mj_gA29UoaApaYEALw_wcB',
            'type': 'include_html_tag',
            'count': 5
        }
        response = self.client.post(self.url, data, format='json')
        pprint(response.json())
        self.assertEqual(response.status_code, 200)

        data = {
            'url': 'https://front.wemakeprice.com/main?utm_source=google&utm_medium=cpc&utm_campaign=null&utm_term=%EC%9C%84%EB%A9%94%ED%94%84%2E&utm_content=wemake&gclid=Cj0KCQjwnv71BRCOARIsAIkxW9FYigrgZN9FzQJ7X3_wXRnMrpbbGjpcV2gHYgEro7Dv14mj_gA29UoaApaYEALw_wcB',
            'type': 'exclude_html_tag',
            'count': 5
        }
        response = self.client.post(self.url, data, format='json')
        pprint(response.json())
        self.assertEqual(response.status_code, 200)

    def test_parser_class(self):
        '''
        parser 클래스를 테스트한다.
        '''
        from .utils.parser import Parser
        parser = Parser('www.test.com', 'test', 5)

        alphabet = ['b', 'A', 'B', 'a', 'A', 'A', 'a']
        decimal = list(map(lambda x: str(x), [0, 1, 0]))
        alphabet.sort(key=lambda alpha: (alpha.casefold(), alpha))
        decimal.sort()

        result = parser.merge_each_items(alphabet, decimal)
        quotient, remainder = parser.divide_text(result)

        self.assertEqual(quotient, 'A0A0A1aaBb')
        self.assertEqual(remainder, '')
