"""
Project Name: Airlines Data Analysis
Created by : Prakhar Tripathi and Ishita Mistra
Project Description: This is a data analysis project that is done by using MySQL and Python, in this analysis we have to
solve the business problem of the airlines, and also for solving it we have to find some insights.
"""

"""
Business Problem: There is a company that operates a diverse fleet of aircraft ranging from small business jets to 
medium-sized machines. However, They are currently facing challenges due to several factors such as stricter 
environmental regulations, higher flight taxes, increased interest rates, rising fuel prices, and a tight labor 
market resulting in increased labor costs.

As a result, the company's profitability is under pressure, and they are seeking ways to address this issue. To tackle 
this challenge, they are looking to conduct an analysis of their database to find ways to increase their occupancy 
rate, which can help boost the average profit earned per seat.
"""

"""

Main Goal of the analysis.....
1. Enhancing the occupancy of flight.
2. Maintain the pricing.
3. Enhancing the customer experience.

The main goal is to find the way to make the airline more profitable and also resolving the issues like occupancy rate
pricing and customer satisfaction.
"""

# importing libraries
"""
First we have to import some libraries to perform our analysis.....
"""
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import seaborn as sns

warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', None)
pd.set_option("display.float_format", str)

# Database Connection
"""
Now we have all the libraries that we want for this project, so our next step is to connect with the SQL database using
sqlite. 
"""
path = "C:\\Users\\prakh\\Downloads\\Practice DataSet\\"
connection = sqlite3.connect(path + "travel.sqlite")
cursor = connection.cursor()

cursor.execute('select name from sqlite_master where type = "table";')
print("list of tables present in the database")
table_list = [table[0] for table in cursor.fetchall()]
print(table_list)

# Data Exploration

"""
We got the names of the tables on which we have to perform our analysis and now we are going to perform our basic data
exploration.
"""

# Checking the data of aircrafts_data column
aircrafts_data = pd.read_sql_query("SELECT * FROM aircrafts_data ", connection)
print(aircrafts_data.head())

# Checking number of rows and column in aircrafts_data
print(f"Number of rows and columns: {aircrafts_data.shape}\n")

# Checking the data of airports_data column
airports_data = pd.read_sql_query("SELECT * FROM airports_data ", connection)
print(airports_data.head())

# Checking number of rows and column in airports_data
print(f"Number of rows and columns: {airports_data.shape}\n")

# Checking the data of boarding_passes column
boarding_passes = pd.read_sql_query("SELECT * FROM boarding_passes ", connection)
print(boarding_passes.head())

# Checking number of rows and column in boarding_passes
print(f"Number of rows and columns: {boarding_passes.shape}\n")

# Checking the data of bookings column
bookings = pd.read_sql_query("SELECT * FROM bookings ", connection)
print(bookings.head())

# Checking number of rows and column in bookings
print(f"Number of rows and columns: {bookings.shape}\n")

# Checking the data of flights column
flights = pd.read_sql_query("SELECT * FROM flights ", connection)
print(flights.head())

# Checking number of rows and column in flights
print(f"Number of rows and columns: {flights.shape}\n")

# Checking the data of seats column
seats = pd.read_sql_query("SELECT * FROM seats ", connection)
print(seats.head())

# Checking number of rows and column in seats
print(f"Number of rows and columns: {seats.shape}\n")

# Checking the data of ticket_flights column
ticket_flights = pd.read_sql_query("SELECT * FROM ticket_flights ", connection)
print(ticket_flights.head())

# Checking number of rows and column in ticket_flights
print(f"Number of rows and columns: {ticket_flights.shape}\n")

# Checking the data of ticket_flights column
tickets = pd.read_sql_query("SELECT * FROM tickets ", connection)
print(tickets.head())

# Checking number of rows and column in tickets
print(f"Number of rows and columns: {tickets.shape}\n")

# Checking the data type of the column that are present in table

for table in table_list:
    print("\nTable:", table)
    column_info = connection.execute("PRAGMA table_info({})".format(table))
    for column in column_info.fetchall():
        print(column[1:3])

# Checking the missing values in columns

for table in table_list:
    print("\nTable:", table)
    df_table = pd.read_sql_query(f"Select * from {table}", connection)
    print(df_table.isnull().sum())

"""
In our dataset we have no any null values and also we have perfect data for our analysis.
"""

# Basic Analysis
"""
We completed our analysis and now we have a perfect data for the analysis, so first we start from basic analysis of data
according to business problem.
"""

# Question 1. How many Planes have more than 100 seats?
# Solution:......
seats_count = pd.read_sql_query("SELECT aircraft_code, count(*) as num_seats from seats group by "
                                "aircraft_code having num_seats > 100", connection)
print(seats_count)


# Question 2. How many number of tickets booked and total amount earned changed at time?
# Solution:......
tickets = pd.read_sql_query("SELECT * from tickets inner join bookings on tickets.book_ref = "
                            "bookings.book_ref", connection)
