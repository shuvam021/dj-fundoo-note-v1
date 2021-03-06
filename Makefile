run:
	python manage.py runserver

migrate:
	python manage.py makemigrations
	python manage.py migrate

mail_debug:
	python -m smtpd -n -c DebuggingServer localhost:1025

test:
	python .\manage.py test

# celery -A config worker -l info
worker:
	celery -A config worker -l info --pool=solo
