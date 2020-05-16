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
        if not post_data.get('url') or post_data.get('type') not in ['include_html_tag', 'exclude_html_tag'] or \
                int(post_data.get('count')) < 1:
            return JsonResponse({"detail": "유효한 값을 입력해주세요."}, status=HttpResponseBadRequest.status_code)

        try:
            parser = Parser(post_data['url'], post_data['type'], int(post_data['count']))
            html = parser.get_html()
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=HttpResponseBadRequest.status_code)

        alphabet, decimal = parser.distribute_text(html)
        alphabet.sort(key=lambda alpha: (alpha.casefold(), alpha))
        decimal.sort()

        result = parser.merge_each_items(alphabet, decimal)
        quotient, remainder = parser.divide_text(result)

        return JsonResponse({
            "detail": {
                'quotient': quotient,
                'remainder': remainder
            }
        })
