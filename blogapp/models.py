from django.db import models
from django.utils import timezone
from django.urls import reverse

# user can create a post 
class User(models.Model):
    
    name = models.CharField(max_length=255)

    def __str__(self):

        return self.name

# posts go to template
class Post(models.Model):

    class Status(models.TextChoices):

        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', null=True)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    class Meta:

        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):

        return self.title

    def get_absolute_url(self):

        return reverse('blog:post_detail', args = [self.slug])

# comments on posts
class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user_name = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):

        return f"comment by {self.user_name} on {self.post}"
