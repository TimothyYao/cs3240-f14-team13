from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'bulletins.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^register/$', 'bulletins.views.register'),
    url(r'^search/$', 'bulletins.views.search'),
    url(r'^bulletin/(?P<bulletin_id>\d+)/$', 'bulletins.views.details'),
    url(r'^bulletin/(?P<bulletin_id>\d+)/edit/$', 'bulletins.views.edit_bulletin'),
    url(r'^myBulletins/$', 'bulletins.views.my_bulletins'),
    url(r'^folder/(?P<folder_id>\d+)/$', 'bulletins.views.folder'),
    url(r'^folder/(?P<folder_id>\d+)/submit/$', 'bulletins.views.submit'),
    url(r'^folder/(?P<folder_id>\d+)/createFolder/$', 'bulletins.views.create_folder'),
    url(r'submit/$', 'bulletins.views.submit'),
)
