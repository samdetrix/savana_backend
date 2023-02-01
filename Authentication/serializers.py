from rest_framework import serializers
from rest_framework.authtoken.admin import User

from Authentication.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    total_product_inventory = serializers.ReadOnlyField()

    class Meta:
        model = RegisterPersonnel
        fields = '__all__'
