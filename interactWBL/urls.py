from django.conf.urls import url
from interactWBL import views

# this is the app-specific urls file, which defines how each address is to be mapped to a view function
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dashboard/$',views.dashboard, name='dashboard'),
    url(r'^about/$', views.about, name='about'),

]