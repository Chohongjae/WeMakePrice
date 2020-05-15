from django.shortcuts import resolve_url
from django.test import TestCase, Client
from pprint import pprint


class StringHandlerTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.url = resolve_url('string_handler:handler')

    def test_get_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_fail_handler_invalid_url(self):
        '''
        No scheme
        '''
        data = {
            'url': 'https://www.naver.com',
            'type': 2,
            'count': -1
        }
        response = self.client.post(self.url, data, format='json')
        pprint(response.json())
        self.assertEqual(response.status_code, 400)
