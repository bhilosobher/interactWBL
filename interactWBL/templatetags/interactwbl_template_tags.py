from django import template
from interactWBL.models import Course, Student, Academic, Enrolment

register = template.Library()


@register.inclusion_tag('interactWBL/courses.html')
def get_courses(user):
    try:
        student = Student.objects.get(user=user)
    except Student.DoesNotExist:
        student = False

    try:
        academic = Academic.objects.get(user = user)
    except Academic.DoesNotExist:
        academic = False

    if student:
        enrolments = list(Enrolment.objects.filter(student = student))
        courses = []
        for e in enrolments:
            courses.append(e.course)
        return {'courses':courses }
    elif academic:
        courses = Course.objects.filter(teacher=academic)
        return {'courses':courses}
    else:
        return {}

