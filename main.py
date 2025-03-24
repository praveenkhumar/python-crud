# Simple CRUD Application with MySQL

import mysql.connector
from mysql.connector import Error
import datetime
import os
from dotenv import load_dotenv


# load environment variables from dotenv
load_dotenv()

class Database:
    def __init__(self):
        #Initialise database connection
        try:
            self.connection = mysql.connector.connect(
                host = os.getenv("DB_HOST","localhost"),
                user = os.getenv("DB_USER","root"),
                password = os.getenv("DB_PASSWORD",""),
                database = os.getenv("DB_NAME","store_db")  
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print("Connected to MySQL database")   
        except Error as e:
            print(f"Error connecting to the mysql database: {e}")
            exit(1)


    def create_tables(self):
        """create tables if they don't exists"""
        try:
            # create users table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # create products table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    price DECIMAL(10, 2) NOT NULL,
                    stock INT NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # create orders table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    status ENUM('pending', 'processing', 'shipped', 'delivered', 'canceled') DEFAULT 'pending',
                    total_amount DECIMAL(10, 2) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)

            # create orders_items table for order details
            self.cursor.execute("""
                 CREATE TABLE IF NOT EXISTS order_items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    order_id INT NOT NULL,
                    product_id INT NOT NULL,
                    quantity INT NOT NULL,
                    price DECIMAL(10, 2) NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
                )   
            """)
            self.connection.commit()
            print("Tables created successfully!")
        except Error as e:
            print(f"Error creating tables: {e}")

    def close(self):
        """close database connection"""
        if hasattr(self,'connection') and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("MySQL connection is closed")


class UserManager:
    def __init__(self,db):
        """Initialise user manager with the database connection"""
        self.db = db
        self.cursor = db.cursor
        self.connection = db.connection
    
    def create_user(self,username,email,password):
        """create a new user"""
        try:
            query="""
                INSERT INTO users(username,email,password)
                VALUES(%s,%s,%s)
        """
            self.cursor.execute(query,(username,email,password))
            self.connection.commit()
            new_user_id = self.cursor.lastrowid
            print(f"User created with ID: {new_user_id}")  # Debugging print
            return new_user_id
        except Error as e:
            print(f"Error creating user: {e}")
            return None
        
    def get_user(self, user_id):
        """Get user by ID"""
        try:
            query = "SELECT * FROM users WHERE id= %s"
            self.cursor.execute(query,(user_id,))
            return self.cursor.fetchone() 
        except Error as e:
            print(f"Error getting the user details: {e}")
            return None
        
    def get_all_users(self):
        """Get all users"""
        try:
            query = "SELECT * FROM users"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching the all users: {e}")
            return []

    def update_user(self, user_id, username=None, email=None, password=None):
        """Updating the user details"""
        try:
            updates = []
            params = []

            if username:
                updates.append("username = %s")
                params.append(username)
            if email:
                updates.append("email = %s")
                params.append(email)
            if password:
                updates.append("password = %s")
                params.append(password)

            if not updates:
                return False

            query = f"UPDATE users SET {','.join(updates)} WHERE id=%s"
            params.append(user_id)

            self.cursor.execute(query, tuple(params))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            print(f"Error updating the details: {e}")
            return False

    def delete_user(self, user_id):
        """Delete the user"""
        try:
            query="DELETE FROM users WHERE id=%s"
            self.cursor.execute(query,(user_id,))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            print(f"Error deleting the user: {e}")
            return False
        
