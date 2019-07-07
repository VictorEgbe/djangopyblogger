from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ArticleCreationForm, UserCommentForm
from .models import Article, Comment


def index(request):
    page_request = request.GET.get('page')
    query = request.GET.get('q')
    if query:
        articles = Article.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query)).distinct()
        paginator = Paginator(articles, 5)
        page = paginator.get_page(page_request)
    else:
        articles = Article.objects.all()
        paginator = Paginator(articles, 5)
        page = paginator.get_page(page_request)
    context = {
        'title': 'Home',
        'page': page
    }
    return render(request, 'articles/index.html', context)


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    comments = Comment.objects.filter(article=article)
    form = UserCommentForm()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            raise PermissionDenied
        form = UserCommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.article = article
            instance.save()
            messages.success(request, f'You commented on the post "{article.title}".')
            return HttpResponseRedirect(article.get_absolute_url())
    context = {
        'title': 'Article Detail',
        'article': article,
        'comments': comments,
        'count': comments.count(),
        'form': form
    }
    return render(request, 'articles/details.html', context)


@login_required
def create_article(request):
    form = ArticleCreationForm()
    if request.method == 'POST':
        form = ArticleCreationForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            messages.success(request, f"Article '{title}' was created successfully.")
            return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'form': form,
        'title': 'Create Article'
    }
    return render(request, 'articles/create.html', context)


@login_required
def update(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if not request.user == article.author:
        raise PermissionDenied
    form = ArticleCreationForm(instance=article)
    if request.method == 'POST':
        form = ArticleCreationForm(request.POST, instance=article)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, f'Article updated successfully')
            return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'title': 'Update Article',
        'form': form,
        'article': article,
    }
    return render(request, 'articles/update.html', context)


@login_required
def delete_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if not request.user == article.author:
        raise PermissionDenied
    if request.method == 'POST':
        article.delete()
        messages.success(request, f'Article deleted successfully')
        return redirect('index')
    context = {'title': 'Delete Article', 'article': article}
    return render(request, 'articles/delete.html', context)


def user_articles(request, username):
    page_request = request.GET.get('page')
    specific_user = get_object_or_404(User, username=username)
    articles = Article.objects.filter(author=specific_user)
    paginator = Paginator(articles, 3)
    page = paginator.get_page(page_request)
    context = {
        'title': specific_user,
        'count': articles.count(),
        'page': page
    }
    return render(request, 'articles/user_articles.html', context)
