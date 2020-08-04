
from flask import Blueprint
from flask import render_template,url_for,flash,redirect,request,current_app
from flask_login import current_user,login_required

from jobplus.forms import CompanyProfileForm
from jobplus.models import db,Company

company = Blueprint('company', __name__, url_prefix='/company')

@company.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    form = CompanyProfileForm(obj=current_user)
    if form.validate_on_submit():
        form.update_profile(current_user)
        flash('企业信息更新成功','success')
        return redirect(url_for('front.index'))
    return render_template('company/profile.html',form=form)


@company.route('/')
def index():
    page  = request.args.get('page', default=1, type=int)
    pagination = Company.query.paginate(
            page=page,
            per_page=current_app.config['INDEX_PER_PAGE'],
            error_out=False
            )
    return render_template('company/index.html', pagination=pagination)

@company.route('/myprofile/<int:company_id>')
@login_required
def myprofile(company_id):
    company = Company.query.get(company_id)
    return render_template('company/myprofile.html',company=company)

@company.route('/<int:company_id>')
def detail(company_id):
    company = Company.query.get_or_404(company_id)
    return render_template('company/detail.html',company=company)



