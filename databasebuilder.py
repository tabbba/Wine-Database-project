import pandas as pd
import mysql.connector as mysql
from mysql.connector import Error

wine_df = pd.read_csv('winemag-data-130k-v2.csv')

psw = input('Insert password for: localhost --> root: ')
db_name = 'wine_database'

try:
    mydb = mysql.connect(host='localhost', user='root', password=psw)
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS " + db_name)
    print("Database is created or already exists!")
    
    mycursor.execute("USE " + db_name)
    mycursor.execute('''
        CREATE TABLE IF NOT EXISTS Wine (
            Country VARCHAR(255),
            Description TEXT,
            Designation VARCHAR(255),
            Points INT,
            Price DECIMAL(10, 2),
            Province VARCHAR(255),
            Region_1 VARCHAR(255),
            Region_2 VARCHAR(255),
            Taster_Name VARCHAR(255),
            Taster_Twitter_Handle VARCHAR(255),
            Title VARCHAR(1000),
            Variety VARCHAR(255),
            Winery VARCHAR(255)
        );
    ''')
    print("Table is created or already exists!")

    for i, row in wine_df.iterrows():
        sql = """
        INSERT INTO Wine (Country, Description, Designation, Points, Price, Province, Region_1, Region_2, Taster_Name, Taster_Twitter_Handle, Title, Variety, Winery)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        mycursor.execute(sql, (row['country'], row['description'], row['designation'], row['points'], row['price'], row['province'], row['region_1'], row['region_2'], row['taster_name'], row['taster_twitter_handle'], row['title'], row['variety'], row['winery']))
        if i % 1000 == 0:  # commit every 1000 inserts
            mydb.commit()

    mydb.commit()  # final commit for any remaining rows
    print('Database correctly filled!')
except Error as e:
    print("Error occurred:", e)
finally:
    if mydb.is_connected():
        mycursor.close()
        mydb.close()
        print("MySQL connection is closed")
