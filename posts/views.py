from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from posts.forms import PostForm
from posts.models import Post, Group


def index(request):
    latest = Post.objects.order_by('-pub_date')[:10]
    return render(request, 'index.html', {'posts': latest})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.group_posts.order_by('-pub_date')[:12]
    return render(request, 'group.html', {'group': group, 'posts': posts})


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        form.author = request.user
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    form = PostForm()
    return render(request, 'new_post.html', {'form': form})
