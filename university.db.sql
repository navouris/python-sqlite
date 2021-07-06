BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Courses" (
	"CODE"	TEXT,
	"NAME"	TEXT NOT NULL,
	PRIMARY KEY("CODE")
);
CREATE TABLE IF NOT EXISTS "Professors" (
	"ID"	INTEGER,
	"NAME"	TEXT NOT NULL,
	"SURNAME"	TEXT NOT NULL,
	PRIMARY KEY("ID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Students" (
	"ΑΜ"	INTEGER,
	"NAME"	ΤΕΧΤ NOT NULL,
	"SURNAME"	TEXT NOT NULL,
	PRIMARY KEY("ΑΜ")
);
CREATE TABLE IF NOT EXISTS "Enrolled" (
	"AM"	INTEGER,
	"CODE"	TEXT,
	"GRADE"	REAL,
	FOREIGN KEY("AM") REFERENCES "Students"("ΑΜ"),
	FOREIGN KEY("CODE") REFERENCES "Courses"("CODE"),
	PRIMARY KEY("AM","CODE")
);
CREATE TABLE IF NOT EXISTS "Teaching" (
	"ID"	INTEGER,
	"CODE"	TEXT,
	FOREIGN KEY("ID") REFERENCES "Professors"("ID"),
	FOREIGN KEY("CODE") REFERENCES "Courses"("CODE"),
	PRIMARY KEY("ID","CODE")
);
INSERT INTO "Courses" VALUES ('Γ703','Βάσεις Δεδομένων');
INSERT INTO "Courses" VALUES ('Γ501','Λειτουργικά Συστηματα');
INSERT INTO "Courses" VALUES ('Γ802','Προγραμματισμός Διαδικτύου');
INSERT INTO "Professors" VALUES (1,'Ευγένιος','Βούλγαρης');
INSERT INTO "Professors" VALUES (2,'Νεόφυτος','Δούκας');
INSERT INTO "Professors" VALUES (3,'Αθανάσιος','Ψαλίδας');
INSERT INTO "Professors" VALUES (4,'Νίκος','Αβούρης');
INSERT INTO "Students" VALUES (101,'Αδαμάντιος','Κοραής');
INSERT INTO "Students" VALUES (102,'Θεόδωρος','Κολοκοτρώνης');
INSERT INTO "Students" VALUES (103,'Λασκαρίνα','Μπουμπουλίνα');
INSERT INTO "Students" VALUES (104,'Κωνσταντίνος','Κανάρης');
INSERT INTO "Students" VALUES (105,'Μαντώ','Μαυρογένους');
INSERT INTO "Enrolled" VALUES (101,'Γ703',8.5);
INSERT INTO "Enrolled" VALUES (101,'Γ802',6.0);
INSERT INTO "Enrolled" VALUES (102,'Γ802',7.0);
INSERT INTO "Enrolled" VALUES (103,'Γ802',4.5);
INSERT INTO "Enrolled" VALUES (103,'Γ703',4.0);
INSERT INTO "Enrolled" VALUES (105,'Γ703',6.0);
INSERT INTO "Enrolled" VALUES (104,'Γ501',7.0);
INSERT INTO "Enrolled" VALUES (102,'Γ501',6.0);
INSERT INTO "Teaching" VALUES (1,'Γ501');
INSERT INTO "Teaching" VALUES (2,'Γ501');
INSERT INTO "Teaching" VALUES (1,'Γ703');
INSERT INTO "Teaching" VALUES (3,'Γ802');
INSERT INTO "Teaching" VALUES (4,'Γ802');
COMMIT;
