from django.http import Http404
from django.shortcuts import render, redirect


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    context = {'pagename': 'Добавление нового сниппета'}
    return render(request, 'pages/add_snippet.html', context)


def snippets_page(request):
    context = {'pagename': 'Просмотр сниппетов'}
    return render(request, 'pages/view_snippets.html', context)


def snippet_page(request, s_id):
    context = {
        'pagename': 'Просмотр сниппетA!',
        'snippet_id': s_id}
    return render(request, 'pages/snippet_page.html', context)
