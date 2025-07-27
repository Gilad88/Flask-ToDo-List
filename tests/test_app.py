import pytest
from app import create_app, db, Task

# זהו fixture של pytest שיגדיר את האפליקציה לבדיקות
@pytest.fixture
def client():
    # העבר את ה-URI של SQLite בזיכרון ישירות ל-create_app
    app = create_app(database_uri='sqlite:///:memory:')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # כדי למנוע אזהרות מיותרות

    # הקונטקסט של האפליקציה מאפשר גישה ל-request/session וכו'
    with app.test_client() as client:
        with app.app_context():
            db.create_all() # יצירת טבלאות ב-DB הזמני
        yield client # הפעלת הבדיקות
        with app.app_context():
            db.drop_all() # ניקוי ה-DB לאחר הבדיקה

# -------------------- בדיקות לדפים ופעולות בסיסיות --------------------

def test_index_page(client):
    """בדיקה שהדף הראשי נטען בהצלחה ומכיל את הכותרת."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Todo List" in response.data # וודא שהכותרת "Todo List" קיימת בדף

def test_create_todo(client):
    """בדיקה של יצירת משימה חדשה."""
    # בדיקה שהמשימה נוספה בהצלחה
    response = client.post('/add', data={'content': 'Test Todo Item'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Test Todo Item" in response.data

    # וודא שהמשימה קיימת בבסיס הנתונים באמצעות הקונטקסט של האפליקציה
    with client.application.app_context():
        todo_item = Task.query.filter_by(content='Test Todo Item').first()
        assert todo_item is not None
        assert todo_item.content == 'Test Todo Item'
        assert todo_item.done == False # משימה חדשה היא לא מבוצעת כברירת מחדל

def test_update_todo_status(client):
    """בדיקה של עדכון סטטוס משימה (מבוצע / לא מבוצע)."""
    with client.application.app_context():
        # הוסף משימה ראשונית לבדיקה
        new_task = Task(content='Status Change Test', done=False)
        db.session.add(new_task)
        db.session.commit()
        todo_id = new_task.id

    # בדיקה של סימון משימה כמבוצעת
    response_mark_done = client.post(f'/update/{todo_id}', data={'done': 'true'}, follow_redirects=True)
    assert response_mark_done.status_code == 200

    with client.application.app_context():
        updated_task = db.session.get(Task, todo_id)
        assert updated_task.done == True

    # בדיקה של סימון משימה כלא מבוצעת
    response_mark_undone = client.post(f'/update/{todo_id}', data={'done': 'false'}, follow_redirects=True)
    assert response_mark_undone.status_code == 200

    with client.application.app_context():
        updated_task = db.session.get(Task, todo_id)
        assert updated_task.done == False

def test_edit_todo(client):
    """בדיקה של עריכת תוכן משימה."""
    with client.application.app_context():
        new_task = Task(content='Original Content')
        db.session.add(new_task)
        db.session.commit()
        todo_id = new_task.id

    # וודא שדף העדכון נטען
    response_get = client.get(f'/update/{todo_id}')
    assert response_get.status_code == 200
    assert b"Original Content" in response_get.data

    # ערוך את המשימה
    response_post = client.post(f'/update/{todo_id}', data={'content': 'Edited Content', 'done': 'false'}, follow_redirects=True)
    assert response_post.status_code == 200
    assert b"Edited Content" in response_post.data

    # וודא שהמשימה עודכנה בבסיס הנתונים
    with client.application.app_context():
        edited_task = db.session.get(Task, todo_id)
        assert edited_task.content == 'Edited Content'

def test_delete_todo(client):
    """בדיקה של מחיקת משימה."""
    with client.application.app_context():
        new_task = Task(content='Item to Delete')
        db.session.add(new_task)
        db.session.commit()
        todo_id = new_task.id

    # מחק את המשימה
    response = client.get(f'/delete/{todo_id}', follow_redirects=True)
    assert response.status_code == 200
    assert b"Item to Delete" not in response.data # וודא שהמשימה לא מופיעה יותר בדף

    # וודא שהמשימה נמחקה מבסיס הנתונים
    with client.application.app_context():
        deleted_task = db.session.get(Task, todo_id)
        assert deleted_task is None

def test_mark_all_complete(client):
    """בדיקה של סימון כל המשימות כמבוצעות."""
    with client.application.app_context():
        db.session.add_all([
            Task(content='Todo 1', done=False),
            Task(content='Todo 2', done=False)
        ])
        db.session.commit()

    response = client.get('/mark_all_completed', follow_redirects=True)
    assert response.status_code == 200

    with client.application.app_context():
        all_tasks = Task.query.all()
        for task_item in all_tasks:
            assert task_item.done == True # וודא שכל המשימות סומנו כמבוצעות