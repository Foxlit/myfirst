from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from .models import Post, Comment, Category  # Дополнительно импортируем категорию, чтобы пользователь мог её выбрать
from .filters import PostFilter
from django.core.paginator import Paginator


class PostsList(ListView):
    paginate_by = 1
    model = Post
    template_name = 'list.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')


class Posts(ListView):
    model = Post
    template_name = 'list.html'
    context_object_name = 'posts'
    ordering = ['-pub_date']


def post(request, *args, **kwargs):
    # берём значения для нового товара из POST-запроса, отправленного на сервер
    name = request.POST['name']
    category_id = request.POST['category']
    pos = Post(name=name, category_id=category_id)  # создаём новую публикацию и сохраняем
    pos.save()
    return super().get(request, *args, **kwargs)  # отправляем пользователя обратно на GET-запрос.


def index(request):
    latest_posts_list = Post.objects.order_by('-pub_date')[:5]
    return render(request, 'posts/list.html', {'latest_posts_list': latest_posts_list})


def get_context_data(self, **kwargs):
    # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
    context = super().get_context_data(**kwargs)
    context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
    return context


def detail(request, posts_id):
    try:
        p = Post.objects.get(id=posts_id)
    except:
        raise Http404("Статья не найдена")

    latest_comments_list = p.comment_set.order_by('-id')[:10]

    return render(request, 'posts/detail.html', {'posts': p, 'latest_comments_list': latest_comments_list})


def create_comment(request, posts_id):
    try:
        p = Post.objects.get(id=posts_id)
    except:
        raise Http404("Статья не найдена")

    p.comment_set.create(author_name=request.POST['name'], comment_text=request.POST['text'])

    return HttpResponseRedirect(reverse('posts:detail', args=p.id,))


def like(comment_id=4):
    c = Comment.objects.get(id=comment_id)
    print(c)
    # return HttpResponseRedirect(reverse('posts:detail', args=c.id))


def dislike(posts_id):
    pass
    # try:
    #     p = Post.objects.get(id=posts_id)
    # except:
    #     raise Http404("Комментарий не найден")
    #
    # p.comment.post()
    # return HttpResponseRedirect(reverse('posts:detail', args=p.id))


def delete_post():
    print("Вы уверены, что хотите удалить публикацию?")
    answer = input('yes')
    if answer:
        Post.delete()
    else:
        pass


def edit_post():
    pass

