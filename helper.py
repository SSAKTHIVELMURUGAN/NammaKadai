# No changec occur
def calculate_main_balance(mysql,user_id):
        transaction_purchase = "P"
        transaction_sale = "S"
        transaction_invest = "I"
        cur = mysql.connection.cursor()
        cur.execute("select sum(balance) as total_balance from Balance where company_id=%s and transaction_type=%s",(user_id,transaction_purchase))
        total_purchase_dict = cur.fetchone()
        if total_purchase_dict['total_balance'] is not None:
            total_purchase = total_purchase_dict['total_balance']
        else:
            total_purchase = 0

        cur.execute("select sum(balance) as total_balance from Balance where company_id=%s and transaction_type=%s",(user_id,transaction_sale))
        total_sale_dict = cur.fetchone()
        
        if total_sale_dict['total_balance'] is not None:
            total_sale = total_sale_dict['total_balance']
        else:
           total_sale= 0

        cur.execute("select sum(balance) as total_balance from Balance where company_id=%s and transaction_type=%s",(user_id,transaction_invest))
        total_invest_dict = cur.fetchone()
        
        if total_invest_dict['total_balance'] is not None:
            total_invest = total_invest_dict['total_balance']
        else:
            total_invest=0

        transaction_change_qty = "CQ"
        cur.execute("select sum(balance) as total_balance from Balance where company_id=%s and transaction_type=%s",(user_id,transaction_change_qty))
        total_change_dict_qty = cur.fetchone()

        if total_change_dict_qty['total_balance'] is not None:
            total_change_qty = total_change_dict_qty['total_balance']
        else:
            total_change_qty=0

        transaction_change_rate_decrease = "CRD"
        cur.execute("select sum(balance) as total_balance from Balance where company_id=%s and transaction_type=%s",(user_id,transaction_change_rate_decrease))
        total_change_dict_rd = cur.fetchone()

        if total_change_dict_rd['total_balance'] is not None:
            total_change_rate_decrease = total_change_dict_rd['total_balance']
        else:
            total_change_rate_decrease=0       

        transaction_change_rate_increase = "CRI"
        cur.execute("select sum(balance) as total_balance from Balance where company_id=%s and transaction_type=%s",(user_id,transaction_change_rate_increase))
        total_change_dict_ri = cur.fetchone()

        if total_change_dict_ri['total_balance'] is not None:
            total_change_rate_increase = total_change_dict_ri['total_balance']
        else:
            total_change_rate_increase=0

        transaction_change_delete = "D"  # change the delete
        cur.execute("select sum(balance) as total_balance from Balance where company_id=%s and transaction_type=%s",(user_id,transaction_change_delete))
        total_change_dict_d = cur.fetchone()

        if total_change_dict_d['total_balance'] is not None:
            total_change_delete = total_change_dict_d['total_balance']
        else:
            total_change_delete=0

        main_balance = total_invest - total_purchase + total_sale + total_change_qty + total_change_rate_decrease - total_change_rate_increase + total_change_delete

        return main_balance