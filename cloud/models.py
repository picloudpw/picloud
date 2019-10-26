from django.db import models
from django.utils import timezone
import os

import bleach
import markdown


class HierarchyLevel(models.Model):
    name = models.CharField(max_length=32, null=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class Hierarchy(models.Model):
    level = models.ForeignKey(HierarchyLevel, null=True, blank=True, on_delete=models.SET_NULL)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=256, null=False, blank=True)
    short_name = models.CharField(max_length=64, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    logo = models.ImageField(
        upload_to="resources/logo/",
        default="resources/default/department.png",
        null=True,
        blank=True,
    )
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.level.name if self.level else ''} - {self.name}"

    def as_dict(self):
        return {
            "level": None if self.level is None else self.level.name,
            "parent_id": None if self.parent is None else self.parent.pk,
            "name": self.name,
            "short_name": self.short_name,
            "link": self.link,
            "logo": self.logo.url,
            "is_approved": self.is_approved,
        }


def migrate():
    university_l, created = HierarchyLevel.objects.get_or_create(name='university')
    department_l, created = HierarchyLevel.objects.get_or_create(name='faculty')
    chair_l, created = HierarchyLevel.objects.get_or_create(name='chair')
    program_l, created = HierarchyLevel.objects.get_or_create(name='program')
    for u in University.objects.all():
        university_obj, _ = Hierarchy.objects.get_or_create(
            level=university_l,
            parent=None,
            name=u.title,
            short_name=u.short_title,
            link=u.link,
            logo=u.logo,
            is_approved=u.is_approved
        )
        for d in Department.objects.filter(university=u):
            department_obj, _ = Hierarchy.objects.get_or_create(
                level=department_l,
                parent=university_obj,
                name=d.title,
                short_name=d.short_title,
                link=d.link,
                logo=None,
                is_approved=d.is_approved
            )
            for lec in Lecturer.objects.filter(department=d):
                lec.hierarchy = department_obj
                lec.save()
            for c in Chair.objects.filter(department=d):
                chair_obj, _ = Hierarchy.objects.get_or_create(
                    level=chair_l,
                    parent=department_obj,
                    name=c.title,
                    short_name=c.short_title,
                    link=c.link,
                    logo=None,
                    is_approved=c.is_approved
                )
                for p in Program.objects.filter(chair=c):
                    program_obj, _ = Hierarchy.objects.get_or_create(
                        level=program_l,
                        parent=chair_obj,
                        name=p.title,
                        short_name=p.code,
                        link=p.link,
                        logo=None,
                        is_approved=p.is_approved
                    )
                    for s in Subject.objects.filter(programs__in=[p]):
                        s.hierarchy.add(program_obj)
                        s.save()
                    for usr in UserInfo.objects.filter(program=p):
                        usr.hierarchy = program_obj
                        usr.save()


