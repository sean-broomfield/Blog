from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
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
    template_name = 'blog/about.html'


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


############################

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


# Primary Key needed to link the Comment to Post
@login_required
def add_comment_to_post(request, pk):

    # Get "post" or a 404 page.
    post = get_object_or_404(Post, pk=pk)

    # If the form has been filled out and hit submit.
    if request.method == 'POST':

        # Above request is passed in here.
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    # 1st form in the context dictionary refers to the name that will be called in the html
    # 2nd form is the form that was initialized above.
    return render(request, 'blog/comment_form.html', {'form':form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()

    # Redirects to a post detail page of the of the original blog pose.
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail,', pk=post_pk)