from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.views import View

from .models import Post, Category  # Дополнительно импортируем категорию, чтобы пользователь мог её выбрать


class PostsList(ListView):
    model = Post
    template_name = 'list.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')


class Posts(ListView):
    model = Post
    template_name = 'list.html'
    context_object_name = 'posts'
    ordering = ['-pub_date']

    def post(self, request, *args, **kwargs):
        # берём значения для нового товара из POST-запроса, отправленного на сервер
        name = request.POST['name']
        category_id = request.POST['category']

        post = Post(name=name, category_id=category_id)
        post.save()
        return super().filter(request, *args, **kwargs)


def index(request):
    latest_posts_list = Post.objects.order_by('-pub_date')[:5]
    return render(request, 'posts/list.html', {'latest_posts_list': latest_posts_list})


def detail(request, posts_id):
    try:
        p = Post.objects.filter(id=posts_id)
    except:
        raise Http404("Статья не найдена")

    latest_comments_list = p.comment_set.order_by('-id')[:10]

    return render(request, 'posts/detail.html', {'posts': p, 'latest_comments_list': latest_comments_list})


def leave_comment(request, posts_id):
    try:
        p = Post.objects.filter(id=posts_id)
    except:
        raise Http404("Статья не найдена")

    p.comment_set.create(author_name=request.POST['name'], comment_text=request.POST['text'])

    return HttpResponseRedirect(reverse('posts:detail', args=(p.id,)))
