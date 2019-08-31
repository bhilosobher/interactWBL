from django.shortcuts import render, redirect
from interactWBL.models import Course, Academic, Competency, Enrolment, Student, Mentor,Company
from django.contrib.auth.models import User
from django.contrib import auth
from interactWBL.forms import CourseForm, StudentForm, MentorForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here.


def index(request):
    return render(request,'interactWBL/index.html')


def dashboard(request):

    course_list = Course.objects.order_by('name')

    context_dict = {'courses': course_list,}
    return render(request, 'interactWBL/dashboard.html', context=context_dict)


def show_course(request, course_name_slug):
    context_dict = {}
    try:
        # check if a course with the name passed as a parameter from the urls engine actually exists
        # then pick all enrollments associated with such course
        course = Course.objects.get(slug = course_name_slug)
        print (course_name_slug)
        print(course)
        enrolments = Enrolment.objects.filter(course = course)
        # some debug code
        # print(enrolments.__len__())
        # for e in enrolments:
        #    print(e)
        students = []

        # then, for all these enrollment, put the enrolled students in a list and order them by last name
        for e in enrolments:
            students.append(e.student)

        def sort_funct(s):
            return s.user.last_name

        students.sort(key = sort_funct)
        context_dict['course'] = course
        context_dict['students'] = students
    except Course.DoesNotExist:
        # get here if the specified course does not exist; do nothing
        context_dict['course'] = None
        context_dict['students'] = None
    return render(request,'interactWBL/course.html',context_dict)

@login_required()
def add_course(request):
    is_teacher = False
    academics = Academic.objects.all()
    for a in academics:
        if a.user == request.user:
            is_teacher = True

    if request.user.is_superuser or is_teacher:
        form = CourseForm()

        # if http POST
        if request.method =='POST':
            form = CourseForm(request.POST)

            # if form data is valid, save the new course to the DB
            if form.is_valid():
                course = form.save(commit=False)
                teacher = Academic.objects.get_or_create(user=request.user)[0]
                course.teacher = teacher
                course.save()
                # what do after created course succesfully? redirect to course page/dashboard
                return dashboard(request)
            else:
                print(form.errors)
        return render(request, 'interactWBL/add_course.html', {'form': form})
    else:
        return HttpResponse("You do not have permission to access this page.")




def about(request):
    return render(request,'interactWBL/about.html')


def competencies(request):
    competency_list = Competency.objects.order_by('name')
    context_dict = {'competencies':competency_list,}
    return render(request,'interactWBL/competencies.html',context_dict)

# create a user profile (and associated student/mentor/academic) according to the user's registration email
# this makes the assumption that the student/academic users will register using their university accounts
# and only caters for University of Glasgow students and staff (though method could be generalised to any UK university)

@login_required
def register_profile(request):
    email = request.user.email
    user, domain = email.split("@")
    student = False
    if domain == 'gla.ac.uk' or domain == 'research.gla.ac.uk':
        academic = Academic(user=request.user)
        academic.save()
        return redirect('interactWBL:dashboard')

    elif domain == 'student.gla.ac.uk':
        form = StudentForm()
        student = True
    else:
        form = MentorForm
    #
    if request.method =='POST':
        if student == True:
            form = StudentForm(request.POST)
            if form.is_valid():
                student_profile = form.save(commit=False)
                student_profile.user = request.user
                student_profile.save()
                return redirect('interactWBL:dashboard')
            else:
                print(form.errors)
        else:
            form = MentorForm(request.POST)
            if form.is_valid():
                mentor_profile = form.save(commit=False)
                mentor_profile.user = request.user
                mentor_profile.save()
                return redirect('interactWBL:dashboard')
    context_dict = {'form':form}

    return render(request, 'interactWBL/profile_registration.html', context_dict)


@login_required
def profile(request, username):
    try:
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        return redirect('dashboard') # here should add red message upon return to dashboard...
    student = False
    email = request.user.email
    before_at, domain = email.split("@")
    if domain == 'gla.ac.uk' or domain == 'research.gla.ac.uk':
        pass
    elif domain == 'student.gla.ac.uk':
        userprofile = Student.objects.get_or_create(user=user)[0]
        form = StudentForm()
        student = True
    else:
        form = MentorForm()
        if(request.user.is_superuser):
            userprofile = None
        else:
            userprofile = Mentor.objects.get_or_create(user=user)[0]

    if request.method == 'POST':
        if form:
            if student:
                form = StudentForm(request.POST, instance=userprofile)
                if form.is_valid():
                    form.save(commit=True)
                    return redirect('interactWBL:dashboard')
                else:
                    print(form.errors)
            else:
                form = MentorForm(request.POST, instance=userprofile)
                if form.is_valid():
                    form.save(commit=True)
                    return redirect('interactWBL:dashboard')
                else:
                    print(form.erros)
    context_dict = {'userprofile': userprofile, 'selecteduser': user, 'form': form}

    return render(request, 'interactWBL/profile.html',context_dict)





