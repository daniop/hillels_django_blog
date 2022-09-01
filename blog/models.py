from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from pytils import translit

from .tasks import comment_active, new_post


class Author(AbstractUser):
    profile_photo = models.ImageField(blank=True, verbose_name='Фото профиля', upload_to='profiles_photo/')
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    description = models.TextField(max_length=200, verbose_name='Описание', blank=True)

    def __str__(self):
        return self.username


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    status_choices = (
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
    )
    title = models.CharField(max_length=250, unique=True, verbose_name='Заголовок')
    post_image = models.ImageField(blank=True, verbose_name='Фото поста', upload_to='posts_photo/')
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author', verbose_name='Автор')
    short_description = models.CharField(max_length=500, verbose_name='Краткое описание')
    body = models.TextField(verbose_name='Текст')
    publish = models.DateTimeField(auto_now=True, verbose_name='Дата публикации')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')
    status = models.CharField(max_length=10,
                              choices=status_choices,
                              default='draft',
                              verbose_name='Статут публикации')
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = translit.translify(self.title)
        super(Post, self).save(*args, **kwargs)
        link = self.get_absolute_url()
        if self.status == 'published':
            message = f'Новый пост. Название: {self.title} автора {self.author}. ' \
                      f'Ссылка на пост: {settings.SCHEMA}://{settings.DOMAIN}{link}'
            new_post.delay("New post", message)


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80, verbose_name='Ваше имя')
    email = models.EmailField(max_length=250, verbose_name='E-mail')
    body = models.TextField(verbose_name='Сообщение')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

    def save(self, *args, **kwargs):
        super(Comment, self).save(*args, **kwargs)
        link = self.post.get_absolute_url()
        if self.active:
            message = f'У вас новый комментарий к посту {self.post.title} от {self.name}' \
                      f'Ссылка на пост: {settings.SCHEMA}://{settings.DOMAIN}{link}'
            comment_active.delay("New comment", self.post.author.email, message)
