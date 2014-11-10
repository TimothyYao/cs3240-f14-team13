from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^polls/$', 'polls.views.index'),
    (r'^polls/(?P<poll_id>\d+)/$', 'polls.views.details'),
    (r'^polls/(?P<poll_id>\d+)/results/$', 'polls.views.results'),
    (r'^polls/(?P<poll_id>\d+)/vote/$', 'polls.views.vote'),
    (r'^account/', include('account.urls')),
    (r'^home/', 'polls.views.home'),
    # Examples:
    # url(r'^$', 'tutorial.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

TEMPLATE_CONTEXT_PROCESSORS = [
    "account.context_processors.account",
]

MIDDLEWARE_CLASSES = [
    "account.middleware.LocaleMiddleware",
    "account.middleware.TimezoneMiddleware",
]