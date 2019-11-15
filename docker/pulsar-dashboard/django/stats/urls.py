from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^property/(?P<property_name>.+)/$', views.property, name='property'),
    url(r'^namespace/(?P<namespace_name>.+)/$', views.namespace, name='namespace'),


    url(r'^brokers/$', views.brokers, name='brokers'),
    url(r'^brokers/(?P<cluster_name>.+)/$', views.brokers_cluster, name='brokers_cluster'),
    url(r'^broker/(?P<broker_url>.+)/$', views.broker, name='broker'),

    url(r'^topics/$', views.topics, name='topics'),
    url(r'^topic/(?P<topic_name>.+)/$', views.topic, name='topic'),

    url(r'^clusters/$', views.clusters, name='clusters'),
]
