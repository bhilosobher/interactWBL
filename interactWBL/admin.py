from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import Student, Mentor, Academic, Course, Competency, Company, Enrolment, Assignment,\
    PersonalCompetency, CompetencyEndorsement, CourseTarget, Reflection, Submission, Appraisal, StudentLogins,\
    MentorLogins, ReflectionTopic
class CompetencyAdmin(admin.ModelAdmin):
    list_display = ('name','description','type')

class MentorAdmin(admin.ModelAdmin):
    list_display = ('user','company',)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user','mentor')

class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(ReflectionTopic)
admin.site.register(Student, StudentAdmin)
admin.site.register(Academic)
admin.site.register(Mentor, MentorAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Company)
admin.site.register(Enrolment)
admin.site.register(Assignment)
admin.site.register(PersonalCompetency)
admin.site.register(CourseTarget)
admin.site.register(CompetencyEndorsement)
admin.site.register(Reflection)
admin.site.register(Submission)
admin.site.register(Appraisal)
admin.site.register(Competency, CompetencyAdmin)
admin.site.register(StudentLogins)
admin.site.register(MentorLogins)