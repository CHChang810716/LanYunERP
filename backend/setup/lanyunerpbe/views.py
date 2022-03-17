from django.shortcuts import render
from django.http import HttpResponse
from .models import Person
from django.contrib.auth.models import User
import simplejson as json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login

# Create your views here.


def homePageView(request):
    return HttpResponse("Hello, World!")

def collectReqFields(requestD, requiredFields):
    reqData = {}
    for field in requiredFields:
        val = requestD.get(field, None)
        if val is None:
            raise RuntimeError(field)
        reqData[field] = val
    return reqData

def createPersonImpl(request):
    if request.method != 'POST':
        return {'code': 1, 'msg': 'this API only accept POST'}
    userRequiredFields = [
        'username',
        'password',
        'email',
        'first_name',
        'last_name'
    ]
    try:
        userReqData = collectReqFields(request.POST, userRequiredFields)
    except RuntimeError as field:
        return {'code': 1, 'msg': 'missing required field: {}'.format(field)}
    u, created = User.objects.get_or_create(**userReqData)
    if not created:
        return {'code': 1, 'msg': 'user already exist'}

    u.set_password(userReqData['password'])
    u.save()
    personReqiredFields = [
        'sn',
        'sArYear'
    ]
    try:
        personReqData = collectReqFields(request.POST, personReqiredFields)
    except RuntimeError as field:
        return {'code': 1, 'msg': 'missing required field: {}'.format(field)}

    p, created = Person.objects.get_or_create(
        authUser=u,
        sn=personReqData['sn'],
        sArYear=personReqData['sArYear']
    )
    if not created:
        return {'code': 1, 'msg': 'user already exist'}
    return {'code': 0, 'msg': 'done'}

def createPerson(request):
    return JsonResponse(createPersonImpl(request))

def personLoginImpl(request):
    if request.method != 'POST':
        return {'code': 1, 'msg': 'this API only accept POST'}
    requiredFields = [
        'username',
        'password'
    ]
    try:
        reqData = collectReqFields(request.POST, requiredFields)
    except RuntimeError as field:
        return {'code': 1, 'msg': 'missing required field: {}'.format(field)}

    user = authenticate(request, **reqData)
    if user is None:
        return {'code': 1, 'msg': 'auth failed'}
    login(request, user)
    return {'code': 0, 'msg': 'done'}

def personLogin(request):
    return JsonResponse(personLoginImpl(request))

def personInfoImpl(request):
    if not request.user.is_authenticated:
        return {'code': 1, 'msg': 'user not authenticated'}
    user = request.user
    person = Person.objects.get(authUser = user)
    return {'code': 0, 'data': {
        'sn': person.sn,
        'sArYear': person.sArYear,
        'email': person.user.email,
        'first_name': person.user.first_name,
        'last_name': person.user.last_name,
        'username': person.user.username
    }, 'msg': 'done'}

def personInfo(request):
    return JsonResponse(personInfoImpl(request))