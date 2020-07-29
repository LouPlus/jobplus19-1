from flask import Blueprint, render_template

from jobplus.models import Job,User,Company
from jobplus.forms import LoginForm,RegisterForm

front = Blueprint('front', __name__)


@front.route('/')
def index():
    job = Job.query.all()
    return render_template('index.html',job=job)

@front.route('/user/profile',methods=['GET','POST'])
def user_profile():
    user = User.query.all()
    return render_template('user_profile.html',job=job)


@front.route('/company/profile/<int:company_id>',methods=['GET','POST'])
def company_profile():
    company = Company.query.get_or_404(company_id)
    form = Company_profile_Form(obj=company)
    if form.validate_on_sumbmit():
        form.update_company(company_user)
        flash('创建成功','success')
        return redirect(url_for('.index'))

    return render_template('company_profile.html',form=form,company=company)

@front.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        role = User.query.filter_by(role=form.role.data).first()
        login_user(user,form.remember_me.data)
        flash('您已成功登录,｛｝'.format(user.username), 'success')
        if role==10:
            return redirect(url_for('.user_profile'))
        elif role==20:
            return redirect(url_for('.company_profile'))
        else:
            return redirect(url_for('.index'))

    return render_template('login.html',form=form)

@front.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功','sucess')
        return redirect(url_for('.login'))
    return render_template('register.html',form=form)

