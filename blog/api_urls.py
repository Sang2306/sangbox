"""
    This module is expected to produce json data
"""

from django.contrib.auth.decorators import login_required
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from .views import search_post, get_content_quick_view

urlpatterns = [
    path('search-post/', login_required(search_post), name='search-post'),
    path('get-content/', login_required(get_content_quick_view), name='get-content-quick-view'),
]

urlpatterns = format_suffix_patterns(urlpatterns)