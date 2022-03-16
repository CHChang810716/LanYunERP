from django.shortcuts import render
from django.http import HttpResponse
from .models import Person
from django.contrib.auth.models import User
# Create your views here.

def homePageView(request):
    return HttpResponse("Hello, World!")

def createPerson(request):
    userName = request.REQUEST.get('username', None)
    userPass = request.REQUEST.get('password', None)
    userMail = request.REQUEST.get('email', None)
    if userName and userPass and userMail:
        u,created = User.objects.get_or_create(
            username = userName, 
            email = userMail,
            password = userPass
        )
        if created:
            return {'code': 0}
        else:
            return {'code': 1, 'message': 'user already exist'}
    else:
        return {'code': 1, 'message': 'empty request'}
