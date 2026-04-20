from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ToDo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToDo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title  = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# @app.route("/", methods = ['GET','POST'])
# def add():
    
#     if request.method == "POST":
#         title = request.form['title']
#         desc = request.form['desc']
#         if title and desc:
#             todo = ToDo(title = title, desc = desc)
#             db.session.add(todo)
#             db.session.commit()
#         return redirect('/')
#     AllToDo = ToDo.query.all()
#     return render_template('index.html', AllToDo = AllToDo)
from sqlalchemy import or_

@app.route("/", methods=['GET', 'POST'])
def add():

    # 🔴 Handle form submission (POST)
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']

        if title and desc:
            todo = ToDo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()

        return redirect('/')

    # 🟢 Handle search (GET)
    query = request.args.get('query')

    if query:
        AllToDo = ToDo.query.filter(
            or_(
                ToDo.title.ilike(f"%{query}%"),
                ToDo.desc.ilike(f"%{query}%")
            )
        ).all()
    else:
        AllToDo = ToDo.query.all()

    return render_template('index.html', AllToDo=AllToDo)


@app.route("/show")
def show():
    AllToDo = ToDo.query.all()
    print(AllToDo)
    return "This is the show page"

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    todo = ToDo.query.filter_by(sno=sno).first()

    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']

        if title and desc:
            todo.title = title
            todo.desc = desc
            db.session.commit()

        return redirect('/')   # 🔥 important

    return render_template('update.html', ToDo=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    item = ToDo.query.filter_by(sno = sno).first()
    db.session.delete(item)
    db.session.commit()
    return redirect('/')


@app.route('/About')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True, port=8000)
