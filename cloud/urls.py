from django.contrib.auth import views as auth_views
from django.urls import path

from cloud import views

urlpatterns = [
    path('', views.index.index, name='index'),
    path('robots.txt', views.robots.robots, name='robots'),

    path('auth/signup/', views.registration.sign_up, name="signup"),
    path('auth/signin/', views.authentication.sign_in, name="signin"),
    path('auth/signout/', views.authentication.sign_out, name="signout"),
    path('activate/<uid>/<token>/', views.registration.activate, name='activate'),

    # auth встроенное приложение, сброс пароля, переопределяющие шаблоны в registration
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('post/new/', views.posts.post_new, name='post_new'),
    path('post/<int:pk>/', views.posts.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.posts.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.posts.post_delete, name='post_delete'),
    path('post/<int:pk>/checked/', views.posts.post_checked, name='post_checked'),

    path('user/<user_id>', views.user.user_page, name='user_page'),
    path('user/<user_id>/posts', views.user.user_posts, name='user_posts'),
    path('user/<user_id>/not_checked_posts', views.user.user_not_checked_posts, name='user_not_checked_posts'),

    path('cloud/', views.posts.post_list, name='post_list'),
    path('search/', views.posts.search, name="search"),
    path('settings/', views.user.settings_page, name="settings"),
    path('message/', views.message.message, name="message"),
    path('moderation/', views.moderation.moderation, name="moderation"),
    path('change_password/', views.user.change_password, name='change_password'),
    path('change_avatar/', views.user.change_avatar, name='change_avatar'),
    path('change_user/', views.user.change_user, name='change_user'),

    path('universities/', views.universities.universities_list, name='universities_list'),
    path('universities/<university_id>/', views.universities.university_page, name='university_page'),
    path('universities/<university_id>/delete', views.universities.university_delete, name='university_delete'),
    path('universities/<university_id>/approve', views.universities.university_approve, name='university_approve'),

    path('program/<program_id>', views.programs.program_page, name='program_page'),
    path('subject/<subject_id>', views.subjects.subject_page, name='subject_page'),
    path('contacts/', views.contacts.contacts, name='contacts'),
    path('memes/', views.memes.get_memes, name='memes'),

    path('submit/university/', views.universities.new_university, name='new_university'),
    path('submit/department/', views.departments.new_department, name='new_department'),
    path('submit/chair/', views.chairs.new_chair, name='new_chair'),
    path('submit/program/', views.programs.new_program, name='new_program'),
    path('submit/subject/', views.subjects.new_subject, name='new_subject'),

    path('legal/privacy-policy/', views.legal.privacy_policy, name='privacy_policy'),

    # TODO: Сделать похожим на RESTful
    path('api/universities/', views.api.get_universities, name='get_universities'),
    path('api/departments/', views.api.get_departments, name='get_departments'),
    path('api/chairs/', views.api.get_chairs, name='get_chairs'),
    path('api/programs/', views.api.get_programs, name='get_programs'),
    path('api/subjects/', views.api.get_subjects, name='get_subjects'),
    path('api/posts/', views.search.search_and_render_posts, name='get_posts'),
    path('api/search_posts/', views.search.search_posts, name='search_posts'),
]
