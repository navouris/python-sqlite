# Έκδοση Α της εφαρμογής university.py

# model
import sqlite3
def select_table(table):
    try:
        result = []
        with sqlite3.connect('university.db') as con:
            cursor = con.execute("SELECT * from {}".format(table))
            result.append([d[0] for d in cursor.description])
            for row in cursor:
                result.append(row)
        con.close()
        return result
    except sqlite3.Error as er:
        print ("select_table", er)
        con.close()
        return False

#  view
def show_table(table):
    for row in table:
        print("\t".join([str(x) for x in row]))

# controller
tables = {"1": "Students", "2": "Professors", "3": "Courses"}
while True:
    print("\n".join([":".join(x) for x in tables.items()]))
    reply = input("Επιλογή:")
    if not reply: break
    if reply in tables.keys():
        show_table(select_table(tables[reply]))
    
