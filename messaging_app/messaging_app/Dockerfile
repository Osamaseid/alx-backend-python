FROM python:3.10

RUN mkdir -p /app

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "messaging_app.wsgi:application", "--bind", "0.0.0.0:8000"]