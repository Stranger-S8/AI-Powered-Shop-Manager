import mysql.connector
from mysql.connector import Error
import hashlib
import datetime as dt
import pandas as pd

class Database:
    def __init__(self):
        try:
            self.__mydb = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "REDACTED",
                database = "shopmanager"
            )
            if self.__mydb.is_connected():
                print("Connected to the Database")
        except Error as e:
            print(f"Error Connecting to the Database : {e}")
            self.__mydb = None
    
    def execute_query(self, query, params=None):
        try:
            cursor = self.__mydb.cursor()
            cursor.execute(query, params)
            self.__mydb.commit()
            return True
        
        except Error as e:
            print(f"Error Executing Query : {e}")
            return False
        
        finally:
            cursor.close()
        
    def fetch_result(self, query, params=None):
        try:
            cursor = self.__mydb.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Error Executing Query : {e}")
        finally:
            cursor.close()
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def close_connection(self):
        if self.__mydb and self.__mydb.is_connected():
            self.__mydb.close()
            print("Connection to the Database is Closed")
        
class Business_Details:
    
    def register_business(self, db, name, email, password, phone):
        regDate = dt.datetime.now().date()
        password = db.hash_password(password)
        
        query = """INSERT INTO business (b_name, email, password, Phone, reg_date)
                   VALUES (%s, %s, %s, %s, %s)
                   """
        params = (name, email, password, phone, regDate)
        
        result = db.execute_query(query, params)
    
        if result:
            return True
        else:
            return False

    def login_business(self, email, password, db):
        
        password = db.hash_password(password)
        query = """SELECT b_id
                   FROM business 
                   WHERE email = %s and password = %s"""
        
        params = (email, password)
        
        result = db.fetch_result(query, params)
        
        if result:
            return result
        else:
            return None
    
    def get_business_name(self, email, password, db):
        
        password = db.hash_password(password)
        query = """SELECT b_name
                   FROM business 
                   WHERE email = %s and password = %s"""
        
        params = (email, password)
        
        result = db.fetch_result(query, params)
        
        if result[0][0]:
            return result[0][0]
        else:
            return
    
    def get_business_details(self, db):
        query = """SELECT * FROM business"""
        result = db.fetch_result(query)
        
        if result:
            return result
        else:
            return 
    
    def business_exist(self, db, email):
        query = """SELECT b_id FROM business
                   WHERE email=%s"""
        params = (email,)

        result = db.fetch_result(query, params)
        
        if result:
            return True
        else:
            return False
    
    def update_name_fn(self, db, new_name, email, password):
        id = self.login_business(email, password, db)
        query = """UPDATE business
                   SET b_name = %s
                   WHERE b_id = %s"""
        
        params = (new_name, id[0][0])

        result = db.execute_query(query, params)

        if result:
            return True
        else:
            return False
    
    def update_password_fn(self, db, new_pass, email, password):
        id = self.login_business(email, password, db)
        query = """UPDATE business
                   SET password = %s
                   WHERE b_id = %s"""
        
        new_pass = db.hash_password(new_pass)
        params = (new_pass, id[0][0])

        result = db.execute_query(query, params)

        if result:
            return True
        else:
            return False
        
class Customer_Details:


    def register_customer(self, db, name, cnic, email, phone):
        regDate = dt.datetime.now().date()
        
        query = """INSERT INTO customerdetails (name, cnic, email, phone, reg_date)
                   VALUES (%s, %s, %s, %s, %s)
                   """
        params = (name, cnic, email, phone, regDate)
        
        result = db.execute_query(query, params)
        if result:
            return True
        else:
            return False
        
    def get_customer_details(self, db, id=0):
        if id == 0:
            query = """SELECT * FROM customerdetails ORDER BY c_id ASC"""
            
            result = db.fetch_result(query)
        else:
            query = """SELECT * FROM customerdetails
                       WHERE c_id = %s"""
            
            result = db.fetch_result(query, (id, ))

        if result:
            return result
        else:
            return
    
    def delete_customer(self, db, id):
        query = """DELETE FROM customerdetails
                   WHERE c_id=%s"""
        params = (id, )
        
        result = db.execute_query(query, params)
        if result:
            return True
        else:
            return False
    
    def alter_customer_info(self, db, id, **kwargs):
        for key,value in kwargs.items():
            query = f"""UPDATE customerdetails
                        SET {key} = %s
                        WHERE c_id = %s"""
            result = db.execute_query(query, (value, id))
        if result:
            return True
        else:
            return False

