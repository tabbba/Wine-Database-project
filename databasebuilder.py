import mysql.connector as mysql
from mysql.connector import Error
import pandas as pd
import getpass
from rich.console import Console
from rich import print
import time

# Initialize Rich console
console = Console()

# Disable chained assignment warning
pd.options.mode.chained_assignment = None

def create_database(db, cursor, db_name: str):
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        console.print(f"\n[bold green]Database '{db_name}' is created or already exists!")
    except Error as err:
        console.print(f"[bold red]Failed to create database '{db_name}': {err}")
        return False
    return True

def create_tables(db, cursor, db_name: str):
    try:
        cursor.execute(f"USE {db_name}")
        table_creation_query = """
        CREATE TABLE IF NOT EXISTS wines (
            id INT AUTO_INCREMENT PRIMARY KEY,
            wine_name VARCHAR(255),
            country VARCHAR(255),
            description TEXT,
            points INT,
            price DECIMAL(10, 2),
            province VARCHAR(255),
            variety VARCHAR(255),
            winery VARCHAR(255)
        )"""
        cursor.execute(table_creation_query)
        console.print("\n[bold green]Table 'wines' is created or already exists!")
    except Error as err:
        console.print(f"[bold red]Failed to create tables: {err}")
        return False
    return True

def load_data_to_database(db, cursor, db_name: str, data_file: str):
    wine_df = pd.read_csv(data_file)
    try:
        for _, row in wine_df.iterrows():
            cursor.execute("INSERT INTO wines (wine_name, country, description, points, price, province, variety, winery) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                           (row['title'], row['country'], row['description'], row['points'], row['price'], row['province'], row['variety'], row['winery']))
        db.commit()
        console.print("[bold green]Data loaded into the database successfully!")
    except Error as err:
        console.print(f"[bold red]Error loading data into the database: {err}")
        return False
    return True

if __name__ == '__main__':
    user = 'root'
    password = getpass.getpass('Insert password for: localhost --> root: ')
    db_name = 'wine_database'

    try:
        db = mysql.connect(host='localhost', user=user, password=password)
        cursor = db.cursor()
        if create_database(db, cursor, db_name) and create_tables(db, cursor, db_name):
            load_data_to_database(db, cursor, db_name, 'winemag-data-130k-v2.csv')
    except Error as e:
        console.print(f"[bold red]Error while connecting to MySQL: {e}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

