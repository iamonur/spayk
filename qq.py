import sqlite3
if __name__ == "__main__":
    query = "SELECT COUNT(*) FROM gengame"
    query2= "SELECT MAX(fitness) FROM gengame"
    query3= "SELECT MIN(fitness) FROM gengame"
    query4= "SELECT * FROM gengame ORDER BY fitness DESC limit 1"

    con = sqlite3.connect("onur.db")
    cur = con.cursor()

    cur.execute(query)
    print(cur.fetchall())

    cur.execute(query2)
    print(cur.fetchall())


    cur.execute(query3)
    print(cur.fetchall())

    cur.execute(query4)
    print(cur.fetchall())
