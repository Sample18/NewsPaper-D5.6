from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Post, Author
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


class PostList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    # queryset = Post.objects.order_by('-post_data')
    ordering = ['-post_data']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context

class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'
    ordering = ['-post_data']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'onenews.html'
    context_object_name = 'onenews'

class PostCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'add.html'
    form_class = PostForm
    permission_required = ('news.add_post',)

    def get(self, request, *args, **kwargs):
        send_mail(
            subject=Post.heading,
            message=Post.content,
            from_email='***@yandex.ru',
            recipient_list=['***@gmail.com']
        )



class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'edit.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
        Author.objects.create(author=user)
    return redirect('/news/')
