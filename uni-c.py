# Έκδοση Γ της εφαρμογής university.py
'''
Λειτουργίες CRUD για τα μαθήματα και τους καθηγητές που τα διδάσκουν
'''

# model
import sqlite3

def insert_course(course):
    try: 
        print(course)
        with sqlite3.connect('university.db') as con:
            # εισαγωγή νέου μαθήματος
            sql = "INSERT INTO Courses VALUES ('{}','{}');".format(course["code"], course["name"])
            print(sql)
            cursor = con.cursor()
            cursor.execute(sql)
            con.commit()
            print('επιτυχής εισαγωγή {} μαθήματος'.format(cursor.rowcount))
            cursor.close()
        con.close()
        return True
    except sqlite3.Error as er:
        print ("insert_course:", er)
        con.close()
        return False

def update_course(course):
    print(course)
    try: 
        with sqlite3.connect('university.db') as con:
                # Τροποποίηση μαθήματος
                sql = "UPDATE Courses SET NAME = '{}' WHERE CODE = '{}';".format(course[1], course[0])
                cursor = con.cursor()
                cursor.execute(sql)
                con.commit()
                print('επιτυχής τροποποίηση μαθήματος')
                cursor.close()
    except sqlite3.Error as er:
        print (er)
        return False
    finally: 
        con.close()
        return True

def delete_course(code):
    reply = input("Είστε βέβαιοι για τη διαγραφή του μαθήματος με κωδικό:{} (ν/ό)".format(code))
    if reply.lower() in 'όοo': return False
    try: 
        with sqlite3.connect('university.db') as con:
                # Διαγραφή μαθήματος
                sql = "DELETE FROM Courses WHERE CODE = '{}';".format(code)
                cursor = con.cursor()
                cursor.execute(sql)
                print('επιτυχής διαγραφή μαθήματος')
                con.commit()
                # Διαγραφή διδασκαλίας μαθήματος
                sql = "DELETE FROM Teaching WHERE CODE = '{}';".format(code)
                cursor = con.cursor()
                cursor.execute(sql)
                print("Διαγραφή {} αναθεσης/αναθέσεων διδασκαλίας του μαθήματος".format(cursor.rowcount))
                cursor = con.cursor()
                cursor.execute(sql)
                con.commit()
                # Διαγραφή βαθμών μαθήματος
                sql = "DELETE FROM Enrolled WHERE CODE = '{}';".format(code)
                cursor = con.cursor()
                cursor.execute(sql)
                print("Διαγραφή {} εγγραφών φοιτητών/βαθμολογιών του μαθήματος".format(cursor.rowcount))
                con.commit()
                cursor.close()
    except sqlite3.Error as er:
        print (er)
        print("ΠΡΟΣΟΧΗ: Ίσως χρειάζεται να διαγράψετε βαθμολογίες ή διδάσκοντες μαθήματος πριν")
        return False
    finally: 
        con.close()
        return True


def update_teaching():
    pass

def insert_prof(prof):
    print(prof)
    try: 
        with sqlite3.connect('university.db') as con:
                # εισαγωγή νέου καθηγητή
                prof_id = None
                sql = "INSERT INTO Professors VALUES (NULL, '{}','{}');".format(prof["name"], prof["surname"])
                cursor = con.cursor()
                cursor.execute(sql)
                con.commit()
                prof_id = cursor.lastrowid
                print('επιτυχής εισαγωγή καθηγητή με ID={}'.format(prof_id))
                cursor.close()
    except sqlite3.Error as er:
        print (er)
        return False
    finally: 
        con.close()
        return prof_id

def insert_teaching(teaching):
    try: 
        with sqlite3.connect('university.db') as con:
                # εισαγωγή νέου καθηγητή
                sql = "INSERT INTO Teaching VALUES ('{}','{}');".format(teaching["id"], teaching["code"])
                cursor = con.cursor()
                cursor.execute(sql)
                con.commit()
                print('επιτυχής εισαγωγή {} διδασκαλίας'.format(cursor.rowcount))
                cursor.close()
    except sqlite3.Error as er:
        print (er)
    finally: 
        con.close()
    pass

def select_table(table):
    try:
        result = []
        with sqlite3.connect('university.db') as con:
            sql = "SELECT * from {}"
            cursor = con.cursor()
            cursor.execute(sql.format(table))
            result.append([d[0] for d in cursor.description])
            for row in cursor:
                result.append(row)
            cursor.close()
        con.close()
        return result
    except sqlite3.Error as er:
        print (er)
        con.close()
        return False

