from django.contrib import admin
from Operations.models import *

# Register your models here.
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("album_title", "user_id",)
admin.site.register(Album, AlbumAdmin)

class PhotoAdmin(admin.ModelAdmin):
    list_display = ("album_image_thumbnail", "album_id",)
admin.site.register(Photos, PhotoAdmin)