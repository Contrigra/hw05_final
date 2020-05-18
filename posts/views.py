from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from posts.forms import PostForm
from posts.models import Post, Group, User


def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    # Take a page number from the request, and let paginator know what page
    # we want to see
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html',
                  {'page': page, 'paginator': paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.group_posts.order_by('-pub_date')[:12]
    return render(request, 'group.html', {'group': group, 'posts': posts})


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    form = PostForm()
    return render(request, 'new_post.html', {'form': form})


def profile(request, username):
    user_data = get_object_or_404(User, username=username)
    current_user = request.user
    user_post_count = user_data.author_posts.count()
    post_list = user_data.author_posts.order_by('-pub_date')
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "profile.html",
                  {
                      'user_data': user_data,
                      'user_post_count': user_post_count,
                      'page': page,
                      'paginator': paginator,
                      'current_user': current_user
                  })


def post_view(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user_data = get_object_or_404(User, username=username)
    user_post_count = user_data.author_posts.count()
    return render(request, "post.html",
                  {'post': post,
                   'user_data': user_data,
                   'user_post_count': user_post_count})


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id)
    # Validating if PK of requesting user is the same as author's
    if request.user.pk != get_object_or_404(User, username=username).pk:
        return redirect('index')
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    form = PostForm(
        {'group': post.group, 'text': post.text, 'post_id': post_id})
    return render(request, 'new_post.html', {'form': form, 'post': post})
