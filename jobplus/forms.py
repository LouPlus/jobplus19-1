from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, Email, EqualTo, DataRequired,Required,URL
from wtforms import ValidationError

from .models import User,Company,db


class LoginForm(FlaskForm):
    name = StringField('邮箱/用户名',validators=[Required()])
#    username = StringField('邮箱/用户名', validators=[Required(), Length(3, 24)])
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交') 

    def validate_name(self, field):
        u1 = User.query.filter_by(email=field.data).first()
        u2 = User.query.filter_by(username=field.data).first()
        if not u1 and  not u2:
            raise ValidationError('邮箱或用户名未注册')

    def validate_password(self, field):
        user = User.query.filter_by(username=field.data).first()
        if not user:
            user = User.query.filter_by(email=field.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(3, 32)])
    email = StringField('邮箱', validators=[DataRequired(), Length(7,256)])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 18)])
    repeat_password = PasswordField('chongfumifa',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('提交')
    '''
    def __init__(self, user, **kw):
        super().__init__(**kw)
        self.user = user 
    '''
    def validate_username(self, field):
#        user = User.query.filter_by(username=self.username.data).first()
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
           raise ValidationError('邮箱已存在')


    def create_user(self, user):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user

'''
实现企业注册的方法二，不推荐
    def create_company_user(self, user):
        user = User()
        user.role = 20
        self.populate_obj(user)
        print(user)
        db.session.add(user)
        db.session.commit()
        return user

class CourseForm(FlaskForm):
    name = StringField('课程名称', validators=[Required(), Length(5, 32)])
    description = TextAreaField('课程简介', validators=[Required(), Length(20, 256)])
    image_url = StringField('封面图片地址', validators=[Required(), URL()])
    author_id = IntegerField('作者ID', validators=[Required(), NumberRange(min=1, message='无效的用户ID')])
    submit = SubmitField('提交')

    def validate_author_id(self, field):
        if not User.query.get(self.author_id.data):
            raise ValidationError('用户不存在')

    def create_course(self):
        course = Course()
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course

    def update_course(self, course):
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course
'''

class AdminCreateUserForm(FlaskForm):
    id = StringField('user id', validators=[Required()])
    username = StringField('user name', validators=[Required()])
    email = StringField('user email', validators=[Required()])
    password = StringField('user password', validators=[Required()])
    submit = SubmitField('submit')

    def validate_id(self, field):
        if  User.query.get(self.id.data):
            raise ValidationError('user exists.')

    def create_user(self):
        user = User()
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user

class AdminEditUserForm(FlaskForm):
    id = StringField('user id', validators=[Required()])
    username = StringField('user name', validators=[Required()])
    email = StringField('user email', validators=[Required()])
    submit = SubmitField('submit')

    def __init__(self, user=None, *args, **kw):
        super().__init__(*args, **kw)
        self.user = user

    def validate_id(self, field):
        id = self.id.data
        if self.user.id != int(id) and User.query.get(id):
            raise ValidationError('user exists.')

    def update_user(self, user):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user

class CompanyProfileForm(FlaskForm):
    username = StringField('企业名称', validators=[DataRequired(), Length(3,15)])
    password = PasswordField('密码(不填写保持不变)')
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    location = StringField('地址', validators=[DataRequired(), Length(1,128)])
    web_site = StringField('网址', validators=[DataRequired(), URL()])
    logo = StringField('logo', validators=[DataRequired(), URL()])
    description = StringField('一句话描述', validators=[DataRequired(), Length(1,50)])
    about = StringField('团队介绍', validators=[DataRequired(), Length(1,256)])
    tags = StringField('标签', validators=[DataRequired(), Length(1,50)])
    submit = SubmitField('提交')
  
    def update_profile(self,user):
        user.password = self.password.data
        user.username = self.username.data
        user.email = self.email.data
        user.logo = self.logo.data
        user.web_site = self.web_site.data
        user.description = self.description.data
        user.about = self.about.data
        user.tags = self.tags.data
        db.session.add(user)
        db.session.commit()

class UserProfileForm(FlaskForm):
    username = StringField('企业名称', validators=[DataRequired(), Length(3,15)])
    password = PasswordField('密码(不填写保持不变)')
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    upload_resume_url = StringField('简历地址', validators=[DataRequired(), URL()])
    submit = SubmitField('提交')
    
    def __init__(self, user, *args, **kw):
        super().__init__(*args, **kw)
        self.user = user

    def update_profile(self,user):
        if not self.password.data : 
            user.password = self.password.data
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()

