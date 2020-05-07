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
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="author_posts")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              null=True, blank=True, verbose_name="Group",
                              related_name="group_posts")

    def __str__(self):
        return self.text
