from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost
from .forms import BlogPostForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate


def home(request):
    posts = BlogPost.objects.all().order_by('-date_added')
    return render(request, 'blogs/home.html', {'posts': posts})
@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = BlogPostForm()
    return render(request, 'blogs/create_post.html', {'form': form})
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blogs/edit_post.html', {'form': form, 'post': post})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Авторизация пользователя
            print(f'User {user.username} logged in successfully.')  # Отладочная информация
            return redirect('home')  # Перенаправление на главную страницу
    else:
        form = UserCreationForm()
    return render(request, 'blogs/register.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Аутентификация пользователя
                return redirect('home')  # Перенаправление на главную страницу
            else:
                form.add_error(None, "Неверное имя пользователя или пароль.")
    else:
        form = LoginForm()

    return render(request, 'blogs/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')