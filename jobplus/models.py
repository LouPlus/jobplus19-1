from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class Base(db.Model):
    """ 所有 model 的一个基类，默认添加了时间戳
    """
    # 表示不要把这个类当作映射类
    __abstract__ = True
    # 设置了 defautl 和 onupdate 这俩个时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)


# 用户职位关系表，添加 user_id,job_id 外键，级联删除
user_job = db.Table(
    'user_job',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')),
    db.Column('job_id', db.Integer, db.ForeignKey('job.id', ondelete='CASCADE'))
)


class User(Base, UserMixin):
    '''用户表映射类
    '''

    ROLE_USER = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    #用户投递职位关联user_job表
    collect_jobs = db.relationship('Job', secondary=user_job)
    #简历名称
    upload_resume_url = db.Column(db.String(64))
    is_disable = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY

class Resume(Base):
    '''简历表映射类
    '''

    id = db.Column(db.Integer, 
            db.ForeignKey('user.id', ondelete='CASCADE'),
            primary_key=True)
    job_experiences = db.relationship('JobExperience')
    edu_experiences = db.relationship('EduExperience')
    project_experiences = db.relationship('ProjectExperience')
    user = db.relationship('User', backref=db.backref('resume', uselist=False))


#简历中的获奖经历表，暂时用不上
class Experience(Base):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    begin_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    # 在职期间，做了什么，解决了什么问题，做出了什么贡献
    # 在校期间做过什么，取得过什么荣誉
    # 项目期间，做了什么，解决了什么问题，做出了什么贡献
    description = db.Column(db.String(1024))

#简历中的工作经历表，暂时用不上
class JobExperience(Experience):
    __tablename__ = 'job_experience'

    company = db.Column(db.String(32), nullable=False)
    city = db.Column(db.String(32), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    resume = db.relationship('Resume', uselist=False)

#简历中的教育经历表，暂时用不上
class EduExperience(Experience):
    __tablename__ = 'edu_experience'

    school = db.Column(db.String(32), nullable=False)
    # 所学专业
    specialty = db.Column(db.String(32), nullable=False)
    degree = db.Column(db.String(16))
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    resume = db.relationship('Resume', uselist=False)


#简历中的项目经历表，暂时用不上
class ProjectExperience(Experience):
    __tablename__ = 'project_experience'

    name = db.Column(db.String(32), nullable=False)
    # 在项目中扮演的角色
    role = db.Column(db.String(32))
    # 多个技术用逗号隔开
    technologys = db.Column(db.String(64))
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    resume = db.relationship('Resume', uselist=False)


class Company(Base):
    '''企业表映射类
    '''

    id = db.Column(db.Integer, 
            db.ForeignKey('user.id', ondelete='CASCADE'),
            primary_key=True)
    name = db.Column(db.String(64), nullable=False, index=True, unique=True)
    logo = db.Column(db.String(64), nullable=False)
    web_site = db.Column(db.String(64), nullable=False)
    location = db.Column(db.String(24), nullable=False)
    description = db.Column(db.String(100))
    team_number = db.Column(db.String(256))
    about = db.Column(db.Text())
    tags = db.Column(db.String(128))
    user = db.relationship('User', backref=db.backref('company', uselist=False))

    def __repr__(self):
        return '<Company {}>'.format(self.name)


class Job(Base):
    '''职位表映射类
    '''

    id = db.Column(db.Integer, primary_key=True)
    # 职位名称
    name = db.Column(db.String(24))
    # 薪水范围用一个字段
    salary_low = db.Column(db.Integer, nullable=False)
    salary_high = db.Column(db.Integer, nullable=False)
    # 工作地点
    location = db.Column(db.String(24))
    # 职位标签，多个标签用逗号隔开，最多10个
    tags = db.Column(db.String(128))
    # 经验要求，职位要求用一个字段
    experience_requirement = db.Column(db.String(32))
    # 暂用不上
    degree_requirement = db.Column(db.String(32))
    # 是否全职
    is_fulltime = db.Column(db.Boolean, default=True)
    # 是否上线
    is_open = db.Column(db.Boolean, default=True)
    #添加company_id外键，级联删除
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'))
    #与企业表关联,设为false为一对一
    company = db.relationship('Company', backref=db.backref('companies'))
    views_count = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return '<Job {}>'.format(self.name)


class Dilivery(Base):
    '''简历投递状态表映射类
    '''

    # 等待企业审核
    STATUS_WAITING = 1
    # 被拒绝
    STATUS_REJECT = 2
    # 被接收，等待通知面试
    STATUS_ACCEPT = 3
    id = db.Column(db.Integer, primary_key=True)
    # 添加职位id,用户id外键,删除关联数据，与之关联的数据设置为null
    job_id = db.Column(db.Integer, db.ForeignKey('job.id', ondelete='SET NULL'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    # 默认投递状态为1－等待企业审核
    status = db.Column(db.SmallInteger, default=STATUS_WAITING)
    # 企业回应,暂时用不上
    response = db.Column(db.String(256))
