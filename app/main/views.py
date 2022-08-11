from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import FormRestartPasword
from ..controllers import tablespaces
# from ..models import Model
# from .. import db
# from ..models import User

@main.route('/')
def inicio():
    return render_template('index.html')

@main.route('/restart', methods=['GET', 'POST'])
def form_restart_pasword():
    form = FormRestartPasword()

    if form.validate_on_submit():
        user = form.user.data
        password = form.password.data
        verify_password = form.verify_password.data
        expire = form.expire.data
        locked = form.locked.data
        form.user.data = ''
        return redirect(url_for('restart'))

    return render_template('FormRestart.html', form=form)