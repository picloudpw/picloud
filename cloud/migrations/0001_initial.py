# Generated by Django 2.0.2 on 2019-09-04 17:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('short_title', models.CharField(blank=True, max_length=64, null=True)),
                ('link', models.URLField(blank=True, max_length=512, null=True)),
                ('is_approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('short_title', models.CharField(blank=True, max_length=64, null=True)),
                ('link', models.URLField(blank=True, max_length=512, null=True)),
                ('is_approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('surname', models.CharField(max_length=64)),
                ('patronymic', models.CharField(blank=True, max_length=64, null=True)),
                ('complexity', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('image', models.ImageField(blank=True, default='resources/default/lec_avatar.png', null=True, upload_to='resources/lec_avatars/')),
                ('is_approved', models.BooleanField(default=False)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cloud.Department')),
            ],
        ),
        migrations.CreateModel(
            name='MemeSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField(blank=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('chair', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cloud.Chair')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cloud.Department')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('text', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.ImageField(blank=True, null=True, upload_to='resources/posts/%Y/%m/%d/')),
                ('link', models.URLField(blank=True, max_length=512, null=True)),
                ('views', models.PositiveIntegerField(default=0)),
                ('file', models.FileField(blank=True, null=True, upload_to='resources/posts/%Y/%m/%d/')),
                ('is_approved', models.BooleanField(default=False)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('last_editor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_editor', to=settings.AUTH_USER_MODEL)),
                ('parent_post', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cloud.Post')),
            ],
        ),
        migrations.CreateModel(
            name='PostType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, unique=True)),
                ('plural', models.CharField(default='', max_length=128)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('code', models.CharField(blank=True, max_length=64, null=True)),
                ('link', models.URLField(blank=True, max_length=512, null=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('chair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cloud.Chair')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('short_title', models.CharField(blank=True, max_length=16, null=True)),
                ('semester', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('lecturer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cloud.Lecturer')),
                ('programs', models.ManyToManyField(to='cloud.Program')),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('short_title', models.CharField(blank=True, max_length=64, null=True)),
                ('link', models.URLField(blank=True, max_length=512, null=True)),
                ('logo', models.ImageField(blank=True, default='resources/default/u_logo.png', null=True, upload_to='resources/u_logo/')),
                ('is_approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, default='resources/default/user_ava.png', null=True, upload_to='resources/user_avatars/')),
                ('karma', models.SmallIntegerField(default=10)),
                ('course', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('vk_id', models.CharField(default=None, max_length=16, null=True)),
                ('program', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cloud.Program')),
            ],
        ),
        migrations.CreateModel(
            name='UserStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('status_level', models.PositiveSmallIntegerField(default=0)),
                ('can_publish_without_moderation', models.BooleanField(default=False)),
                ('can_moderate', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='userinfo',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cloud.UserStatus'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cloud.Subject'),
        ),
        migrations.AddField(
            model_name='post',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cloud.PostType'),
        ),
        migrations.AddField(
            model_name='memesource',
            name='program',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cloud.Program'),
        ),
        migrations.AddField(
            model_name='memesource',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cloud.Subject'),
        ),
        migrations.AddField(
            model_name='memesource',
            name='university',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cloud.University'),
        ),
        migrations.AddField(
            model_name='department',
            name='university',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cloud.University'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='cloud.Post'),
        ),
        migrations.AddField(
            model_name='chair',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cloud.Department'),
        ),
    ]
