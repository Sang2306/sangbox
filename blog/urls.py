from django.urls import path, include

app_name = 'blog'

urlpatterns = [
    path('dashboard/', include(('blog.dashboard_urls', app_name), namespace='dashboard')),
]
