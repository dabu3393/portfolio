from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
import smtplib

app = Flask(__name__)
app.secret_key = 'srdetfyguhjknbhgvfytguhijl'

bootstrap = Bootstrap5(app)


class ContactForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired()])
    message = TextAreaField(label='Message', validators=[DataRequired()])
    submit = SubmitField(label='Send Message')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    contact_form = ContactForm()
    if request.method == 'POST':
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            connection.starttls()
            connection.login(user='davispython@gmail.com', password='slpn lhhb dacv dfxt')
            connection.sendmail(
                from_addr='davispython@gmail.com',
                to_addrs='davisburrill@icloud.com',
                msg=f'Subject:Contact Form Submission from Portfolio!\n\nSomeone filled out your contact form on your '
                    f'portfolio. Here\'s the message!\n\n'
                    f'Name: {contact_form.name.data}\n\n'
                    f'Email: {contact_form.email.data}\n\n'
                    f'Message: {contact_form.message.data}'
            )
        return redirect(url_for('home')) # Have this say the message was successfully sent
    return render_template('contact.html', form=contact_form)


# @app.route('/project')
# def projects():
#     return render_template('')



if __name__ == '__main__':
    app.run(debug=True)