from django.db import models

from django.contrib.auth.models import User

from MainController.models import BaseModel


# Create your models here.
# register user
class RegisterPersonnel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    phone_number = models.CharField(max_length=256, unique=True)
    id_number = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
