from django.urls import path
from .views import homePageView, createPerson, login, logout, personInfo, propertyList

urlpatterns = [
    path("", homePageView),
    path("create_person", createPerson),
    path("login", login),
    path("logout", logout),
    path("person_info", personInfo),
    path("property_list", propertyList)
]
