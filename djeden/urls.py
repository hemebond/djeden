from django.conf.urls import patterns, include, url
from django.conf import settings
from .views.generic import Root

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'djeden.views.home', name='home'),
	# url(r'^djeden/', include('djeden.foo.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),

	url(r'^$', Root.as_view(), name='root'),
	url(r'^projects/', include('projects.urls')),

	url(r'^organisations/', include('organisations.urls')),

	url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
	url(r'^logout/$', 'django.contrib.auth.views.logout', name="logout"),
)


if settings.DEBUG:
	urlpatterns += patterns('django.views.static',
		(r'^uploads/(?P<path>.*)$', 'serve', {'document_root': settings.MEDIA_ROOT}),
	)
	from django.contrib.staticfiles.urls import staticfiles_urlpatterns
	urlpatterns += staticfiles_urlpatterns()


urlpatterns += patterns('django.contrib.flatpages.views',
	url(r'^contact/$', 'flatpage', {'url': '/contact/'}, name='contact'),
	url(r'^about/$', 'flatpage', {'url': '/about/'}, name='about'),
)
