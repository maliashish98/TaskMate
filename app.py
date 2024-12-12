#imports
from flask import Flask, render_template, redirect , request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column 

from datetime import datetime



# my app
app = Flask(__name__)

#import Base class for setup database and define object
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

#setup database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///TaskMate_database.db"
db.init_app(app)

#setup/create model or row
class Todo(db.Model):
    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    content:Mapped[str] = mapped_column(String(50),nullable=False)
    complete:Mapped[int] = mapped_column(Integer,default=0)
    created:Mapped[datetime] = mapped_column(default=datetime.utcnow)
     

# main page index
@app.route("/",methods=['GET','POST'])
def index():
    # add Task
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"Error:{e}"
    # show Tasks    
    else:
        tasks = Todo.query.order_by(Todo.created).all()
        return render_template('index.html',tasks=tasks)

#delete task
@app.route('/delete/<int:id>')
def del_task(id):
    delete_task = Todo.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"Error : {e}"
    
#update task
@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit_task(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Error : {e}"
    else:
        return render_template('update.html',task=task)

#Runner and debugger
if __name__ == "__main__":  
    #create table
    with app.app_context():
        db.create_all()

    app.run(debug=True)
