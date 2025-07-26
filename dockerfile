FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV FLASK_APP=app/__init__.py 

EXPOSE 5000

CMD ["sh", "-c", "python init_db.py && gunicorn --bind 0.0.0.0:5000 --timeout 120 app:app"]
