from django.conf.urls import url, include
from django.contrib import admin

from .views import ImageDetailAPIView, GetTopImages, GetOwnerImages, CreateGetImagesAPI

urlpatterns = [
    url(r'profile/(?P<profile_id>\d+)/?$', GetOwnerImages.as_view(), name='profile'),
    url(r'(?P<image_id>\d+)/comments/?', include("src.comments.api.urls", namespace='image-comments')),
    url(r'(?P<image_id>\d+)/likes/?', include("src.likes.api.urls", namespace='image-likes')),
    url(r'(?P<image_id>\d+)/tags/?', include("src.tags.api.urls", namespace='image-tags')),
    url(r'(?P<image_id>\d+)/?$', ImageDetailAPIView.as_view(), name='detail'),
    url(r'top/?$', GetTopImages.as_view(), name='top'),
    url(r'$', CreateGetImagesAPI.as_view(), name='images-list-create')
]


