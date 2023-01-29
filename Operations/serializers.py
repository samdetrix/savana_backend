from rest_framework import serializers
from rest_framework.authtoken.admin import User

from Authentication.models import RegisterPersonnel
from Authentication.serializers import CustomerSerializer
from Operations.models import Album, Photos


class AlbumSerializer(serializers.ModelSerializer):
    user = CustomerSerializer()

    class Meta:
        model = Album
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = '__all__'
