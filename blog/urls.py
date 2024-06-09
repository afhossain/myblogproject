from django.urls import path
from . import views
from .views import PostListView,UserPostListView,PostDetailsView,PostCreateView,PostUpdateView,PostDeleteView

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('<int:pk>/', PostDetailsView.as_view(), name='post-detail'),
    path('new/', PostCreateView.as_view(), name='post-create'),
    path('update/<int:pk>/', PostUpdateView.as_view(), name='post-update'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    # path('', PostListView.as_view(), name='blog-home'),
    path('about/', views.about, name='blog-about'),
]

