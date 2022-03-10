run:
    python manage.py runserver

mail_debug:
    python -m smtpd -n -c DebuggingServer localhost:1025