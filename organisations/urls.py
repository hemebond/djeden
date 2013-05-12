from django.conf.urls import patterns, url
from organisations import views


urlpatterns = patterns('organisations.views',
	url(
		r'^(?:(?P<url_method>create)/)?$',
		views.OrganisationList.as_view(),
		name="organisation_list"
	),
	url(
		r'^(?P<pk>\d+)/(?:(?P<url_method>read|update|delete)/)?$',
		views.OrganisationDetail.as_view(),
		name="organisation_detail"
	),
	url(
		r'^types/(?:(?P<url_method>create)/)?$',
		views.OrganisationTypeList.as_view(),
		name="organisation_type_list"
	),
	url(
		r'^types/(?P<pk>\d+)/$',
		views.OrganisationTypeDetail.as_view(),
		name="organisation_type_detail"
	),
	url(
		r'^(?P<pk>\d+)/offices/(?:(?P<url_method>create)/)?$',
		views.OrganisationOfficeList.as_view(),
		name="organisation_detail_office_list"
	),
	url(
		r'^(?P<pk>\d+)/offices/(?:(?P<url_method>create)/)?$',
		views.OfficeList.as_view(),
		name="organisation_component_office_list"
	),
	url(
		r'^offices/(?:(?P<url_method>create)/)?$',
		views.OfficeList.as_view(),
		name="organisation_office_list"
	),
	url(
		r'^(?P<pk>\d+)/offices/(?P<office_pk>\d+)/(?:(?P<url_method>read|update|delete)/)?$',
		views.OfficeList.as_view(),
		name="organisation_office_list"
	),
)
