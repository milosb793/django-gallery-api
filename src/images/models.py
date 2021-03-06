import ipdb
from django.db import models

# Create your models here.
from django.urls import reverse

from src.gallery.helpers import prepare_path


def content_file_name(instance, filename):
    """
    Функција за припремање локације где ће се слика чувати;
    На media/img/ ће бити надодато име албума и име слике
    :param instance:
    :param filename:
    :return: str
    """

    name = prepare_path(instance.album.name)
    return '/'.join(['img', name, filename])


class Image(models.Model):
    name        = models.CharField(max_length=120, blank=False, null=True)
    album       = models.ForeignKey("albums.Album", related_name="album_id", null=True, blank=True)
    image       = models.ImageField(verbose_name="Image", blank=True, null=True, upload_to=content_file_name)
    description = models.TextField(max_length=500, null=True, blank=True)
    # comments    = models.ManyToManyField("comments.Comment", related_name="all_comments", blank=True, unique=False)
    # likes       = models.ManyToManyField("likes.Like", related_name="all_likes", blank=True, unique=False)
    # tags        = models.ManyToManyField("tags.Tag", related_name="all_tags", blank=True)
    is_public   = models.BooleanField(default=False)
    timestamp   = models.DateField(auto_now_add=True)
    updated     = models.DateField(auto_now=True)

    # стринг репрезентација објекта
    def __str__(self):
        return self.name

    # функција која враћа апсолутну путању до објекта
    def get_absolute_url(self): # get_absolute_url
        return reverse('images:detail', kwargs={'image_id': self.pk})
