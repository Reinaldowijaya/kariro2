from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic import DetailView, ListView, TemplateView
from kariro_main.models import Job_Vacancy
from kariro_main import views
import settings
admin.autodiscover()
from django.conf.urls.static import static
from kariro_main.views import Jobs,Jobs_Detail

urlpatterns = patterns('',
    # Examples:

    # url(r'^kariro/', include('kariro.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
	#(r'^tinymce/', include(tinymce.urls)),

	url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    	url(r'^admin/', include(admin.site.urls)),

    	url(r'^dashboard/$',views.dashboard, name="user_dashboard"),

	#Job postings
	url(r'^jobs/$',Jobs.as_view(),name='jobs'),
	url(r'^jobs/(?P<pk>\d+)/$',Jobs_Detail.as_view(), name='jobs_detail'),
	url(r'^jobs/(?P<pk>\d+)/(?P<slug>[-\w]+)/$',Jobs_Detail.as_view(), name='jobs_detail'),

	#User login/signup
	(r'^accounts/', include('allauth.urls')),

	#First time login for userprofile editing
	url(r'^accounts/signup/profile/$', views.profile, name="signup_profile"),
	url(r'^accounts/profile/$', views.user_profile, name="userprofile"),

	#Company
	(r'^company/', include('company.urls')),
	('^activity/', include('actstream.urls')),
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
		'document_root': settings.MEDIA_ROOT}),
	url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
		'document_root': settings.STATIC_ROOT}),
)
