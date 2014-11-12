#!/usr/bin/env python
import os
import sys  #had to click and install package . . .

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Secure_Witness.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


# my superuser is john, password is password.
#If /admin does not let you login, you may need to create a super user via windows console commands, pycharm is bugged.

#To start a fresh project, you must recall to run ctrl+alt+r, SQL, and the name of folder with your views, models and admin.
#THen must run SQL, syncDB as well.  This is wher epycharm would try to create a superuser but break anyhow.  Need to access admin pages.


#  http://forum.jetbrains.com/thread/PyCharm-2221

"""

Same thing here, Windows, Pycharm 3.4.1, Python 3.4.2, Django 1.7.

Workaround to create superuser:
Using Django Shell in Pycharm (tools, Run Django console) and then:

from django.contrib.auth.models import User
User.objects.create_superuser(username='maarten', password='TopSecret', email='A@A.nl')

"""

"""
from django.contrib.auth.models import User
User.objects.create_superuser(username='john', password='password', email='jls9fc@virginia.edu')

"""
#TODO clean out old test useracocunts.  Also creates 'superuser' pw: 'password' with ctrl+alt+r and apparently the user is in the database as a staff memeber, but can't be logged into from admin page.  wat?

#todo Current admin created via the django consol commands above is 'john' pw: 'password'.