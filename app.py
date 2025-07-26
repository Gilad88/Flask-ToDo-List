# app.py
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow) 

    def __repr__(self):
        return '<Task %r>' % self.id

# הגדרת מסלולים (Routes) עבור האפליקציה
@app.route('/')
def index():
    tasks = Task.query.order_by(Task.date_created).all() # אם יש לך שדה date_created
    # אם אין לך שדה date_created, שנה לשורה הבאה:
    # tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    content = request.form['content']
    if not content:
        return 'Task content cannot be empty!'
    new_task = Task(content=content)
    try:
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return 'There was an issue adding your task'

@app.route('/delete/<int:id>')
def delete_task(id):
    task_to_delete = Task.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    task = db.session.get(Task, id) # השתמש ב-db.session.get במקום query.get_or_404
    if task is None:
        return 'Task not found!', 404

    if request.method == 'POST':
        # אם יש 'content' ב-form, זה עדכון מטופס העריכה
        if 'content' in request.form:
            task.content = request.form['content']
            task.done = 'done' in request.form # checkbox value from modal form
        # אם אין 'content' אבל יש רק 'done' (או ריק), זה עדכון מתיבת הסימון
        elif 'done' in request.form:
             task.done = request.form['done'] == 'true' # From AJAX, send 'true' or 'false'

        try:
            db.session.commit()
            if request.is_json: # If it's an AJAX request (though we send form data, a simple return can work)
                return '', 204 # No Content, success
            return redirect(url_for('index'))
        except Exception as e:
            print(f"Error updating task: {e}") # לוג השגיאה
            return 'There was an issue updating your task', 500
    else: # GET request, for the dedicated update page (if you still use it)
        # Note: If you're only using the modal for editing, this GET route might become obsolete.
        # But it's fine to keep it.
        return render_template('update.html', task=task)
    
@app.route('/mark_all_completed') # שיניתי את השם למה שהגדרנו קודם
def mark_all_completed():
    try:
        Task.query.update(dict(done=True))
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error marking all completed: {e}")
        return 'There was an issue marking all tasks as completed', 500

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Task': Task} 
