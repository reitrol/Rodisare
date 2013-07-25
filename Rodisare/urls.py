from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/feedreader/')),
    url(r'^feedreader/$', 'feedreader.views.index'),
    url(r'^feedreader/displayfeed/$', 'feedreader.views.displayfeed'),
    url(r'^feedreader/displayfeedinfo/$', 'feedreader.views.displayfeedinfo'),
    url(r'^feedreader/displayfeedentry/$', 'feedreader.views.displayfeedentry'),
    url(r'^feedreader/search/$', 'feedreader.views.search'),


    url(r'^feedreader/logout/$', 'feedreader.views.logoutUser'),
    url(r'^feedreader/register/$', 'feedreader.views.register'),

    url(r'^feedreader/manage/$', 'feedreader.views.manage'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls))


)
