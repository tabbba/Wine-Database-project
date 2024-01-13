import mysql.connector as mysql
from mysql.connector import Error

psw = input('Insert password for: localhost --> root: ')
db_name = 'wine_database'
try:
    mydb = mysql.connect(host='localhost', user='root', password=psw)
    if mydb.is_connected():
        mycursor = mydb.cursor()
        mycursor.execute('USE ' + db_name)
        mydb.commit()
except Error as e:
     print("Error while connecting to MySQL", e)

queries = {
    1: '''
    SELECT w1.Country, 
           w1.MaxPoints, 
           w2.Title, 
           w2.Winery
    FROM (
        SELECT Country, MAX(Points) AS MaxPoints
        FROM Wine
        GROUP BY Country
    ) AS w1
    JOIN Wine w2 ON w1.Country = w2.Country AND w1.MaxPoints = w2.Points;
    ''',
    2: "SELECT Variety, AVG(Price) AS AvgPrice FROM Wine WHERE Price IS NOT NULL GROUP BY Variety ORDER BY AvgPrice DESC;",
    3: "SELECT Title, Description, Points FROM Wine WHERE Description LIKE '%fruity%' ORDER BY Points DESC LIMIT 10;",
    4: "SELECT Province, COUNT(*) AS NumberOfWines FROM Wine GROUP BY Province ORDER BY NumberOfWines DESC;",
    5: '''
    SELECT 
  w1.Taster_Name, 
  w1.MaxPrice, 
  w2.Title, 
  w2.Winery
FROM (
  SELECT 
    Taster_Name, 
    MAX(Price) AS MaxPrice
  FROM 
    Wine
  GROUP BY 
    Taster_Name
) AS w1
JOIN Wine w2 ON w1.Taster_Name = w2.Taster_Name AND w1.MaxPrice = w2.Price;
'''
}

queries_type = [
    '1) Find the highest rated wines for each country',
    '2) Calculate the average price of wine by variety',
    '3) List wines with "fruity" in the description, sorted by points',
    '4) Count the number of wines by province',
    '5) Find the most expensive wine for each taster'
]

cont = True
while cont:

    print('\nWhich type of query would you like to run?')
    print('0) No one: quit application')
    for query in queries_type:
        print(query)
    query_n = input('Select a number: ')
    try:
        query_n = int(query_n)
        if 0 < query_n <= len(queries):
            # Execute the selected query
            mycursor.execute(queries[query_n])
            rows = mycursor.fetchall()
            if not rows:
                print('No results for this query!')
            else:
                print('Here are the results of your query:')
                for row in rows:
                    print(row)
        elif query_n == 0:
            cont = False
        else:
            print('Not recognized answer! Please select a valid query number.')
    except ValueError:
        print('Not recognized answer! Please select a valid number.')

# Close the cursor and the connection
if mydb.is_connected():
    mycursor.close()
    mydb.close()
    print("MySQL connection is closed")
