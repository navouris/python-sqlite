# Έκδοση B της εφαρμογής university.py
'''
Η έκδοση αυτή περιλαμβάνει τη δυνατότητα παρουσίασης όπως η παρουσίαση 
της καρτέλας φοιτητή, και συνοπτικά στατιστικά επιτυχίας σε κάθε μάθημα.
Η διεπαφή σε αυτή την περίπτωση έχει δύο επιλογές: 1.στοιχεία φοιτητών, 
και 2. στοιχεία μαθημάτων
- Η επιλογή 1 οδηγεί σε διάλογο για τον καθορισμό του φοιτητή που οδηγεί 
στην παρουσίαση της καρτέλας του (μαθήματα, βαθμοί, μέσος όρος)
- Η επιλογή 2 οδηγεί σε παρουσίαση των μαθημάτων και των στοιχείων τους, 
πλήθος φοιτητών, μέσος όρος βαθμολογίας τους.
'''

# model
import sqlite3
def get_transcript(am):
    '''ανάκτηση στοιχείων φοιτητή και μαθημάτων στα οποία έχει εγγραφεί'''
    try:
        result = {}
        with sqlite3.connect('university.db') as con:
            # ανάκτηση δεδομένων φοιτητή
            results = con.execute("SELECT * from Students WHERE ΑΜ = {};".format(int(am)))
            rows = ([d[0] for d in results.description])
            record = results.fetchone()
            if not record: 
                con.close()
                return False
            for field in record:
                result[rows[record.index(field)]] = field
            # ανάκτηση δεδομένων μαθημάτων
            result["courses"] = []
            cursor = con.cursor()
            results = cursor.execute('''
            SELECT Courses.NAME, Enrolled.GRADE 
            FROM Enrolled JOIN Courses on Enrolled.CODE = Courses.CODE
            WHERE Enrolled.AM = {};'''.format(am))
            for course in results:
                result["courses"].append(course)
            # ανάκτηση μέσου όρου βαθμολογίας
            if result["courses"] :
                results = con.execute('''
                SELECT AVG(GRADE)
                FROM Enrolled 
                WHERE AM = {};'''.format(am))
                result["average_grade"] = results.fetchone()[0]
        con.close()
        return result
    except sqlite3.Error as er:
        print ("get_trasncript", er)
        con.close()
        return False

def get_courses():
    # ανάκτηση στοιχείων μαθημάτων
    courses = []
    try:
        with sqlite3.connect('university.db') as con:
            # ανάκτηση δεδομένων μαθημάτων
            results = con.execute('''
            SELECT Enrolled.CODE, Courses.NAME, AVG(GRADE), COUNT(GRADE)
            FROM Enrolled JOIN Courses on Enrolled.CODE = Courses.CODE
            GROUP BY Enrolled.CODE
            ORDER BY AVG(GRADE) DESC;''')
            rows = ([d[0] for d in results.description])
            for course in results:
                new_course = {}
                for field in course:
                    new_course[rows[course.index(field)]] = field
                courses.append(new_course)
        con.close()
        return courses
    except sqlite3.Error as er:
        con.close()
        print ("get_courses", er)
        return False

#  view
def show_courses(courses):
    if not courses: return False
    print("\nΣΤΑΤΙΣΤΙΚΑ ΜΑΘΗΜΑΤΩΝ")
    for course in courses:
        print("ΜΑΘΗΜΑ:{} {:40s} ΜΕΣΗ ΒΑΘΜ:{:.2f} ({} φοιτητές)".format(course["CODE"], \
            course["NAME"], course["AVG(GRADE)"], course["COUNT(GRADE)"]))
    print("\n")

def show_transcript(student):
    if not student: return False
    print("\nΟΝΟΜΑ ΦΟΙΤΗΤΗ: {}".format(student["NAME"]))
    print("ΕΠΩΝΥΜΟ ΦΟΙΤΗΤΗ: {}".format(student["SURNAME"]))
    print("ΑΡΙΘΜΟΣ ΜΗΤΡΩΟΥ:{}".format(student["ΑΜ"]))
    print(60*"_","\nΒΑΘΜΟΛΟΓΙΑ")
    for course in student["courses"]:
        print("Μάθημα: {:40s}Βαθμός: {:.2f}".format(*course))
    print(60*"_")
    print("ΜΕΣΗ ΒΑΘΜΟΛΟΓΙΑ: {:.2f}\n\n".format(student["average_grade"]))

# controller
options = {"1": "Καρτέλες Φοιτητών", "2": "Στατιστικά Μαθημάτων"}
while True:
    print("\n".join([":".join(x) for x in options.items()]))
    reply = input("Επιλογή:")
    if not reply: break
    if reply == "1":
        am = input("Αριθμός Μητρώου φοιτητή:")
        show_transcript(get_transcript(am))
    if reply == "2":
        show_courses(get_courses())
    