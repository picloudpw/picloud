from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


def index(request):
    if request.user.is_authenticated:
        return redirect('cloud')
    else:
        return redirect('about')


def robots(request):
    return render(request, 'robots.txt', content_type="text/plain")


def about(request):
    return render(request, 'index.html')


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


@login_required(login_url='/signin/')
def profile_page(request):
    return render(request, 'profile.html')


def moderation_page(request):
    return render(request, 'moderation.html')


def post_page(request):
    return render(request, 'posts.html')


def departments_page(request):
    return render(request, 'departments.html')


@login_required(login_url='/signin/')
def students_page(request):
    return render(request, 'students.html')


@login_required(login_url='/signin/')
def memes_page(request):
    return render(request, 'memes.html')
