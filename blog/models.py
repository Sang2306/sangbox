import uuid

from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db import models

from .utils import utils


class Articles(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=512, help_text='title of a post', null=False, blank=True)
    content = models.TextField(help_text='content for editor mode')
    html = models.TextField(help_text='content for quick view', null=True)
    publish_date = models.DateTimeField(auto_now_add=True, help_text='publish date of a content')
    slug = models.SlugField(max_length=255, unique=True, help_text='This is used for SEO purposes')
    is_shareable = models.BooleanField(default=False, help_text='mark if the article was able to share')
    owner = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='articles', help_text='owner of the article'
    )

    class Meta:
        ordering = ['publish_date']
        db_table = 'blog_articles'

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        """slugify the title"""
        self.slug = slugify(self.title, allow_unicode=False)
        super().save(*args, **kwargs)


class Tags(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, help_text='tags_name for SEO purpose')
    article = models.ForeignKey(to=Articles, on_delete=models.CASCADE, related_name='tags')

    class Meta:
        db_table = 'blog_tags'

    def __str__(self):
        return self.name


class Medias(models.Model):
    media = models.FileField(upload_to='file/%Y/%m/%d/', null=True, blank=True)
    url_cdn = models.URLField(max_length=512, null=True, blank=True)
    article = models.ForeignKey(to=Articles, on_delete=models.CASCADE, related_name='medias')

    class Meta:
        db_table = 'blog_medias'

    def __str__(self):
        return str(self.id)


class APITokens(models.Model):
    api_key = models.CharField(max_length=255, help_text='APi key for retrieve data')
    created_date = models.DateTimeField(auto_now_add=True)
    locked = models.BooleanField(default=False, help_text='indicate whether this api was locked or not')
    owner = models.OneToOneField(to=User, on_delete=models.DO_NOTHING, related_name='api')

    class Meta:
        db_table = 'blog_api_tokens'

    def __str__(self):
        return self.owner.username + " - " + self.api_key

    def save(self, *args, **kwargs):
        """Create api key for instance before saving it to database"""
        self.api_key = utils.generate_api_key();
        super().save(*args, **kwargs)
