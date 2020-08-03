from flask import Blueprint, render_template
from flask import url_for,redirect,request, current_app
from flask import flash
from flask_login import login_required, login_user, logout_user

from jobplus.models import Job,User,Company
from jobplus.forms import LoginForm,RegisterForm

front = Blueprint('front', __name__)

@front.route('/')
def index():
    jobs = Job.query.order_by(Job.created_at.desc()).limit(3)
    companies = Company.query.order_by(Company.created_at.desc()).limit(3)
    return render_template('index.html',jobs=jobs,companies=companies)
'''
@front.route('/')
def jobs():
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.paginate(
        page=page,
        per_page=current_app.config['INDEX_PER_PAGE'],
        error_out=False
    )
    return render_template('jobs.html', pagination=pagination)


@front.route('/<int:job_id>')
def jobs(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('jobs.html', job=job)
'''
@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.name.data).first()
        if not user:
            user=User.query.filter_by(username=form.name.data).first()
        login_user(user, form.remember_me.data)
        flash('you have logged in', 'success')
        
        if user.is_company:
            return redirect(url_for('company.profile'))
        elif user.is_admin:
            return redirect(url_for('.index'))
        else:
            return redirect(url_for('user.profile'))
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
