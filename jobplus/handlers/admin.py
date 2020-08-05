from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash
from jobplus.decorators import admin_required, company_required
from jobplus.models import User, db, Job, Dilivery
from jobplus.forms import AdminEditUserForm, AdminCreateUserForm, AdminEditJobForm

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')

@admin.route('/company_admin')
@company_required
def com_index():
    return render_template('admin/com_index.html')

'''
@admin.route('/courses')
@admin_required
def courses():
    page = request.args.get('page', default=1, type=int)
    pagination = Course.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/courses.html', pagination=pagination)
'''

@admin.route('/users')
@admin_required
def users():
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/users.html', pagination=pagination)

@admin.route('/jobs')
@admin_required
def jobs():
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/jobs.html', pagination=pagination)


@admin.route('/com_jobs')
@company_required
def com_jobs():
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/com_jobs.html', pagination=pagination)

@admin.route('/jobs/create', methods=['GET', 'POST'])
@company_required
def create_job():
    form = AdminEditJobForm()
    if form.validate_on_submit():
        form.create_job()
        flash('职位创建成功', 'success')
        return redirect(url_for('admin.com_jobs'))
    return render_template('admin/create_jobs.html', form=form)

@admin.route('/users/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    form = AdminCreateUserForm()
    if form.validate_on_submit():
        form.create_user()
        flash('user创建成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/create_users.html', form=form)

@admin.route('/jobs/<int:job_id>/edit', methods=['GET', 'POST'])
@company_required
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    form = AdminEditJobForm(obj=job)
    if form.validate_on_submit():
        form.update_job(job)
        flash('职位更新成功', 'success')
        return redirect(url_for('admin.com_jobs'))
    return render_template('admin/edit_jobs.html', form=form, job=job)

@admin.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = AdminEditUserForm(user=user, obj=user)
    if form.validate_on_submit():
        form.update_user(user)
        flash('user更新成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/edit_user.html', form=form, user=user)

@admin.route('/jobs/<int:job_id>/delete')
@company_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash('成功删除职位', 'success')
    return redirect(url_for('admin.com_jobs'))

@admin.route('/users/<int:user_id>/disable_user', methods=['GET', 'POST'])
@admin_required
def disable_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_disable:
        user.is_disable = False
        flash('用户启用成功', 'success')
    else:
        user.is_disable = True
        flash('用户禁用成功', 'success')
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('admin.users'))

@admin.route('/jobs/<int:job_id>/open_job', methods=['GET', 'POST'])
@admin_required
def open_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.is_open:
        job.is_open = 0
        flash('工作下线成功', 'success')
    else:
        job.is_open = 1
        flash('工作上线成功', 'success')
    db.session.add(job)
    db.session.commit()
    return redirect(url_for('admin.jobs'))


@admin.route('/com_dilivery')
@company_required
def com_dilivery():
    page = request.args.get('page', default=1, type=int)
    pagination = Dilivery.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/com_dilivery.html', pagination=pagination)



@admin.route('/com_diliveryr')
@company_required
def com_diliveryr():
    page = request.args.get('page', default=1, type=int)
    pagination = Dilivery.query.filter(Dilivery.status == 2).paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/com_dilivery.html', pagination=pagination)


@admin.route('/com_dilivery/<int:dilivery_id>/dilivery_interview', methods=['GET', 'POST'])
@company_required
def dilivery_interview(dilivery_id):
    dilivery = Dilivery.query.get_or_404(dilivery_id)
    dilivery.status = dilivery.STATUS_ACCEPT
    db.session.add(dilivery)
    db.session.commit()
    return redirect(url_for('admin.com_dilivery'))

@admin.route('/com_dilivery/<int:dilivery_id>/dilivery_reject', methods=['GET', 'POST'])
@company_required
def dilivery_reject(dilivery_id):
    dilivery = Dilivery.query.get_or_404(dilivery_id)
    dilivery.status = dilivery.STATUS_REJECT
    db.session.add(dilivery)
    db.session.commit()
    return redirect(url_for('admin.com_dilivery'))
