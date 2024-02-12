git clone https://github.com/Shanmukhi12/kaizntree-takehome.git
cd kaizntree-takehome
cd TAKEHOME
Configure database settings in settings.py:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
python manage.py migrate
python manage.py runserver
Access the application in your web browser at http://127.0.0.1:8000/
python manage.py test