class Products:
    
    def add_category(self, category_name, description, db):
        query = """INSERT INTO category (category_name, description)
                   VALUES (%s, %s, %s)"""
        params = (category_name, description)
        
        result = db.execute_query(query, params)
        if result:
            return True
        else:
            return False
        
    def add_product(self, db, name, price, stocklevel, category_id):
        query = """INSERT INTO products (name, price, stocklevel, category_id)
                   VALUES (%s, %s, %s, %s)"""
        params = (name, price, stocklevel, category_id)
        
        result = db.execute_query(query, params)
        if result:
            return True
        else:
            return False
    
    def get_category_details(self, db, desire, name):
        query = f"SELECT {desire} FROM category WHERE category_name = %s"
        
        result = db.fetch_result(query, (name,))
        if result:
            return result
        else:
            return
    
    def get_product_details(self, db, id=0):
        if id == 0:
            query = """SELECT p.p_id, p.name, p.price, p.stocklevel, c.category_name 
                    FROM products p
                    INNER JOIN category c
                    ON p.category_id = c.id
                    ORDER BY p.p_id ASC
                    """
            params = None
        else:
            query = """SELECT p.p_id, p.name, p.price, p.stocklevel, c.category_name 
                    FROM products p
                    INNER JOIN category c
                    ON p.category_id = c.id
                    WHERE p.p_id = %s
                    ORDER BY p.p_id ASC
                    """
            params = (id, )

        result = db.fetch_result(query, params)
        if result:
            return result
        else:
            return
    
    def delete_product(self, db, id):
        query = """DELETE FROM products
                   WHERE p_id=%s"""
        params = (id, )
        
        result = db.execute_query(query, params)
        if result:
            return True
        else:
            return False
    
    def alter_product(self, db, id, **kwargs):
        for key,value in kwargs.items():
            query = f"""UPDATE products
                        SET {key} = %s
                        WHERE p_id = %s"""
            result = db.execute_query(query, (value, id))
        if result:
            return True
        else:
            return False
    
class Orders:
    
    def place_order(self, db, cus_id,  total_amount):
        self.order_date = dt.datetime.now().date()
        self.order_time = dt.datetime.now().time().strftime("%I : %M : %S %p")
        
        query = """INSERT INTO orders (cus_id, ord_date, ord_time, total_amount)
                   VALUES (%s, %s, %s, %s)"""
        params = (cus_id, self.order_date, self.order_time, total_amount)
        
        result = db.execute_query(query, params) 
        if result:
            return True
        else:
            return False
    
    def check_stocks_fn(self, db, id, quan):
        query = """SELECT stocklevel FROM products
                   WHERE p_id = %s"""
        params = (id, )

        result = db.fetch_result(query, params)
 
        if result[0][0]:
            stock = result[0][0] - quan
            if stock >= 0:
                return True
            else:
                return False
        else:
            return False
    
    def update_stocks_fn(self, db, id, quan):
        query = """SELECT stocklevel FROM products
                   WHERE p_id = %s"""
        params = (id, )

        result = db.fetch_result(query, params)
 
        if result[0][0]:
            stock = result[0][0] - quan
            sub_query = """UPDATE products 
                        SET stocklevel = %s
                        WHERE p_id = %s"""
            params1 = (stock, id)

            sub_result = db.execute_query(sub_query, params1)

            if sub_result:
                return True
            else:
                return False
        else:
            return False
            
    def place_orderDetails(self, db, cus_id, p_id, quantity, total_amount):

        order_query = """SELECT o_id FROM orders
                         WHERE cus_id=%s AND ord_date=%s AND ord_time=%s AND total_amount=%s"""
        params = (cus_id, self.order_date, self.order_time, total_amount)
        result = db.fetch_result(order_query, params)
        
        if result:
            order_id = result[0][0]
            orderItem_query = """INSERT INTO orderdetails (o_id, p_id, quantity)
                                 VALUES (%s, %s, %s)"""
            orderItem_params = (order_id, p_id, quantity)
            result1 = db.execute_query(orderItem_query, orderItem_params)
            
                    
    def get_order_details(self, db, id=0, check_value=0, sub_check=0):
        params = None

        if sub_check == 0:
            if check_value == 0:
                query = """SELECT* FROM orders"""
            else:
                query = """SELECT* FROM orderdetails"""
        else:
            if check_value == 0:
                query = """SELECT* FROM orders
                           WHERE o_id = %s"""
            else:
                query = """SELECT* FROM orderdetails
                           WHERE id = %s"""
            params=(id, )
        
        
        result = db.fetch_result(query, params)
        
        if result:
            return result
        else:
            return 
    
    def Model_Sales_Data_fn(self, db):
        query = """SELECT
                        o.ord_date,
                        o.ord_time,
                        od.p_id,
                        SUM(od.quantity) AS quantity_sold,
                        SUM(od.quantity * p.price) AS total_sales
                   FROM orders o
                   JOIN orderdetails od ON o.o_id = od.o_id
                   JOIN products p ON od.p_id = p.p_id
                   GROUP BY o.ord_date, od.p_id, o.ord_time"""
        
        result = db.fetch_result(query)

        if result:
            df = pd.DataFrame(result, columns=["ord_date", "ord_time", "p_id", "quantity_sold", "total_sales"])
            df.to_csv("data/Sales Data/sales_data.csv", index=False)
            return True
        else:
            return False
    