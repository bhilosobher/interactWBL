from django import forms
from interactWBL.models import Course, Competency, PersonalCompetency, Mentor, Student, Company, CourseTarget, Enrolment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# these are form models which handle creating and saving a model into the database (by users)


# SignUpForm taken from https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
class SignUpForm(UserCreationForm):

    first_name = forms.CharField(max_length=30, required=True, help_text='')
    last_name = forms.CharField(max_length=30, required=True, help_text='')
    email = forms.EmailField(max_length=254, help_text='Required. Please provide your university or company email.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class CompetencyForm(forms.ModelForm):
    COMPETENCY_TYPE_CHOICES = (
        ('technical', 'Technical competency'),
        ('social', 'Social competency'),
        ('personal', 'Personal competency')
    )
    name = forms.CharField(max_length=128, help_text="Please enter the name for your new competency")
    description = forms.Textarea()
    type = forms.ChoiceField( choices=COMPETENCY_TYPE_CHOICES, help_text="Please select the new competency's type")
    class Meta:
        help_texts = {'description': 'Please define and describe the competency',}
        model = Competency
        exclude = ()


class CourseTargetsForm(forms.ModelForm):
    competency = forms.ModelChoiceField(queryset=Competency.objects.all(),
                                        help_text="Please select a competency for the course to target")
    class Meta:
        model = CourseTarget
        exclude = ('course',)


class EnrollmentForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=Student.objects.all(), help_text="Please select a student to enroll in course")

    class Meta:
        model = Enrolment
        exclude = ('course',)


class StudentForm(forms.ModelForm):
    YEAR_CHOICES = (
        ('1', 'first year'),
        ('2', 'second year'),
        ('3', 'third year'),
        ('4', 'fourth year'),
        ('5', 'postgraduate')
    )
    year = forms.ChoiceField(choices=YEAR_CHOICES, initial=1, help_text="Please enter your current year group")
    # select the mentor if known in advance
    mentor = forms.ModelChoiceField(queryset=Mentor.objects.all(), required=False,
                                    help_text="Please select your mentor, if known in advance ")

    class Meta:
        model = Student
        exclude = ('user',)


class MentorForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all())

    class Meta:
        model = Mentor
        exclude = ('user','competency_in_focus')


class CourseForm(forms.ModelForm):
    YEAR_CHOICES = (
        ('1', 'first year'),
        ('2', 'second year'),
        ('3', 'third year'),
        ('4', 'fourth year'),
        ('5', 'postgraduate')
    )
    name = forms.CharField(max_length=129, help_text="Please enter the course's name")
    year = forms.ChoiceField(choices=YEAR_CHOICES,initial=1,help_text="Please enter the year group for the course")
    moodle = forms.URLField(max_length=200,
                            help_text="Please enter link to course page in existing learning environment")
    description = forms.Textarea()
    ILOs = forms.Textarea()
    missed_lecture_procedure = forms.Textarea()
    lecture_recordings = forms.URLField(required=False, max_length=300, help_text="Please enter the link to the video "
                                                                                  "recordings resource")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        moodle = cleaned_data.get('moodle')

        if moodle and not (moodle.startswith('https://') or moodle.startswith('http://')):
            moodle ='https'+ moodle
            cleaned_data['moodle'] = moodle

            return cleaned_data

    class Meta:
        help_texts = {'description': 'Please enter course description',
                      'missed_lecture_procedure': 'Please specify the missed lectures procedure',
                      'ILOs': 'Please list the intended learning outcomes of the course',}
        model = Course
        exclude = ('teacher',)