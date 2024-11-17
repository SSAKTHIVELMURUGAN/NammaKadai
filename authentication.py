from flask import Flask,render_template,Blueprint,session,request, url_for,current_app,redirect,flash
from werkzeug.security import generate_password_hash, check_password_hash
authentication = Blueprint('authentication',__name__)

@authentication.route("/signup",methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        #getting data from signup
        name = request.form['company_name']
        email = request.form['company_email']
        password = generate_password_hash(request.form['company_password'])

        # store in db in company details
        cur = current_app.mysql.connection.cursor()

        sql = "select email_id from CompanyDetails where email_id=%s"
        cur.execute(sql,(email,))
        check_email = cur.fetchone()

        if check_email:     
            #already register person try to register again 
            flash("Already registered. please login!","warning")
            return redirect(url_for('authentication.login'))
        
        #not login - new user
        id = id_generate()
        sql = "insert  into CompanyDetails (company_id,company_name,email_id,password_hash,access_code) values (%s,%s,%s,%s,%s)"
        cur.execute(sql,(id,name,email,password,id,))
        current_app.mysql.connection.commit()
        cur.close()
        flash("Signup successful!.", "success")
        flash(f"Please remember your permanent access code {id}", "info")
        return redirect(url_for('home')) 
   
    return render_template('signup.html')

@authentication.route("/login",methods=['POST','GET'])
def login():
    if request.method == "POST":
        access_code = request.form['company_access_code']
        email = request.form['company_email']
        password = request.form['company_password']

        #check user is register or not
        cur = current_app.mysql.connection.cursor()
        sql = "select email_id,password_hash,access_code,company_id,company_name from CompanyDetails where email_id=%s"
        cur.execute(sql,(email,))
        check_user = cur.fetchone()
        cur.close()

        if check_user:
            if check_password_hash(check_user['password_hash'],password) and check_user['access_code'] == access_code:
                #setting session to login person
                session['company_id'] = check_user['company_id']
                session['company_name'] = check_user['company_name']
                flash("Login successful!","success")
                return redirect(url_for('home'))
            else:
                flash("Invalid Password or access code","error")
        else:
            # new user not registered but try to login
            flash("Please register it","danger")

    return render_template('login.html')

@authentication.route("/logout")
def logout():
    if request.method == "GET":
        session.clear()
        flash("Logged out successfully","info")
        return redirect(url_for('authentication.login'))

def id_generate():
    str1 = "NK"
    email = request.form['company_email']
    name = request.form['company_name']
    val= sum(ord(c) for c in email)
    val= sum(ord(c) for c in name)
    companyId = str1+str(val)
    return companyId