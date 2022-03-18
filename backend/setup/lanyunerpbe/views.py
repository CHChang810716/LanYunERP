from django.shortcuts import render
from django.http import HttpResponse
from .models import Person,Property
from django.contrib.auth.models import User
import simplejson as json
from django.http import JsonResponse
from django.contrib import auth # authenticate, login
from typing import Final

# Create your views here.

authFailed: Final = {'code': 1, 'msg': 'user not authenticated'}
doneMsg: Final = {'code': 0, 'msg': 'done'}

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
    return doneMsg

def createPerson(request):
    return JsonResponse(createPersonImpl(request))

def loginImpl(request):
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

    user = auth.authenticate(request, **reqData)
    if user is None:
        return {'code': 1, 'msg': 'auth failed'}
    auth.login(request, user)
    return doneMsg

def login(request):
    return JsonResponse(loginImpl(request))

def logout(request):
    auth.logout(request)
    return JsonResponse(doneMsg)
    

def personInfoImpl(request):
    if not request.user.is_authenticated:
        return authFailed
    user = request.user
    person = Person.objects.get(authUser = user)
    authUser = person.authUser
    return {'code': 0, 'data': {
        'sn':           person.sn,
        'sArYear':      person.sArYear,
        'email':        authUser.email,
        'first_name':   authUser.first_name,
        'last_name':    authUser.last_name,
        'username':     authUser.username
    }, 'msg': 'done'}

def personInfo(request):
    return JsonResponse(personInfoImpl(request))

def propertyListImpl(request):
    user = request.user
    if not user.is_authenticated:
        return authFailed
    person = Person.objects.get(authUser = user)
    if not person.canListProperties:
        return authFailed
    res = [{
        'name': p.name,
        'mgroup': p.mgroup.__str__(),
        'igroup': p.igroup.__str__(),
        'mgroup_id': p.mgroup.id,
        'igroup_id': p.igroup.id,
        'borrowedBy': '{} {}'.format(
            p.borrowedBy.authUser.last_name,
            p.borrowedBy.authUser.first_name
        ),
        'borrowedBy_id': p.borrowedBy.id,
        'activated': p.activated
    } for p in Property.objects.all()]
    return {'code': 0, 'data': res, 'msg': 'done'}

def propertyList(request):
    return JsonResponse(propertyListImpl(request))