from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^home$', views.home),
    url(r'^login', views.login),
    url(r'^logout', views.logout),
    url(r'^register$', views.register),
    url(r'^addQuote$', views.addQuote),
    url(r'^addremove$', views.addremove),
    url(r'^Quote/(?P<created_by>\w+)$', views.Quote)

]
