from django.shortcuts import render, redirect
from interactWBL.models import Course, Academic, Competency, Enrolment, Student, Mentor, Company, CourseTarget, StudentLogins, MentorLogins, Reflection, Assignment, Submission
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from interactWBL.forms import CourseForm, StudentForm, MentorForm, SignUpForm, CompetencyForm,CourseTargetsForm,EnrollmentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# custom registration view;
def signup(request):
    # if user is already logged in, no need to register - redirect to dashboard
    if request.user.is_authenticated:
        return redirect('interactWBL:dashboard')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # once user successfully registered their basic profile, now register their academic/student/mentor profile
            return redirect('interactWBL:register_profile')
    else:
        form = SignUpForm()
    return render(request, 'registration/registration_form.html', {'form': form})


def landing(request):
    # the landing view, containing the login and signup buttons
    return render(request, 'interactWBL/landing.html')


# not a view, this is a a helper function which helps determine what type of user is authenticated
def determine_profile(request):
    # return a tuple of booleans: (is_teacher, is_student, is_mentor)
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return (False, False, False)
        else:
            email = request.user.email
            before_at, domain = email.split("@")
            if domain == 'gla.ac.uk' or domain == 'research.gla.ac.uk':
                return True, False, False
            elif domain == 'student.gla.ac.uk':
                return False, True, False
            else:
                return False, False, True


def dashboard(request):
    # only logged in users can access this
    if not request.user.is_authenticated:
        return redirect('interactWBL:landing')
    # now that we know that the user is logged in, determine its type (student/mentor/academic)
    (is_teacher, is_student, is_mentor) = determine_profile(request)

    context_dict = {}
    context_dict['all_courses'] = Course.objects.order_by('name')
    context_dict['is_academic'] = is_teacher
    context_dict['is_student'] = is_student
    context_dict['is_mentor'] = is_mentor
    # if user is an academic, find out what courses they are teaching
    active_academic_courses = None
    if is_teacher:
        active_academic = Academic.objects.filter(user=request.user)
        active_academic_courses = Course.objects.filter(teacher=active_academic)
        context_dict['courses'] = active_academic_courses


    # if it is a student, then find out what courses they are taking to they can be displayed as well
    elif is_student:
        active_student = Student.objects.filter(user=request.user)
        enrolments = Enrolment.objects.filter(student=active_student)
        courses = []
        for e in enrolments:
            courses.append(e.course)
        context_dict['courses'] = courses
    elif is_mentor:
        mentor = Mentor.objects.get(user = request.user)
        students = list(Student.objects.filter(mentor=mentor))
        context_dict['students'] = students


    # finally, find out the students enrolled in the courses the academic is teaching

    if active_academic_courses:
        active_academic_enrolments = []
        for c in active_academic_courses:
            enrolments = list(Enrolment.objects.filter(course=c))
            # we obtain a list of enrolments for each of the academics' courses; we then in turn add it to a list (of lists)
            active_academic_enrolments.append(enrolments)
        context_dict['enrolments'] = active_academic_enrolments

        # we also want to know the number of logins of the students in the academic user's courses
        students_of_active_academic = []
        # we look at all the students enrolled in the academic's courses and we collect them in a list
        for enrolment_list in active_academic_enrolments:
            for enrolment in enrolment_list:
                students_of_active_academic.append(enrolment.student)
        # now we take that list and we transform it in a set, to remove duplicates
        students_set= set(students_of_active_academic)

        # find out how many reflections and submissions there are for the academic's courses
        number_of_submissions = 0
        number_of_reflections = 0
        for course in active_academic_courses:
            reflections = list(Reflection.objects.filter(course=course))
            submissions = list(Submission.objects.filter(course=course))
            number_of_submissions+=len(submissions)
            number_of_reflections+=len(reflections)
        # after finding out, add them to the dictionary to pass the values to the templates for display
        context_dict['reflections_number'] = number_of_reflections
        context_dict['submissions_number'] = number_of_submissions

        # finally, for each student login in the DB, we see if the student belongs to the set of the academic's pupils
        student_logins = list(StudentLogins.objects.all())
        number_of_logins = 0
        for login in student_logins:
            if login.student in students_set:
                number_of_logins+=1

        context_dict["pupils_logins"] = number_of_logins

    return render(request, 'interactWBL/dashboard.html', context=context_dict)


def my_courses(request):
    (is_teacher, is_student, is_mentor) = determine_profile(request)
    context_dict = {}


    # if the user is a teacher, determine the courses they are teaching and later list them in the template
    if is_teacher:
        active_academic = Academic.objects.filter(user=request.user)
        context_dict['courses'] = Course.objects.filter(teacher=active_academic)
    # if it is a student, then find out what courses they are taking to they can be displayed as well
    elif is_student:
        active_student = Student.objects.filter(user=request.user)
        enrolments = Enrolment.objects.filter(student=active_student)
        courses = []
        for e in enrolments:
            courses.append(e.course)
        context_dict['courses'] = courses

    context_dict['is_academic'] = is_teacher
    context_dict['is_student'] = is_student
    context_dict['is_mentor'] = is_mentor

    return render(request, 'interactWBL/my_courses.html', context_dict)


