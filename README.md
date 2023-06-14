# -milestone-project-four

Django administration
Username: mikehdolding
Password: MichaelNivelle

Username: superadmin
Password: MichaelNivelle

Terminal command update
Since this video was created Django have introduced a new version that will be automatically installed if you use the command in the video.

To ensure that you get the same version of django used in this video and so that nothing breaks as you do the walkthrough, instead of the command pip3 install django, please use this:

pip3 install 'django<4'

Django 3.2 is the LTS (Long Term Support) version of Django and is therefore preferable to use over the newest Django 4

Viewing your new Django App
At the end of the video, Chris runs the app. Depending on the computer you are running on, you may have to allow a host for the app.

To ensure you get all the files you need, please use the command pip3 install django-allauth==0.41.0 when installing django-allauth, instead of the command in the video (pip3 install django-allauth)

Please ensure os is imported into settings.py
The newest version of Django does not automatically import the os module at the top of the settings.py file as it does for the instructor in this video.

Please check if this line of code is at the top of your settings.py file, it is not, please add it yourself:

import os

https://fontawesome.com/docs/web/use-with/python-django


python3 manage.py runserver


items.Item.image: (fields.E210) Cannot use ImageField because Pillow is not installed.
        HINT: Get Pillow at https://pypi.org/project/Pillow/ or run command "python -m pip install Pillow".
pip3 install pillow

python3 manage.py makemigrations --dry-run
python3 manage.py makemigrations
python3 manage.py migrate --plan
python3 manage.py migrate
python3 manage.py shell


You can pass 'zero' to unapply migrations for an app.
all migrations: python3 manage.py migrate example_app zero 
specific migration: python3 manage.py migrate socialaccount 0004