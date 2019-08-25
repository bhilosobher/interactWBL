import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devproj.settings')

# names package will help us generate random names to create student users; random for creating student ids
import django, names, random

django.setup()
from interactWBL.models import Student, User, Mentor

def populate():
    mentor_list = list(Mentor.objects.all())
    for i in range(1,200):
        # set up all the student info so it mocks UoG student info
        student_number = 2000000 + random.randint(0,999999)
        f_name = names.get_last_name()
        l_name = names.get_last_name()
        initial = l_name[0].lower()
        student_year = random.randint(1,5)
        student_id = student_number.__str__()+initial
        student_email = student_id+'@student.gla.ac.uk'
        print(student_email)
        # now that we have all the pieces, create the user
        u = User.objects.get_or_create(username=student_id,password='securepassword',email=student_email,
                                       last_name=l_name,first_name=f_name)[0]
        # lastly create the user, using the random module to assign a random mentor from the existing ones
        s = Student.objects.get_or_create(user=u, year = student_year,mentor=mentor_list[random.randint(0,len(mentor_list)-1)])




if __name__=='__main__':
    print('starting student population script...')
    populate()