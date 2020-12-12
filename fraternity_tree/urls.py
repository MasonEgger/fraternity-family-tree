from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'my_tree', views.my_tree, name='my_tree'),
    url(r'pledge_class', views.pledge_class, name='pledge_class'),
]
