from django.contrib.auth.models import AbstractUser
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural="companies"


# user models/profiles
class User(AbstractUser):
    # extend the default AbstractUser class from the auth package, in order to customize the user
    is_student = models.BooleanField(default=False)
    is_academic = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)


class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company = models.ForeignKey(Company)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    mentor = models.ForeignKey(Mentor, on_delete=models.SET_NULL, null=True)


class Academic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class Course(models.Model):
    teacher = models.OneToOneField(Academic, null=True, on_delete=models.SET_NULL)


class Enrolment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.TextField

class Reflection(models.Model):
    REFLECTION_TYPE_CHOICES = (
        (1, 'Quick Reflection'),
        (2, 'Weekly Reflection'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    type = models.CharField(choices=REFLECTION_TYPE_CHOICES, max_length=32)
    date = models.DateField(auto_now_add=True)
    content = models.TextField


class Competency(models.Model):
    description = models.TextField()
    assignments = models.ManyToManyField(Assignment)
    reflections = models.ManyToManyField(Reflection)

    class Meta:
        verbose_name_plural="competencies"


class CourseTarget(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    competency = models.ForeignKey(Competency, on_delete=models.CASCADE)


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.TextField
    grade = models.CharField(max_length=20)
    file = models.FileField
    date = models.DateField(auto_now_add=True)


class PersonalCompetency(models.Model):
    COMPETENCY_PROGRESS_CHOICES=(
        (1, 'none'),
        (2, 'basic'),
        (3, 'good'),
        (4, 'excellent'),
    )
    competency = models.ForeignKey(Competency)
    course = models.ForeignKey(Course)
    progress = models.CharField(choices=COMPETENCY_PROGRESS_CHOICES, max_length=16, default= 1)

    class Meta:
        verbose_name_plural="personal competencies"

class CompetencyEndorsement(models.Model):
    COMPETENCY_PROGRESS_CHOICES=(
        (1, 'none'),
        (2, 'basic'),
        (3, 'good'),
        (4, 'excellent'),
    )
    author = models.ForeignKey(User)
    competency = models.ManyToManyField(PersonalCompetency)
    date = models.DateField(auto_now_add=True)
    progress = (models.CharField(choices=COMPETENCY_PROGRESS_CHOICES, max_length=16))
