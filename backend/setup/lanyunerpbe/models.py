from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Person(models.Model):
    authUser = models.ForeignKey(User, on_delete=models.CASCADE)
    sn = models.CharField(max_length=128)  # serial number
    sArYear = models.IntegerField(default=1911)  # school arrival year
    canBorrow = models.BooleanField(default=False)
    canListProperties = models.BooleanField(default=False)
    canActivateUser = models.BooleanField(default=False)

    def __str__(self):
        return '{}:{} {}:#{}'.format(
            self.sArYear,
            self.authUser.last_name,
            self.authUser.first_name,
            self.sn
        )

    def name(self):
        user = self.authUser
        return '{} {}'.format(user.last_name, user.first_name)


class ManageGroup(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class InstrGroup(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Property(models.Model):
    name = models.CharField(max_length=256)
    serialNum = models.CharField(max_length=2048, unique=True)
    mgroup = models.ForeignKey(ManageGroup, on_delete=models.PROTECT)
    igroup = models.ForeignKey(InstrGroup, on_delete=models.PROTECT)
    borrowedBy = models.ForeignKey(
        Person, null=True, on_delete=models.PROTECT, blank=True)
    activated = models.BooleanField(default=True)
    def json(self): 
        res = {
            'name': self.name,
            'mgroup': self.mgroup.__str__(),
            'igroup': self.igroup.__str__(),
            'mgroup_id': self.mgroup.id,
            'igroup_id': self.igroup.id,
            'serialNum': self.serialNum,
            'activated': self.activated
        }
        if self.borrowedBy is not None:
            res['borrowedBy'] = self.borrowedBy.name()
            res['borrowedBy_id'] = self.borrowedBy.id
        return res
    
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
