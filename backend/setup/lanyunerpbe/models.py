from django.db import models

# Create your models here.

class Object(models.Model):
  activated = models.BooleanField(default=True)

class Person(Object):
  sn = models.CharField(max_length=128) # serial number
  sArYear = models.IntegerField(default = 1911) # school arrival year
  name = models.CharField(max_length=64, default='xxx')
  def __str__(self):
    return '{}:{}:#{}'.format(self.sArYear, self.name, self.sn)
  
class ManageGroup(Object):
  name = models.CharField(max_length=128)
  def __str__(self):
    return self.name

class InstrGroup(Object):
  name = models.CharField(max_length=128)
  def __str__(self):
    return self.name

class Property(Object):
  name = models.CharField(max_length=256)
  serialNum = models.CharField(max_length=2048)
  mgroup = models.ForeignKey(ManageGroup, on_delete=models.PROTECT)
  igroup = models.ForeignKey(InstrGroup, on_delete=models.PROTECT)
  borrowedBy = models.ForeignKey(Person, null=True, on_delete=models.PROTECT, blank=True)
  def __str__(self):
    pref = '#{}:{}:{}:{}'.format(
      self.serialNum, 
      self.name, 
      self.mgroup,
      self.igroup
    )
    if self.borrowedBy is not None:
      return pref + ' borrowed by ' + self.borrowedBy.name
    return pref