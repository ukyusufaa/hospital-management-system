import sqlite3

class Database:

    def __init__(self, database_path):
        self.database_path = database_path
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(self.database_path)
        self.cursor = self.connection.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")


database = Database("hospital.db")
database.connect()

database.cursor.execute("""
CREATE TABLE IF NOT EXISTS gp_surgery(
                surgery_id INTEGER PRIMARY KEY AUTOINCREMENT,
                surgery_name TEXT NOT NULL,
                address TEXT NOT NULL)
""")

database.cursor.execute("""
CREATE TABLE IF NOT EXISTS department(
               department_id INTEGER PRIMARY KEY AUTOINCREMENT,
               department_name TEXT NOT NULL)
""")

database.cursor.execute("""
CREATE TABLE IF NOT EXISTS medication(
               medication_id INTEGER PRIMARY KEY AUTOINCREMENT,
               medication_name TEXT NOT NULL
                              CHECK(length(trim(medication_name)) > 0),
               cost REAL NOT NULL
                    CHECK(cost > 0))
""")

database.cursor.execute("""
CREATE TABLE IF NOT EXISTS gp(
               gp_id INTEGER PRIMARY KEY AUTOINCREMENT,
               first_name TEXT NOT NULL,
               surname TEXT NOT NULL,
               surgery_id INTEGER,

               FOREIGN KEY(surgery_id)
               REFERENCES gp_surgery(surgery_id))
""")

database.cursor.execute("""
CREATE TABLE IF NOT EXISTS patient(
               patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
               first_name TEXT NOT NULL,
               surname TEXT NOT NULL,
               dob TEXT NOT NULL
                CHECK (
                length(dob) = 10
                AND dob GLOB '[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]'
                AND CAST(substr(dob, 7, 4) AS INTEGER) >= 1900
                AND CAST(substr(dob, 4, 2) AS INTEGER) BETWEEN 1 AND 12
                AND CAST(substr(dob, 1, 2) AS INTEGER) BETWEEN 1 AND
                CASE CAST(substr(dob, 4, 2) AS INTEGER)
                    WHEN 1 THEN 31
                    WHEN 2 THEN
                        CASE
                            WHEN (
                                CAST(substr(dob, 7, 4) AS INTEGER) % 400 = 0
                                OR (
                                    CAST(substr(dob, 7, 4) AS INTEGER) % 4 = 0
                                    AND CAST(substr(dob, 7, 4) AS INTEGER) % 100 != 0
                                    )
                                )
                                THEN 29
                                ELSE 28
                            END
                    WHEN 3 THEN 31
                    WHEN 4 THEN 30
                    WHEN 5 THEN 31
                    WHEN 6 THEN 30
                    WHEN 7 THEN 31
                    WHEN 8 THEN 31
                    WHEN 9 THEN 30
                    WHEN 10 THEN 31
                    WHEN 11 THEN 30
                    WHEN 12 THEN 31
                    ELSE 0
                END
                ),
               address TEXT NOT NULL,
               gp_id INTEGER,

               FOREIGN KEY(gp_id)
               REFERENCES gp(gp_id))
""")

database.cursor.execute("""
CREATE TRIGGER IF NOT EXISTS patient_dob_not_future_insert
BEFORE INSERT ON patient
FOR EACH ROW
WHEN date(
    substr(NEW.dob, 7, 4) || '-' ||
    substr(NEW.dob, 4, 2) || '-' ||
    substr(NEW.dob, 1, 2)
) > date('now')
BEGIN
    SELECT RAISE(
        ABORT,
        'Date of birth cannot be in the future'
    );
END;
""")

database.cursor.execute("""
CREATE TRIGGER IF NOT EXISTS patient_dob_not_future_update
BEFORE UPDATE OF dob ON patient
FOR EACH ROW
WHEN date(
    substr(NEW.dob, 7, 4) || '-' ||
    substr(NEW.dob, 4, 2) || '-' ||
    substr(NEW.dob, 1, 2)
) > date('now')
BEGIN
    SELECT RAISE(
        ABORT,
        'Date of birth cannot be in the future'
    );
END;
""")


database.cursor.execute("""
CREATE TABLE IF NOT EXISTS consultant(
               consultant_id INTEGER PRIMARY KEY AUTOINCREMENT,
               first_name TEXT NOT NULL,
               surname TEXT NOT NULL,
               department_id INTEGER,

               FOREIGN KEY(department_id)
               REFERENCES department(department_id))
""")

