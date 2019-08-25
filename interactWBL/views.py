from django.shortcuts import render
from interactWBL.models import Course, Student, Competency
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("This is the landing page. It will include a login, a register and an about button.")

def dashboard(request):

    course_list = Course.objects.order_by('name')
    competency_list = Competency.objects.order_by('name')
    context_dict = {'courses': course_list, 'competencies':competency_list}
    return render(request, 'interactWBL/dashboard.html', context=context_dict)


def about(request):

    return render(request,'interactWBL/about.html')
