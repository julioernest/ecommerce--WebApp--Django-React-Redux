from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.models import User

# try and make the registration with email authentification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string 
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse
from base.utils import Util
#End of trying the email registration

from base.serializers import ProductSerializer, UserSerializer, UserSerializerWithToken

# Create your views here.
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password
from rest_framework import status, generics
#function based views vs classes TO DO WITH CLASSES

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
def registerUser(request):
    data = request.data 
    try:
        user = User.objects.create(
            first_name = data['name'],
            username = data['email'],
            email=data['email'],
            password=make_password(data['password']),
            is_active = False
        )    
        serializer = UserSerializerWithToken(user, many=False)
        current_site = get_current_site(request).domain
        # relativeLink = reverse('email-verify')
        # token = serializer.data['token']
        # print (token)
        # absurl = 'http://' + current_site + relativeLink +'?token=' + token
        # email_subject = 'Activate your account'
       
        # email_body = 'Hi' + user.first_name + 'Use the link bellow to activate your account \n' + absurl
        # data_email = {'email-body': email_body,'to_email': user.email, 'email-subject': email_subject}
        # Util.send_email(data_email)

        return Response(serializer.data)
    except:
        message = {'detail':'User with this email already exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(generics.GenericAPIView):
    def get(self):
        pass

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializers = UserSerializerWithToken(user, many=False)

    data = request.data

    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']

    if data['password'] != '':
        user.password = make_password(data['password'])
    
    user.save()
    
    return Response(serializers.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializers = UserSerializer(user, many=False)
    
    return Response(serializers.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializers = UserSerializer(users, many=True)

    return Response(serializers.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsersById(request, pk):
    user = User.objects.get(id=pk)
    serializers = UserSerializer(user, many=False)

    return Response(serializers.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request, pk):
    user = User.objects.get( id = pk)
    data = request.data

    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    user.is_staff = data['isAdmin']

    user.save()
    serializers = UserSerializer(user, many=False)

    return Response(serializers.data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    userForDeletion =  User.objects.get( id = pk)
    userForDeletion.delete()

    return Response('User was deleted')