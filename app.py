from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

# models
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)

    @property
    def time_left(self):
        if self.deadline:
            delta = self.deadline - datetime.utcnow()
            if delta.days > 0:
                return f"{delta.days} days left"
            return "Due today or overdue"
        return "No deadline"

    def __repr__(self):
        return '<Task %r>' % self.id

# Create the database within the app context
with app.app_context():
    db.create_all()

# routes
@app.route('/', methods=['POST', 'GET'])
def dashboard():
    return render_template('index.html')

@app.route('/tasks', methods=['POST', 'GET'])
def addTask():
    if request.method == 'POST':
        task_content = request.form.get('content')
        task_description = request.form.get('description')
        task_deadline = request.form.get('deadline')
        new_task = Todo(
            content = task_content,
            description = task_description,
            deadline = task_deadline
        )

        try:
            

    return render_template('tasks.html')

@app.route('/calendar')
def calender():
    return render_template('calendar.html')

if __name__ == '__main__':
    app.run(debug=True)