import sqlite3
import alphavantage as av
from sqlite3 import Error
import sqlalchemy 

def sql_connection():
    try:
        con = sqlite3.connect('testdb.db')
        return(con)
    except Error:
        print(Error)

def sql_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE BHP( open, high, low, close, volume, timestamp)")
    con.commit()

con = sql_connection()
sql_table(con)

data = av.get_data('BHP.AX')
data.to_sql(name = 'BHP', con=con, index=False, if_exists='replace')


