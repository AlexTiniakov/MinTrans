from flask import Flask, request, json, jsonify, render_template
import requests
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import os
import magic

#from app import mail

server = Flask(__name__)
server.config['UPLOAD_FOLDER'] = 'files'
server.config['DEBUG'] = True
server.config['MAIL_SERVER'] = 'smtp.googlemail.com'
server.config['MAIL_PORT'] = 465
server.config['MAIL_USE_TLS'] = False
server.config['MAIL_USE_SSL'] = True
server.config['MAIL_USERNAME'] = 'test.frs.01@gmail.com'
server.config['MAIL_PASSWORD'] = 'FRS11223344'
mail = Mail(server)

@server.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@server.route('/prod_obl', methods=['GET', 'POST'])
def prod_obl():
    return render_template('prod_obl.html')

@server.route('/vidkr_midj_narod', methods=['GET', 'POST'])
def vidkr_midj_narod():
    return render_template('vidkr_midj_narod.html')

@server.route('/vnesen_zmin', methods=['GET', 'POST'])
def vnesen_zmin():
    return render_template('vnesen_zmin.html')

@server.route('/prod_midj_narod', methods=['GET', 'POST'])
def prod_midj_narod():
    return render_template('prod_midj_narod.html')

@server.route('/prod_obl_mail', methods=['GET', 'POST'])
def prod_obl_mail():
    file_names = ['anketa_prodovj_stroky', 'vidom_avtobusy', 'vidom_dodatk_ymovi', 'vidom_invest']
    txt_names = ['carrrier_name',\
        'post_addr',\
        'finans_recviz',\
        'edrpoy',\
        'id_pereviz',\
        'ur_addr',\
        'fact_addr',\
        'licence',\
        'nazva_marshruty',\
        'last_nane',\
        'first_name',\
        'second_name',\
        'posada',\
        'emailHelp']
    ru_names = ['Назва організації-перевізника',\
        'Поштова адреса',\
        'Фінансові реквізити',\
        'ЄДРПОУ',\
        'Ідентифікаційний номер автомобільного перевізника',\
        'Юридична адреса',\
        'Фактична адреса',\
        'Номер та дата прийняття рішення щодо видачі ліцензії на здійснення перевезень',\
        'Назва маршруту із зазначенням номерів рейсів',\
        'Прізвище',\
        'Ім\'я',\
        'По батькові',\
        'Посада',\
        'Адреса електронної пошти']
    msg = Message('Заява на продовження строку дії договору (дозволу) з перевезення пасажирів на автобусному маршруті загального користування', \
        sender='test.frs.01@gmail.com', recipients=['tiniakov.alex@gmail.com', request.form['emailHelp']])
    
    mime = magic.Magic(mime=True)
    for file_name in file_names:
        try:
            file = request.files[file_name]
            name = secure_filename(file.filename)
            path = os.path.join(server.config['UPLOAD_FOLDER'], name)
            file.save(path)
            with server.open_resource(path) as fp:
                msg.attach(name, mime.from_file(path), fp.read())
                os.remove(path)
        except:
            pass
    html_body = ''
    for i in range(len(txt_names)):
        html_body += '<h3>' + ru_names[i] + ': <h3>' + '<h4>\n    ' + request.form[txt_names[i]] + '<h4>'
    msg.html = html_body
    mail.send(msg)
    return render_template('index.html')

@server.route('/vidkr_midj_narod_mail', 
methods=['GET', 'POST'])
def vidkr_midj_narod_mail():
    return render_template('index.html')

@server.route('/vnesen_zmin_mail', 
methods=['GET', 'POST'])
def vnesen_zmin_mail():
    return render_template('index.html')

@server.route('/prod_midj_narod_mail', 
methods=['GET', 'POST'])
def prod_midj_narod_mail():
    return render_template('index.html')

if __name__ == "__main__":
    server.run()