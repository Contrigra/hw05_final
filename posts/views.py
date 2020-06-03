from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from posts.forms import PostForm, CommentForm
from posts.models import Post, Group, User, Comment, Follow


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
    post_list = group.group_posts.order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'group.html',
                  {'group': group, 'page': page, 'paginator': paginator})


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    form = PostForm()
    return render(request, 'new_post.html', {'form': form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.author_posts.order_by('-pub_date')
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    item_dict = {
        'author': author,
        'page': page,
        'paginator': paginator,

    }
    if not request.user.is_anonymous:
        following = Follow.objects.filter(user=request.user, author=author)
        item_dict['following'] = following

    return render(request, "profile.html", item_dict
                  )


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, author=author, pk=post_id)
    items = Comment.objects.filter(post=post_id)

    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            return redirect('post_view', username=username,
                            post_id=post_id)

    form = CommentForm(request.POST or None)
    return render(request, 'post.html',
                  {'post': post,
                   'author': author,
                   'form': form,
                   'items': items})


@login_required
def post_edit(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=author)

    if request.user != author:
        return redirect("post_view", username=request.user.username,
                        post_id=post_id)

    form = PostForm(request.POST or None, files=request.FILES or None,
                    instance=post)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("post_view", username=request.user.username,
                            post_id=post_id)

    return render(
        request, "new_post.html", {"form": form, "post": post},
    )


def page_not_found(request, exception):
    """The redefinition of the 404 page.
    Exception contains debug info given by django"""

    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author = get_object_or_404(User, username=username)
    items = Comment.objects.filter(post=post.id)

    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            return redirect('post_view', username=username,
                            post_id=post_id)

    form = CommentForm(request.POST or None)
    return render(request, 'post.html',
                  {'post': post,
                   'author': author,
                   'form': form,
                   'items': items})


@login_required
def follow_index(request):
    user = request.user
    followed_authors = user.follower.all()

    # Create a list of posts to paginate
    post_list = []
    for author in followed_authors:
        post_list += Post.objects.filter(author_id=author.author_id)

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html',
                  {'page': page, 'paginator': paginator})

    # return render(request, "follow.html", {...})


@login_required
def profile_follow(request, username):
    author = User.objects.get(username=username)
    if Follow.objects.filter(user=request.user,
                             author_id=author.id).count() == 1:
        return redirect('profile', username=username)

    if request.user != author:
        Follow.objects.create(user=request.user, author=author)
        return redirect('profile', username=username)

    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = User.objects.get(username=username)
    follow_to_delete = Follow.objects.filter(user=request.user,
                                             author=author)
    follow_to_delete.delete()
    return redirect('profile', username=username)
