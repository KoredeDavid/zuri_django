from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import CustomUserCreationForm, PostForm, CommentForm
from .models import Post, Category, Comment, CustomUser


# Create your views here.

def register(request):
    next_page = request.GET.get('next')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = CustomUser.objects.get(username__iexact=username)
            login_user = authenticate(username=user, password=password)
            print(login_user)
            login(request, login_user)
            if next_page is None:
                return redirect('home')
            elif user is not None:
                return redirect(next_page)
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('home')
    next_page = request.GET.get('next')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == "" or password == "":
            messages.error(request, 'Both username/email and password must be filled')
            return render(request, 'blog/login.html')
        try:
            username = CustomUser.objects.get(username__iexact=username).username
        except CustomUser.DoesNotExist:
            pass
        print(username, password)
        user = authenticate(request=request, username=username, password=password)
        if next_page is None:
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Guy, your login details are incorrect')
                return render(request, 'blog/login.html')
        elif user is not None:
            login(request, user)
            return redirect(next_page)
        else:
            messages.error(request, 'Guy, your login details are incorrect')
            return render(request, 'blog/login.html')

    else:
        return render(request, 'blog/login.html')


def repo(request):
    return redirect('https://github.com/korededavid/zuri_django/')


def home(request):
    blog_category = Category.objects.all()
    context = {
        'category': blog_category
    }
    return render(request, 'blog/home.html', context)


@login_required
def articles_factory(request):
    if request.user.is_author:
        print(request.user)
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                if 'save_as_draft' in request.POST:
                    fill_author_name = form.save(commit=False)
                    fill_author_name.author = request.user
                    fill_author_name.save_as_draft()
                if 'save' in request.POST and request.user.is_pro_author or request.user.is_boss:
                    fill_author_name = form.save(commit=False)
                    fill_author_name.author = request.user
                    fill_author_name.publish()
                    fill_author_name.save()
                if 'send_for_approval' in request.POST and not request.user.is_pro_author or not request.user.is_boss:
                    pass
        else:
            form = PostForm()
        context = {'form': form}
        return render(request, 'blog/articles_factory.html', context)
    else:
        raise PermissionDenied


@login_required
def drafts(request):
    if request.user.is_author:
        drafts = Post.objects.filter(draft=True)
        context = {'drafts': drafts}
        return render(request, 'blog/drafts.html', context)
    else:
        raise PermissionDenied


def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug, )
    posts = Post.objects.filter(category__slug=category_slug, published=True, draft=False)
    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'blog/category.html', context)


def post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug, published=True, draft=False)
    category = Category.objects.get(post__slug=post_slug)

    if request.method == 'POST':
        print('rgerget')
        if request.user.is_authenticated:
            print('rgt')
            form = CommentForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.post = post
                instance.save()
                messages.success(request, 'Comment Saved')
                return redirect(f'/post/{post_slug}/#form')
    form = CommentForm()
    context = {
        'post': post,
        'category': category,
        'form': form
    }
    return render(request, 'blog/post.html', context)


def blog_index(request):
    posts = Post.objects.all().order_by('-created_on')
    context = {
        "posts": posts,
    }
    return render(request, "blog_index.html", context)


# @login_required
def comment(request, post):
    comments = Comment.objects.filter(post=post).values('body', 'user__display_name').order_by('-created_on')
    data = {'comments': list(comments)}
    return JsonResponse(data, safe=False)


# @login_required
# def make_comment(request, user, post):
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.user = user
#             instance.post = post
#             instance.save()
#             post_slug = Post.objects.get(id=post).slug
#             return redirect('post', post_slug)


def sign_out(request):
    logout(request)
    messages.success(request, 'Logged Out Successfully  👑Sire')
    return redirect("sign_in")
