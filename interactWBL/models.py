from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from datetime import timedelta, timezone


class Competency(models.Model):
    COMPETENCY_TYPE_CHOICES = (
        ('technical', 'Technical competency'),
        ('social', 'Social competency'),
        ('personal', 'Personal competency')
    )
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    type = models.CharField(choices=COMPETENCY_TYPE_CHOICES, default='technical', max_length=16)

    class Meta:
        verbose_name_plural = "competencies"

    def __str__(self):
        return self.name



class Company(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = "companies"

    def __str__(self):
        return self.name


class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company = models.ForeignKey(Company)

    def __str__(self):
        return self.user.username


class Student(models.Model):
    YEAR_CHOICES = (
        ('1', 'first year'),
        ('2', 'second year'),
        ('3', 'third year'),
        ('4', 'fourth year'),
        ('5', 'postgraduate')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    mentor = models.ForeignKey(Mentor, on_delete=models.SET_NULL, null=True)
    year = models.CharField(default=1,choices=YEAR_CHOICES,max_length=8)
    competencies_in_focus = models.ManyToManyField(Competency, blank=True)


    def __str__(self):
        return self.user.username


class Academic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class StudentLogins (models.Model):
    student = models.ForeignKey(Student)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Student logins"

    def __str__(self):
        return str(self.student) + ':' + str(self.date)


class MentorLogins(models.Model):
    mentor = models.ForeignKey(Mentor)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Mentor logins"

    def __str__(self):
        return str(self.mentor) + ':' + str(self.date)


class Course (models.Model):
    YEAR_CHOICES = (
        ('0', 'mixed year'),
        ('1', 'first year'),
        ('2', 'second year'),
        ('3', 'third year'),
        ('4', 'fourth year'),
        ('5', 'postgraduate')
    )
    name = models.CharField(max_length=128)
    teacher = models.ForeignKey(Academic, blank=True, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    year = models.CharField(blank=True,choices=YEAR_CHOICES, null=True,max_length=8)
    moodle = models.URLField(blank=True,null=True,max_length=200)
    ILOs = models.TextField(blank=True,null=True)
    missed_lecture_procedure = models.TextField(blank=True,null=True)
    lecture_recordings = models.URLField(blank=True,null=True,max_length=300)
    slug = models.SlugField()

    def save(self,*args,**kwargs):
        i = 0
        courses = Course.objects.all()
        for c in courses:
            if c.name == self.name:
                i+=1
        if i == 0:
            self.slug = slugify(self.name)
        else:
            self.slug = slugify(self.name) + i.__str__()
        super(Course,self).save(*args,**kwargs)

    def __str__(self):
        return self.name


class Enrolment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.student.user.username + ' in ' + self.course.name
# assigment.competency.add(c)

class Assignment(models.Model):
    name = models.CharField(max_length=128)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField()
    deadline = models.DateField(auto_now_add=True)
    mentor = models.ForeignKey(Mentor, blank=True, null=True)
    # the assignment model refers to the student field because it was envisaged that the students might be given
    # individual assignments by their mentors, through the system (as an extra feature)
    student = models.ForeignKey(Student, blank=True, null=True)
    competencies = models.ManyToManyField(Competency)

    def __str__(self):
        return self.name + " assignment"

class ReflectionTopic(models.Model):
    topic = models.TextField()
    student = models.ForeignKey(Student, null=True, blank=True)
    course = models.ForeignKey(Course, null =True, blank= True)
    academic = models.ForeignKey(Academic, null=True, blank=True)
    mentor = models.ForeignKey(Mentor, null= True, blank=True)
    def __str__(self):
        return "reflection on "+self.topic


class Reflection(models.Model):
    REFLECTION_TYPE_CHOICES = (
        ('quick', 'Quick Reflection'),
        ('weekly', 'Weekly Reflection'),
    )
    topic = models.ForeignKey(ReflectionTopic, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True,null=True)
    type = models.CharField(choices=REFLECTION_TYPE_CHOICES, max_length=32)
    date = models.DateField(auto_now_add=True)
    content = models.TextField()
    competencies = models.ManyToManyField(Competency)
    assignment = models.ForeignKey(Assignment, blank=True, null=True)

    def __str__(self):
        return "reflection on the " + self.course.name + " course"


class CourseTarget(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    competency = models.ForeignKey(Competency, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Course targets'

    def __str__(self):
        return "["+self.course.name + "]     " + self.competency.name


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.TextField(max_length=1000, blank=True)
    grade = models.CharField(max_length=16, default="not graded")
    file = models.FileField(upload_to='coursework_submissions', null=True,blank = True)
    date = models.DateField(auto_now_add=True)
    grader = models.ForeignKey(Academic, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(Course, null=True, blank=True)

    def __str__(self):
        return 'submission for '+self.course.name + " by "+ self.student.user.username


class PersonalCompetency(models.Model):
    student = models.ForeignKey(Student)
    COMPETENCY_PROGRESS_CHOICES = (
        ('0', 'none'),
        ('1', 'basic'),
        ('2', 'good'),
        ('3', 'excellent'),
    )
    competency = models.ForeignKey(Competency)
    assignments = models.ManyToManyField(Assignment, blank=True)
    progress = models.CharField(choices=COMPETENCY_PROGRESS_CHOICES, max_length=16, default='0')

    class Meta:
        verbose_name_plural = "personal competencies"

    def __str__(self):
        return self.student.user.username + " " + self.competency.name + " competency"


class CompetencyEndorsement(models.Model):
    COMPETENCY_PROGRESS_CHOICES = (
        ('0', 'none'),
        ('1', 'basic'),
        ('2', 'good'),
        ('3', 'excellent'),
    )
    mentor = models.ForeignKey(Mentor, null=True,blank=True)
    academic = models.ForeignKey(Academic, null=True,blank=True)
    competency = models.ForeignKey(PersonalCompetency)
    date = models.DateField(auto_now_add=True)
    progress = (models.CharField(choices=COMPETENCY_PROGRESS_CHOICES, max_length=16))

    class Meta:
        verbose_name_plural = "competency endorsements"

    def __str__(self):
        return self.competency.competency.name + " endorsement"


class Appraisal(models.Model):
    author = models.ForeignKey(Mentor)
    subject = models.ForeignKey(Student)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.subject.user.username + "'s appraisal"
