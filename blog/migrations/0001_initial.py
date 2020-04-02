# Generated by Django 3.0.1 on 2019-12-20 03:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField(help_text='content')),
                ('publish_date', models.DateTimeField(auto_now_add=True, help_text='publish date of a content')),
                ('slug', models.SlugField(help_text='This is used for SEO purposes', max_length=255, unique=True)),
                ('owner', models.ForeignKey(help_text='owner of the article', on_delete=django.db.models.deletion.CASCADE, related_name='articles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'blog_articles',
                'ordering': ['publish_date'],
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='tags_name for SEO purpose', max_length=64)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='blog.Articles')),
            ],
            options={
                'db_table': 'blog_tags',
            },
        ),
        migrations.CreateModel(
            name='Medias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media', models.FileField(blank=True, null=True, upload_to='file/%Y/%m/%d/')),
                ('url_cdn', models.URLField(blank=True, max_length=512, null=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medias', to='blog.Articles')),
            ],
            options={
                'db_table': 'blog_medias',
            },
        ),
        migrations.CreateModel(
            name='APITokens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_key', models.CharField(help_text='APi key for retrieve data', max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('locked', models.BooleanField(default=False, help_text='indicate whether this api was locked or not')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='api', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'blog_api_tokens',
            },
        ),
    ]