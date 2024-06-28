from datetime import timedelta, timezone
from itertools import count
from django.shortcuts import render
from .models import Post
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.utils import timezone




def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone()).order_by('-published_date')
    return render(request, 'myblog/post_list.html', {'posts': posts})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)  # Agar postni tafsilotlari sahifasiga o'tish kerak bo'lsa
    else:
        form = PostForm()
    return render(request, 'myblog/post_form.html', {'form': form})


def index(request):
    latest_posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:5]
    popular_posts = Post.objects.order_by('-views')[:5]  # Masalan, ko'p ko'rilganlar
    # Ommabop postlar uchun filtr
    # hafta:
    popular_posts_week = Post.objects.filter(published_date__gte=timezone.now()-timedelta(days=7)).annotate(num_views=count('view')).order_by('-num_views')[:5]
    # Oy:
    popular_posts_month = Post.objects.filter(published_date__gte=timezone.now()-timedelta(days=30)).annotate(num_views=count('view')).order_by('-num_views')[:5]

    context = {
        'latest_posts': latest_posts,
        'popular_posts': popular_posts,
        'popular_posts_week': popular_posts_week,
        'popular_posts_month': popular_posts_month,
    }
    return render(request, 'myblog/index.html', context)


