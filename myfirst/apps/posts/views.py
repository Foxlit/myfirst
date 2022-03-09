from django.shortcuts import render
from .models import Post
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView


class PostsList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'posts.html'
    context_object_name = 'posts'


def index(request):
    latest_posts_list = Post.objects.order_by('-pub_date')[:5]
    return render(request, 'posts/list.html', {'latest_posts_list': latest_posts_list})


def detail(request, posts_id):
    try:
        p = Post.objects.get(id=posts_id)
    except:
        raise Http404("Статья не найдена")

    latest_comments_list = p.comment_set.order_by('-id')[:10]

    return render(request, 'posts/detail.html', {'posts': p, 'latest_comments_list': latest_comments_list})


def leave_comment(request, posts_id):
    try:
        p = Post.objects.get(id=posts_id)
    except:
        raise Http404("Статья не найдена")

    p.comment_set.create(author_name=request.POST['name'], comment_text=request.POST['text'])

    return HttpResponseRedirect(reverse('posts:detail', args=(p.id,)))
