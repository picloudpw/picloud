"""PiCloud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('social_django.urls', namespace='social')),
    path('', include('cloud.urls')),
    path('', include('website.urls')),
    path('admin/', admin.site.urls, name='admin'),
    path('hierarchy/', include('hierarchy.urls', namespace='hierarchy')),
    path('memes/', include('memes.urls', namespace='memes')),
    path('posts/', include('posts.urls', namespace='posts')),
    path('students/', include('students.urls', namespace='students')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
