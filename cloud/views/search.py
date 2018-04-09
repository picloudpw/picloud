from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render

from cloud.models import Post
from .posts import POSTS_PER_PAGE


def search_posts(request):
    words = request.GET.get('search_request', None).lover().split(" ")
    posts = Post.objects.filter(approved=True)
    posts = posts.order_by('created_date').reverse()[:100]
    posts = [obj.as_dict() for obj in posts]
    return JsonResponse(posts, safe=False)


def search_and_render_posts(request):
    subject_id = request.GET.get('subject_id', None)
    type_id = request.GET.get('type_id', None)
    posts = Post.objects.filter(approved=True)
    if subject_id is not None:
        posts = posts.filter(subject=subject_id)
    if type_id is not None:
        posts = posts.filter(type=type_id)
    posts = posts.order_by('created_date').reverse()[:100]

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, POSTS_PER_PAGE)
    try:
        posts_page = paginator.page(page)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
        posts_page = paginator.page(paginator.num_pages)

    return render(request, 'cloud/bare_post_list.html', {'posts': posts_page})