from flask import Flask,render_template,Blueprint,session,request, url_for,current_app,redirect,flash
from decimal import Decimal
from helper import calculate_main_balance

sale = Blueprint('sale',__name__)

@sale.route("/saleItem",methods=['POST','GET'])
def saleItem():
    user_id = session.get('company_id')  # Ensure the user is logged in
    cur = current_app.mysql.connection.cursor()

    # Fetch items for rendering in the template
    cur.execute("SELECT * FROM Item WHERE company_id = %s", (user_id,))
    item_list = cur.fetchall()

    if request.method == 'POST':
        sale_sucess = False
        sale_item = []
        # Iterate through item_list to process only selected items
        for item in item_list:
            checkbox_value = request.form.get(f"item_{item['item_id']}")  # Check if the item is selected
            if checkbox_value:
                for item in item_list:
                    sale_qty = request.form.get(f"sale_qty{item['item_id']}")
                    sale_rate = request.form.get(f"sale_rate{item['item_id']}")
                    if sale_qty and sale_rate:
                        sale_qty = Decimal(sale_qty)
                        sale_rate = Decimal(sale_rate)
                        sale_item.append({
                        "item_id": item['item_id'],
                        "item_name": item["item_name"],
                        "sale_qty": Decimal(sale_qty),
                        "sale_rate": Decimal(sale_rate),
                        })
                        for sale in sale_item:
                            item_name = sale["item_name"].lower()
                            qty = sale["sale_qty"]
                            rate = sale["sale_rate"]
                            amount = Decimal(qty)*Decimal(rate)

                            user_id = session['company_id']
                            #check if the item in purchase db or not 
                            sql = "select * from Purchase where purchase_item_name=%s"
                            cur.execute(sql,(item_name,))
                            sale_check_item = cur.fetchone()

                            cur.execute("select * from Item where item_name=%s and company_id=%s",(item_name,user_id,))
                            item_check = cur.fetchone()
                        if sale_check_item and item_check:
                            if int(qty) > 0 and int(rate) > 0 :
                                #check for quantity to sale within the purchase limit
                                cur.execute("select remaining_quantity from Item where item_name=%s and company_id=%s",(item_name,user_id))
                                item_qty_dict = cur.fetchone()
                                purchased_qty = item_qty_dict['remaining_quantity']
                                saled_qty = int(purchased_qty) - int(qty)
                                if int(purchased_qty) >= int(qty):
                                    # add to sale db
                                    cur.execute("insert into Sale(company_id,sale_item_name,quantity,rate) values(%s,%s,%s,%s)",(user_id,item_name,qty,rate))
                                    current_app.mysql.connection.commit()

                                    # balance add, item table, qty, profit, loss, amount 
                                    sale_sucess = True
                                    # balance table also need to update
                                    transaction_type = "S"
                                    cur.execute("insert into Balance(balance,company_id,transaction_type) values(%s,%s,%s)",(amount,user_id,transaction_type))
                                    current_app.mysql.connection.commit()

                                    #update in item to remaining quantity
                                    cur.execute("update Item set remaining_quantity=%s where company_id=%s and item_name=%s",(saled_qty,user_id,item_name))
                                    current_app.mysql.connection.commit()
                                else:
                                    flash("Please sale the item with in the purchase limit","danger")
                            else:
                                flash("Please enter rate or quantity atleast one","warning")
                        else:
                        #if not in purchase
                            flash("Please purchase it","warning")
            else:
                flash("Please click atleast any one item")
            
        if sale_sucess:
            flash("Saled successfully","success")
            return redirect(url_for('sale.saleItem'))
        
        
    user_id = session.get('company_id')
    cur = current_app.mysql.connection.cursor()
    cur.execute("select * from Item where company_id=%s",(user_id,))
    item_list = cur.fetchall()
    cur.close()
    return render_template("sale.html",item_list = item_list)
