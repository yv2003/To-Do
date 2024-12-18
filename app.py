#api = https://api.jikan.moe/v4

from flask import Flask,url_for,request,render_template,redirect
# from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone
# from db import db
app = Flask(__name__)#instance of flask class
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)
# db.init_app(app)


class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(200),nullable=False)
    date_created = db.Column(db.DateTime,default = datetime.now(timezone.utc))
    
    def __repr__(self):
        return '<Task %r>' % self.id
    
with app.app_context():
    db.create_all()  # This will create the necessary database tables
    print("Database tables created!")

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        task_content = request.form['content']
        new_task=Todo(content= task_content)
        
        try: 
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'couldnt delete task'

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task_to_update=Todo.query.get_or_404(id)
    if request.method=='POST':
        task_to_update.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'couldnt update task'
    else:
        return render_template('update.html',task=task_to_update)


if __name__ == '__main__':
    app.run(debug=True)
