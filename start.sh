echo Starting Gunicorn.
exec gunicorn --reload app:app --bind 0.0.0.0:80
