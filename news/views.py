from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from django.core.paginator import Paginator
from .models import Post
from .filters import PostFilter
from .forms import PostForm

class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    # queryset = Post.objects.order_by('-post_data')
    ordering = ['-post_data']
    paginate_by = 10

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

class PostCreateView(CreateView):
    template_name = 'add.html'
    form_class = PostForm

class PostUpdateView(UpdateView):
    template_name = 'edit.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDeleteView(DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
