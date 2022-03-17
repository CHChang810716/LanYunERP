from django.urls import path
from .views import homePageView, createPerson, personLogin

urlpatterns = [
    path("", homePageView),
    path("create_person", createPerson),
    path("person_login", personLogin)
]
