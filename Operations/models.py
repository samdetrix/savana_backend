from django.db import models
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from rest_framework.authtoken.admin import User

from Authentication.models import RegisterPersonnel
from MainController.models import BaseModel


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


# Create your models here.
class Album(BaseModel):
    album_title = models.TextField()
    user_id = models.ForeignKey(RegisterPersonnel, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.album_title



class Photos(BaseModel):
    album_image_thumbnail = models.ImageField(upload_to=upload_to, null=True)
    album_id = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True)
   