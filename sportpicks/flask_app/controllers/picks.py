from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.pick import Pick
from flask_app.models.user import User

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'id': session['user_id']
    }
    thisUser = User.get_by_id(data)
    thisPick = Pick.allPicks()
    return render_template("dashboard.html",user=thisUser,pick=thisPick)

@app.route('/new',methods=['POST'])
def new():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Pick.validate_pick(request.form):
        return redirect('/new/picks')
    data = {
        "name": request.form["name"],
        "number": request.form["number"],
        "bet": request.form["bet"],
        "record": request.form["record"],
        "date": request.form["date"],
        "user_id": session["user_id"]
    }
    Pick.save(data)
    return redirect('/dashboard')

@app.route("/new/picks")
def new_pick():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    thisUser = User.get_by_id(data)
    return render_template('new_pick.html',user=thisUser)

@app.route('/update/<int:id>',methods=['POST'])
def update_pick(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Pick.validate_pick(request.form):
        return redirect('/edit/{}'.format(id))    
    data = {
        "name": request.form["name"],
        "number": request.form["number"],
        "bet": request.form["bet"],
        "record": request.form["record"],
        "date": request.form["date"],
        "id": id
    }
    Pick.update(data)
    return redirect('/dashboard')

@app.route('/edit/<int:id>')
def edit_pick(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data= {
        "id": id
    }
    user_id = {
        "id": session['user_id']
    }
    thisUser = User.get_by_id(user_id)
    thisPick = Pick.get_by_id(data)
    return render_template("edit_pick.html",user=thisUser, pick=thisPick)

@app.route('/pick/<int:id>')
def view_pick(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_id = {
        "id": session['user_id']
    }
    thisUser = User.get_by_id(user_id)
    theUsers = User.get_all()
    thisPick = Pick.get_by_id(data)
    return render_template("view.html",user=thisUser, users=theUsers, pick=thisPick)

@app.route('/destroy/<int:id>')
def destroy_pick(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Pick.destroy(data)
    return redirect('/dashboard')
