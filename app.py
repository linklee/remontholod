# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, redirect, g
from mailer import send_message, send_message_self
from validator import Validator
import urllib
import os
import sqlite3

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

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'db.sqlite3'),
    USERNAME='admin',
    PASSWORD='default'
))


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route("/", methods=['GET'])
def index():
    # print(os.path.join(app.root_path, 'db.sqlite3'))
    # print('xxx')
    db = get_db()
    cur = db.execute('SELECT id, title, text FROM pages')
    pages = cur.fetchall()
    key = request.args.get('term')
    # print(pages)
    return render_template("index.html", key=key, pages=pages)


@app.route("/?<string:link>", methods=['GET'])
def index_param():
    return render_template("index.html", key=key)


@app.route("/<string:link>", methods=['GET'])
def index_link(link):
    if not link.endswith('.ico'):
        return render_template(link)
    return render_template("index.html")


@app.route("/stellazhi", methods=['GET'])
def stellazhi():
    db = get_db()
    cur = db.execute("SELECT id, title, text FROM pages WHERE id = 2 ") #url = 'stellazhi'
    pages = cur.fetchall()
    return render_template("stellazhi.html", page=pages[0])


@app.route("/torg-mebel", methods=['GET'])
def torg_mebel():
    db = get_db()
    cur = db.execute("SELECT id, title, text FROM pages WHERE id = 3")  # url = 'torg-mebel'
    pages = cur.fetchall()

    return render_template("torg-mebel.html", page=pages[0])


@app.route("/telezhki-korzini", methods=['GET'])
def telezhki_korzini():
    return render_template("telezhki-korzini.html")


@app.route("/kass-boxes", methods=['GET'])
def kass_boxes():
    return render_template("kass-boxes.html")


@app.route("/holod-oborudovanie", methods=['GET'])
def holod_oborudovanie():
    db = get_db()
    cur = db.execute("SELECT id, title, text FROM pages WHERE id = 4 ")  # url = 'holod-oborudovanie'
    pages = cur.fetchall()
    return render_template("holod-oborudovanie.html", page=pages[0])


@app.route("/delivery", methods=['GET'])
def delivery():
    return render_template("delivery.html")


@app.route("/about", methods=['GET'])
def about():
    return render_template("about.html")


# 301 redirect
@app.route("/remont", methods=['GET'])
def remont_redirect():
    return redirect("/remont-oborudovaniya", code=301)


@app.route("/remont-oborudovaniya", methods=['GET'])
def remont():
    return render_template("/remont/remont_index.html")


# 301 redirect
@app.route("/technicheskoe-obsluzhivanie", methods=['GET'])
def tech_redirect():
    return redirect("/technicheskoe-obsluzhivanie-oborudovaniya", code=301)


@app.route("/technicheskoe-obsluzhivanie-oborudovaniya", methods=['GET'])
def tech():
    return render_template("tech.html")


@app.route("/montazh-oborudovaniya", methods=['GET'])
def montazh():
    return render_template("montazh.html")


@app.route('/robots.txt')
def robots():
    return render_template("assets/docs/robots.txt")


@app.route('/sitemap.xml')
def sitemap():
    return render_template("assets/docs/sitemap.xml")


@app.route("/remont-holodilnogo-oborudovaniya", methods=['GET'])
def remont_holodilnogo_oborudovaniya():
    db = get_db()
    cur = db.execute("SELECT id, title, text FROM pages WHERE id = 1")

    pages = cur.fetchall()

    return render_template("/remont/holod.html", page=pages[0])


@app.route("/remont-neitralnogo-oborudovaniya", methods=['GET'])
def remont_neitralnogo_oborudovaniya():
    return render_template("/remont/neutral.html")


@app.route("/remont-kofemashin", methods=['GET'])
def remont_kofemashin():
    return render_template("/remont/coffee.html")


@app.route("/remont-elektricheskih-plit", methods=['GET'])
def remont_elektricheskih_plit():
    return render_template("/remont/plita.html")


@app.route("/remont-vesov", methods=['GET'])
def remont_vesov():
    return render_template("/remont/vesi.html")


@app.route("/remont-prochego-oborudovaniya", methods=['GET'])
def remont_etc():
    return render_template("/remont/etc.html")


@app.route("/pages", methods=['GET'])
def manage():
    action = request.args.get('action')
    if action != "edit":
        return redirect("/", code=301)
    db = get_db()
    cur = db.execute('SELECT id, title, url, text FROM pages')
    pages = cur.fetchall()

    return render_template("manage/manage_index.html", pages=pages)


@app.route("/change_page", methods=['GET'])
def manage_page():
    action = request.args.get('action')
    page_id = request.args.get('page')
    if action != "edit_page":
        return redirect("/", code=301)
    if request.args.get('msg'):
        msg = "Изменения сохранены"
    db = get_db()
    cur = db.execute('SELECT id, title, url, text FROM pages WHERE id = ?', page_id)
    page = cur.fetchall()[0]

    return render_template("manage/manage_page.html", page=page, page_id=page_id)


@app.route('/save_changes', methods=['POST'])
def save_changes():
    page_id = request.args.get('page')
    db = get_db()
    print('xxx')
    query = "UPDATE pages SET title ='" + request.form['title'] + "', text ='" + request.form['text'] + "' WHERE id = " + page_id
    #query = 'UPDATE pages SET title = ?, text = ? WHERE id = ?',request.form['title'], request.form['text'], page_id
    db.execute(query)
    db.commit()
    redirect_url = '/change_page?action=edit_page&page=' + page_id
    return redirect(redirect_url)


@app.route("/send-form", methods=['POST'])
def send_form():
    name = phone = email = country = text = success = None
    data = request.data
    name = request.form['name']
    phone = request.form['phone']
    text = request.form['text']
    errors = []
    if len(errors) <= 0:
        send_message_self('name: ' + name.encode('utf8') + '<br/>' +
                          'Phone/email: ' + phone.encode('utf8') + '<br/>' + ' comment: ' + text.encode('utf8'))
        return render_template("index.html", success="true", name=name)

    return jsonify(success=False, errors=errors)


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
