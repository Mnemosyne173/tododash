from flask import Flask, render_template, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_super_secret_key_here' # required for flashing?
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
    search_query = request.args.get('search')
    if search_query:
        # Filter tasks where the content contains the search string
        tasks = Todo.query.filter(Todo.content.ilike(f'%{search_query}%')).order_by(Todo.date_created).all()
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template('index.html', tasks=tasks)

@app.route('/calendar')
def calender():
    return render_template('calendar.html')

@app.route('/tasks', methods=['POST', 'GET'])
def addTask():
    if request.method == 'POST':
        task_content = request.form.get('content')
        task_description = request.form.get('description')
        deadline_str = request.form.get('deadline')
        # converting deadline string to a python object
        task_deadline = None
        if deadline_str:
            task_deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
        
        new_task = Todo(
            content = task_content,
            description = task_description,
            deadline = task_deadline
        )
        # saving task
        try:
            db.session.add(new_task)
            db.session.commit()
            flash("Task added successfully")
            return redirect('/') 
        except Exception as e:
            print(f"Error: {e}")
            return "There was an issue adding your task."
    return render_template('tasks.html')

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    
    # Update fields from the form data
    task.content = request.form.get('name')
    task.description = request.form.get('description')
    
    deadline_str = request.form.get('deadline')
    if deadline_str:
        task.deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
    else:
        task.deadline = None

    try:
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print(f"Update error: {e}")
        return "Could not update task."

if __name__ == '__main__':
    app.run(debug=True)