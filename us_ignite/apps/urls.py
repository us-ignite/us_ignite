from django.conf.urls import patterns, url


urlpatterns = patterns(
    'us_ignite.apps.views',
    url(r'^$', 'app_list', name='app_list'),
    url(r'^add/$', 'app_add', name='app_add'),
    url(r'^(?P<slug>[-\w]+)/$', 'app_detail', name='app_detail'),
)