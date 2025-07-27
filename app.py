import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return '<Task %r>' % self.id

# פונקציה שיוצרת ומחזירה את מופע האפליקציה
# מקבלת כעת database_uri כארגומנט אופציונלי
def create_app(database_uri=None):
    app = Flask(__name__)

    # אם database_uri סופק, השתמש בו (לבדיקות).
    # אחרת, השתמש במשתנה סביבה או בברירת המחדל של PostgreSQL.
    if database_uri:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@db:5432/todo_db')
        
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app) # **כאן מקשרים את ה-db לאפליקציה**

    # הגדרת מסלולים (Routes) עבור האפליקציה
    @app.route('/')
    def index():
        tasks = Task.query.order_by(Task.date_created).all()
        return render_template('index.html', tasks=tasks)

    @app.route('/add', methods=['POST'])
    def add_task():
        content = request.form['content']
        if not content:
            return 'Task content cannot be empty!', 400
        new_task = Task(content=content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'There was an issue adding your task'

    @app.route('/delete/<int:id>')
    def delete_task(id):
        task_to_delete = db.session.get(Task, id)
        if task_to_delete is None:
            return 'Task not found!', 404
        try:
            db.session.delete(task_to_delete)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'There was a problem deleting that task'

    @app.route('/update/<int:id>', methods=['GET', 'POST'])
    def update_task(id):
        task = db.session.get(Task, id)
        if task is None:
            return 'Task not found!', 404

        if request.method == 'POST':
            if 'content' in request.form:
                task.content = request.form['content']
                task.done = 'done' in request.form
            elif 'done' in request.form:
                task.done = request.form['done'] == 'true'

            try:
                db.session.commit()
                if request.is_json:
                    return '', 204
                return redirect(url_for('index'))
            except Exception as e:
                print(f"Error updating task: {e}")
                return 'There was an issue updating your task', 500
        else:
            return render_template('update.html', task=task)
            
    @app.route('/mark_all_completed')
    def mark_all_completed():
        try:
            Task.query.update(dict(done=True))
            db.session.commit()
        except Exception as e:
            print(f"Error marking all completed: {e}")
            return 'There was an issue marking all tasks as completed', 500
        return redirect(url_for('index'))


    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'Task': Task}
        
    return app

# ***השורה החשובה הזו יוצרת את מופע האפליקציה ש-Gunicorn מחפש באופן גלובלי.***
app = create_app()

# בלוק זה יופעל רק כאשר הקובץ app.py רץ ישירות (לצורך פיתוח מקומי)
if __name__ == '__main__':
    with app.app_context(): # השתמש ב-'app' שכבר נוצר למעלה
        db.create_all() # יצירת טבלאות בסיס הנתונים אם אינן קיימות
    app.run(debug=True, host='0.0.0.0')