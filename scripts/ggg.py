import os
import json
from random import randint
from faker import Faker
from jobplus.models import User,db,Company,Job

fake = Faker()
'''
# 普通用户
def iter_users():
    yield User(
        username = 'admin',
        email = 'admin@a.com',
        _password = '111111',
        role = 30
        #upload_resume_url = 'https://jobs.zhaopin.com/CC296'
        )
'''
def iter_job():
    with open(os.path.join(os.path.dirname('__file__'),'scripts','data_job.json')) as f:
        jobb = json.load(f)
    com = Company.query#.all()
    for j in jobb:
       # for i in range(24,47):
        yield Job(
                name=j['name'],
                location=j['location'],
                salary_high='{}'.format(randint(2,6)),
                salary_low='{}'.format(randint(6,50)),
                tags=fake.company_suffix(),
                company_id=com.get(id)

#                experience_requirement=j['experience_requirement']
                )
        
'''
def iter_company():
    user_id = User.query.filter_by(id=1).first()
    with open(os.path.join(os.path.dirname('__file__'),'scripts','data_company.json')) as f:
        com = json.load(f)
    for c in com:
        yield Company(
                name = c['name'],
                description = c['description'],
                location = c['location'],
                logo = c['logo'],
                about = c['about'],
                tags =c['tags'],
                email= fake.email(),#'coma1@126.com',
                site = fake.url(),#'www.bootstrap.com',
                user_id = user_id,
                contact = fake.phone_number()#'010-1111'
                #slug = str0.index('this')
                )
'''
def run():
    '''
    for user in iter_users():
        db.session.add(user)
    
    for com in iter_company():
        db.session.add(com)
    '''
    for job in iter_job():
        db.session.add(job)
   
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
