from flask import redirect , render_template, request, session, flash, url_for, Blueprint
from .forms import LoginForm, RegisterForm
from project import engine, Base
from project.models import Users
from sqlalchemy.orm import scoped_session,sessionmaker
from functools import wraps


users_blueprint = Blueprint("users", __name__)

def dbSession():
    Base.metadata.bind = engine
    DBSession = scoped_session(sessionmaker(bind=engine))
    return DBSession

def login_required(endpoint):
    @wraps(endpoint)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return endpoint(*args, **kwargs)
        else:
            flash('Necessário o login!!!')
            return(redirect(url_for('users.login')))
    return wrap


@users_blueprint.route('/', methods=['GET','POST'])
def login():
    error = None
    form = LoginForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            db_session = dbSession()
            user = db_session.query(Users).filter_by(name=request.form['name']).first()
            print(user)
            if user is not None and user.password == request.form['password']:
                session['logged_in'] = True
                session['user_id'] = user.id
                session['role'] = user.role
                session['name'] = user.name
                flash('Bem vindo ao Painel de Cursos!!!')
                return redirect(url_for('courses.courses'))
            else:
                error = "Usuário ou senha errada!!!"

    return render_template('login.html', form=form, error=error)


@users_blueprint.route('/logout',methods=['GET'])
@login_required
def logout():
    session.pop('logged_in',None)
    session.pop('user_id',None)
    session.pop('role',None)
    session.pop('name',None)
    return redirect(url_for('users.login'))
    
@users_blueprint.route("/register", methods=['GET','POST'])
def register():
    error = None
    form = RegisterForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            print(request.form['name'])
            print(request.form['email'])
            print(request.form['password'])
            print(request.form['confirm'])
            return redirect(url_for('users.login'))

    return render_template('register.html', form=form, error=error)
