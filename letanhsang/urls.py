from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='accounts/login/')),
    path('admin/', admin.site.urls),
    path('accounts/', include('account.urls', namespace='account')),
    path('blog/', include('blog.urls', namespace='blog')),
]

media = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += media
