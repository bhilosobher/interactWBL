from django import forms
from interactWBL.models import Course, Reflection, Competency, PersonalCompetency, Mentor, Student, Company
from django.contrib.auth.models import User
# these are form models which handle creating and saving a model into the database (by users)


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
    description = forms.Textarea(attrs={'size': 5, 'placeholder': 'Enter course description'})
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
                      'missed_lecture_procedure': 'Please specify themissed lectures procedure',
                      'ILOs': 'Please list the intended learning outcomes of the course',}
        model = Course
        exclude = ('teacher',)