import sqlite3

conn = sqlite3.connect("hospital.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS gp_surgery(
                surgery_id INTEGER PRIMARY KEY AUTOINCREMENT,
                surgery_name TEXT NOT NULL,
                address TEXT NOT NULL)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS department(
               department_id INTEGER PRIMARY KEY AUTOINCREMENT,
               department_name TEXT NOT NULL)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS medication(
               medication_id INTEGER PRIMARY KEY AUTOINCREMENT,
               medication_name TEXT NOT NULL,
               cost REAL NOT NULL)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS gp(
               gp_id INTEGER PRIMARY KEY AUTOINCREMENT,
               first_name TEXT NOT NULL,
               surname TEXT NOT NULL,
               surgery_id INTEGER,
               FOREIGN KEY(surgery_id)
               REFERENCES gp_surgery(surgery_id))
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS patient(
               patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
               first_name TEXT NOT NULL,
               surname TEXT NOT NULL,
               dob TEXT NOT NULL,
               address TEXT NOT NULL,
               gp_id INTEGER,
               FOREIGN KEY(gp_id)
               REFERENCES gp(gp_id))
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS consultant(
               consultant_id INTEGER PRIMARY KEY AUTOINCREMENT,
               first_name TEXT NOT NULL,
               surname TEXT NOT NULL,
               department_id INTEGER,
               FOREIGN KEY(department_id)
               REFERENCES department(department_id))
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointment(
               appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
               patient_id INTEGER,
               appointment_date TEXT NOT NULL,
               appointment_time TEXT NOT NULL,
               consultant_id INTEGER,
               FOREIGN KEY(patient_id)
               REFERENCES patient(patient_id),
               FOREIGN KEY(consultant_id)
               REFERENCES consultant(consultant_id))
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS prescription(
               prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
               appointment_id INTEGER,
               FOREIGN KEY(appointment_id)
               REFERENCES appointment(appointment_id))
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS prescription_medication(
               prescription_instructions TEXT NOT NULL,
               prescription_id INTEGER,
               medication_id INTEGER,
               FOREIGN KEY(prescription_id)
               REFERENCES prescription(prescription_id),
               FOREIGN KEY(medication_id)
               REFERENCES medication(medication_id))
              
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS bill(
               bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
               total_amount REAL NOT NULL,
               appointment_id INTEGER,
               FOREIGN KEY(appointment_id)
               REFERENCES appointment(appointment_id))
""")

conn.commit()

conn.close()