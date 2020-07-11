from app import db


class Profession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, unique=True)
    vacancies = db.relationship("Vacancy", backref="vacancy", lazy='dynamic')

    def __repr__(self):
        return "<Profession {}>".format(self.name)


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, unique=True)

    def __repr__(self):
        return "<Skill {}>".format(self.name)


vacancy_skill = db.Table('vacancy_skill', db.Model.metadata,
    db.Column('vacancy_id', db.Integer, db.ForeignKey('vacancy.id')),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'))
)


class Vacancy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vacancy_id = db.Column(db.Integer)
    name = db.Column(db.String(256), index=True)
    expirience = db.Column(db.String(32), index=True)
    area = db.Column(db.String(32), index=True)
    salary = db.Column(db.Float, index=True)
    profession_id = db.Column(db.Integer, db.ForeignKey('profession.id'))
    skills = db.relationship('Skill', secondary=vacancy_skill)

    def __repr__(self):
        return "<Vacancy {}>".format(self.name)
