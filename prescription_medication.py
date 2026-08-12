import sqlite3

conn = sqlite3.connect("hospital.db")

cursor = conn.cursor()

# Enable foreign key constraints to maintain relationships between tables.
cursor.execute("PRAGMA foreign_keys = ON;")

class PrescriptionMedication():
        # Store the prescription-medication relationship and associated instructions.
    def __init__(self,prescription_instructions = None, 
                 prescription_id = None, medication_id = None):
        self.prescription_instructions = prescription_instructions
        self.prescription_id = prescription_id
        self.medication_id = medication_id

    def show_prescription_medication_details(self):
        print("-" * 30)
        print(f"Regimen Instructions:{self.prescription_instructions}")
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

        # Validate that the regimen instructions are within the permitted length.
    def validate_character_length(self,character):
        if len(character) == 0 or len(character) > 100:
            return False
        return True

    def create_prescription_medication(self):
        while True:
            self.prescription_instructions = input(
                "Please enter the regimen "
                "instructions(0-100): ")
            if not self.validate_character_length(self.prescription_instructions):
                print("Please enter the regimen " \
                "instructions between 1 and 100 characters.")
                continue 
            break 

        while True:
            try:
                self.prescription_id = int(
                input("Please enter the prescription ID:"))
                if not self.validate_login_id(self.prescription_id):
                    print("Please enter a valid prescription ID.")
                    continue 
                break 

            except ValueError:
                print("Please enter a valid prescription ID " \
                "using numbers only.")
                continue 

        while True:
                try:
                    self.medication_id = int(
                        input("Please enter the medication ID:"))
                    if not self.validate_login_id(self.medication_id):
                        print("Please enter a valid medication ID.")
                        continue 
                    break 
    
                except ValueError:
                    print("Please enter a valid medication ID " \
                    "using numbers only.")
                    continue

        try:
        # Create the link between the prescription and medication.
        # Store the associated regimen instructions.
            cursor.execute("""
            INSERT INTO prescription_medication(
                        prescription_instructions,
                        prescription_id,
                        medication_id)
            VALUES(?,?,?)
            """,(self.prescription_instructions,
             self.prescription_id,
             self.medication_id))

        # Save the new prescription-medication record to the database.
            conn.commit()

        except sqlite3.Error as e:
            print("Unable to add the " \
            "regimen. Please " \
            "try again.", e)
            return

        print("Regimen added successfully.")
        self.show_prescription_medication_details()
        return

    def display_all_prescription_medications(self):
        try:
        # Retrieve all the prescription-medication relationships from the database.
            cursor.execute("SELECT * FROM prescription_medication")

        except sqlite3.Error as e:
            print("Unable to display regimens. " \
            "Please try again.", e)
            return

        rows = cursor.fetchall()
        if not rows:
            print("No regimens stored "
            "in the database.")
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
                self.prescription_id = int(
                    input("Please enter prescription ID: "))
                if not self.validate_login_id(self.prescription_id):
                    print("Please enter valid prescription ID.")
                    continue 
                break 

            except ValueError:
                print("Please enter a valid " \
                "prescription ID using numbers only.")
                continue 
        try:
        # Find the regimen associated with the specified medication.
            cursor.execute("""
            SELECT * FROM prescription_medication
            WHERE prescription_id = ?
            """,(self.prescription_id,))

        except sqlite3.Error as e:
            print("Unable to search for " \
            "the regimen.", e)
            return 

        row = cursor.fetchone()
        if not row:
            print("No regimen was found " \
            "for this prescription")
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
                self.prescription_id = int(
                    input("Please enter the prescription ID:"))
                if not self.validate_login_id(self.prescription_id):
                    print("Please enter a valid " \
                    "prescription ID.")
                    continue 
                break 

            except ValueError:
                print("Please enter a valid " \
                "prescription ID using numbers only.")
                continue 

        while True:
                try:
                    self.medication_id = int(
                        input("Please enter the medication ID:"))
                    if not self.validate_login_id(self.medication_id):
                        print("Please enter a " \
                        "valid medication ID.")
                        continue 
                    break 
    
                except ValueError:
                    print("Please enter a valid " \
                    "medication ID using numbers only.")
                    continue
        try:
        # Locate the specific prescription-medication relationship using both IDs.
            cursor.execute("""
            SELECT * FROM prescription_medication
            WHERE medication_id = ?
            AND prescription_id = ?
            """,(self.medication_id,self.prescription_id))

        except sqlite3.Error as e:
            print("Unable to find " \
            "the regimen. Please " \
            "try again.", e)
            return 

        row = cursor.fetchone()
        if not row:
            print("No regimen was found for " \
            "this prescription and medication.")
            return
        else:
            self.prescription_instructions = row[0]
            self.prescription_id = row[1]
            self.medication_id = row[2]
            self.show_prescription_medication_details()

            while True:
                update = input(
                    "Update the regimen instructions? (Y/N):").lower()
                if not self.validate_yes_no(update):
                    print("Please enter Y/y " \
                    "or N/n.")
                    continue 
                if update == 'n':
                    print("Regimen update cancelled. " \
                    "No changes were made.")
                    break 
                else:
                    while True:
                        updated_prescription_instructions = input(
                            "Please enter the new regimen "
                            "instructions (1 - 100 characters):")
                        if not self.validate_character_length(updated_prescription_instructions):
                            print("Please enter regimen " \
                            "instructions between 1 and " \
                            "100 characters.")
                            continue
                        break 

                    self.prescription_instructions = updated_prescription_instructions

                    try:
        # Update regimen instructions for the selected prescription-medication relationship.
                        cursor.execute("""
                        UPDATE prescription_medication
                        SET prescription_instructions = ?
                        WHERE prescription_id = ?
                        AND medication_id = ?
                        """,(self.prescription_instructions,self.prescription_id,
                         self.medication_id))

        # Save the updated regimen instructions to the database.
                        conn.commit()

                    except sqlite3.Error as e:
                        print("Unable to update the " \
                        "regimen instructions. " \
                        "Please try again.", e)
                        return 
                    
                    print("Regimen instructions updated successfully.")
                    return

        
