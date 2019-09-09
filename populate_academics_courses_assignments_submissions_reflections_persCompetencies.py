import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devproj.settings')

import django,names,random

django.setup()
from interactWBL.models import User, Academic, Course, Competency, CourseTarget, Student, Enrolment, Assignment, Submission, Reflection, PersonalCompetency, CompetencyEndorsement


def populate():
    # have existing competencies ready in a list and calculate how many there are
    competencies_list = list(Competency.objects.all())
    comps_no = len(competencies_list)

    # academic first names
    academics_names = ['Mechelle', 'Evelia', 'Sylvie', 'Stephania', 'Octavio', 'Shona', 'Spencer', 'Natisha', 'Guadalupe',
             'Lea', ]

    # course names for courses to be created
    course_names = ['Programming', 'Cyber Security Fundamentals', 'Systems and Networks', 'Enterprise Cyber Security',
                    'Database Theory and Application', 'Software Engineering', 'Software Project Managements',
                    'Internet Technology', 'Advanced Programming', 'Algorithms and Data Structures',]

    # collect existing students in a list and determine their number
    students_list = list(Student.objects.all())
    studs_no = len(students_list)
    print("there are " + str(studs_no) + " students")


    # create 10 users, then associate 10 academics with the 10 users & create 10 courses, 1 for taught by each academic

    i = 0
    for n in academics_names:
        # create a user with name from the list above
        u = User.objects.get_or_create(username=n.lower(), password='')[0]
        u.set_password('securepassword')
        u.save()
        # then associate an academic profile with that user
        a = Academic.objects.get_or_create(user=u)[0]
        u.first_name = academics_names[i]
        u.last_name = names.get_last_name()
        u.email = academics_names[i].lower() + '.'+ u.last_name.lower()+'@gla.ac.uk'
        u.save()
        # after the academic profile is fully set up, create a course taught by that academic

        c = Course.objects.get_or_create(teacher=a, year = random.randint(1,5), name=course_names[i],
                                         lecture_recordings="http://www.echo360.com",missed_lecture_procedure="The exact procedure will be announced later, but please make sure to message me if you have any pressing doubts at the moment.",
                                         ILOs="The course aims to provide students with mathematical/quantitative skills and knowledge that consititute the foundation for techniques and instruments in both microeconomic theory and intertemporal macroeconomics (such as multivariate calculus and integration, constrained optimisation, differential equations, dynamic programming methods, functional analysis), and to demonstrate various mathematical techniques are applied to economic problems.",
                                         moodle='https://moodle.org/',
                                         description="The aim of this course is to provide students with a comprehensive overview of web application development. It will provide students with the skills to design and develop distributed web applications in a disciplined manner, using a range of tools and technologies. It will also strengthen their understanding of the context and rationale of distributed systems.")[0]
        i += 1 # this is so we iterate through academic and course names at the same time

        """
                 this next sections deals with randomly assigning competency objectives to the created courses
                 We select a competency at random from the list and add about 8-9 targets to the most recent course
        """

        for j in range (1,10):
            t = CourseTarget.objects.get_or_create(course=c,competency=competencies_list[random.randint(0,comps_no-1)])[0]

        """
                this next sections deals with enrolling students in courses (according to the year of the course)
        """
    course_list = list(Course.objects.all())
    for course in course_list:
        print(course)
        print("now enrolling:")
        for s in students_list:
            if s.year == course.year:
                e = Enrolment.objects.get_or_create(course=course, student=s)[0]
                e.save()
                print(e)
            else:
                pass
    print("Generating assignments...")
    print("Generating submissions...")
    print("Generating reflections and personal competencies...")
    for course in course_list[0:6]:
        # for half of the courses determine the students enrolled
        enrollments  = list(Enrolment.objects.filter(course= course))
        students_in_course =[]
        # for each course, create an assignment
        assignment = Assignment.objects.get_or_create(name=course.name + " project", course=course,
                                                      description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",)[0]
        # add associate 4 competencies with this assignment
        for i in range(1, 5):
            random_competency = competencies_list[random.randint(0, comps_no - 1)]
            assignment.competencies.add(random_competency)
        # from the list of enrollments, obtain the list of all students enrolled in this course
        for e in enrollments:
            students_in_course.append(e.student)

        #for each student in the course, create a weekly reflection by that student
        for student in students_in_course:
            weekly_reflection = Reflection.objects.get_or_create(student=student, course=course,type='weekly',assignment=assignment,
                                                                 content="Diam sit amet nisl suscipit adipiscing bibendum est ultricies. In pellentesque massa placerat duis ultricies lacus. Cursus mattis molestie a iaculis at erat. Libero enim sed faucibus turpis in eu mi bibendum. Purus in massa tempor nec feugiat nisl pretium fusce id. Sit amet purus gravida quis. Nisl pretium fusce id velit ut tortor. Eu consequat ac felis donec et odio pellentesque. Diam sollicitudin tempor id eu nisl nunc mi ipsum. Faucibus interdum posuere lorem ipsum. Vitae nunc sed velit dignissim sodales ut. Aenean pharetra magna ac placerat vestibulum lectus. Dictum non consectetur a erat nam at lectus urna. Nunc sed velit dignissim sodales. Eget nunc lobortis mattis aliquam faucibus purus in massa tempor. Fames ac turpis egestas integer eget aliquet nibh. Sit amet massa vitae tortor. Potenti nullam ac tortor vitae. Odio aenean sed adipiscing diam. In cursus turpis massa tincidunt dui ut ornare.")[0]
            # print info to show to the user while they are waiting for pop script to complete:
            print("created assignment: "+assignment.__str__())
            # for each weekly reflection associated with that assignment, associate some competencies with them
            for i in range(1,4):
                random_competency = competencies_list[random.randint(0,comps_no-1)]
                weekly_reflection.competencies.add(random_competency)
                # also create a PersonalCompetency object to track the student's progress with the competencies targeted by the assignment
                personal_competency = PersonalCompetency.objects.get_or_create(student=student, progress='1', competency=random_competency)[0]
                personal_competency.assignments.add(assignment)
            # for each assignment, create a submission
            submission = Submission.objects.get_or_create(student=student, assignment=assignment, course=course)[0]
            submission.file.name='codesubmission.txt'
            submission.save()
            print(submission)



    print('Printing created academics' + '\n')
    for a in Academic.objects.all():
        print(a.__str__() + '\n')

    print('Printing created courses' + '\n')
    for c in Course.objects.all():
        print(c.__str__() + '\n')


if __name__ == '__main__':
    print('Starting academic, course and course targets population script:' + '\n')
    populate()
