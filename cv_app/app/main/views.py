from . import main
from datetime import datetime , timezone 
from flask import render_template, session, redirect, url_for, make_response, request, flash, current_app
from .forms import ContactForm 
from app.email import send_email

@main.route('/',methods=['GET','POST'])
def index():
    current_time = datetime.now(timezone.utc)
    return render_template('base.html', current_time=current_time)

@main.route('/projects',methods=['GET'])
def projects():
    return render_template('projects.html')

@main.route('/aiprev',methods=['GET'])
def aiprev():
    return render_template('ai_prev.html')

@main.route('/interCharts',methods=['GET','POST'])
def interCharts():
    return render_template('interActiveCharts.html')


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Formularz jest poprawny, wysyłamy e-mail
        admin_email = current_app.config['ADMIN_EMAIL']
        
        send_email(
            to=admin_email,
            subject='Nowa wiadomość z formularza kontaktowego',
            template='email/contact_notification', # Nazwa szablonu (bez .txt/.html)
            # Przekazujemy dane z formularza do szablonu e-maila
            name=form.name.data,
            email=form.email.data,
            message=form.message.data
        )
        
        flash('Dziękuję! Twoja wiadomość została wysłana.', 'success')
        return redirect(url_for('main.contact')) # Przekieruj, aby uniknąć ponownego wysłania

    # Renderujemy stronę z formularzem
    return render_template('contact.html', title='Kontakt', form=form)