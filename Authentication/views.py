from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render
from rest_framework import status, authentication, permissions
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import HttpResponse

from Authentication.models import RegisterPersonnel
from Authentication.serializers import CustomerSerializer


# Create your views here.
class CustomerRegisterView(APIView):
    def post(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        id_number = request.data.get('id_number')
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        email = request.data.get('email')
        username = email

        if first_name is None or last_name is None or \
                id_number is None or phone_number is None or email is None or password is None:
            return Response({'error': 'Please fill in all fields'}, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(username=username)
        customers = RegisterPersonnel.objects.filter(Q(phone_number=phone_number) | Q(id_number=id_number))
        if len(users) > 0 or len(customers) > 0:
            return Response({
                "customer": None,
                "message": "User Account already exists. Provide unique e-mail, id and phone number"
            },
                status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                        email=email, password=password)
        customer = RegisterPersonnel.objects.create(
            user=user,
            phone_number=phone_number,
            id_number=id_number,
        )
        customer_serializer = CustomerSerializer(customer)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "customer": customer_serializer.data,
            "token": token.key,
            "message": "User Created"
        },
            status=status.HTTP_200_OK
        )


class LoginApiView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({'error': 'Please fill in both fields'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=username)
            current_password = user.password
            match_check = check_password(password, current_password)
            if not match_check:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            token, created = Token.objects.get_or_create(user=user)
            customers = RegisterPersonnel.objects.get(user__id=user.id)
            customer_serializer = CustomerSerializer(customers)

            return Response({
                "token": token.key,
                "personnel": customer_serializer.data,
                "message": "log in successfully",
                "status": 200
            },
                status=status.HTTP_200_OK
            )
        except ObjectDoesNotExist:
            return Response({
                "personnel": None,
                "message": "Invalid credentials",
                "status": 400
            },
                status=status.HTTP_404_NOT_FOUND
            )


class PersonnelQueryView(APIView):
    def post(self, request):
        return Response({
            "message": "OK"
        },
            status=status.HTTP_200_OK
        )

    def get(self, request):

        phone_number = request.GET.get("phone_number")
        if phone_number:
            try:
                customer = RegisterPersonnel.objects.get(phone_number=phone_number)
                customer_serializer = CustomerSerializer(customer)
                return Response(customer_serializer.data,
                                status=status.HTTP_200_OK
                                )
            except ObjectDoesNotExist:
                return Response({
                    "data": None,
                    "message": "Personnel not registered"
                },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response({
                "data": None,
                "message": "Provide personnel identification"
            },
                status=status.HTTP_400_BAD_REQUEST
            )


class GetAllCustomerAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        pass

    def get(self, request):
        customer = RegisterPersonnel.objects.all()
        customer_serializer = CustomerSerializer(customer, many=True)
        res = {"result": customer_serializer.data, "status": status.HTTP_200_OK}
        return Response(res)
