"""
    This module is expected to produce json data
"""

from django.contrib.auth.decorators import login_required
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from .views import search_post, get_content_quick_view, \
					list_all_articles, get_an_article, update_or_create_an_article, delete_the_article

urlpatterns = [
    path('search-post/', search_post, name='search-post'),
    path('get-content/', get_content_quick_view, name='get-content-quick-view'),
    path('list/', list_all_articles, name='list_all_articles'),
    path('article/<uuid:uuid>/', get_an_article, name='get_an_article'),
    path('update-or-create/article/', update_or_create_an_article, name='update-or-create-an-article'),
    path('delete/article/<uuid:uuid>/', delete_the_article, name='delete-the-article'),
]
