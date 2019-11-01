from django import template
from interactWBL.models import Course, Student, Academic, Enrolment, Mentor

register = template.Library()

# check what type of user is viewing the section generated by these custom template tags, then act accordingly...
@register.inclusion_tag('interactWBL/courses.html')
def get_courses(user):
    try:
        student = Student.objects.get(user=user)
    except Student.DoesNotExist:
        student = False

    try:
        academic = Academic.objects.get(user=user)
    except Academic.DoesNotExist:
        academic = False

    try:
        mentor = Mentor.objects.get(user=user)
    except Mentor.DoesNotExist:
        mentor = False

    # if the user is a student, then we will show the courses the student user is enrolled in
    if student:
        enrolments = list(Enrolment.objects.filter(student=student))
        courses = []
        for e in enrolments:
            courses.append(e.course)
        return {'courses': courses}

    # if the user is an academic, then we will show the courses they are teaching
    elif academic:
        courses = Course.objects.filter(teacher=academic)
        return {'courses': courses}

    # if the user is a mentor, then we will try to show the courses in which they their *mentorees* are enrolled in...
    # difficult to query for this data due to efficient (but unfriendly) DB design...
    elif mentor:
        # first, collect all students mentored by the relevant mentor
        students = Student.objects.filter(mentor=mentor)
        enrolments = []
        # the tricky part: for each student, collect their enrollments in a list and while also concatenating the lists
        for student in students:
            enrolments = enrolments + list(Enrolment.objects.filter(student=student))
        courses_with_duplicates = []
        # translate the list of enrolments into a list of courses, which will have duplicates (if more than one of
        # the mentor's students is enrolled in any one course
        for enrolment in enrolments:
            courses_with_duplicates.append(enrolment.course)
        # crucial step: by converting the list into a set, eliminate duplicates and finally determine the needed courses
        distinct_courses = set(courses_with_duplicates)
        return {'courses': distinct_courses}

    else:
        return {}