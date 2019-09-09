"""devproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from interactWBL import views
from interactWBL.models import Student, Mentor, StudentLogins, MentorLogins
from django.conf import settings
from django.conf.urls.static import static
from registration.backends.simple.views import RegistrationView
from django.core.urlresolvers import reverse
from django.views.generic import RedirectView
from django.contrib.auth.views import LoginView

"""   custom view class that was used during development and is now abandoned here
class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return reverse('interactWBL:register_profile')
    def registration_allowed(self):
        if self.request.user.is_authenticated:
            return False
        else:
            return True
"""
class MyLoginView(LoginView):
    def form_valid(self, form):
        login(self.request, form.get_user())
        if self.request.user.is_authenticated:
            user = self.request.user
            try:
                logged_student = Student.objects.get(user=user)
                StudentLogins.objects.create(student=logged_student)
                print("One student login logged!")
            except Student.DoesNotExist:
                print("logged in user is not a student")
                pass
            try:
                logged_mentor = Mentor.objects.get(user=user)
                MentorLogins.objects.create(mentor=logged_mentor)
                print("One mentor login logged!")
            except Mentor.DoesNotExist:
                print("logged in user is not a mentor!")
                pass
        return HttpResponseRedirect(self.get_success_url())
    redirect_authenticated_user = True

urlpatterns = [
    url(r'^$', views.landing, name='landing'),
    url(r'^interactWBL/', include('interactWBL.urls')), # mapping the WBL app urls to the project urls w/ 'include'function
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/register/$', views.signup, name='registration_register'),
   # url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/login/$', MyLoginView.as_view(), name='auth_login'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    # favicon to be displayed in browser
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/images/favicon.ico')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
