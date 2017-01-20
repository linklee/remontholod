# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, redirect
from mailer import send_message,send_message_self
from validator import Validator
import urllib
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse



app = Flask(__name__,
            static_path=None,
            static_url_path=None,
            static_folder='templates/assets',
            template_folder='templates',
            instance_path=None,
            instance_relative_config=False)
app.debug = True


@app.route("/", methods=['GET'])
def index():
    key = request.args.get('term')
    return render_template("index.html",key = key)

@app.route("/?<string:link>", methods=['GET'])
def index_param():
    return render_template("index.html", key = key)

@app.route("/<string:link>", methods=['GET'])
def index_link(link):
    if not link.endswith('.ico'):
        return render_template(link)
    return render_template("index.html")
    
@app.route("/stellazhi", methods=['GET'])
def stellazhi():
    return render_template("stellazhi.html")

@app.route("/torg-mebel", methods=['GET'])
def torg_mebel():
    return render_template("torg-mebel.html")

@app.route("/telezhki-korzini", methods=['GET'])
def telezhki_korzini():
    return render_template("telezhki-korzini.html")
    
@app.route("/kass-boxes", methods=['GET'])
def kass_boxes():
    return render_template("kass-boxes.html")
    
@app.route("/holod-oborudovanie", methods=['GET'])    
def holod_oborudovanie():
    return render_template("holod-oborudovanie.html")

@app.route("/delivery", methods=['GET'])    
def delivery():
    return render_template("delivery.html")

@app.route("/about", methods=['GET'])    
def about():
    return render_template("about.html")

@app.route("/remont", methods=['GET'])    
def remont():
    return render_template("remont.html")

@app.route("/technicheskoe-obsluzhivanie", methods=['GET'])    
def tech():
    return render_template("tech.html")

@app.route("/montazh-oborudovaniya", methods=['GET'])    
def montazh():
    return render_template("montazh.html")


@app.route("/send-form", methods=['POST'])
def send_form():
    name = phone = email = country = text = success = None
    data = request.data
    name = request.form['name']
    phone = request.form['phone']
    text = request.form['text']
    errors = []
    if len(errors) <= 0:
        send_message_self ('name: '+ name.encode('utf8') + '<br/>' +
        'Phone/email: ' + phone.encode('utf8') + '<br/>' + ' comment: ' + text.encode('utf8'))
        return render_template("index.html", success = "true", name = name)
        

    return jsonify(success=False, errors=errors)


if __name__ == "__main__":
    app.run(debug=True)