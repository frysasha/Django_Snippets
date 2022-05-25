from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from MainApp.forms import SnippetForm


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("snippets_list")
        return render(request, 'add_snippet.html', {'form': form})
    elif request.method == "GET":
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form
        }
        return render(request, 'pages/add_snippet.html', context)


def edit_snippet(request, s_id):
    try:
        snippet = Snippet.objects.get(pk=s_id)
        form = SnippetForm(request.POST)
        context = {
            'pagename': 'Изменение сниппета',
            'form': form,
            'snippet': snippet
        }
        if request.method == "POST":
            snippet.name = request.POST.get('name')
            snippet.lang = request.POST.get('lang')
            snippet.code = request.POST.get('code')
            snippet.save()

            return HttpResponseRedirect("/")
        else:
            return render(request, 'pages/snippet_edit_page.html', context)
    except Snippet.DoesNotExist:
        return HttpResponseNotFound('Snippet not found')


def delete_snippet(request, s_id):
    try:
        snippet = Snippet.objects.get(pk=s_id)
        snippet.delete()
        return redirect("snippets_list")
    except Snippet.DoesNotExist:
        return HttpResponseNotFound('Snippet not found')


def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets}
    return render(request, 'pages/view_snippets.html', context)


def snippet_page(request, s_id):
    snippet = Snippet.objects.get(pk=s_id)
    context = {
        'pagename': 'Просмотр сниппетA!',
        'snippet': snippet}
    return render(request, 'pages/snippet_page.html', context)


