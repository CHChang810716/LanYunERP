from django.contrib import admin
from .models import Person, Property, ManageGroup, InstrGroup

# Register your models here.

admin.site.register(Person)
admin.site.register(Property)
admin.site.register(ManageGroup)
admin.site.register(InstrGroup)