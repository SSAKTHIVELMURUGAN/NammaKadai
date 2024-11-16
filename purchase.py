from flask import Flask,render_template,Blueprint,session,request, url_for,current_app,redirect,flash
from decimal import Decimal
from helper import calculate_main_balance
purchase = Blueprint('purchase',__name__)

@purchase.route("/purchaseItem",methods=['POST','GET'])
def purchaseItem():
    if request.method == 'POST':
        item_name = request.form['purchase_item_name'].lower()
        qty = request.form['purchase_qty']
        rate  = request.form['purchase_rate']
        amount = int(qty)*int(rate)
        user_id = session['company_id']

        cur = current_app.mysql.connection.cursor()
        # remaining quantity = total purchase qty - total sale qty
        sql = "select IFNULL(sum(quantity), 0) as sum_quantity from Purchase where company_id = %s and purchase_item_name=%s "
        cur.execute(sql,(user_id,item_name)) 
        total_purchase_qty_dict = cur.fetchone()
        total_purchase_qty = total_purchase_qty_dict['sum_quantity']
        sql = "select IFNULL(sum(quantity), 0) as sum_quantity from Sale where company_id = %s and sale_item_name=%s"
        cur.execute(sql,(user_id,item_name)) 
        total_sale_qty_dict = cur.fetchone()
        total_sale_qty = total_sale_qty_dict['sum_quantity']
        remaining_quantity = total_purchase_qty - total_sale_qty

        #check purchase item in item table or not if not add to it
        sql = "select * from Item where item_name=%s"
        cur.execute(sql,(item_name,))
        check_item = cur.fetchone()

        if not check_item:
           sql = "insert into Item(company_id,item_name,remaining_quantity,rate) values(%s,%s,%s,%s)"
           cur.execute(sql,(user_id,item_name,remaining_quantity,rate))
           current_app.mysql.connection.commit()
 
        if int(qty) > 0 and int(rate) > 0:
            #purchase update - qty rate item name
            cur.execute("insert into Purchase(company_id,purchase_item_name,quantity,rate) values(%s,%s,%s,%s)",(user_id,item_name,qty,rate))
            current_app.mysql.connection.commit()
            #item update - balance, profit, loss,remaining_quantity
            remaining_quantity += Decimal(qty)

            cur.execute("update Item set remaining_quantity=%s,rate=%s where company_id=%s and item_name=%s",(remaining_quantity,rate,user_id,item_name))
            current_app.mysql.connection.commit()
            # balance table also need to update
            flash("Purchased successfully","success")

            transaction_type = "P"
            cur.execute("insert into Balance(balance,company_id,transaction_type) values(%s,%s,%s)",(amount,user_id,transaction_type))
            current_app.mysql.connection.commit()
            cur.close()

            balance = calculate_main_balance(current_app.mysql,user_id)
            if balance <= 0:
                flash("Your balance is Zero","warning")
            return redirect(url_for('home'))
        else:
            flash("Please enter rate or quantity atleast one","warning")

    return render_template("purchase.html")