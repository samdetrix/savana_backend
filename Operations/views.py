from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import authentication, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from Authentication.models import RegisterPersonnel
from Operations.models import Album, Photos
from Operations.serializers import AlbumSerializer, PhotoSerializer


# Create your views here.

class AlbumAPIView(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def Post(self, request):
        request_data = request.get
        album_title = request_data.get('album_title')
        user_id = request_data.get('user')
        user = None
        try:
            user = RegisterPersonnel.objects.get(id=user_id)
        except ObjectDoesNotExist:
            res = {
                "message": "The selected user does not exist",
                "status": status.HTTP_400_BAD_REQUEST
            }
        albumObj = Album.objects.get_or_create(
            album_title=album_title,
            user=user
        )
        if albumObj:

            res = {
                "message": "Album posted successfully",
                "status": status.HTTP_200_OK
            }
            return Response(res)
        else:
            res = {
                "message": "Failed to post album",
                "status": status.HTTP_400_BAD_REQUEST
            }
        return Response(res)

    def get(self, request):
        id = request.GET.get('id')
        if id:
            albums = Album.objects.get(id=id)
            album_serializer = AlbumSerializer(albums)
            res = {
                "message": "Success",
                "results": album_serializer.data,
                "status": status.HTTP_200_OK
            }
        else:
            albums = Album.objects.all()
            album_serializer = AlbumSerializer(albums, many=True)
            res = {
                "message": "Success",
                "results": album_serializer.data,
                "status": status.HTTP_200_OK
            }
        return Response(res)


class PhotosAPIVIew(APIView):
    def post(self, request):
        request_data = request.data
        album_image_thumbnail = request.FILES.get('album_image_thumbnail')
        album_id = request_data.get('album')

        try:
            album = Album.objects.get(id=album_id)
        except ObjectDoesNotExist:
            res = {
                "message": "The selected album does not exist",
                "status": status.HTTP_400_BAD_REQUEST
            }

        photoObj = Photos.objects.create(
            album_image_thumbnail=album_image_thumbnail,
            album=album,
        )
        photo_serializers = PhotoSerializer(photoObj)
        if photoObj:
            res = {
                "message": "Photo successfully uploaded",
                "status": status.HTTP_200_OK,
                "results": photo_serializers.data
            }
            return Response(res)
        else:
            res = {
                "message": "Failed to upload photo",
                "status": status.HTTP_400_BAD_REQUEST,

            }
            return Response(res)

    def get(self, request):
        id = request.GET.get('id')
        if id:
            photos = Photos.objects.get(id=id)
            photo_serializer = PhotoSerializer(photos)
            res = {
                "data": photo_serializer.data,
                "message": "Success",
                "status": 200

            }
        else:
            photos = Photos.objects.all().order_by('-created_at')
            photo_serializer = PhotoSerializer(photos, many=True)
            res ={
                "data" : photo_serializer.data,
                "message": "Success",
                "status": 200
            }
        return Response(res)
