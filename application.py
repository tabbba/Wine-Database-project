import mysql.connector as mysql
from mysql.connector import Error
from getpass import getpass

def connect_to_database(password, db_name='wine_database'):
    try:
        mydb = mysql.connect(host='localhost', user='root', password=password, database=db_name)
        print("Successfully connected to the database.")
        return mydb, mydb.cursor()
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None, None

def get_distinct_values(cursor, column_name, table_name):
    query = f"SELECT DISTINCT {column_name} FROM {table_name} WHERE {column_name} IS NOT NULL ORDER BY {column_name};"
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]

def execute_query(cursor, query, params=None):
    try:
        cursor.execute(query, params)
        return cursor.fetchall()
    except Error as e:
        print(f"Error executing the query: {e}")
        return []

def print_results(rows):
    if not rows:
        print('No results for this query!')
    else:
        for row in rows:
            print(row)

def interactive_queries(cursor, query_n):
    if query_n == 7:
        provinces = get_distinct_values(cursor, 'Province', 'Wine')
        print("Available provinces:")
        for province in provinces:
            print(province)
        user_province = input('Enter the province name from the above list: ')
        user_points = input('Enter the minimum points: ')
        try:
            user_points = int(user_points)
        except ValueError:
            print('Please enter a valid number for points.')
            return
        query = queries[query_n]
        params = (user_province, user_points)
    elif query_n == 8:
        tasters = get_distinct_values(cursor, 'Taster_Name', 'Wine')
        print("Available tasters:")
        for taster in tasters:
            print(taster)
        user_taster = input('Enter the taster name from the above list: ')
        user_min_price = input('Enter the minimum price: ')
        user_max_price = input('Enter the maximum price: ')
        try:
            user_min_price, user_max_price = float(user_min_price), float(user_max_price)
        except ValueError:
            print('Please enter valid numbers for the prices.')
            return
        query = queries[query_n]
        params = (user_taster, user_min_price, user_max_price)
    else:
        return

    rows = execute_query(cursor, query, params)
    print_results(rows)

# Defining queries 
queries = {
    1: "SELECT Country, MAX(Points) AS MaxPoints FROM Wine GROUP BY Country;",
    2: "SELECT Variety, AVG(Price) AS AvgPrice FROM Wine GROUP BY Variety ORDER BY AvgPrice DESC;",
    3: "SELECT Title, Description, Points FROM Wine WHERE Description LIKE '%fruity%' ORDER BY Points DESC LIMIT 10;",
    4: "SELECT Province, COUNT(*) AS NumberOfWines FROM Wine GROUP BY Province ORDER BY NumberOfWines DESC;",
    5: "SELECT Taster_Name, MAX(Price) AS MaxPrice FROM Wine GROUP BY Taster_Name;",
    6: "SELECT Title FROM Wine WHERE Country = 'Italy' AND Price > 100 ORDER BY Points DESC LIMIT 10;",
    7: "SELECT Title, Points FROM Wine WHERE Province = %s AND Points >= %s;",  # Interactive query requiring province and points
    8: "SELECT Title, Price, Points FROM Wine WHERE Taster_Name = %s AND Price BETWEEN %s AND %s ORDER BY Price ASC LIMIT 10;"  # Interactive query requiring taster name and price range
}

queries_type = [
    'Find the highest rated wines for each country',
    'Calculate the average price of wine by variety',
    'List wines with "fruity" in the description, sorted by points',
    'Count the number of wines by province',
    'Find the most expensive wine for each taster',
    'Find the highest rated Italian wines over $100',
    'Find all wines from a specified province with a minimum rating',
    'Display wines within a price range reviewed by a specified taster'
]

# Main application flow
psw = getpass('Insert password for: localhost --> root: ')
mydb, mycursor = connect_to_database(psw)

if mydb and mycursor:
    cont = True
    while cont:
        print('\nWhich type of query would you like to run?')
        print('0) Exit the application')
        for idx, query in enumerate(queries_type, start=1):
            print(f"{idx}) {query}")
        query_n = input('Select a number: ')

        try:
            query_n = int(query_n)
            if 0 < query_n <= len(queries):
                if query_n in [7, 8]:  # Interactive queries
                    interactive_queries(mycursor, query_n)
                else:
                    rows = execute_query(mycursor, queries[query_n])
                    print_results(rows)
            elif query_n == 0:
                cont = False
            else:
                print('Not recognized answer! Please select a valid query number.')
        except ValueError:
            print('Please select a valid number.')

    mycursor.close()
    mydb.close()
    print("MySQL connection is closed")