tickets["book_date"] = pd.to_datetime(tickets["book_date"])
tickets["date"] = tickets["book_date"].dt.date
number_of_ticket_date = tickets.groupby("date")[["date"]].count()

plt.figure(figsize=(18, 6))
plt.plot(number_of_ticket_date.index, number_of_ticket_date["date"], marker="^")
plt.xlabel("Date", fontsize=20)
plt.ylabel("Number of tickets", fontsize=20)
plt.show()

# Question 3. Calculate the average charges for each aircraft with different fare condition?
# Solution:......

df = pd.read_sql_query("SELECT fare_conditions, aircraft_code, avg(amount) as Average_Amount from ticket_flights "
                       "join flights on ticket_flights.flight_id = flights.flight_id "
                       "group by aircraft_code, fare_conditions", connection)

print(df)

sns.barplot(data=df, x="aircraft_code", y="Average_Amount", hue="fare_conditions")
plt.show()

# Analyzing Occupancy rate

# Question 4. For each aircraft, calculate the total revenue and average revenue per ticket
# Solution.....
revenue_per_ticket = pd.read_sql_query("SELECT  aircraft_code, ticket_count, total_revenue, "
                                       "total_revenue/ticket_count as avg_revenue_per_ticket from "
                                       "(SELECT aircraft_code, count(*) as ticket_count, sum(amount) "
                                       "as total_revenue from ticket_flights "
                                       "join flights on ticket_flights.flight_id = flights.flight_id group by "
                                       "aircraft_code)", connection)
print(revenue_per_ticket)

# Question 5. Calculate the average occupancy per aircraft
# Solution.....

occupancy_rate = pd.read_sql_query("SELECT a.aircraft_code, avg(a.booked_seats) as seat_booked, b.num_seats, "
                                   "avg(a.booked_seats/b.num_seats) as occupancy_rate from "
                                   "(SELECT aircraft_code, flights.flight_id, count(*) as booked_seats from "
                                   "boarding_passes "
                                   "inner join flights on boarding_passes.flight_id = flights.flight_id group by "
                                   "aircraft_code, flights.flight_id) "
                                   "as a inner join (SELECT aircraft_code, count(*) as num_seats from seats group by "
                                   "aircraft_code) as b "
                                   "on a.aircraft_code = b.aircraft_code group by a.aircraft_code", connection)
print(occupancy_rate)

# Question 6. Calculate by how much the total annual turnover could increase by giving all aircraft a 10% higher
# occupancy rate.
# Solution.....

occupancy_rate["Inc. occupancy rate"] = occupancy_rate["occupancy_rate"] + occupancy_rate["occupancy_rate"] * 0.1
print(occupancy_rate)

total_revenue = pd.read_sql_query("SELECT aircraft_code, sum(amount) as total_revenue from ticket_flights " 
                                  "join flights on ticket_flights.flight_id = flights.flight_id group by aircraft_code",
                                  connection)
occupancy_rate["Inc.occupancy rate"] = ((total_revenue["total_revenue"] / occupancy_rate["occupancy_rate"])
                                        * occupancy_rate["Inc. occupancy rate"])

print(occupancy_rate)

# Question 7. Checking the flight status count and also checking the aircraft which has maximum cancellation.

flight = pd.read_sql_query("SELECT status from flights", connection)
print(flight.value_counts())

cancel_aircrafts = pd.read_sql_query("SELECT aircraft_code, count(status) as seat_count from flights "
                                     "where status == 'Cancelled'", connection)
print(cancel_aircrafts)

# Question 8. Checking the count of airport that  have cancelled status.

cancel_airport = pd.read_sql_query("SELECT departure_airport from flights where status == 'Cancelled'",
                                   connection)
print(cancel_airport.value_counts())

# Question 9. Count the fair conditions on which passengers ues most.
# Solution.....

fair_count = pd.read_sql_query("SELECT fare_conditions from ticket_flights", connection)
print(fair_count.value_counts())

# Question 10. Checking the date and total amount of booking.
# Solution.....
booking = pd.read_sql_query("SELECT * from bookings", connection)
booking["book_date"] = pd.to_datetime(booking["book_date"])
booking["date"] = booking["book_date"].dt.date
booking_amount = booking.groupby("date")[["total_amount"]].sum()

plt.figure(figsize=(18, 6))
plt.plot(booking_amount.index, booking_amount["total_amount"], marker="*")
plt.xlabel("Date", fontsize=20)
plt.ylabel("Total amount", fontsize=20)
plt.show()

# Question 11. Checking the month of booking.
# Solution.....
booking["month"] = booking["book_date"].dt.month_name()
month_count = booking["month"].value_counts()
plt.figure(figsize=(10, 5))
sns.barplot(x=month_count.index, y=month_count.values)
plt.show()