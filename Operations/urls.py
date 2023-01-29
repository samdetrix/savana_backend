from django.urls import path, include

from Operations.views import *

urlpatterns = [
    path('albums/', AlbumAPIView.as_view(), name='albums'),
    path('photos/', PhotosAPIVIew.as_view(), name='photos'),
]