import sqlite3

conn = sqlite3.connect("hospital.db")

cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

class PrescriptionMedication():
    def __init__(self,prescription_instructions = None, 
                 prescription_id = None, medication_id = None):
        self.prescription_instructions = prescription_instructions
        self.prescription_id = prescription_id
        self.medication_id = medication_id

    def show_prescription_medication_details(self):
        print("-" * 30)
        print(f"Prescription Instructions:{self.prescription_instructions}")
        print(f"Prescription ID:{self.prescription_id}")
        print(f"Medication ID:{self.medication_id}")
        print("-" * 30)

    def validate_login_id(self,number):
        if number < 1:
            return False
        return True 

    def validate_yes_no(self,choice):
        if not choice == "y" and choice != "n":
            return False
        return True

    def validate_character_length(self,character):
        if len(character) == 0 or len(character) > 100:
            return False
        return True

    def create_prescription_medication(self):
        while True:
            self.prescription_instructions = input("Prescription Instructions(0-100): ")
            if not self.validate_character_length(self.prescription_instructions):
                print("Prescription Instructions - Character length "
                "is either too small or too great(0-70)")
                continue 
            break 

        while True:
            try:
                self.prescription_id = int(input("Prescription ID:"))
                if not self.validate_login_id(self.prescription_id):
                    print("Prescription ID must be greater than 0")
                    continue 
                break 

            except ValueError:
                print("Prescription ID must be numbers")
                continue 

        while True:
                try:
                    self.medication_id = int(input("Medication ID:"))
                    if not self.validate_login_id(self.medication_id):
                        print("Medication ID must be greater than 0")
                        continue 
                    break 
    
                except ValueError:
                    print("Medication ID must be numbers")
                    continue

        try:
            cursor.execute("""
            INSERT INTO prescription_medication(
                        prescription_instructions,
                        prescription_id,
                        medication_id)
            VALUES(?,?,?)
            """,(self.prescription_instructions,
             self.prescription_id,
             self.medication_id))

            conn.commit()

        except sqlite3.Error as e:
            print("Database Error", e)
            return

        print("Prescription Instructions successfully Inserted")
        self.show_prescription_medication_details()
        return

    def display_all_prescription_medications(self):
        try:
            cursor.execute("SELECT * FROM prescription_medication")

        except sqlite3.Error as e:
            print("Database Error", e)
            return

        rows = cursor.fetchall()
        if not rows:
            print("No medical/prescription data found")
        else:
            for row in rows:
                prescripts_meds = PrescriptionMedication(
                    row[0],
                    row[1],
                    row[2]
                )
                prescripts_meds.show_prescription_medication_details()
            return

    def search_prescription_medication(self):
        while True:
            try:
                self.prescription_id = int(input("Prescription ID:"))
                if not self.validate_login_id(self.prescription_id):
                    print("Prescription ID must be greater than 0")
                    continue 
                break 

            except ValueError:
                print("Prescription ID must be numbers")
                continue 
        try:
            cursor.execute("""
            SELECT * FROM prescription_medication
            WHERE prescription_id = ?
            """,(self.prescription_id,))

        except sqlite3.Error as e:
            print("Database Error", e)
            return 

        row = cursor.fetchone()
        if not row:
            print("No medication/prescription data found")
            return
        else:
            self.prescription_instructions = row[0]
            self.prescription_id = row[1]
            self.medication_id = row[2]
            self.show_prescription_medication_details()
            return

    def update_prescription_medication(self):
        while True:
            try:
                self.prescription_id = int(input("Prescription ID:"))
                if not self.validate_login_id(self.prescription_id):
                    print("Prescription ID must be greater than 0")
                    continue 
                break 

            except ValueError:
                print("Prescription ID must be numbers")
                continue 

        while True:
                try:
                    self.medication_id = int(input("Medication ID:"))
                    if not self.validate_login_id(self.medication_id):
                        print("Medication ID must be greater than 0")
                        continue 
                    break 
    
                except ValueError:
                    print("Medication ID must be numbers")
                    continue
        try:
            cursor.execute("""
            SELECT * FROM prescription_medication
            WHERE medication_id = ?
            AND prescription_id = ?
            """,(self.medication_id,self.prescription_id))

        except sqlite3.Error as e:
            print("Database Error", e)
            return 

        row = cursor.fetchone()
        if not row:
            print("No medication/prescription data found")
            return
        else:
            self.prescription_instructions = row[0]
            self.prescription_id = row[1]
            self.medication_id = row[2]
            self.show_prescription_medication_details()

            while True:
                update = input("Are you sure you want to update instructions(Y/N)?").lower()
                if not self.validate_yes_no(update):
                    print("Enter either Y or N to proceed")
                    continue 
                if update == 'n':
                    print("Instructions - Update process aborted")
                    break 
                else:
                    while True:
                        updated_prescription_instructions = input("Prescription Instructions(0-100)")
                        if not self.validate_character_length(updated_prescription_instructions):
                            print("Prescription Instructions - Character length "
                            "is either too small or too great(0-70)")
                            continue
                        break 

                    self.prescription_instructions = updated_prescription_instructions

                    try:
                        cursor.execute("""
                        UPDATE prescription_medication
                        SET prescription_instructions = ?
                        WHERE prescription_id = ?
                        AND medication_id = ?
                        """,(self.prescription_instructions,self.prescription_id,
                         self.medication_id))

                        conn.commit()

                    except sqlite3.Error as e:
                        print("Database Error", e)
                        return 
                    
                    print("Medical Instructions updated sucessfully")
                    return

        