database.cursor.execute("""
CREATE TABLE IF NOT EXISTS appointment(
               appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
               patient_id INTEGER,
               appointment_date TEXT NOT NULL
               CHECK (
                      length(appointment_date) = 10
                      AND appointment_date GLOB '[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]'
                      AND CAST(substr(appointment_date, 7, 4) AS INTEGER) >= 1900
                      AND CAST(substr(appointment_date, 4, 2) AS INTEGER) BETWEEN 1 AND 12
                            AND CAST(substr(appointment_date, 1, 2) AS INTEGER) BETWEEN 1 AND
                            CASE CAST(substr(appointment_date, 4, 2) AS INTEGER)
                                WHEN 1 THEN 31
                                WHEN 2 THEN
                                    CASE
                                        WHEN (
                                            CAST(substr(appointment_date, 7, 4) AS INTEGER) % 400 = 0
                                            OR (
                                                CAST(substr(appointment_date, 7, 4) AS INTEGER) % 4 = 0
                                                AND CAST(substr(appointment_date, 7, 4) AS INTEGER) % 100 != 0
                                                )
                                            )
                                            THEN 29
                                            ELSE 28
                                        END
                                WHEN 3 THEN 31
                                WHEN 4 THEN 30
                                WHEN 5 THEN 31
                                WHEN 6 THEN 30
                                WHEN 7 THEN 31
                                WHEN 8 THEN 31
                                WHEN 9 THEN 30
                                WHEN 10 THEN 31
                                WHEN 11 THEN 30
                                WHEN 12 THEN 31
                                ELSE 0
                            END
                            ),
               appointment_time TEXT NOT NULL
               CHECK (
                    appointment_time GLOB '[0-1][0-9]:[0-5][0-9]'
                    AND CAST(substr(appointment_time, 1, 2) AS INTEGER) BETWEEN 8 AND 18
                    AND CAST(substr(appointment_time, 4, 2) AS INTEGER) IN (0, 15, 30, 45)
                    AND (
                        CAST(substr(appointment_time, 1, 2) AS INTEGER) < 18
                        OR CAST(substr(appointment_time, 4, 2) AS INTEGER) = 0
                    )
                ),
               consultant_id INTEGER,

               FOREIGN KEY(patient_id)
               REFERENCES patient(patient_id),

               FOREIGN KEY(consultant_id)
               REFERENCES consultant(consultant_id),

               UNIQUE(consultant_id, appointment_date, appointment_time),

               UNIQUE(patient_id, appointment_date, appointment_time))
""")

database.cursor.execute("""
CREATE TRIGGER IF NOT EXISTS appointment_date_future_insert
BEFORE INSERT ON appointment
FOR EACH ROW
WHEN date(
    substr(NEW.appointment_date, 7, 4) || '-' ||
    substr(NEW.appointment_date, 4, 2) || '-' ||
    substr(NEW.appointment_date, 1, 2)
) <= date('now')
BEGIN
    SELECT RAISE(ABORT, 'Appointment date must be in the future');
END;
""")

database.cursor.execute("""
CREATE TRIGGER IF NOT EXISTS appointment_date_future_update
BEFORE UPDATE OF appointment_date ON appointment
FOR EACH ROW
WHEN date(
    substr(NEW.appointment_date, 7, 4) || '-' ||
    substr(NEW.appointment_date, 4, 2) || '-' ||
    substr(NEW.appointment_date, 1, 2)
) <= date('now')
BEGIN
    SELECT RAISE(ABORT, 'Appointment date must be in the future');
END;
""")

database.cursor.execute("""
CREATE TABLE IF NOT EXISTS prescription(
               prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
               appointment_id INTEGER UNIQUE,

               FOREIGN KEY(appointment_id)
               REFERENCES appointment(appointment_id))
""")

database.cursor.execute("""
CREATE TABLE IF NOT EXISTS prescription_medication(
               prescription_instructions TEXT NOT NULL,
               prescription_id INTEGER,
               medication_id INTEGER,

               FOREIGN KEY(prescription_id)
               REFERENCES prescription(prescription_id),

               FOREIGN KEY(medication_id)
               REFERENCES medication(medication_id),

               UNIQUE(prescription_id, medication_id))
            
""")

database.cursor.execute("""
CREATE TABLE IF NOT EXISTS bill(
               bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
               total_amount REAL NOT NULL,
               appointment_id INTEGER UNIQUE,
               payment_status TEXT NOT NULL
                              CHECK(payment_status IN ('UNPAID', 'PAID')),

               FOREIGN KEY(appointment_id)
               REFERENCES appointment(appointment_id))

""")

database.connection.commit()
