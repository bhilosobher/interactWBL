import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devproj.settings')

import django

django.setup()
from interactWBL.models import Competency


def populate():
    # technical skills
    analytical_technical_capability = ('Project management', 'Requirements analysis', 'Software design', 'Programming',
                                       'Validation and verification tests', 'Configuration management', 'Quality',
                                       'Tests', 'Documentation', 'Maintenance',)
    use_of_technology = ("Evaluation and selection of tools to support problem areas",
                         "Adaptation and use of tools to support problem areas",)

    # social skills
    interpersonal = ('Communication', 'Adaptability', 'Aptitude to relate', 'Sociability',
                     'Interpersonal sensibility',)
    cooperation = ('Understanding of the dynamics of debates and the follow-up of an agenda', 'Desire to contribute',
                   'Leadership', 'Motivation', 'Decision making to allow different opinions',
                   'The skill of presenting ideas and listening to the ideas of others', 'Orientation to achievement',)
    conflict_handling = ('Effective handling of the emotions', 'Aptitude to listen to others',
                         'Resolution of conflicts',
                         'Negotiating skills', 'Judgement, common sense and realism', 'Empathy',)

    # personal skills
    development_in_job = ('Capability to learn alone', 'Capability to search information', 'Capability to take risks',
                          'Flexibility', 'Verbal reasoning', 'Stress resistance', 'Pro-activeness', 'Responsibility',)

    personal_development = ('Identify areas of personal opportunity', 'Define a project and establish a personal goal',
                            'Determine priorities and refine the goals',
                            'Identify and evaluate available and required resources',
                            'Balance necessary resources to satisfy multiple goals',
                            'Monitor the progress, to make adjustments during the project development',
                            'Learn from past actions to project future results', 'High self-esteem',
                            'Entrepreneurial skill',
                            'Commitment', 'Self-control', 'Optimism',)

    rights_limits = ('Ability to understand own interest and needs',
                     'Know the rules and written principles to identify limits',
                     'Ability to argue for own rights', 'Ability to suggest arrangements or alternative solutions',)

    technicals = {analytical_technical_capability: 'Possess analytical and learning capability in this technical area',
                  use_of_technology: 'Masters the use of technology thus', }

    socials = {interpersonal: 'Ability in handling interpersonal relations',
               cooperation: 'Cooperates and works well in a team',
               conflict_handling: 'Has the ability to handle and solve conflicts by exhibiting this competency', }

    personals = {
        development_in_job: 'The student possesses the ability to adapt and excel in the work environment through this competency',
        personal_development: 'The students has this competency, which enables them to develop and grow',
        rights_limits: 'The student is aware of their rights and limits in any given context and adapts to these'}

    competencies = {'technical': technicals ,'social': socials, 'personal':personals}

    add_competency(competencies)
    for c in Competency.objects.all():
        print(c.__str__() + "\n")


def add_competency(competencies):
    for competency_type, competency_list in competencies.items():
        for competency_group, competency_description in competency_list.items():
            for competency_name in competency_group:
                c = Competency.objects.get_or_create(name=competency_name, description=competency_description,
                                                     type=competency_type)[0]


#start execution here

if __name__ == '__main__':
    print("Starting competencies population script...")
    populate()