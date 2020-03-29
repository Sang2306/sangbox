from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from . import api_urls
from .views import ListArticles, CreateArticle, delete_article, edit_article

urlpatterns = [
    # blog/dashboard/
    path('', login_required(ListArticles.as_view()), name='list-articles'),
    path('add-article/', login_required(cache_page(60*60*24)(CreateArticle.as_view())), name='add-article'),
    path('delete-article/<uuid:id>/', login_required(delete_article), name='delete-article'),
    path('edit-article/<slug:title>/', login_required(edit_article), name='edit-article'),
    path('api/', TemplateView.as_view(template_name='blog/api.html'), name='api'),
] + api_urls.urlpatterns