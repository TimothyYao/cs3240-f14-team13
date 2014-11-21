from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^search/$', 'bulletins.views.search'),
    url(r'^register/$', 'bulletins.views.register'),
    url(r'^(?P<bulletin_id>\d+)/$', 'bulletins.views.details'),
    url(r'', include('bulletins.urls')),
)
