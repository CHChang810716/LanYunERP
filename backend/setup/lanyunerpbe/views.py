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
def wrongMethod(method):
    return {'code': 1, 'msg': 'this API only accept {}'.format(method)}

def json_rep(impl):
    return lambda req: JsonResponse(impl(req))

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

@json_rep
def createPerson(request):
    if request.method != 'POST':
        return wrongMethod('POST')
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

@json_rep
def login(request):
    if request.method != 'POST':
        return wrongMethod('POST')
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

@json_rep
def logout(request):
    auth.logout(request)
    return doneMsg
    
@json_rep
def personInfo(request):
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


@json_rep
def propertyInfo(request):
    if not request.GET:
        return wrongMethod('GET')
    user = request.user
    if not user.is_authenticated:
        return authFailed
    person = Person.objects.get(authUser = user)
    if not person.canListProperties:
        return authFailed
    sn = request.GET.get('serialNum')
    p = Property.objects.get(serialNum = sn)
    return {
        'code': 0,
        'msg': 'done',
        'data': p.json()
    }

@json_rep
def propertyList(request):
    user = request.user
    if not user.is_authenticated:
        return authFailed
    person = Person.objects.get(authUser = user)
    if not person.canListProperties:
        return authFailed
    res = [ p.json() for p in Property.objects.all()]
    return {'code': 0, 'data': res, 'msg': 'done'}

@json_rep
def personList(request):
    user = request.user
    if not user.is_authenticated:
        return authFailed
    person = Person.objects.get(authUser = user)
    if not person.canActivateUser:
        return authFailed
    
    res = [{
        'name': p.name(),
        'sn': p.sn,
        'sArYear': p.sArYear,
        'canBorrow': p.canBorrow,
        'canListProperties': p.canListProperties,
        'canActivateUser/ser': p.canActivateUser
    } for p in Person.objects.all()]

    return {'code': 0, 'data': res, 'msg': 'done'}