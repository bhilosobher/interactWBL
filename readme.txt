
_______________________________________________
SETUP - STARTING THE DJANGO DEVELOPMENT SERVER
-----------------------------------------------

The project has not been deployed, because implementation had to be ended abruptly.

The project has been developed with PyCharm, using PyCharm's integrated virtualenv virtual environment tool.

Both <.idea> directory and the <vir> directories have been left in the project folder, in case the marker can open the project in PyCharm.

To check out the project, in Pycharm:
- import project
- CTRL + ALT + R to open Django console. In the console:
- makemigrations interactWBL
- migrate
Then, in the terminal, run the main population script which is in the parent project directory: python populate_all.py
Then, back in the Django console:
- createsuperuser (follow the instructions to create admin account)
- runserver


If no Pycharm, there is a requirements.txt file which can be used to create a virtual environment with all the project's dependencies. Alternatively,
just make sure you have virtual env installed then navigate in the scritps subfolder of the vir folder in the project root, and run the <activate> script.

Then run the same commands as above, except from the terminal using the manage.py utility from the project root...
- python manage.py makimigrations InteractWBL
- python manage.py migrate
- python populate_all
- python manage.py createsuperuser
...
- python manage.py runserver

_______________________________________
TESTING THE APP
--------------------------------------


Once the server is up and running, the DB populated and the admin setup, you can go to the main page and create different types of accounts.
However, these won't have any data associated with them, so to see more functionality you should use accounts which were just created by the pop script

Academic:
username: shona pw: securepassword
Mentor
username: andrea pw: securepassword
Student:
username: check the DB for a populated username (use your admin login details at  /admin/), as these are all created dynamically password: securepassword

Then, use these accounts (and manually created ones, if you wish) to explore the implemented functionality.
  
  *******
!!WARNING!!: do not use the admin account to log in to the app and explore it - it won't work because the admin won't have any academic/student/mentor
profile associated with it! The pages are generated dynamically based on profile type. Use a student/mentor/academic account instead.

  *******