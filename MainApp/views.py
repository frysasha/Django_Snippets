from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from MainApp.models import Snippet, Comment
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method == "POST":

        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)  # создаем объект но не отправляет в БД
            if request.user.is_authenticated:
                snippet.user = request.user
            snippet.save()
            return redirect("snippets_list")
        return render(request, 'add_snippet.html', {'form': form})
    if request.method == "GET":
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
    snippets = Snippet.objects.all().exclude(private=True)
    if request.user.is_authenticated:
        private_snippets = Snippet.objects.filter(user=request.user).filter(private=True)
        snippets = snippets | private_snippets
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets}
    return render(request, 'pages/view_snippets.html', context)

@login_required
def my_snippets_list(request):
    snippets = Snippet.objects.filter(user=request.user)
    context = {
        'pagename': 'Мои сниппеты',
        'snippets': snippets}
    return render(request, 'pages/view_snippets.html', context)


def snippet_page(request, s_id):
    snippet = Snippet.objects.get(pk=s_id)
    form = CommentForm(request.POST)
    context = {
        'pagename': 'Просмотр сниппетA!',
        'snippet': snippet,
        'form': form}
    return render(request, 'pages/snippet_page.html', context)


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(request, username=username, password=password)
        if user:
            auth.login(request, user)
        else:
            # Return error message
            pass
    redirect_to = request.GET.get('next', '')
    return redirect(redirect_to)


def logout(request):
    auth.logout(request)
    redirect_to = request.GET.get('next', '')
    return redirect(redirect_to)


def registration(request):
    if request.method == "GET":
        form = UserRegistrationForm()
        context = {'pagename': 'Регистрация пользователя', "form": form}
        return render(request, 'pages/registration.html', context)
    if request.method == "POST":  # информацию от формы
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        context = {
            'pagename': 'Регистрация пользователя',
            "form": form,
        }
        return render(request, 'pages/registration.html', context)


def comment_add(request):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        snippet_id = request.POST.get('snippet_id')
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.snippet = Snippet.objects.get(id=snippet_id)
            comment.save()
        #return render(request, 'snippet_page.html', {'comment_form': comment_form})
        return redirect(f'/snippets/{snippet_id}')
    raise Http404
