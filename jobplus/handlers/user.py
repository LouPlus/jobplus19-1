
from flask import Blueprint
from flask import render_template,url_for,flash,redirect,request
from flask_login import current_user,login_required

from jobplus.forms import UserProfileForm
from jobplus.models import User

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    form = UserProfileForm(current_user, obj=current_user)
    if form.validate_on_submit():
        #if not form.password.data:
        #    current_user.password = form.user.password
        form.update_profile(current_user)
        #db.session.add(current_user)
        #db.session.commit()
        flash('个人信息更新成功','success')
        return redirect(url_for('front.index'))
    return render_template('user/profile.html',form=form)

@user.route('/myprofile/<int:user_id>')
@login_required
def myprofile(user_id):
    user = User.query.get(user_id)
    return render_template('user/myprofile.html',user=user)
