from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse


# Create your models here.

class Post(models.Model):
    # Grabs the name of the authenticated user.
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()

    # timezone is set in settings.py file
    create_date = models.DateTimeField(default=timezone.now())

    # Post not immediately published and can be empty/blank.
    published_date = models.DateTimeField(blank=True, null=True)

    # This function will be called when the post is submitted.
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        # Grab the comments and filter the approved comments to display on the site.
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
         # After post is created, return to the post_detail page that matches this PrimaryKey.
        return reverse("post_detail", kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now())
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        # The home page.
        return reverse('post_list')

    def __str__(self):
        return self.text
