from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Secure_Witness.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^home/$', 'Secure_Witness_App.views.home'),  #with arg
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}),  #points url to django's built in login view, instead of making a new form and such
    #(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/home'}),  #points url to django's built i
    #@login, to pass params to a view function, send a dict to the url function which contains all the params you want passed into the view function pointed to.  ?
    #So is this saying, if you get this url, call the polls.views.details method./
    #Next_page, sending param of next page to redirect when logout.  21:48
    url(r'^admin/', include(admin.site.urls)),
    url(r'^bulletin_form/$', 'Secure_Witness_App.views.bulletin_form'),
    url(r'^secureWitness/$', 'Secure_Witness_App.views.secureWitness'),
    url(r'^register_account/$', 'Secure_Witness_App.views.register_account'),
    (r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/secureWitness'}),

)


#admin might be superuser, password.  Or john, password.  Or something.