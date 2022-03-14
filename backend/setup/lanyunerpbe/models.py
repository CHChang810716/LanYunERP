from django.db import models

# Create your models here.

class Object(models.Model):
  activated = models.BooleanField(default=True)

class Person(Object):
  sn = models.CharField(max_length=128) # serial number
  sArYear = models.IntegerField(default = 1911) # school arrival year
  
class ManageGroup(Object):
  name = models.CharField(max_length=128)

class InstrGroup(Object):
  name = models.CharField(max_length=128)

class Property(Object):
  name = models.CharField(max_length=256)
  serialNum = models.CharField(max_length=2048)
  mgroup = models.ForeignKey(ManageGroup, on_delete=models.PROTECT)
  igroup = models.ForeignKey(InstrGroup, on_delete=models.PROTECT)
  borrowedBy = models.ForeignKey(Person, null=True, on_delete=models.PROTECT)