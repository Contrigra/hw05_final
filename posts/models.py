from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True,
                                    db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_posts')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              null=True, blank=True, verbose_name='Group',
                              related_name='group_posts')
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True,
                             blank=True, verbose_name='Comment',
                             related_name='post_comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comment_author')
    text = models.TextField()
    created = models.DateTimeField('date published', auto_now_add=True)
