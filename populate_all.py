import populate_academics_courses_assignments_submissions_reflections_persCompetencies,populate_mentors,populate_students,populate_with_competencies
# a script that collects together and runs all other population scripts

# the order in which these smaller scripts are run is important, because of Model dependencies
populate_with_competencies.populate()       # add the default competencies
populate_mentors.populate()                 # create a bunch of companies and then some mentors working for each
populate_students.populate()                # create students (and corresponding users); associate them with mentors

# next, create users; associate them with academics; associate academics with courses; create course targets; enroll
# students in courses, create an assignment for each course and associate it with each student taking it, further
# create a submission for that assignment, and reflections & personal competencies associated with the assignment
# a personal competency is an object that refers to one of the competencies defined in the DB and tracks a certain
# student's progress towards achieving that competency

populate_academics_courses_assignments_submissions_reflections_persCompetencies.populate()
