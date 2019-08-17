from django.contrib import admin
# Register your models here.
from .models import Student
from .models import Mentor
from .models import Academic
from .models import Course
from .models import Competency
from .models import Company
admin.site.register(Student)
admin.site.register(Academic)
admin.site.register(Mentor)
admin.site.register(Course)
admin.site.register(Competency)
admin.site.register(Company)