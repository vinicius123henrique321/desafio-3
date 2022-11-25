from flask import Flask, redirect, render_template, request, url_for
from flask_mysqldb import MySQL
import numpy as np

app = Flask(__name__)
mysql = MySQL(app)

app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='ds4'

@app.route("/")
@app.route("/index")
def home():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * from contatos''')
    rv = cur.fetchall()
    print(rv)
    return render_template("index.html")

@app.route("/contato", methods=['GET', 'POST'])
def contatos():
    if request.method == "POST":
        cur = mysql.connection.cursor()
        email = request.form['email']
        assunto = request.form['assunto']
        desc = request.form['descricao']
        cur.execute(f'''INSERT INTO `ds4`.`contatos` (`email`, `assunto`, `descricao`) VALUES ('{email}', '{assunto}', '{desc}')''')
        cur.connection.commit()
        return redirect('/list')
    return render_template("contato.html")

@app.route("/quemsomos")
def quemsomos():
    return render_template("quemsomos.html")


@app.route("/list")
def list():
    cur = mysql.connection.cursor()
    list = cur.execute('''SELECT * FROM contatos''')
    if list > 0:
        listDetails = cur.fetchall()
    else:
        listDetails = ()

    return render_template('list.html', contatos=listDetails)