def show_course(request, course_name_slug):
    try:
        # check if a course with the name passed as a parameter from the urls engine actually exists
        # then pick all enrollments associated with such course
        course = Course.objects.get(slug=course_name_slug)
        print(course_name_slug)
        print(course)
        enrolments = Enrolment.objects.filter(course=course)
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

        # when displaying the students enrolled in the course, they will be listed alphabetically (by last name)
        students.sort(key=sort_funct)

        (is_teacher, is_student, is_mentor) = determine_profile(request)
        context_dict = {}
        # get the list of target competencies for the course
        context_dict['competencies'] = list(CourseTarget.objects.filter(course=course))
        context_dict['is_academic'] = is_teacher
        context_dict['is_student'] = is_student
        context_dict['is_mentor'] = is_mentor
        context_dict['course'] = course
        context_dict['students'] = students
        # if the user is a teacher, determine the courses they are teaching and later list them in the template
        if is_teacher:
            active_academic = Academic.objects.get(user=request.user)
            context_dict['active_academic'] = active_academic
            context_dict['courses'] = Course.objects.filter(teacher=active_academic)
        # if it is a student, then find out what courses they are taking to they can be displayed as well
        elif is_student:
            active_student = Student.objects.filter(user=request.user)
            enrolments = Enrolment.objects.filter(student=active_student)
            courses = []
            for e in enrolments:
                courses.append(e.course)
            context_dict['courses'] = courses

    except Course.DoesNotExist:
        # get here if the specified course does not exist; do nothing
        context_dict= {}
        context_dict['course'] = None
        context_dict['students'] = None
    return render(request, 'interactWBL/course.html', context_dict)


@login_required()
def add_competency(request):
    # check if the user is academic: if not, deny access
    is_academic = determine_profile(request)[0]
    if not is_academic:
        return HttpResponse("You do not have access to this page")

    # if the user is an academic and the request is a get, display the form to be filled in

    form = CompetencyForm()

    # if the academic user fills in the form and attempts a HTTP POST, process it
    if request.method == 'POST':
        form = CompetencyForm(request.POST)
        if form.is_valid():
            competency = form.save(commit=True)
            return dashboard(request)
        else:
            print(form.errors)

    context_dict = {}
    context_dict['form'] = form
    return render(request, 'interactWBL/add_competency.html', context_dict)

@login_required
def add_target(request, course_name_slug):

    course = Course.objects.get(slug = course_name_slug)
    is_academic = determine_profile(request)[0]
    if not is_academic:
        return HttpResponse("You do not have access to this page")
    form = CourseTargetsForm()
    if request.method == 'POST':
        form = CourseTargetsForm(request.POST)
        if form.is_valid():
            course_target = form.save(commit=False)
            course_target.course = course
            course_target.save()
            return show_course(request, course.slug)
        else:
            print(form.errors)
    context_dict = {}
    context_dict['course'] = course
    context_dict['form'] = form
    return render(request, 'interactWBL/add_competency_targets_to_course.html', context_dict)

@login_required
def enroll(request, course_name_slug):
    course = Course.objects.get(slug=course_name_slug)
    is_academic = determine_profile(request)[0]
    if not is_academic:
        return HttpResponse("You do not have access to this page")
    form = EnrollmentForm()
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            course_target = form.save(commit=False)
            course_target.course = course
            course_target.save()
            return show_course(request, course.slug)
        else:
            print(form.erros)
    context_dict = {}
    context_dict['course'] = course
    context_dict['form'] = form
    return render(request, 'interactWBL/enroll.html', context_dict)

@login_required
def add_course(request):
    # dermine if the user requesting this page has an academic profile (i.e. is an academic)
    is_academic = False
    academics = Academic.objects.all()
    for a in academics:
        if a.user == request.user:
            active_academic = a
            is_academic = True
    # next, determine the courses the academic is already teaching (if any), to display them in the sidebar dropdown
    if active_academic:
        courses = Course.objects.filter(teacher=active_academic)

    # unless the user is an academic or admmin, this form won't be rendered
    if request.user.is_superuser or is_academic:
        form = CourseForm()

        # if http POST
        if request.method == 'POST':
            form = CourseForm(request.POST)

            # if form data is valid, save the new course to the DB
            if form.is_valid():
                course = form.save(commit=False)
                teacher = Academic.objects.get_or_create(user=request.user)[0]
                course.teacher = teacher
                course.save()
                # what do after created course succesfully? redirect to course page/dashboard
                return add_target(request,course.slug)
            else:
                print(form.errors)

        return render(request, 'interactWBL/add_course.html',
                      {'form': form, 'is_academic': is_academic, 'courses': courses})
    else:
        return HttpResponse("You do not have permission to access this page.")


def about(request):
    return render(request, 'interactWBL/about.html')


