# Application Overview

```bash
./env/Scripts/activate
python app.py
```

It will run on the port `5000` at [http://localhost:5000](http://localhost:5000).  
Here, I use MySQL as the database.

## Sign-Up and Login Page

![Sign-Up and Login Page](https://drive.google.com/uc?id=1vgINmbq0x3dQ3Oa0tSVLllN3JbUF4SZp)  
![Another Sign-Up Screenshot](https://drive.google.com/uc?id=1qj_RogBHb1soFGsuLtgIJSVxYUClLjfO)  

**Note:** The access code is required to log in. Without the access code, login is not possible.

### Authentication Logic
- **Sign-Up:**  
  - The `authentication.py` script handles sign-up and login management.  
  - If an already-registered person tries to register again, it checks the email using `check_email`.  
  - If not registered, it displays a flash message:  
    - `flash("Signup successful!.", "success")`  
    - `flash(f"Please remember your permanent access code {id}", "info")`

- **Login:**  
  - It checks if the person is registered and verifies the access code, email, and password.  
  - Displays appropriate flash messages:  
    - `flash("Invalid Password or Access Code", "error")`  
    - `flash("Please register", "danger")`

### Access Code Generation
The access code is generated using `id_generate()` by summing the values in the email and company name.  
It must be unique with the prefix "NK" (e.g., `NK11025` where `NK` stands for **Namma Kaddai**).

---

## Home Page

![Home Page Screenshot 1](https://drive.google.com/uc?id=1fpmUcBWTzA2MevYVeEm2P6_1K6RfqyKZ)  
![Home Page Screenshot 2](https://drive.google.com/uc?id=1U6eLpxjegc0Ds1UzsocbwO_tSQLcjtdR)

On the homepage:
- You can add a balance for investment, handled by `app.py` and stored in the `Balance` table in MySQL.  
- Displays a flash message:  
  - `flash("Balance is added successfully!", "success")`

---

## Purchase Page

![Purchase Screenshot 1](https://drive.google.com/uc?id=1IIdOmtDeODfF8mM6Y33UWVU3lFF72FyV)  
![Purchase Screenshot 2](https://drive.google.com/uc?id=1Dxe4bSFDKrdgJ0WxlOhc9UDvgswVVFPt)

On the purchase page:
- Add items by specifying the item name, quantity, and rate.  
- Logic is managed by `purchase.py`:  
  - Quantity and rate cannot be negative.  
  - If the balance goes below zero, it shows a warning:  
    - `flash("Your balance is Zero", "warning")`  
  - Negative balance is allowed for merchants to facilitate tracking (similar to bank overdrafts).

---

## Sale Page

![Sale Page Screenshot 1](https://drive.google.com/uc?id=1YDnIiKQhII0O7MksRjJwQ4A-VxTjprME)  
![Sale Page Screenshot 2](https://drive.google.com/uc?id=1JDr9_yavJ8qTzG0FWh9KsW7f4_I-4poe)

On the sale page:
- List all purchased items.  
- Select items using checkboxes and sell them by entering the rate and quantity.  
- Logic managed by `sale.py`:  
  - Ensures the item exists in both the purchase and item lists.  
  - Quantity must be positive and within the purchased limit.  
  - Displays appropriate flash messages for success or errors.

---

## History Page

![History Screenshot](https://drive.google.com/uc?id=1UQWNfpeRPB9hIQFd26hC7JNtutdxSmFl)
The history page displays purchase and sale transactions, handled by `app.py` using the `list_history()` function from the `Purchase` and `Sale` tables.

---

## Edit/Remove Options

The homepage provides options to edit or remove items if mistakes are made:
- **Edit:**  
  - Updates the rate and quantity in the `Item` table.  
  - Adjusts the balance accordingly.  
  - Handled by `crud.py`.

- **Remove:**  
  - Prompts for confirmation before deletion.  
  - Removes the item from the `Item` table and adjusts the balance.

---

## Helper Script

`helper.py` updates the balance after every action (edit, delete, purchase, and sale) and tracks changes in the `Balance` table.

---

## Database Design

**Database Name:** `NammaKadai`

### Tables:
1. **CompanyDetails:**  
   - Stores company name, email ID, password (encrypted), and access code.  
   - Used for authentication.

2. **Item:**  
   - Stores purchased items with the corresponding company ID (foreign key).

3. **Balance:**  
   - Tracks balance changes (`P`, `I`, `S`, `CRI`, `CRD`, `D`):  
     - `P` - Purchase  
     - `I` - Investment  
     - `S` - Sale  
     - `CRI` - Rate increased during edit  
     - `CRD` - Rate decreased during edit  
     - `D` - Deleted item  

4. **Purchase:**  
   - Stores purchase details with timestamps.

5. **Sale:**  
   - Stores sale details with timestamps.


Handwritten Notes PDF -  https://drive.google.com/file/d/1e2NODWadoSpB-w7epCHex0ZmCU4v3YJL/view?usp=drive_link


---

## Terminal Logs

Sample logs while running the application:
- "POST /auth/signup HTTP/1.1" 302 
- "GET / HTTP/1.1" 200 
- "GET /static/css/login.css HTTP/1.1" 304
- "GET /static/css/home.css HTTP/1.1" 304


### HTTP Status Codes:
- **200 (OK):** Everything is working fine. 
- **302 (Found):** Temporary redirection to another URL.  
- **304 (Not Modified):** Resource hasn’t changed since the last request.  
- **400 (Bad Request):** The server couldn’t understand the request (e.g., invalid syntax).  
- **401 (Unauthorized):** Authentication failed or is required.  
- **404 (Not Found):** The requested resource doesn’t exist.  
- **500 (Internal Server Error):** Something went wrong on the server.  
These codes help identify issues in app requests and responses. 
  
