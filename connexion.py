#-------------------------------------------------------------
# Author      :   Aliou Mbengue  & Sokhna Ndioba Mbacké Faye
# -------------------------------------------------------------
from library import *


conn = sqlite3.connect ('shop.db')

cur1 = conn.cursor()
create_admin = "CREATE TABLE IF NOT EXISTS admin (my_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,my_name TEXT, my_pass TEXT NOT NULL)"
cur1.execute(create_admin)
cur2 = conn.cursor()
create_customers = "CREATE TABLE IF NOT EXISTS customers (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, phone INTEGER, email TEXT)"
cur2.execute(create_customers)
cur3 = conn.cursor()
create_products = "CREATE TABLE IF NOT EXISTS products (id_product INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name_product TEXT NOT NULL, name_range TEXT NOT NULL,cost INTEGER, date_add TEXT)"
cur3.execute(create_products)
cur4 = conn.cursor()
create_ranges = "CREATE TABLE IF NOT EXISTS ranges (name_range TEXT NOT NULL PRIMARY KEY)"
cur4.execute(create_ranges)
cur5 = conn.cursor()
create_orders = "CREATE TABLE IF NOT EXISTS orders ( id_order INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, id_customer INTEGER NOT NULL, id_product INTEGER NOT NULL, date_order TEXT)"
cur5.execute(create_orders)

conn.commit()
conn.close()
