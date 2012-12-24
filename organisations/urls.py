from django.conf.urls import patterns, url
from organisations import views


urlpatterns = patterns('organisations.views',
	url(
		r'^(?:(?P<url_method>create)/)?$',
		views.OrganisationList.as_view(),
		name="organisation-list"
	),
	url(
		r'^(?P<pk>\d+)/(?:(?P<url_method>read|update|delete)/)?$',
		views.OrganisationDetail.as_view(),
		name="organisation-detail"
	),
	url(
		r'^types/(?:(?P<url_method>create)/)?$',
		views.OrganisationTypeList.as_view(),
		name="organisation-type-list"
	),
	url(
		r'^types/(?P<pk>\d+)/$',
		views.OrganisationTypeDetail.as_view(),
		name="organisation-type-detail"
	),
)
