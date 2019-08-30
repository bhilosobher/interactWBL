from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


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

    def __str__(self):
        return self.user.username


class Academic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


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


class Competency(models.Model):
    COMPETENCY_TYPE_CHOICES = (
        ('technical', 'Technical competency'),
        ('social', 'Social competency'),
        ('personal', 'Personal competency')
    )
    name = models.CharField(max_length=128)
    description = models.TextField()
    type = models.CharField(choices=COMPETENCY_TYPE_CHOICES, default='technical', max_length=16)

    class Meta:
        verbose_name_plural = "competencies"

    def __str__(self):
        return self.name


class Assignment(models.Model):
    name = models.CharField(max_length=128)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField()
    deadline = models.DateField()
    mentor = models.ForeignKey(Mentor, blank=True, null=True)
    student = models.ForeignKey(Student, blank=True, null=True)
    competencies = models.ManyToManyField(Competency)

    def __str__(self):
        return self.name + " assignment"


class Reflection(models.Model):
    REFLECTION_TYPE_CHOICES = (
        ('quick', 'Quick Reflection'),
        ('weekly', 'Weekly Reflection'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
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
    file = models.FileField(upload_to='coursework_submissions')
    date = models.DateField(auto_now_add=True)
    grader = models.ForeignKey(Academic, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return 'submission ' + str(self.id)


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
    author = models.ForeignKey(User)
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
