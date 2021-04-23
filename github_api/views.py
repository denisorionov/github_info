import requests
from django.shortcuts import render

from github_api.utils import search, token


def view_search(request):
    args = {}
    if request.GET.get('search', ''):
        owner = request.GET.get('search', '')
        result_search = search(token, owner)

        if result_search is None:
            args["message"] = "Пользователь не найден"
        elif not result_search:
            args["message"] = "У пользователя нет пул-реквестов"

        return render(request, template_name='search.html', context={"result_search": result_search, "args": args})

    return render(request, template_name='search.html')