class University(models.Model):
    title = models.CharField(max_length=256, null=False)
    short_title = models.CharField(max_length=64, null=True, blank=True)
    link = models.URLField(max_length=512, null=True, blank=True)
    logo = models.ImageField(upload_to='resources/u_logo/',
                             default='resources/default/u_logo.png',
                             null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def as_dict(self):
        return {
            "id": self.pk,
            "title": self.title,
            "short_title": self.short_title
        }

    def as_hierarchical_dict(self):
        return {
            "id": self.pk,
            "title": self.title,
            "short_title": self.short_title,
            "departments": {
                d.id: d.as_hierarchical_dict()
                for d in Department.objects.filter(university=self.pk, is_approved=True)
            }
        }


class Department(models.Model):
    university = models.ForeignKey('University', on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False)
    short_title = models.CharField(max_length=64, null=True, blank=True)
    link = models.URLField(max_length=512, null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def as_dict(self):
        return {
            "id": self.pk,
            "title": self.title,
            "short_title": self.short_title
        }

    def as_hierarchical_dict(self):
        return {
            "id": self.pk,
            "title": self.title,
            "short_title": self.short_title,
            "chairs": {
                c.id: c.as_hierarchical_dict()
                for c in Chair.objects.filter(department=self.pk, is_approved=True)
            }
        }


class Chair(models.Model):
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False)
    short_title = models.CharField(max_length=64, null=True, blank=True)
    link = models.URLField(max_length=512, null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.short_title

    def as_dict(self):
        return {
            "id": self.pk,
            "title": self.title,
            "short_title": self.short_title
        }

    def as_hierarchical_dict(self):
        return {
            "id": self.pk,
            "title": self.title,
            "short_title": self.short_title,
            "programs": {
                p.id: p.as_hierarchical_dict()
                for p in Program.objects.filter(chair=self.pk, is_approved=True)
            }
        }


class Program(models.Model):
    chair = models.ForeignKey('Chair', on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False)
    code = models.CharField(max_length=64, null=True, blank=True)
    link = models.URLField(max_length=512, null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title + " (" + str(self.chair) + ")"

    def as_dict(self):
        return {
            "id": self.pk,
            "title": self.title,
            "code": self.code
        }

    def as_hierarchical_dict(self):
        return {
            "id": self.pk,
            "title": self.title,
            "code": self.code,
            "subjects": {
                s.id: s.as_hierarchical_dict()
                for s in Subject.objects.filter(programs=self.pk, is_approved=True)
            }
        }


class Lecturer(models.Model):
    department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True, blank=True)
    hierarchy = models.ForeignKey(Hierarchy, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=64, null=False)
    surname = models.CharField(max_length=64, null=False)
    patronymic = models.CharField(max_length=64, null=True, blank=True)
    complexity = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    image = models.ImageField(upload_to='resources/lec_avatars/',
                              default='resources/default/lec_avatar.png',
                              null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.surname + " " + self.name + " " + self.patronymic


class Subject(models.Model):
    programs = models.ManyToManyField("Program")
    hierarchy = models.ManyToManyField(Hierarchy)
    lecturer = models.ForeignKey('Lecturer', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=256, null=False)
    short_title = models.CharField(max_length=16, null=True, blank=True)
    semester = models.PositiveSmallIntegerField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.displayed_title()

    def displayed_title(self):
        if self.semester != 0:
            return self.title + " (" + str(self.semester) + " сем.)"
        else:
            return self.title

    def as_dict(self):
        return {
            "id": self.pk,
            "title": self.displayed_title(),
            "short_title": self.short_title,
            "semester": self.semester
        }

    def as_hierarchical_dict(self):
        return {
            "id": self.pk,
            "title": self.title,
            "short_title": self.short_title,
            "semester": self.semester,
        }


class UserStatus(models.Model):
    title = models.CharField(max_length=256, null=False)
    status_level = models.PositiveSmallIntegerField(default=0, null=False)
    can_publish_without_moderation = models.BooleanField(default=False, null=False)
    can_moderate = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    avatar = models.ImageField(upload_to='resources/user_avatars/',
                               default='resources/default/user_ava.png',
                               null=True, blank=True)
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    status = models.ForeignKey('UserStatus', on_delete=models.CASCADE)
    program = models.ForeignKey('Program', on_delete=models.CASCADE, null=True, blank=True)
    hierarchy = models.ForeignKey(Hierarchy, on_delete=models.SET_NULL, null=True, blank=True)
    karma = models.SmallIntegerField(default=10, null=False)
    course = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class MemeSource(models.Model):
    link = models.URLField(null=False, blank=True)
    author = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    hierarchy = models.ForeignKey(Hierarchy, on_delete=models.SET_NULL, null=True, blank=True)
    university = models.ForeignKey('University', on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    chair = models.ForeignKey('Chair', on_delete=models.SET_NULL, null=True, blank=True)
    program = models.ForeignKey('Program', on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.ForeignKey('Subject', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.link


class PostType(models.Model):
    class Meta:
        ordering = ['title']

    title = models.CharField(max_length=256, null=False, unique=True)
    plural = models.CharField(max_length=128, default="")

    def __str__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey('auth.User', null=True, on_delete=models.SET_NULL)
    parent_post = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    last_editor = models.ForeignKey('auth.User', related_name='last_editor', null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=256, null=False)
    text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    type = models.ForeignKey('PostType', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='resources/posts/%Y/%m/%d/', null=True, blank=True)
    link = models.URLField(max_length=512, null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    file = models.FileField(upload_to='resources/posts/%Y/%m/%d/', null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    ALLOWED_HTML_TAGS = allowed_html_tags = bleach.ALLOWED_TAGS + [
        u'h1',
        u'h2',
        u'h3',
        u'h4',
        u'p',
        u'a',
        u'li',
        u'ul',
        u'ol',
        u'pre',
        u'code',
        u'hr',
        u'br',
        u'strong',
    ]

    def html(self):
        dangerous_html = markdown.markdown(self.text, extensions=['markdown.extensions.fenced_code'])
        safe_html = bleach.clean(dangerous_html, tags=self.ALLOWED_HTML_TAGS)
        html_with_hyperlinks = bleach.linkify(safe_html)
        return html_with_hyperlinks

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return ""

    def get_image_width(self):
        if not self.image:
            return None
        try:
            return self.image.width
        except IOError or FileNotFoundError:
            return None

    def get_image_height(self):
        if not self.image:
            return None
        try:
            return self.image.height
        except IOError or FileNotFoundError:
            return None

    def get_file_url(self):
        if self.file and hasattr(self.file, 'url'):
            return self.file.url
        else:
            return ""

    def as_dict(self):
        return {
            "id": self.pk,
            "author_username": self.author.username,
            "author_id": self.author.pk,
            "title": self.title,
            "text": self.text,
            "created_date": self.created_date,
            "subject_id": self.subject.pk,
            "subject_short_title": self.subject.short_title,
            "type_title": self.type.title,
            "link": self.link,
            "views": self.views,
            "image": self.get_image_url(),
            "file": self.get_file_url(),
        }

    def can_be_edited_by(self, user):
        return self.author == user or \
               user.userinfo.status.can_moderate or \
               user.is_staff() or \
               user.is_superuser()

    def is_parent(self):
        return self.post_set.count() > 0

    def get_childs(self):
        return self.post_set

    def file_extension(self):
        if self.file:
            return os.path.splitext(self.file.name)[1][1:].upper()
        else:
            return None

    def get_comment_count(self):
        return Comment.objects.filter(post=self).count()

    def created_date_human(self):
        import datetime
        import pytz
        import locale
        try:
            locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')
        except Exception as e:
            # for mac os
            locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
        timezone = pytz.timezone('Europe/Moscow')
        date = self.created_date.astimezone(timezone)
        today = datetime.date.today()
        if datetime.datetime.now(tz=timezone) - date < datetime.timedelta(minutes=1):
            return "Только что"
        if date.date() == today:
            return date.strftime("сегодня %H:%M")
        if date.date() == today - datetime.timedelta(days=1):
            return date.strftime("вчера %H:%M")
        if today - date.date() < datetime.timedelta(days=5):
            return date.strftime("%A ").lower() + date.strftime("%H:%M")
        if date.year == today.year:
            return date.strftime("%d %b %H:%M")
        return date.strftime("%d %b %Y %H:%M")


class Comment(models.Model):
    author = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=False, blank=True)
    text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "(" + self.pk + ") " + self.post.title + " - " + self.author.username

    def get_author_avatar_url(self):
        user_info = UserInfo.objects.get(user=self.author)
        return user_info.avatar.url

    def as_dict(self):
        return {
            "pk": self.pk,
            "post_id": self.post.pk,
            "author_id": self.author.pk,
            "author_username": self.author.username,
            "author_avatar": self.get_author_avatar_url(),
            "text": self.text,
            "created_date": self.created_date,
        }
