# Έκδοση Α της εφαρμογής university.py

# model
import sqlite3
def select_table(table, sql=""):
    try:
        result = []
        with sqlite3.connect('university.db') as con:
            sql = "SELECT * from {}".format(table) if not sql else sql
            cursor = con.execute(sql)
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
# get table names.
table_names = select_table(None, "SELECT name FROM sqlite_master WHERE type='table';")
tables = {}
for table in table_names[1:]:
    if table[0] != "sqlite_sequence": tables[str(table_names.index(table))] = table[0]
# tables = {"1": "Students", "2": "Professors", "3": "Courses"}
while True:
    print("\n".join([":".join(x) for x in tables.items()]))
    reply = input("Επιλογή:")
    if not reply: break
    if reply in tables.keys():
        show_table(select_table(tables[reply]))
    