class ProductManager:
    def __init__(self,db):
        """Initializing the db connection for products table"""
        self.db = db
        self.cursor = db.cursor
        self.connection = db.connection
    
    def create_product(self, name, description, price, stock):
        """Creating a new product"""
        try:
            query = """
            INSERT INTO products(name,description,price,stock)
            VALUES(%s,%s,%s,%s)
        """
            self.cursor.execute(query,(name,description,price,stock))
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            print(f"Error creating a product: {e}")
            return None    


    def get_product(self, product_id):
        """Getting the product by Id"""
        try:
            query = "SELECT * FROM products WHERE id= %s"
            self.cursor.execute(query,(product_id,))
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error getting the product: {e}")
            return None    

    def get_all_products(self):
        """Get all the products"""
        try:
            query = "SELECT * FROM products"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching the all products: {e}")
            return []
        
    def update_product(self, product_id, name=None, description=None, price=None, stock=None):
        """Update product information"""
        try:
            updates = []
            params = []
        
            if name:
                updates.append("name = %s")
                params.append(name)
            if description:
                updates.append("description = %s")
                params.append(description)
            if price:
                updates.append("price = %s")
                params.append(price)
            if stock is not None:
                updates.append("stock = %s")
                params.append(stock)
        
            if not updates:
                print("No updates provided")  # Debugging print
                return False  # Nothing to update
        
            query = f"UPDATE products SET {', '.join(updates)} WHERE id = %s"
            params.append(product_id)  # Append product_id to match WHERE condition
        
            # Debugging prints
            print(f"SQL Query: {query}")
            print(f"Params: {tuple(params)}")
        
            self.cursor.execute(query, tuple(params))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            print(f"Error updating the product: {e}")
            return False
  

    def delete_product(self, product_id):
        """Deleting a product by product id"""
        try:
            query = "DELETE FROM products WHERE id=%s"
            self.cursor.execute(query,(product_id,))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            print(f"Error deleting a product: {e}")
            return False  


