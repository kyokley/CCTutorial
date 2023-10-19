from django.shortcuts import render


def home(request):
    rendered = render(request, 'cctutorial/home.html', {})
    return rendered
