# Setup Instructions for MySQL CRUD Application

## Prerequisites

- Python 3.6 or higher
- MySQL database server

## Step 1: Set Up Virtual Environment (Optional but Recommended)

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

## Step 2: Install Required Packages

```bash
pip install mysql-connector-python python-dotenv
```

## Step 3: Create MySQL Database

1. Log in to MySQL server:

```bash
mysql -u root -p
```

2. Create a new database:

```sql
CREATE DATABASE store_db;
```

3. Create a new user (optional):

```sql
CREATE USER 'store_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON store_db.* TO 'store_user'@'localhost';
FLUSH PRIVILEGES;
```

## Step 4: Configure Environment Variables

Create a `.env` file in your project directory with the following content:

```
DB_HOST=localhost
DB_USER=store_user  # or root
DB_PASSWORD=your_password
DB_NAME=store_db
```

## Step 5: Run the Application

```bash
python main.py
```

## Database Schema

This application uses the following tables:

1. `users` - Store user information

   - id (Primary Key)
   - username (Unique)
   - email (Unique)
   - password
   - created_at

2. `products` - Store product information

   - id (Primary Key)
   - name
   - description
   - price
   - stock
   - created_at

3. `orders` - Store order information

   - id (Primary Key)
   - user_id (Foreign Key)
   - status
   - total_amount
   - created_at

4. `order_items` - Store order items
   - id (Primary Key)
   - order_id (Foreign Key)
   - product_id (Foreign Key)
   - quantity
   - price

## Extending the Application

You can extend this application by:

1. Adding authentication with password hashing
2. Creating a web interface using a framework like Flask or Django
3. Implementing search functionality for products
4. Adding payment processing capabilities
5. Creating reports and analytics
