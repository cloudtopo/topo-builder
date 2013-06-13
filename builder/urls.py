#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^builder/', include('builder.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    #
    (r'^jobmng/startserver$', 'builder.jobmng.views.startserver'),
    (r'^jobmng/stopserver$', 'builder.jobmng.views.stopserver'),
    (r'^jobmng/dojob/(?P<job_id>\d+)$', 'builder.jobmng.views.dojob'),
    (r'^jobmng/clear/(?P<job_id>\d+)$', 'builder.jobmng.views.clearjob'),
    (r'^jobmng/canceljob$', 'builder.jobmng.views.canceljob'),
    (r'^jobmng/forcejob/(?P<job_id>\d+)/(?P<vcs_id>\d+)$', 'builder.jobmng.views.forcejob'),
    (r'^jobmng/delete/(?P<job_id>\d+)/(?P<build_ids>[\d_]+)$', 'builder.jobmng.views.delete'),
    (r'^jobmng/publish/(?P<build_id>\d+)$', 'builder.jobmng.views.publish'),
    (r'^jobmng/trigcmd/(?P<job_id>\d+)/(?P<build_id>\d+)/(?P<cmd_id>\d+)$', 'builder.jobmng.views.trigcmd'),
    (r'^jobmng/execcmd/(?P<job_id>\d+)/(?P<build_id>\d+)/(?P<cmd_id>\d+)$', 'builder.jobmng.views.execcmd'),
    (r'^$', 'builder.jobmng.views.index'),
    (r'^jobmng/(?P<job_id>\d+)/$', 'builder.jobmng.views.detail'),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    #django_xmlrpc
    (r'xmlrpc/$', 'django_xmlrpc.views.handle_xmlrpc',),
    
    #静态文件的url,注意document_root即使是英文也必须用unicode字符串, 这样os.listdir才会返回unicode的字符
    #将artifact和workspace都设置为可静态访问
    (r'^artifact/(?P<path>.*)$', 'django.views.static.serve', 
                                    {'document_root': u'../artifact', 
                                      'show_indexes': True}),
    (r'^workspace/(?P<path>.*)$', 'django.views.static.serve', 
                                    {'document_root': u'../workspace', 
                                      'show_indexes': True}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', 
                                    {'document_root': u'static', 
                                      'show_indexes': True}),
)
