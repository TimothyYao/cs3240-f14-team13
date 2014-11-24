from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'bulletins.views.index'),
    url(r'submit/$', 'bulletins.views.submit'),
)