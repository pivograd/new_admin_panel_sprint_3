FROM python:3.10

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE 'example.settings'

COPY requirements.txt requirements.txt
COPY example/wsgi.py wsgi.py

RUN  mkdir -p /var/www/static/ \
     && mkdir -p /var/www/media/ \
     && mkdir -p /opt/app/static/ \
     && mkdir -p /opt/app/media/ \
     && pip install --upgrade pip \
     && pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput --clear

#CMD python manage.py runserver 0.0.0.0:8000
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "example.wsgi:application"]
