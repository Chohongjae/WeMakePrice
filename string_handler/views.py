from django.http import JsonResponse
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic.base import View

from .utils.parser import Parser


class StringHandlerView(View):
    def get(self, request):
        return render(request, 'string_handler/index.html', {})

    def post(self, request):
        post_data = request.POST
        parser = Parser(post_data['url'])
        try:
            html = parser.get_html()
        except Exception as e:
            return JsonResponse({
                "is_valid": False,
                "detail": str(e)
            }, status=HttpResponseBadRequest.status_code)

        alphabet, decimal = parser.distribute_text(html, post_data['type'])
        alphabet.sort(key=lambda alpha: (alpha.casefold(), alpha))
        decimal.sort()

        result = parser.merge_each_items(alphabet, decimal)
        length = len(result)
        if length < int(post_data['count']):
            quotient = ''
            remainder = result
        elif length == int(post_data['count']):
            quotient = result
            remainder = ''
        else:
            quotient = result[:(length // int(post_data['count'])) * int(post_data['count'])]
            if quotient == result:
                remainder = ''
            else:
                remainder = result[-(length % int(post_data['count'])):]

        return JsonResponse({
            "is_valid": True,
            "detail": {
                'quotient': quotient,
                'remainder': remainder
            }
        })
