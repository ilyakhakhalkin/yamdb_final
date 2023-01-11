FROM python:3.7-slim

WORKDIR /app

COPY . .

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip3 install psycopg2

RUN pip3 install -r api_yamdb/requirements.txt --no-cache-dir

CMD ["gunicorn", "api_yamdb/api_yamdb.wsgi:application", "--bind", "0:8000" ] 