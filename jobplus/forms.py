from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, Email, EqualTo, DataRequired
from wtforms import ValidationError
from .models import User,Company

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(3,15)])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_password(self,field):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')


class User_profile_Form(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(3,15)])
    password = PasswordField('密码(不填写保持不变)', validators=[DataRequired(), Length(6, 24)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    upload_resume = StringField('上传简历', validators=[DataRequired(), Length(1,50)])
    submit = SubmitField('提交')
    '''
    def validate_email(self,field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已存在')
    '''


class Company_profile_Form(FlaskForm):
    username = StringField('企业名称', validators=[DataRequired(), Length(3,15)])
    password = PasswordField('密码(不填写保持不变)', validators=[DataRequired(), Length(6, 24)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
#    location＝StringField('地址', validators=[DataRequired(), Length(3,128)])
#    web＝StringField('网址', validators=[DataRequired(), Length(3,128)])
 #   logo＝StringField('logo', validators=[DataRequired(), Length(1，128)])
  #  description＝StringField('一句话描述', validators=[DataRequired(), Length(1，50)])
  #  team_introduction = StringField('团队介绍', validators=[DataRequired(), Length(1，256)])
    submit = SubmitField('提交')
    '''
    def validate_email(self,field):
        email = User.query.filter_by(email=field.data).first()
        raise ValidationError('邮箱已存在')
    '''


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(3, 32)])
    email = StringField('邮箱', validators=[DataRequired(), Length(7,256)])
    password = PasswordField('密码', validators=[DataRequired(), Length(3, 18)])
    submit = SubmitField('提交')
    '''
    def __init__(self, user, **kw):
        super().__init__(**kw)
        self.user = user 
    '''
    def validate_username(self, field):
        if self.user.username != field.data and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')

    def validate_email(self,field):
         email = User.query.filter_by(email=field.data).first()
         raise ValidationError('邮箱已存在')

    def create_user(self):
        user = User()
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user
    '''
    def update_user(self, user):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user
    '''
