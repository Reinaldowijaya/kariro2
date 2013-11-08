from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',

	url(r'^$',Company_List.as_view(), name='company_list'),
	url(r'^(?P<pk>\d+)/(?P<slug>[-\w]+)/$',Company_Detail, name='company_detail'),
	url(r'^(?P<pk>\d+)/$',Company_Detail, name='company_detail2'),

	url(r'^dashboard/$',Company_Dashboard,name='company_dashboard'),
	url(r'^dashboard/profile/$',Company_Profile,name='company_profile'),
	url(r'^dashboard/lowongan/$',Company_Job,name='company_job'),
	url(r'^dashboard/lowongan/new$',Post_Job,name='post_job'),
	url(r'^dashboard/lowongan/(?P<job_id>\d+)/$',Company_Job_Detail,name='company_job_detail'),
	url(r'^dashboard/lowongan/(?P<job_id>\d+)/edit$',Edit_Job,name='edit_job'),
	)
