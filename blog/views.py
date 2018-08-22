from django.shortcuts import render
from django.utils import timezone

# Below statement is akin to the login_required decorator.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)


class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):
    # This statement connects this view to the Post Model
    model = Post

    # Defines how to grab and display the list. Allows the use of django's ORM when dealing with generic views.
    def get_queryset(self):
        # Means you want all of the Post objects and they'll be filtered based on the "published_date" being less than
        # or equal to (__lte) the current time then order them by published date in descending order. (- means
        # descending, while + means ascending.)
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin, CreateView):
    # If user isn't logged in then the user is redirected to login.url.
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class PostUpdateView(LoginRequiredMixin, UpdateView):
    # If user isn't logged in then the user is redirected to login.url.
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    # Url referred to when delete is successful.
    # Reverse_lazy means it waits until confirmation before redirection.
    success_url = reverse_lazy('post_list')


class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        # __isnull means that there is no value for the published date.
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')