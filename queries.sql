# FIND THE HIGHEST RATED WINE IN EACH COUNTRY
SELECT 
  Country,
  MaxPoints,
  (SELECT Title FROM Wine w2 WHERE w2.Country = w1.Country AND w2.Points = MaxPoints LIMIT 1) AS Title,
  (SELECT Winery FROM Wine w2 WHERE w2.Country = w1.Country AND w2.Points = MaxPoints LIMIT 1) AS Winery
FROM (
  SELECT Country, MAX(Points) AS MaxPoints
  FROM Wine
  GROUP BY Country
) AS w1
ORDER BY MaxPoints DESC;

# CALCULATE THE AVERAGE PRICE OF WINE BY VARIETY
SELECT Variety, AVG(Price) AS AvgPrice
FROM Wine
WHERE Price IS NOT NULL
GROUP BY Variety
ORDER BY AvgPrice DESC;

# LIST WINES WITH THE WORD FRUITY IN THE DESCRIPTION SORTED BY POINTS
SELECT Title, Description, Points
FROM Wine
WHERE Description LIKE '%fruity%'
ORDER BY Points DESC
LIMIT 10;

# COUNT THE NUMBER OF WINES BY PROVINCE AND ORDER BY COUNT DESCENDING
SELECT Province, COUNT(*) AS NumberOfWines
FROM Wine
GROUP BY Province
ORDER BY NumberOfWines DESC;

# FIND THE MOST EXPENSIVE WINE FOR EACH TASTER
SELECT Taster_Name, MAX(Price) AS MaxPrice, Title, Winery
FROM Wine
GROUP BY Taster_Name
ORDER BY MaxPrice DESC;
