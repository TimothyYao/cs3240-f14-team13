from django.db import models

# Create your models here.

#https://youtrack.jetbrains.com/issue/PY-13434
#  http://forum.jetbrains.com/thread/PyCharm-2221  bug fix, run createsuperuer from django console
#  from django.contrib.auth.models import User
##    User.objects.create_superuser(username='maarten', password='TopSecret', email='A@A.nl')



"""  from django.contrib.auth.models import User
User.objects.create_superuser(username='john', password='john', email='jls9fc@virginia.edu')   """

#says  . . .

#  IntegrityError: column username is not unique


# TODO admin username is john2 and pw is password.  email jls9fc.
# todo Must find way to view / delete old attempted usernames: john, ass, test, admin, etc.



class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()