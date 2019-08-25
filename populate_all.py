import populate_academics_and_courses,populate_mentors,populate_students,populate_with_competencies
# a script that collects together and runs all other population scripts

# the order in which these smaller scripts are run is important, because of Model dependencies
populate_with_competencies.populate()       # add the default competencies
populate_mentors.populate()                 # create a bunch of companies and then some mentors working for each
populate_students.populate()                # create students (and corresponding users); associate them with mentors
populate_academics_and_courses.populate()   # create users; associate them with academics; associate academics with
                                            # courses; create course targets; enroll students in courses
