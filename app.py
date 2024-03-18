from flask import Flask, render_template, request, redirect
from hashids import Hashids
from db_worker import init_db, set_link, get_link_information
from flask_qrcode import QRcode
import random


app = Flask(__name__)
hashids = Hashids()
QRcode(app)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        source_link = request.form.get("link")

        if source_link == '':
            return render_template('index.html', error_message='Введите ссылку')

        new_alias = request.form.get("alias")
        password = request.form.get("password")
        token = new_alias

        if get_link_information(token) or new_alias == '':
            token = hashids.encode(random.randint(0, 1000000))

        shrinked_link = f'http://localhost:5000/{token}'

        set_link(token, password, source_link)
        return render_template('index.html', shrinked_link=shrinked_link)
    else:
        return render_template('index.html')


@app.route("/<uniq_token>", methods=["POST", "GET"])
def go_to_short_link(uniq_token):
    link_information = get_link_information(uniq_token)

    if request.method == "POST":
        getted_pass = request.form.get("password")
        correct_pass = link_information.get('password')

        if getted_pass == correct_pass:
            source_link = link_information.get('source_link')
            return redirect(source_link)

        return render_template('auth.html', uniq_token=uniq_token, error_message='Вы ввели некорректный пароль')
    else:
        if link_information.get('password'):
            return render_template('auth.html', uniq_token=uniq_token)

        source_link = link_information.get("source_link")
        return redirect(source_link)

if __name__ == "__main__":
    init_db()
    app.run(debug = True, host = '0.0.0.0')
