from rest_framework import serializers
from rest_framework.authtoken.admin import User

from Authentication.models import *


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)



