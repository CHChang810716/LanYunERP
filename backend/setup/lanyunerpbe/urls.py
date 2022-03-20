from django.urls import path
from . import views

urlpatterns = [
    path("", views.homePageView),
    path("create_person", views.createPerson),
    path("login", views.login),
    path("logout", views.logout),
    path("person_info", views.personInfo),
    path("person_list", views.personList),
    path("property_list", views.propertyList),
    path("property_info", views.propertyInfo),
]
