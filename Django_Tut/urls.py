from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Django_Tut.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #added  - - -
    (r'^polls/$', 'polls.views.index'),
    (r'^polls/(?P<poll_id>\d+)/$', 'polls.views.details'),
    (r'^polls/(?P<poll_id>\d+)/results/$', 'polls.views.results'),
    (r'^polls/(?P<poll_id>\d+)/vote/$', 'polls.views.vote'),
    (r'^home/$', 'myPages.views.home'),  #with arg
     (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}),  #points url to django's built in login view, instead of making a new form and such
     (r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/home'}),  #points url to django's built i
#@login, to pass params to a view function, send a dict to the url function which contains all the params you want passed into the view function pointed to.  ?
          #So is this saying, if you get this url, call the polls.views.details method./
    #Next_page, sending param of next page to redirect when logout.  21:48
    url(r'^admin/', include(admin.site.urls)),
    url(r'^bulletin_form/$', 'myPages.views.bulletin_form'),


#TODO might want to create a 'main' page.  with a login form and displays username if already logged in, else something



)

"""
These patterns refer to the views, which do not yet exist.
You can spend some effort to create the view methods
and associated templates manually, but it is much easier to use PyCharm's assistance: as you hover
your mouse pointer over an unresolved reference (which is, by the way, highlighted),
a yellow light bulb screenshots/yellowLightBulb.png?version=1&modificationDate=1403265658000 appears,
 which means that a quick fix is suggested. To show this quick fix, click the bulb,
  or, with the caret at the view name, just press Alt+Enter:
"""