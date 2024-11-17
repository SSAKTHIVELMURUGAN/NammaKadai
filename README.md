# Namma Kadai Application

## Running the Application

To run the application, use the following commands:

```bash
./env/Scripts/activate
python app.py
```
The application will run on port 5000. You can access it at http://localhost:5000.

This application uses MySQL as the database.

### Features
Authentication: Sign-Up and Login
The authentication process is handled by authentication.py.
Key functionalities include:
Sign-Up:
Ensures the email is unique using check_email.
Displays the following flash messages:
flash("Signup successful!", "success")
flash("Please remember your permanent access code {id}", "info")
Login:
Verifies the email, password, and access code.
Flash messages:
flash("Invalid Password or Access Code", "error")
flash("Please register", "danger")
Note:
The access code is generated using id_generate() by summing values in the email and company name.
The access code is prefixed with "NK" (e.g., NK11025, where NK stands for "Namma Kadai").

Screenshots:
![screenshot24](https://drive.google.com/file/d/1vgINmbq0x3dQ3Oa0tSVLllN3JbUF4SZp/view?usp=sharing)
![screenshot22](https://drive.google.com/file/d/1qj_RogBHb1soFGsuLtgIJSVxYUClLjfO/view?usp=sharing)

Home Page
The home page allows users to add balance for investment.

Managed by app.py and stored in the Balance Table (MySQL).
Flash message: flash("Balance is added successfully!", "success")
Screenshots:

Purchase Page
The purchase page allows users to add items for purchase.
Users need to enter the item name, quantity, and rate per item.
This functionality is handled by purchase.py.

Validations:
Quantity and rate cannot be negative.
If the balance goes below zero, a warning is displayed:
flash("Your balance is Zero", "warning")
The system allows merchants to purchase items even if the balance is negative, ensuring merchant-friendly functionality.

Screenshots:

Sale Page
The sale page lists all purchased items. Users can:

Select items using checkboxes.
Enter the rate and quantity for sale.
Key features:

Validates that items exist in the purchased list.
Ensures the quantity is above zero and doesn’t exceed purchased limits.
If valid, completes the sale and displays:
flash("Successfully sold!", "success")
Screenshots:

History Page
The history page displays purchase and sale transaction details.
This functionality is managed by list_history() in app.py.

Screenshot:

Edit and Remove Options
The home page includes options to edit or remove items:

Edit: Updates item rate and quantity in the Item Table.
Balance changes are tracked.
Remove: Deletes the item from the table and increments the balance.
These features are managed by crud.py.

Helper Functions
helper.py manages balance updates for tasks like:

Edit
Delete
Purchase
Sale
Balance changes are tracked in the Balance Table.

Database Design
The application uses a MySQL database named NammaKadai.

Tables:
CompanyDetails:

Stores company name, email, password (encrypted), and access code.
Used for authentication.
Item:

Stores purchased items linked to a company (foreign key).
Balance:

Tracks balance changes with codes:
P: Purchase
I: Invested
S: Sale
CRI: Rate increased during edit
CRD: Rate decreased during edit
D: Item removed
Purchase:

Stores purchase details (timestamp, quantity, rate, amount).
Sale:

Stores sale details (timestamp, quantity, rate, amount).
Handwritten Database Design:

Understanding Terminal Logs
During execution, the terminal logs HTTP requests and responses, like:

POST /auth/signup HTTP/1.1" 302 -
GET / HTTP/1.1" 200 -
GET /static/css/login.css HTTP/1.1" 304 -
HTTP Status Codes:
200 (OK): Request was successful. ✅
302 (Found): Temporary redirection.
304 (Not Modified): Cached resource unchanged.
400 (Bad Request): Invalid request syntax.
401 (Unauthorized): Authentication failed.
404 (Not Found): Resource doesn’t exist.
500 (Internal Server Error): Server-side issue.
These logs are helpful for debugging and ensuring proper app functionality. 
 
