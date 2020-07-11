import requests
from datetime import datetime, timedelta
from app import db
from app.models import Profession, Skill, Vacancy


def check_id_amount(url, pofession):
    par = {'text': pofession}
    response = requests.get(url, params=par)
    json_response = response.json()
    return print(f"Планируемое количество вакансий за 30 дней {json_response['found']}")


def get_id_list(pofession, day_interval):
    id_set = set()                                             
    endTime = datetime.now()
    startTime = endTime - timedelta(days=day_interval)
    interval_time = startTime + timedelta(days=1)

    i = 0
    while startTime <= endTime:                                             
        url = 'https://api.hh.ru/vacancies'
        par = {
            'text': pofession,
            'per_page': '100',
            'page': i,
            'date_from': startTime.strftime('%Y-%m-%d'),
            'date_to': interval_time.strftime('%Y-%m-%d'),
        }
        while True:
            response = requests.get(url, params=par)
            json_response = response.json()
            vacancies = json_response["items"]
            for vacancy in vacancies:
                id_set.add(vacancy["id"])
            amount_pages = json_response["pages"]
            i += 1
            if i > amount_pages:
                break
        startTime += timedelta(days=1)
        interval_time += timedelta(days=1)
        i = 0
    print(f"Количество какансий по профессии {pofession} = {len(id_set)}")
    return id_set


def get_currencies():
    currencies_dict = {}
    dictionaries = requests.get('https://api.hh.ru/dictionaries').json()
    for currency in dictionaries['currency']:
        currencies_dict[currency['code']] = currency['rate']
    return currencies_dict


def set_salary(vacancy, currencies_dict):
    salary = None
    if vacancy['salary']:
        if vacancy['salary']['to']:
            salary = vacancy['salary']['to']
            salary /= currencies_dict[vacancy['salary']['currency']]
            return float(salary)
        if vacancy['salary']['from']:
            salary = vacancy['salary']['from']
            salary /= currencies_dict[vacancy['salary']['currency']]
            return float(salary)
    return 0


def get_key_skills(vacancy):
    skill_str = ""
    if vacancy['key_skills']:
        for skill in vacancy['key_skills']:
            skill_str += skill["name"]+", "
        return skill_str
    return "None"


def vacancy_request(id_list, profession):
    print("Собираю атрибуты вакансий")

    currences = get_currencies()
    p = Profession.query.filter_by(name=profession).first()
    if p is None:
        p = Profession(name=profession)
        db.session.add(p)   

    for vacancy_id in id_list:
        response = requests.get("https://api.hh.ru/vacancies/" + vacancy_id)
        vacancy = response.json()

        if not vacancy["key_skills"]:
            continue
        for skills in vacancy["key_skills"]:
            if Skill.query.filter_by(name=skills["name"]).first():
                continue
            s = Skill(name=skills["name"])
            db.session.add(s)
        db.session.commit()
  
        v = Vacancy(
            vacancy_id=vacancy["id"],
            name=vacancy["name"],
            expirience=vacancy["experience"]["name"],
            area=vacancy["area"]["name"],
            salary=set_salary(vacancy, currences),
            profession_id=p.id
            )

        if vacancy["key_skills"] is not None:
            for skills in vacancy["key_skills"]:
                s = Skill.query.filter_by(name=skills["name"]).first()
                v.skills.append(s)
                db.session.add(v)
            db.session.commit()


def starter(day_interval=0):
    print("Сбор вакансий запущен ")
    prof_list = [
        "QA",
        "DevOps",
        "Front-end",
        "DBA",
        "Back-end",
        "Full-stack",
        "Business Analyst",
        "IOS developer",
        "Python developer",
        "Business Analyst",
        "Data Scientist"
    ]
    for profession in prof_list:
        print(f"Сбор вакансии по професси {profession} начат")
        id_list = get_id_list(profession, day_interval)
        vacancy_request(id_list, profession)
    print("done")


day_interval = int(input("Введите количество дней: "))
starter(day_interval)
