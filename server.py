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

@server.route('/send_mail', methods=['GET', 'POST'])
def prod_obl_mail():
    type_of = request.form["type_of"]
    subject = {"prod_obl":"Заява на продовження строку дії договору (дозволу) з перевезення пасажирів на автобусному маршруті загального користування",
                "vidkr_midj_narod":"Заява на відкриття регулярного міжнародного автомобільного маршруту",
                "prod_midj_narod":"Заява на продовження дії дозволу на регулярний міжнародний автомобільний маршрут",
                "vnesen_zmin":"Заява на внесення змін до функціонуючого регулярного міжнародного автомобільного маршруту"}
    file_names = {"prod_obl":['anketa_prodovj_stroky', 'vidom_avtobusy', 'vidom_dodatk_ymovi', 'vidom_invest'],\
            "vidkr_midj_narod":['shema_marshr','rozklad_ryhy','grafik_vidpochinky','taryfy','spusok_avtob','vidpovidnist_avtob','svidotstva','licenzii','rekomendacii','ygodu'],\
            "prod_midj_narod":[],\
            "vnesen_zmin":[]}
    #ru_file_names = {"prod_obl":['Анкета для продовження дії договору (дозволу)','Відомості про автобуси, які будуть використовуватись на маршруті','Відомості про додаткові умови обслуговування маршруту','Відомості щодо інвестування коштів на придбання більш нових та/або комфортабельних автобусів']}
    txt_names = {"prod_obl":['carrrier_name','post_addr','finans_recviz','edrpoy','id_pereviz','ur_addr','fact_addr','licence','nazva_marshruty','last_nane','first_name','second_name','posada','emailHelp'],\
            "vidkr_midj_narod":['carrrier_name','post_addr','finans_recviz','edrpoy','last_nane','first_name','second_name','posada','emailHelp','nazva_marshruty'],\
            "prod_midj_narod":[],\
            "vnesen_zmin":[]}
    ru_names = {"prod_obl":['Назва організації-перевізника','Поштова адреса','Фінансові реквізити','ЄДРПОУ','Ідентифікаційний номер автомобільного перевізника','Юридична адреса','Фактична адреса','Номер та дата прийняття рішення щодо видачі ліцензії на здійснення перевезень','Назва маршруту із зазначенням номерів рейсів','Прізвище','Ім\'я','По батькові','Посада','Адреса електронної пошти'],\
            "vidkr_midj_narod":['Назва організації-перевізника','Поштова адреса','Фінансові реквізити','ЄДРПОУ','Прізвище','Ім\'я','По батькові','Посада','Адреса електронної пошти','Назва маршруту'],\
            "prod_midj_narod":[],\
            "vnesen_zmin":[]}
    msg = Message(subject=subject[type_of], \
        sender='test.frs.01@gmail.com', \
        recipients=['tiniakov.alex@gmail.com', request.form['emailHelp']])
    
    mime = magic.Magic(mime=True)
    for file_name in file_names[type_of]:
        try:
            file = request.files[file_name]
            name = secure_filename(file.filename)
            name = file_name + '.' + name.split('.')[-1]
            path = os.path.join(server.config['UPLOAD_FOLDER'], name)
            file.save(path)
            with server.open_resource(path) as fp:
                msg.attach(name, mime.from_file(path), fp.read())
                os.remove(path)
        except:
            pass
    html_body = ''
    for i in range(len(txt_names[type_of])):
        html_body += '<h3>' + ru_names[type_of][i] + ': <h3>' + '<h4>\n    ' + request.form[txt_names[type_of][i]] + '<h4>'
    msg.html = html_body
    mail.send(msg)
    return render_template('index.html')
    
if __name__ == "__main__":
    server.run()