def select_teaching(courses):
    # συνάρτηση για ανάκτηση δεδομένων διδασκαλίας από πίνακα Teaching και σύνδεσης με 
    # τον πίνακα μαθημάτων 
    
    def add_teaching(courses, teaching):
        # Βοηθητική συνάρτηση για προσθήκη των διδασκόντων στα μαθήματα
        the_courses = [list(courses[0]+["Διδάσκοντες"])]
        for course in courses[1:]:
            code = course[0]
            teachers= ", ".join(" ".join(x[1:]) for x in teaching if x[0] == code)
            the_courses.append(list(course)+[teachers])
        return the_courses

    try:
        with sqlite3.connect('university.db') as con:
            sql = '''SELECT Teaching.CODE, Professors.NAME, Professors.SURNAME
            from Teaching JOIN Professors on Teaching.ID = Professors.ID;'''
            cursor = con.cursor()
            cursor.execute(sql)
            teaching = []
            for row in cursor:
                teaching.append(row)
            cursor.close()
        con.close()
        return add_teaching(courses, teaching)
    except sqlite3.Error as er:
        print (er)
        con.close()
        return False

#  view
def new_course():
    # εισαγωγή στοιχείων νέου μαθήματος
    while True:
        print("Εισάγετε τα στοιχεία νέου μαθήματος")
        code = input("Κωδικός μαθήματος:")
        name = input("Όνομα μαθήματος:")
        if code and name:
            return {'code':code, 'name': name}

def new_prof():
    # εισαγωγή στοιχείων νέου καθηγητή
    while True:
        print("Εισάγετε τα στοιχεία νέου καθηγητή")
        name = input("Όνομα καθηγητή:")
        surname = input("Επίθετο καθηγητή:")
        if name and surname:
            return {'name':name, 'surname': surname}    

def show_profs(profs):
    # παρουσίαση καθηγητών
    if not profs:
        print("Δεν υπάρχουν καθηγητές στο σύστημα") 
        return False
    for prof in profs[1:]:
        print("{}\t{} {}".format(*prof))
    print("\n")
    return True
    
def show_courses(courses):
    # παρουσίαση μαθημάτων
    if not courses: 
        print("Δεν υπάρχουν μαθήματα")
        return False
    print("\nΚατάσταση ΜΑΘΗΜΑΤΩΝ")
    for course in courses:
        print("\t".join(course))

# controller
def new_course_controller():
    course = new_course() # ζήτησε στοιχεία (κωδικό και όνομα) για το νέο μάθημα
    inserted = insert_course(course) # εισαγωγή στη βάση δεδομένων
    print("inserted:",inserted)
    if inserted:    # διάλογος επιλογής διδάσκοντα μαθήματος
        teachers =[]
        while True:
            print("\nΕισαγωγή καθηγητή μαθήματος {}".format(course["name"]))
            print("Καθηγητές μαθήματος: ", *teachers if len(teachers) > 0 else "κανείς")
            the_profs = select_table("Professors")
            if show_profs(the_profs): #δείξε πίνακα καθηγητών
                reply = input("Επιλέξτε καθηγητή ή εισάγετε νέο καθηγητή(+), enter για τέλος:")
                if reply in [str(x[0]) for x in the_profs]: # επιλογή ενός από τους καθηγητές του πίνακα
                    insert_teaching({"id":int(reply), "code": course['code']})
                    if int(reply) not in teachers: 
                        teachers.append(int(reply))
                        prof_surname = [x[2] for x in the_profs if int(reply) in x]
                        print("Ο καθηγητής {} προστέθηκε στους διδάσκοντες του μαθήματος".format(prof_surname))
                elif reply == "+": # προσθήκη καθηγητή και επιλογή του ως διδάσκοντα
                    new_prof_id = insert_prof(new_prof() )
                    if new_prof_id: teachers.append(new_prof_id)
                    insert_teaching({"id": new_prof_id, "code": course['code']})
                elif reply == "" and len(teachers) > 0: # αν έχει οριστεί έστω ένας καθηγητής, έξοδος
                    print(teachers)
                    break 

def update_course_controller():
    print("\nΤροποποίηση ονόματος ή διδασκαλίας μαθήματος, τα μαθήματα είναι:")
    the_courses = select_table("Courses")
    show_courses(the_courses)
    while True:
        reply = input("Επιλέξτε u code για τροποποίηση, d code για διαγραφή μαθήματος:")
        if len(reply.split())>0 and reply.split()[1].strip() in [x[0] for x in the_courses[1:]] and \
            reply.split()[0] in "du":
            if reply.split()[0] == "u":
                while True:
                    new_name = input("Νέο όνομα μαθήματος, enter για μη αλλαγή:")
                    if new_name:
                        update_course((reply.split()[1].strip(), new_name))
                        break
                break
            elif reply.split()[0] == "d":
                delete_course(reply.split()[1].strip())
                break
        if not reply: break

# main program
options = {"1": "Κατάλογος Μαθημάτων", "2":"Νέο Μάθημα", "3": "Τροποποίηση μαθήματος"}
while True:
    print(60*"-", "\nΔΙΑΧΕΙΡΙΣΗ ΜΑΘΗΜΑΤΩΝ")
    print("\n".join([":".join(x) for x in options.items()]))
    reply = input("Επιλογή:")
    if not reply: break
    if reply == "1":
        teaching = select_teaching(select_table("Courses"))
        show_courses(teaching)
    elif reply == "2":
        new_course_controller()
    elif reply == "3":
        update_course_controller()