def competencies(request):
    (is_teacher, is_student, is_mentor) = determine_profile(request)
    context_dict = {}
    competency_list = Competency.objects.order_by('name')

    context_dict['competencies'] = competency_list
    context_dict['is_academic'] = is_teacher
    context_dict['is_student'] = is_student
    context_dict['is_mentor'] = is_mentor

    # if the user is an academic, find the courses they teach and pass them to the template to be displayed
    if is_teacher:
        active_academic = Academic.objects.filter(user=request.user)
        context_dict['courses'] = Course.objects.filter(teacher=active_academic)
    # if the user is a student, find the courses they are enrolled in, put them in a list and pass it to the template
    elif is_student:
        active_student = Student.objects.filter(user=request.user)
        enrolments = Enrolment.objects.filter(student=active_student)
        courses = []
        for e in enrolments:
            courses.append(e.course)
        context_dict['courses'] = courses
    elif is_mentor:
        mentor = Mentor.objects.get(user=request.user)
        students = list(Student.objects.filter(mentor=mentor))
        context_dict['students'] = students

    return render(request, 'interactWBL/competencies.html', context_dict)


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
    if request.method == 'POST':
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
    context_dict = {'form': form}

    return render(request, 'interactWBL/profile_registration.html', context_dict)


@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('dashboard')  # here should add red message upon return to dashboard...
    student = False
    email = request.user.email
    before_at, domain = email.split("@")
    userprofile = None
    form = None
    if domain == 'gla.ac.uk' or domain == 'research.gla.ac.uk':
        pass
    elif domain == 'student.gla.ac.uk':
        userprofile = Student.objects.get_or_create(user=user)[0]
        form = StudentForm()
        student = True
    else:
        form = MentorForm()
        if (request.user.is_superuser):
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
                    print(form.errors)

    (is_teacher, is_student, is_mentor) = determine_profile(request)
    context_dict = {}
    context_dict['is_academic'] = is_teacher
    context_dict['is_student'] = is_student
    context_dict['is_mentor'] = is_mentor
    context_dict['userprofile'] = userprofile
    context_dict['selecteduser'] = user
    context_dict['form'] = form
    # if the user is an academic, find the courses they teach and pass them to the template to be displayed
    if is_teacher:
        active_academic = Academic.objects.filter(user=request.user)
        active_academic_courses = Course.objects.filter(teacher=active_academic)
        context_dict['courses'] = active_academic_courses

        # now let's do some further querying to find & list the student's reflections
        try:
            reflections = []
            student_being_viewed = Student.objects.get(user=user)
            for course in active_academic_courses:
                reflections += list(Reflection.objects.filter(student=student_being_viewed).filter(course=course))
            context_dict['reflections'] = reflections
        except Student.DoesNotExist:
            pass
    # if the user is a student, find the courses they are enrolled in, put them in a list and pass it to the template
    elif is_student:
        active_student = Student.objects.filter(user=request.user)
        enrolments = Enrolment.objects.filter(student=active_student)
        courses = []
        for e in enrolments:
            courses.append(e.course)
        context_dict['courses'] = courses







    return render(request, 'interactWBL/profile.html', context_dict)


def mentors(request):
    context_dict = {}
    (is_teacher, is_student, is_mentor) = determine_profile(request)
    if is_student:
        student = Student.objects.get(user=request.user)
        context_dict['student_mentor'] = student.mentor

    # boilerplate code for properly rendering the data in the sidebar - should be refactored into custom template tags
    # to avoid this repetition

    context_dict = {}
    context_dict['mentors'] = Mentor.objects.all()
    context_dict['is_academic'] = is_teacher
    context_dict['is_student'] = is_student
    context_dict['is_mentor'] = is_mentor
    if is_teacher:
        active_academic = Academic.objects.filter(user=request.user)
        context_dict['courses'] = Course.objects.filter(teacher=active_academic)
    # if the user is a student, find the courses they are enrolled in, put them in a list and pass it to the template
    elif is_student:
        active_student = Student.objects.filter(user=request.user)
        enrolments = Enrolment.objects.filter(student=active_student)
        courses = []
        for e in enrolments:
            courses.append(e.course)
        context_dict['courses'] = courses

    return render(request, 'interactWBL/mentors.html', context_dict)

def remove_target(request, target_id):
    course = CourseTarget.objects.get(id=target_id).course
    CourseTarget.objects.get(id = target_id).delete()
    return show_course(request,course.slug)

def students(request):
    context_dict = {}
    (is_teacher, is_student, is_mentor) = determine_profile(request)
    if is_teacher:
        active_academic = Academic.objects.get(user=request.user)
        active_academic_courses = active_academic.course_set
        context_dict['courses'] = active_academic_courses

        # if it is a student, then find out what courses they are taking to they can be displayed as well
    elif is_mentor:
        mentor = Mentor.objects.get(user=request.user)
        students = list(Student.objects.filter(mentor=mentor))
        context_dict['students'] = students

    return render(request, 'interactWBL/students.html', context_dict)