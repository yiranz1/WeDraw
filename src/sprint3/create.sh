rm db.sqlite3
rm -r wedraw/migrations
python manage.py makemigrations wedraw
python manage.py makemigrations
python manage.py migrate wedraw
python manage.py migrate
python manage.py dbshell < words.sql 
