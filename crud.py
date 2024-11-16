from flask import Flask,render_template,Blueprint,session,request, url_for,current_app,redirect,flash
from helper import calculate_main_balance
from decimal import Decimal

crud = Blueprint('crud',__name__)

@crud.route("/edit/<item_name>",methods=['POST','GET'])
def edit_operation(item_name):
    if request.method == "POST":
        name= request.form['item_name'].lower()
        new_qty = request.form['qty']
        new_rate = request.form['rate']
        user_id = session['company_id']
        cur = current_app.mysql.connection.cursor()

        #if qty change balance + qty --> item table, balance
        # if rate change balance+rate --> item table, balance
        
        # change in quantiy -- decrease
        # balance = I - P + S + C
        # new qty =  old-qty - new-qty --> new amount = new qty * rate --> bal += new amount
        cur.execute("select * from Item where item_name=%s and company_id=%s",(name,user_id,))
        old_qty_list = cur.fetchone()
        old_qty = old_qty_list['remaining_quantity']
        old_rate = old_qty_list['rate']
        changed_qty = Decimal(old_qty) - Decimal(new_qty)
        new_amount = changed_qty * Decimal(old_rate)

        # if quanity change 
        if Decimal(new_qty) < Decimal(old_qty):
        # insert in balance
            transaction_type = "CQ"  #change qty - cq
            cur.execute("insert into Balance(balance,company_id,transaction_type) values(%s,%s,%s)",(new_amount,user_id,transaction_type))
            current_app.mysql.connection.commit()

            #change in quantity and update in item table
            cur.execute("update Item set remaining_quantity=%s where company_id=%s and item_name=%s",(new_qty,user_id,name,))
            current_app.mysql.connection.commit()

            flash("Changes in Quantity Done", "success")
            return redirect(url_for('home'))
        
        if Decimal(new_qty) > Decimal(old_qty):
            flash("You can directly purchase it from Purchase Option","warning")
            main_balance = calculate_main_balance(current_app.mysql,user_id)
            return redirect(url_for('home', main_balance=main_balance))

        if Decimal(old_rate) > Decimal(new_rate):
        # insert in balance - change in rate
            changed_rate = Decimal(old_rate) - Decimal(new_rate)
            new_amount = Decimal(changed_rate) * Decimal(new_qty)

            transaction_type = "CRD"   # crd = change in rate decrease
            cur.execute("insert into Balance(balance,company_id,transaction_type) values(%s,%s,%s)",(new_amount,user_id,transaction_type))
            current_app.mysql.connection.commit()

            # changes need to update in item table
            cur.execute("update Item set rate=%s where company_id=%s and item_name=%s",(new_rate,user_id,name,))
            current_app.mysql.connection.commit()

            flash("Changes Done in rate - Rate is reduced", "success")
            return redirect(url_for('home'))
        
        if Decimal(old_rate) < Decimal(new_rate):
        # insert in balance - change in rate
            changed_rate = Decimal(new_rate) - Decimal(old_rate)
            new_amount = Decimal(changed_rate) * Decimal(new_qty)

            transaction_type = "CRI"  # cri = change in rate increase
            cur.execute("insert into Balance(balance,company_id,transaction_type) values(%s,%s,%s)",(new_amount,user_id,transaction_type))
            current_app.mysql.connection.commit()

            # changes need to update in item table
            cur.execute("update Item set rate=%s where company_id=%s and item_name=%s",(new_rate,user_id,name,))
            current_app.mysql.connection.commit()
            flash("Changes Done in rate - Rate is increased","success")
            return redirect(url_for('home'))
        
        cur.close()
        return redirect(url_for('home'))
    cur = current_app.mysql.connection.cursor()
    user_id = session['company_id']
    cur.execute("select * from Item where company_id=%s and item_name=%s",(user_id,item_name,))
    item = cur.fetchone()
    return render_template("crud.html",item=item) 

@crud.route("/delete/<string:item_name>",methods=['POST','GET'])
def delete_operation(item_name):
    if request.method == "POST":
        user_id = session['company_id']
        cur = current_app.mysql.connection.cursor()
        #if delte the item need to update the balance based on its remaining quanity and rate
        cur.execute("select * from Item where item_name=%s and company_id=%s",(item_name,user_id,))
        item_list = cur.fetchone()
        new_amount = item_list['remaining_quantity'] * item_list['rate']

        transaction_type = "D"
        cur.execute("insert into Balance(balance,company_id,transaction_type) values(%s,%s,%s)",(new_amount,user_id,transaction_type))
        current_app.mysql.connection.commit()

        # remove from item table
        cur.execute("delete from Item where item_name=%s and company_id=%s",(item_name,user_id,))
        current_app.mysql.connection.commit()  
        cur.close()
        flash("Item deleted successfully!", "success")
        return redirect(url_for('home'))
    return redirect(url_for('home')) 