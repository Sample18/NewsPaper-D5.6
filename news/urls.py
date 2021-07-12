from django.urls import path
from .views import PostList, PostDetail, PostSearch, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>/', PostDetail.as_view()),
    path('search/', PostSearch.as_view()),
    path('add/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]