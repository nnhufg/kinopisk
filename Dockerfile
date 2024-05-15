# Создаем кастомный image для Django.
# Кастомный, так как нам надо перекинуть локальные файлы в образ.
# Для PostgreSQL мы возьмем готовый образ и соберем его сразу в docker-compose.yml.
# Docker-compose.yml файл, при помощи которого мы объединяем images и создаем полный сервис для Docker.

# копируем готовый образ python из dockerhub
FROM python:3.10.0-alpine

# устанавливаем зависимости для проекта
RUN apk add postgresql-client build-base postgresql-dev linux-headers pcre-dev

# устанавливаем рабочую директорию внутри docker контейнера
WORKDIR /movies_admin

# копируем файлы зависимостей и проекта Django в образ
COPY requirements.txt .

# устанавливаем зависимости для проекта, не кешируя их
RUN pip install -r requirements.txt --no-cache-dir

# устанавливаем порт, на котором будет работать Docker
EXPOSE 8000

# в рабочую директорию копируем папку с Django вне контейнера
COPY movies_admin .

# cобираем статику для Django
RUN python3 manage.py collectstatic --no-input

# запускаем через uwsgi
CMD [ "uwsgi", "--ini", "/movies_admin/uwsgi.ini" ]

