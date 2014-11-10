from django.conf.urls import patterns, include, url
from django.contrib import admin
from forum import views

urlpatterns = patterns('',
    url(r"^$", "forum.views.main"),
	url(r"^forum/(\d+)/$", "forum.views.forum"),
	url(r"^thread/(\d+)/$", "forum.views.thread"),
	url(r"^post/(new_thread|reply)/(\d+)/$", "forum.views.post"),
	#url(r"^reply/(\d+)/$", "forums.views.reply"),
	#url(r"^new_thread/(\d+)/$", "forums.views.new_thread"),
)