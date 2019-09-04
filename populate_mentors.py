import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devproj.settings')

import django, names

django.setup()
from interactWBL.models import Company, User, Mentor


def populate():
    # a list with 10 fictitious company names
    companies=[]
    company_names = ['Morgan', 'JP', 'Macrosoft', 'Poodle', 'SAR', 'Samsong', 'Parclays', 'HRBC', 'BM', 'PristineMedia', ]
    for n in company_names:
        c = Company.objects.get_or_create(name=n)[0]
        companies.append(c)

    # a list of 50 names
    mentor_names = ['James', 'George', 'Dean', 'Arran', 'Claudius', 'John', 'Tom', 'Thomas', 'Charles', 'Paul',
                    'David', 'Dave', 'Chris', 'Derek', 'Sam', 'Jacob', 'Bilbo', 'Gabriel', 'Fred', 'Joe',
                    'Joseph', 'Euan', 'Martin', 'Declan', 'Arthur', 'Daisy', 'Margaret', 'Mary', 'Tina', 'Georgia',
                    'Rachel', 'Chloe', 'Stella', 'Jeanne', 'Jane', 'Immogen', 'Victoria', 'Adele', 'Martha', 'Melissa',
                    'Paula', 'Andrea', 'Ninon', 'Susan', 'Bertha', 'Margery', 'Holy', 'Ruby', 'Olivia', 'Julia', ]
    mentors = []
    i = 0
    while i < 50:
        for c in companies:
            u = User.objects.get_or_create(username=mentor_names[i].lower(), password='securepassword')[0]
            u.set_password('securepassword')
            u.save()
            m = Mentor.objects.get_or_create(company=c, user=u)
            u.first_name=mentor_names[i]
            u.last_name=names.get_last_name()
            u.email=mentor_names[i]+'.'+u.last_name.lower()+'@'+ c.name.lower()+'.com'
            u.save()
            print(u.email+'\n')
            i+=1
            mentors.append(m)


if __name__=='__main__':
    print("Starting mentors population script...")
    populate()