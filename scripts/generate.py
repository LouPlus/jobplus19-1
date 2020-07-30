import os
import json
from random import randint
from faker import Faker

from manage import app
from jobplus.models import db, User, Company, Job


app.app_context().push()


fake = Faker('zh-cn')


def create_user_and_company():
    with open('scripts/data_company.json') as f1, \
            open('scripts/data_job.json') as f2:
        job_name_list = [i['name'] for i in json.load(f2)]
        experience_list = ['不限', '1-3年', '3-5年', '5-10年']
        degree_list = ['不限', '本科', '博士后']
        for i in json.load(f1):
            user = User(username=fake.name(), email=fake.email())
            user.password = 'shiyanlou'
            yield user
            company = Company(
                    name = i['name'],
                    logo = i['logo'],
                    location = i['location'],
                    description = i['description'],
                    about = i['about'] if len(i['about']) > 9 else \
                            fake.sentence(nb_words=11),
                    tags = i['tags'],
                    user = user,
            )
            yield company
            for i in range(randint(1, 5)):
                job = Job(
                    name = job_name_list[randint(1, len(job_name_list))-1],
                    salary_low = randint(3, 8) * 1000,
                    salary_high = randint(9, 15) * 1000,
                    location = fake.address(),
                    is_fulltime = 1,
                    experience_requirement = experience_list[
                            randint(1, len(experience_list)) - 1],
                    degree_requirement = degree_list[
                            randint(1, len(degree_list)) - 1],
                    company = company
                )
                yield job


def run():
    for i in create_user_and_company():
        db.session.add(i)
    db.session.commit()
    print('OK')


if __name__ == '__main__':
    run()
