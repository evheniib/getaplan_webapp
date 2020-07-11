from app import app
from flask import render_template, redirect, flash, url_for, request
from app.forms import SelectProf
from app.models import Profession


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SelectProf()
    if request.method == 'POST':
        return redirect(url_for("profession", name=form.select.data))
    return render_template("index.html", title="Select proffesion", form=form)

@app.route('/profession/<name>')
def profession(name):
    profession = Profession.query.filter_by(name=name).first_or_404()
    return render_template('profession.html', profession=profession)