from django.shortcuts import render


def home(request):
    rendered = render(request, 'polls/base.html', {})
    return rendered
