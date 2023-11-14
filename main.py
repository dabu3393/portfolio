import subprocess
from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
import smtplib
import sys
import webbrowser

sys.path.append('projects')  # Add the 'projects' directory to the Python path


app = Flask(__name__)
app.secret_key = 'srdetfyguhjknbhgvfytguhijl'

bootstrap = Bootstrap5(app)

python_projects = [
    {'project': 'project_1',
     'name': 'Text to Morse Code Converter',
     'project_url': 'https://replit.com/@dabu3393/Text-to-Morse-Code-Converter?v=1',
     'github_url': 'https://github.com/dabu3393/English-to-Morse-Code-Converter',
     'description': 'A text-based Python program to convert Strings into Morse Code.'},
    {'project': 'project_3',
     'name': 'Tic Tac Toe',
     'project_url': 'https://replit.com/@dabu3393/Tic-Tac-Toe?v=1',
     'github_url': 'https://github.com/dabu3393/Tic-Tac-Toe',
     'description': 'A text-based version of the Tic Tac Toe game.'},
    {'project': 'project_4',
     'name': 'Image Watermarking App',
     'project_url': 'Tkinter_app',
     'github_url': 'https://github.com/dabu3393/Image-Watermarking-App',
     'description': 'A Desktop program where you can upload images and add a watermark.'},
    {'project': 'project_5',
     'name': 'Typing Speed Test',
     'project_url': 'Tkinter_app',
     'github_url': 'https://github.com/dabu3393/Typing-Speed-Test',
     'description': 'A Tkinter GUI desktop application that tests your typing speed.'},
    {'project': 'project_6',
     'name': 'Breakout Game',
     'project_url': 'Tkinter_app',
     'github_url': 'https://github.com/dabu3393/Breakout-Game',
     'description': 'The beloved 80s arcade classic, Breakout, using the Python Turtle graphics library.'},
    {'project': 'project_7',
     'name': 'Cafe and Wifi Website',
     'project_url': 'https://replit.com/@dabu3393/Text-to-Morse-Code-Converter?v=1',
     'github_url': 'https://github.com/dabu3393/Cafe-and-Wifi-Website',
     'description': 'A website that lists cafes with wifi and power for remote working.'},
    {'project': 'project_8',
     'name': 'Todo List Website',
     'project_url': 'https://replit.com/@dabu3393/Text-to-Morse-Code-Converter?v=1',
     'github_url': 'https://github.com/dabu3393/Todo-List-Website',
     'description': 'A website for your todo lists.'},
    {'project': 'project_9',
     'name': 'Disappearing Text Writing App',
     'project_url': 'https://replit.com/@dabu3393/Text-to-Morse-Code-Converter?v=1',
     'github_url': 'https://github.com/dabu3393/Disappearing-Text-Writing-App',
     'description': 'An online writing app where if you stop typing, your work will disappear.'},
    {'project': 'project_10',
     'name': 'Convert PDF to Audiobook',
     'project_url': 'Tkinter_app',
     'github_url': 'https://github.com/dabu3393/Convert-PDF-to-Audiobook',
     'description': 'A Python script that takes a PDF file and converts it into speech.'},
    {'project': 'project_11',
     'name': 'Image Colour Palette Generator',
     'project_url': 'https://replit.com/@dabu3393/Text-to-Morse-Code-Converter?v=1',
     'github_url': 'https://github.com/dabu3393/Image-Colour-Palette-Generator',
     'description': 'A website that finds the most common colours in an uploaded image.'},
    {'project': 'project_12',
     'name': 'Custom Web Scraper',
     'project_url': 'https://replit.com/@dabu3393/Text-to-Morse-Code-Converter?v=1',
     'github_url': 'https://github.com/dabu3393/Custom-Web-Scraper',
     'description': 'A custom web scraper to collect data on things that you are interested in.'},
    {'project': 'project_13',
     'name': 'Automate the Google Dinosaur Game',
     'project_url': 'https://replit.com/@dabu3393/Text-to-Morse-Code-Converter?v=1',
     'github_url': 'https://github.com/dabu3393/Automate-the-Google-Dinosaur-Game',
     'description': 'Code to play the Google Dinosaur Game for you.'},
    {'project': 'project_14',
     'name': 'Space Invaders',
     'project_url': 'https://replit.com/@dabu3393/Text-to-Morse-Code-Converter?v=1',
     'github_url': 'https://github.com/dabu3393/Space-Invaders',
     'description': 'The classic arcade game where you shoot down alien ships.'},
    {'project': 'project_15',
     'name': 'Custom API Based Website',
     'project_url': 'https://replit.com/@dabu3393/Text-to-Morse-Code-Converter?v=1',
     'github_url': 'https://github.com/dabu3393/Custom-API-Based-Website',
     'description': 'A custom website using an API that I find interesting.'},
    {'project': 'project_16',
     'name': 'An Online Shop',
     'project_url': 'https://replit.com/@dabu3393/Text-to-Morse-Code-Converter?v=1',
     'github_url': 'https://github.com/dabu3393/An-Online-Shop',
     'description': 'An eCommerce website with payment processing.'},
    {'project': 'project_17',
     'name': 'Custom Automation',
     'project_url': 'https://replit.com/@dabu3393/Text-to-Morse-Code-Converter?v=1',
     'github_url': 'https://github.com/dabu3393/Custom-Automation',
     'description': 'Automating some aspect of your life using Python.'},
    {'project': 'project_18',
     'name': 'Analyse and Visualise the Space Race',
     'project_url': 'https://replit.com/@dabu3393/Text-to-Morse-Code-Converter?v=1',
     'github_url': 'https://github.com/dabu3393/Analyse-and-Visualise-the-Space-Race',
     'description': 'Using space mission data from 1957 onwards to analyse and visualise trends over time.'},
    {'project': 'project_19',
     'name': 'Analyse Deaths involving Police in the United States',
     'project_url': 'https://replit.com/@dabu3393/Text-to-Morse-Code-Converter?v=1',
     'github_url': 'https://github.com/dabu3393/Analyse-Deaths-involving-Police-in-the-United-States',
     'description': 'Extracting insights from combining US census data and the Washington Post\'s database on deaths by police in the United States.'}
]


class ContactForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired()])
    message = TextAreaField(label='Message', validators=[DataRequired()])
    submit = SubmitField(label='Send Message')


@app.route('/')
def home():
    # Create a list of project names
    return render_template('index.html', projects=python_projects[:6])



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


@app.route('/project')
def projects():
    return render_template('projects.html', projects=python_projects)


@app.route('/run_tkinter/<string:project_id>')
def run_tkinter(project_id):
    project_url = request.args.get('project_url')
    github_url = request.args.get('github_url')
    if project_url != 'Tkinter_app':
        webbrowser.open_new_tab(project_url)
    else:
        subprocess.Popen(['python', f'projects/{project_id}/main.py'])
    return redirect(github_url)


if __name__ == '__main__':
    app.run(debug=True)