from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse # TODO delete it
from .models import Post, Group
# Create your views here.


def index(request):
    # Делаем запрос в базу SQL
    latest = Post.objects.order_by("-pub_date")[:10]
    # собираем тексты в один, разедляя строкой
    return render(request, "index.html", {"posts": latest})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    return render(request, "group.html", {"group": group, "posts": posts})
