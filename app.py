from flask import Flask,render_template,Blueprint,request,session,flash,redirect,url_for
from authentication import authentication
from purchase import purchase
from sale import sale
from crud import crud
from  flask_mysqldb import MySQL
from helper import calculate_main_balance
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

# MYSQL Configuration
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config["MYSQL_DB"] = os.getenv('MYSQL_DB')
app.config["MYSQL_CURSORCLASS"] = os.getenv('MYSQL_CURSORCLASS')


mysql = MySQL(app)
app.mysql = mysql
app.secret_key = "namma_kadai_project"

# register for blueprint
app.register_blueprint(authentication, url_prefix='/auth')
app.register_blueprint(purchase, url_prefix='/purchase')
app.register_blueprint(sale, url_prefix='/sale')
app.register_blueprint(crud, url_prefix='/editOrDelete')


@app.route("/",methods=["GET","POST"])
def home():
    if request.method == "GET":
        user_id = session.get('company_id')
        if not user_id:
            return render_template("login.html")
        main_balance = calculate_main_balance(mysql,user_id)
        cur = mysql.connection.cursor()
        cur.execute("select * from Item where company_id=%s",(user_id,))
        item_list = cur.fetchall()
        cur.close()
        return render_template("home.html",item_list = item_list,main_balance=main_balance)

@app.route("/balance",methods=['POST','GET'])
def balance():
    if request.method == 'POST':
        balance = request.form['add_balance']
        user_id = session['company_id']
        cur = mysql.connection.cursor()
        transaction_type = "I"  #I - Initial balance or amount added by user
        cur.execute('insert into Balance(balance,company_id,transaction_type) values(%s,%s,%s)',(balance,user_id,transaction_type))
        mysql.connection.commit()
        flash("Balance is added successfully!","success")
        cur.close()
        return redirect(url_for('home'))
    # return render_template("home.html")

@app.route("/history",methods=["GET","POST"])
def list_history():
    if request.method == 'GET':
        user_id = session['company_id']
        cur = mysql.connection.cursor()
        cur.execute("select * from Purchase where company_id=%s",(user_id,))
        purchase_list = cur.fetchall()
        cur.execute("select * from Sale where company_id=%s",(user_id,))
        sale_list = cur.fetchall()
        cur.close()
        return render_template("history.html",purchase_list=purchase_list,sale_list=sale_list)
    

#calculate profit and loss

if __name__ == '__main__':
    app.run(debug=True)