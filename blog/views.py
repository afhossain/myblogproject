from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Post, Blog_Category
from django.views.generic import (
    ListView,DetailView,
    CreateView,UpdateView,DeleteView)




class PostListView(ListView):
    model=Post
    context_object_name='posts'
    template_name='blog/home.html'
    ordering=['-date_posted']
    paginate_by=2

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add extra variables to the context
        context['blog_categories'] = get_blog_categories()
        return context

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5 

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add extra variables to the context
        context['blog_categories'] = get_blog_categories()
        return context

class PostDetailsView(DetailView):
    model=Post

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add extra variables to the context
        context['blog_categories'] = get_blog_categories()
        return context
    

class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    fields=['title','content','image','category']

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add extra variables to the context
        context['blog_categories'] = get_blog_categories()
        return context

    

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Post
    fields=['title','content']

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self) -> bool | None:
        post=self.get_object()
        if self.request.user==post.author:
            return True
        else:
            return False
        
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add extra variables to the context
        context['blog_categories'] = get_blog_categories()
        return context

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    success_url = '/'  # Redirect after deletion
    # template_name = 'post_confirm_delete.html'

    
    
    def test_func(self) :
        post=self.get_object()
        if self.request.user==post.author:
            return True
        else:
            return False
        
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add extra variables to the context
        context['blog_categories'] = get_blog_categories()
        return context


def get_blog_categories():

    return Blog_Category.objects.all()
        
    
    

    




def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
