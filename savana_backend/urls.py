from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic.base import RedirectView

from savana_backend import settings

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('admin:index'))),
    path('api/admin/', admin.site.urls),
    path('api/', include('Authentication.urls')),
    path('api/', include('Operations.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
