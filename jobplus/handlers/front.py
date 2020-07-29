from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from jobplus.models import User, Job
from jobplus.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required

front = Blueprint('front', __name__)


@front.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.paginate(
        page=page,
        per_page=current_app.config['INDEX_PER_PAGE'],
        error_out=False
    )
    return render_template('index.html', pagination=pagination)



@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, form.remember_me.data)
        flash('you have logged in', 'success')
        return redirect(url_for('.index'))
    return render_template('login.html', form=form)

@front.route('/admin/users')
def adminlogin():
    return render_template('admin/users.html')

@front.route('/user_register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user(User())
        flash('用户注册成功，请登录！', 'success')
        return redirect(url_for('.login'))
    return render_template('register.html', form=form)

'''
实现企业注册的方法二，不推荐
@front.route('/company_register', methods=['GET', 'POST'])
def company_register():
    form = RegisterForm()
    form.username.label = u'企业名称'
    if form.validate_on_submit():
        form.create_company_user(User())
        flash('企业注册成功，请登录！', 'success')
        return redirect(url_for('.login'))
    return render_template('company_register.html', form=form)
'''

@front.route('/company_register', methods=['GET', 'POST'])
def company_register():
    form = RegisterForm()
    form.username.label = u'企业名称'
    if form.validate_on_submit():
        form.create_user(User(role=User.ROLE_COMPANY))
        flash('企业注册成功，请登录！', 'success')
        return redirect(url_for('.login'))
    return render_template('company_register.html', form=form)

@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经退出登录', 'success')
    return redirect(url_for('.index'))

