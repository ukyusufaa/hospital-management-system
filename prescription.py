import sqlite3

conn = sqlite3.connect("hospital.db")

cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

class Prescription():
    def __init__(self,appointment_id):
        self.appointment_id = appointment_id

    def show_prescription_details(self):
        print(f"Appointment ID:{self.appointment_id}")

    def validate_login_id(self,number):
        if number < 1:
            return False
        return True

    def validate_yes_no(self,option):
        if option != 'y' and not option =='n':
            return False
        return True

    def create_prescription(self):
        while True:
            try:
                self.appointment_id = int(input("Appointment ID:"))
                if not self.validate_login_id(self.appointment_id):
                    print("Appointment ID must be greater than 0")
                    continue 
                break 

            except ValueError:
                print("Appointment ID must be numbers")
                continue 

        try:
            cursor.execute("""
            INSERT INTO prescription(
                        appointment_id)
            VALUES(?)
            """,(self.appointment_id,))

            conn.commit()

        except sqlite3.Error as e:
            print("Database Error", e)
            return 

        print("Prescription inserted sucessfully")
        row = cursor.lastrowid
        print(f"Prescription ID:{row}")
        self.show_prescription_details()
        return

    def display_all_prescriptions(self):
        try:
            cursor.execute("SELECT * FROM prescription")

        except sqlite3.Error as e:
            print("Database Error", e)
            return 

        rows = cursor.fetchall()
        if not rows:
            print("No Prescriptions found")
        else:
            for row in rows:
                self.appointment_id = row[1]
                print(f"Prescription ID:{row[0]}")
                self.show_prescription_details()
            return

    def search_prescription(self): 
        while True:
            try:
                self.appointment_id = int(input("Appointment ID:"))
                if not self.validate_login_id(self.appointment_id):
                    print("Appointment ID must be greater than 0")
                    continue 
                break 
    
            except sqlite3.Error as e:
                print("Appointment ID must be in numbers")
                continue 

        try:
            cursor.execute("""
            SELECT * FROM prescription
            WHERE appointment_id = ?
            """,(self.appointment_id,))
    
        except sqlite3.Error as e:
            print("Database Error", e)
            return 
    
        row = cursor.fetchone()
        if not row:
            print("No prescription found")
            return 
        else:
            self.appointment_id = row[1]
            print(f"Prescription ID:{row[0]}")
            self.show_prescription_details()
            return
    
    def delete_prescription(self):
        while True:
            try:
                self.appointment_id = int(input("Appointment ID:"))
                if not self.validate_login_id(self.appointment_id):
                    print("Appointment ID must be greater than 0")
                    continue 
                break 

            except sqlite3.Error as e:
                print("Appointment ID must be in numbers")
                continue 
        try:
            cursor.execute("""
            SELECT * FROM prescription
            WHERE appointment_id = ?
            """,(self.appointment_id,))

        except sqlite3.Error as e:
            print("Database Error", e)
            return 

        row = cursor.fetchone()
        if not row:
            print("No prescription found")
            return 
        else:
            self.appointment_id = row[1]
            print(f"Prescription ID:{row[0]}")
            self.show_prescription_details()

            while True:
                delete = input("Are you sure you want to delete prescription(Y/N)?").lower()
                if not self.validate_yes_no(delete):
                    print("Enter either Y or N to proceed")
                    continue 
                if delete == 'n':
                    print("Prescription - Delete aborted")
                    break 
                else:
                    while True:
                        try:
                            cursor.execute("""
                            DELETE FROM prescription
                            WHERE appointment_id = ?
                            """,(self.appointment_id,))

                            conn.commit()

                        except sqlite3.Error as e:
                            print("Database Error", e)
                            return 

                        print("Prescription deleted successfully")
                        return 


test = Prescription(
    "appointment_id"
    )
test.delete_prescription()

