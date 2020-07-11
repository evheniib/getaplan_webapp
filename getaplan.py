from app import app, db
from app.models import Profession, Skill, Vacancy, vacancy_skill


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Profession': Profession,
        'Skill': Skill,
        'Vacancy': Vacancy,
        "vacancy_skill": vacancy_skill
    }
