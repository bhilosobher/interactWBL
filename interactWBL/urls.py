from django.conf.urls import url
from interactWBL import views
app_name ='interactWBL'
# this is the app-specific urls file, which defines how each address is to be mapped to a view function
urlpatterns = [
    url(r'^$', views.landing, name='landing'),
    url(r'^dashboard/$',views.dashboard, name='dashboard'),
    url(r'^about/$', views.about, name='about'),
    url(r'^add_competency/$', views.add_competency, name='add_competency'),
    url(r'add_course/$',views.add_course, name='add_course'),
    url(r'course/(?P<course_name_slug>[\w\-]+)/$',views.show_course, name='show_course'),
    url(r'course/$', views.my_courses, name= 'my_courses'),
    url(r'^competencies/$',views.competencies, name='competencies'),
    url(r'^register_profile/$',views.register_profile, name='register_profile'),
    url(r'^profile/(?P<username>[\w\-]+)/$',views.profile, name = 'profile'),
    url(r'^mentors/$', views.mentors, name= 'mentors'),
    url(r'^remove_target/(?P<target_id>[\w]+)/$', views.remove_target, name = 'remove_target'),


]