class OrderManager:
    def __init__(self,db):
        """Initialize the db connection for orders table"""
        self.db = db
        self.cursor = db.cursor
        self.connection = db.connection

    def create_order(self, user_id, items):
        """
        Create a new order
        items: list of dicts with product_id, quantity
        """
        try:
            # Ensure any previous transaction is rolled back before starting a new one
            self.connection.rollback()  # 🔹 Fix: Reset any uncommitted transaction
        
            # Start new transaction
            self.connection.start_transaction()

            # Check if user exists
            self.cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
            if not self.cursor.fetchone():
                print("User not found")
                self.connection.rollback()
                return None
            
            # Calculate total amount and check stock
            total_amount = 0
            order_items = []

            for item in items:
                product_id = item['product_id']
                quantity = item['quantity']

            # Get product details
            self.cursor.execute(
                "SELECT id, price, stock FROM products WHERE id = %s",
                (product_id,)
            )
            product = self.cursor.fetchone()    

            if not product:
                print(f"Product {product_id} not found")
                self.connection.rollback() # Undo everything
                return None
            
            if product['stock'] < quantity:
                print(f"Insufficient stock for the product: {product_id}")
                self.connection.rollback() # Undo everything
                return None
            
            # Update the Stock
            self.cursor.execute(
                "UPDATE products SET stock = stock - %s WHERE id = %s",
                (quantity, product_id)
            )

            # Calculate item total
            item_total = product['price'] * quantity
            total_amount += item_total

            # Add to order items
            order_items.append({
                'product_id': product_id,
                'quantity': quantity,
                'price': product['price']
            })

            # Create order
            self.cursor.execute(
                "INSERT INTO orders (user_id, total_amount) VALUES (%s, %s)",
                (user_id, total_amount)
            )
            order_id = self.cursor.lastrowid

            # Create order items
            for item in order_items:
                self.cursor.execute(
                    """
                    INSERT INTO order_items (order_id, product_id, quantity, price)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (order_id, item['product_id'], item['quantity'], item['price'])
                )
            
            # Commit transaction
            self.connection.commit()
            return order_id
        except Error as e:
            print(f"Error creating order: {e}")
            self.connection.rollback() # Undo everything
            return None
        
    def get_order(self, order_id):
        """Get order by ID with items"""
        try:
            # Get order details
            self.cursor.execute(
                "SELECT * FROM orders WHERE id = %s",
                (order_id,)
            )
            order = self.cursor.fetchone()

            if not order:  # 🔹 Fix: Check if order is None
                print(f"Order with ID {order_id} not found")
                return None
            
            # Get order items
            self.cursor.execute(
                """
                SELECT oi.*, p.name as product_name
                FROM order_items oi
                JOIN products p ON oi.product_id = p.id
                WHERE oi.order_id = %s
                """,
                (order_id,)
            )
            order['items'] = self.cursor.fetchall()
            return order
        except Error as e:
            print(f"Error retrieving order: {e}")
            return None
        
    def get_all_orders(self, user_id=None):
        """Get all orders, optionally filtered by user_id"""
        try:
            if user_id:
                query = "SELECT * FROM orders WHERE user_id = %s ORDER BY created_at DESC"
                self.cursor.execute(query, (user_id,))
            else:
                query = "SELECT * FROM orders ORDER BY created_at DESC"
                self.cursor.execute(query)
            
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error retrieving orders: {e}")
            return []
        
    def update_order_status(self, order_id, status):
        """Update order status"""
        try:
            valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'canceled']
            if status not in valid_statuses:
                print(f"Invalid status: {status}")
                return False
            
            query = "UPDATE orders SET status = %s WHERE id = %s"
            self.cursor.execute(query, (status, order_id))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            print(f"Error updating order status: {e}")
            return False
        
    def delete_order(self, order_id):
        """Delete an order and return items to inventory"""
        try:
            # Start transaction
            self.connection.start_transaction()
            
            # Get order items
            self.cursor.execute(
                "SELECT product_id, quantity FROM order_items WHERE order_id = %s",
                (order_id,)
            )
            items = self.cursor.fetchall()
            
            # Return items to inventory
            for item in items:
                self.cursor.execute(
                    "UPDATE products SET stock = stock + %s WHERE id = %s",
                    (item['quantity'], item['product_id'])
                )
            
            # Delete order (cascade will delete order_items)
            self.cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))
            
            # Commit transaction
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            print(f"Error deleting order: {e}")
            self.connection.rollback()
            return False

# Main application
def main():
    """Main application function"""
    # Initialize database
    db = Database()
    db.create_tables()
    
    # Initialize managers
    user_manager = UserManager(db)
    product_manager = ProductManager(db)
    order_manager = OrderManager(db)

    # Example usage
    def demo():
        # Create users
        print("\n--- Creating Users ---")
        user1_id = user_manager.create_user("john_doe", "john@example.com", "password123")
        user2_id = user_manager.create_user("jane_smith", "jane@example.com", "password456")

        # Create products
        print("\n--- Creating Products ---")
        product1_id = product_manager.create_product("Laptop", "High-performance laptop", 1299.99, 10)
        product2_id = product_manager.create_product("Smartphone", "Latest smartphone model", 799.99, 20)
        product3_id = product_manager.create_product("Headphones", "Noise-cancelling headphones", 199.99, 30)

        # Display all products
        print("\n--- All Products ---")
        products = product_manager.get_all_products()
        for product in products:
            print(f"ID: {product['id']}, Name: {product['name']}, Price: ${product['price']}, Stock: {product['stock']}")

        # Create an order
        print("\n--- Creating Order ---")
        order_items = [
            {"product_id": product1_id, "quantity": 1},
            {"product_id": product3_id, "quantity": 2}
        ]
        order_id = order_manager.create_order(user1_id, order_items)

        # Display order details
        print("\n--- Order Details ---")
        order = order_manager.get_order(order_id)
        print(f"Order ID: {order['id']}, User ID: {order['user_id']}, Total: ${order['total_amount']}")
        print("Items:")
        for item in order['items']:
            print(f"  - {item['product_name']}: {item['quantity']} x ${item['price']}")

        # Update order status
        print("\n--- Updating Order Status ---")
        order_manager.update_order_status(order_id, "processing")
        updated_order = order_manager.get_order(order_id)
        print(f"Updated status: {updated_order['status']}")
        
        # Update product stock
        print("\n--- Updating Product ---")
        product_manager.update_product(product2_id, stock=25)
        updated_product = product_manager.get_product(product2_id)
        print(f"Updated stock for {updated_product['name']}: {updated_product['stock']}")
        
        # Display all users
        print("\n--- All Users ---")
        users = user_manager.get_all_users()
        for user in users:
            print(f"ID: {user['id']}, Username: {user['username']}, Email: {user['email']}")

    # Run demo
    try:
        demo()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close database connection
        db.close()


if __name__ == "__main__":
    main()