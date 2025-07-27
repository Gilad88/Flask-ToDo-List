FROM python:3.11-slim-bullseye

# התקן כלי עזר של PostgreSQL (כולל pg_isready)
RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client && rm -rf /var/lib/apt/lists/*

# הגדר את תיקיית העבודה בתוך הקונטיינר
WORKDIR /app

# העתק את קובץ הדרישות והתקן אותן
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# חשוף את הפורט שהאפליקציה מאזינה לו
EXPOSE 5000

# הגדר משתני סביבה עבור Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# הגדר את ה-entrypoint של הקונטיינר לסקריפט שיצרנו
ENTRYPOINT ["entrypoint.sh"]

# זהו ה-CMD שיועבר כארגומנט לסקריפט ה-entrypoint
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
