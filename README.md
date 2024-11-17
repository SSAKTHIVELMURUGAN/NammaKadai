run this command to run the application
 ./env/Scripts/activate
   python app.py

It will run in the port of 5000 link http://localhost:5000
here i use the mysql db

sign up and login page
screenshot24 link - [https://drive.google.com/file/d/1vgINmbq0x3dQ3Oa0tSVLllN3JbUF4SZp/view?usp=sharing]
screenshot 22 - [https://drive.google.com/file/d/1qj_RogBHb1soFGsuLtgIJSVxYUClLjfO/view?usp=sharing]
Note the access code to login, without access code it cant be login

the authentication.py handles the sign up and login management 
it manages as signup
if you already login person try to register or not using the check_email 
if not it show flash message
       flash("Signup successful!.", "success")
      flash(f"Please remember your permanent access code {id}", "info")
for login mamages as
check if the person register or not
and correctly entered the access code, email, password or not 
it show the flash message as 
flash("Invalid Password or access code","error")
flash("Please register it","danger")

the access code will be generate by using the id_generate() by summing the values in email and company name also the email should be unique
with prefix common as "NK" - Eg. (NK11025) where NK - Namma Kaddai

homepage 
screenshot25 - https://drive.google.com/file/d/1fpmUcBWTzA2MevYVeEm2P6_1K6RfqyKZ/view?usp=sharing
screenshot 26 - https://drive.google.com/file/d/1U6eLpxjegc0Ds1UzsocbwO_tSQLcjtdR/view?usp=sharing

in home page there will be add balance for investment it handle by app.py and store in Balance Table in MySQL DB
and displays the flash message as flash("Balance is added successfully!","success")

purchase
screenshot27 https://drive.google.com/file/d/1IIdOmtDeODfF8mM6Y33UWVU3lFF72FyV/view?usp=sharing
screenshot 28 https://drive.google.com/file/d/1Dxe4bSFDKrdgJ0WxlOhc9UDvgswVVFPt/view?usp=sharing
in purchase page you can add the item for purchase and you need to enter the item name quantity and rate for one item 
these logic are manage by the purchase.py
it handles like
the qunatity and rate should not be negative
if main balance goes below zero it show flash message as
flash("Your balance is Zero","warning")

even if the balance goto below the merchant can purchase item because the main objective of this application to be merchant friendly there will be loss or gain but all are need to
tracked so even if the balance is negative it allows to purchase more item
example in bank also there will be negative balance amount it also entered like wise same concept follows here

sale page
screenshot 30 https://drive.google.com/file/d/1YDnIiKQhII0O7MksRjJwQ4A-VxTjprME/view?usp=sharing
screenshot 31 https://drive.google.com/file/d/1JDr9_yavJ8qTzG0FWh9KsW7f4_I-4poe/view?usp=sharing

in sale page it will list all the purchases item and using check box you can select the item and sale that by enter the rate and quantity these will handled by sale.py
it manages to sell by each item we can sale it by the whole item by just click the checkbox of item 
this logic contains the dictornary of these item make store in list using that fetching the item details
here before saleing also check it in the item list and purchases list or not
also it need to enter the qunatity and above zero
also if they entered above the purchased limit  it show the flash message
if all verified it will sale and show flash message as successfully sale

history
screenshot - https://drive.google.com/file/d/1UQWNfpeRPB9hIQFd26hC7JNtutdxSmFl/view?usp=sharing
here it show the purchase and sale history it directly show the transaction details and that will be handled by app.py for list_history() from the purchase and sale table

in home page you can also see the edit/remove option if you did any mistakenly purchase you can use this option to change the rate and quantity will be updated in item table
and balance also changes these will handle by crud.py
if you click delete option it will ask the alert to delete confirm then it will be delted from the item table and balance also will get incremented

there will helper.py this file handles the balance updation on every task of edit, delete, purchase and sale these will be tracked in balance table 

DB Design 
created DB name as NammaKadai

Created table as 
CompanyDetails - store the company name, mail id and password, access code it helps for authentication.py for manageing login and signup here the password is stored in encrypted form;
Item - It store the item only the purchaseing item with corresponding company id who login here the company id is foreign key store secured data;
Balance - It track the every changes in balance helps to helper.py using that it track P,I,S,CRI,CRD,D;
P - Purchase amount
I - Invested amount
S - Saled amount
CRI - edited the rate but it increase from the previous one
CRD -  edited the rate but it decrease from the previous one
D - removed from the item
Purchase - Stores the purchases item with the time stamp, quantity rate and amount will be calculated itself by amount  = qty * rate;
Sale -  Stores the sale item with the time stamp, quantity rate and amount will be calculated itself by amount  = qty * rate;; 

Document to know more my DB plan hand written notes it may be difficult to understand my hand writing soon I will attach a designed database
- document drive link[https://drive.google.com/file/d/1e2NODWadoSpB-w7epCHex0ZmCU4v3YJL/view?usp=sharing]

  By runing my application if you will see in terminal many command running
like this
 "POST /auth/signup HTTP/1.1" 302 -
 "GET / HTTP/1.1" 200 -
 "GET /static/css/login.css HTTP/1.1" 304 -
 "GET /static/css/home.css HTTP/1.1" 304 -

these show as request and response about of HTTPS

- **200 (OK):** Everything is working fine. ✅  
- **302 (Found):** Temporary redirection to another URL.  
- **304 (Not Modified):** Resource hasn’t changed since the last request.  
- **400 (Bad Request):** The server couldn’t understand the request (e.g., invalid syntax).  
- **401 (Unauthorized):** Authentication failed or is required.  
- **404 (Not Found):** The requested resource doesn’t exist.  
- **500 (Internal Server Error):** Something went wrong on the server.  
These codes help identify issues in your app's requests and responses. 😊
