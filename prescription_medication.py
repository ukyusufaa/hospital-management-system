# Import SQLite to work with the database
import sqlite3

# Import the shared database connection and cursor from database.py module.
from database import conn, cursor

class PrescriptionMedication():
        # Store the prescription-medication relationship and associated instructions.
    def __init__(self,prescription_instructions = None, 
                 prescription_id = None, medication_id = None):
        self.prescription_instructions = prescription_instructions
        self.prescription_id = prescription_id
        self.medication_id = medication_id

    def show_prescription_medication_details(self):
        print("-" * 30)
        print(f"Regimen Instructions: {self.prescription_instructions}")
        print(f"Prescription ID: {self.prescription_id}")
        print(f"Medication ID: {self.medication_id}")
        print("-" * 30)

    def validate_login_id(self,number):
        return number >= 1

    def validate_yes_no(self,choice):
        return choice == "y" or choice == "n"

        # Validate that the regimen instructions are within the permitted length.
    def validate_character_length(self,character):
        return 1 <= len(character) <= 100

    def create_prescription_medication(self):
        while True:
            self.prescription_instructions = input(
                "Please enter the regimen instructions(0-100): ").strip()
            
            if not self.validate_character_length(self.prescription_instructions):
                print("Please enter the regimen " \
                        "instructions between 1 and 100 characters.")
                continue 
            break 

        while True:
            try:
                self.prescription_id = int(input(
                    "Please enter the prescription ID: "))
                
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
                    self.medication_id = int(input(
                        "Please enter the medication ID: "))
                    
                    if not self.validate_login_id(self.medication_id):
                        print("Please enter a valid medication ID.")
                        continue 
                    break 
    
                except ValueError:
                    print("Please enter a valid medication ID " \
                    "using numbers only.")
                    continue

        # Check whether the prescription already contains the medication.
        try:
            cursor.execute("""
                SELECT * FROM prescription_medication
                WHERE prescription_id = ?
                AND medication_id = ?
            """,(self.prescription_id,
                 self.medication_id))

        except sqlite3.Error as e:
            print("Unable to check the prescription " \
                    "medication relationship. Please " \
                    "try again.", e)
            return

        # Check whether a relationship was found.
        relationship = cursor.fetchone()

        if relationship:
            print("This medication is already " \
                    "included on the prescription.")
            return

        # Create the prescription-medication relationship.
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

        # Save the new prescription-medication record to the database.
            conn.commit()

        except sqlite3.Error as e:
            print("Unable to add the " \
                    "regimen. Please " \
                    "try again.", e)
            return

        print("Regimen added successfully.")

        self.show_prescription_medication_details()
    

    def display_all_prescription_medications(self):
        try:
        # Get all prescription-medication records from the database.
            cursor.execute("SELECT * FROM prescription_medication")

        except sqlite3.Error as e:
            print("Unable to display regimens. " \
                    "Please try again.", e)
            return

        records = cursor.fetchall()

        if not records:
            print("No regimens stored "
                    "in the database.")
            return
        
        for record in records:
            prescription_medication = PrescriptionMedication(
                record[0],
                record[1],
                record[2]
            )

            prescription_medication.show_prescription_medication_details()
            

    def search_prescription_medication(self):
        while True:
            try:
                self.prescription_id = int(input(
                    "Please enter prescription ID: "))
                
                if not self.validate_login_id(self.prescription_id):
                    print("Please enter valid prescription ID.")
                    continue 
                break 

            except ValueError:
                print("Please enter a valid " \
                        "prescription ID using numbers only.")
                continue

        while True:
            try:
                self.medication_id = int(input(
                    "Please enter medication ID: "))
                
                if not self.validate_login_id(self.medication_id):
                    print("Please enter valid medication ID.")
                    continue 
                break 

            except ValueError:
                print("Please enter a valid " \
                        "medication ID using numbers only.")
                continue 
        try:
        # Find the prescription-medication record in the database.
            cursor.execute("""
                SELECT * FROM prescription_medication
                WHERE prescription_id = ?
                AND medication_id = ?
            """,(self.prescription_id,
                 self.medication_id))

        except sqlite3.Error as e:
            print("Unable to search for " \
                    "the regimen.", e)
            return 

        record = cursor.fetchone()

        if not record:
            print("No regimen was found " \
                    "for this prescription")
            return
        
        self.prescription_instructions = record[0]
        self.prescription_id = record[1]
        self.medication_id = record[2]

        self.show_prescription_medication_details()
        

    def update_prescription_medication(self):
        while True:
            try:
                self.prescription_id = int(input(
                    "Please enter the prescription ID:"))
                
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
                    self.medication_id = int(input(
                        "Please enter the medication ID:"))
                    
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
        # Find the prescription-medication record in the database.
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

        record = cursor.fetchone()

        if not record:
            print("No regimen was found for " \
                    "this prescription and medication.")
            return
        
        self.prescription_instructions = record[0]
        self.prescription_id = record[1]
        self.medication_id = record[2]

        self.show_prescription_medication_details()

        while True:
            update = input(
                "Update the regimen instructions? (Y/N):").lower()
            
            if not self.validate_yes_no(update):
                print("Please enter Y/y or N/n.")
                continue

            if update == 'n':
                print("Regimen update cancelled. " \
                        "No changes were made.")
                return
            break 
                
        while True:
            updated_prescription_instructions = input(
                        "Please enter the new regimen "
                        "instructions (1 - 100 characters): ")
                
            if not self.validate_character_length(updated_prescription_instructions):
                print("Please enter regimen " \
                        "instructions between 1 and " \
                        "100 characters.")
                continue
            break 

        self.prescription_instructions = updated_prescription_instructions

        try:
        # Update the regimen instructions for the selected prescription-medication record.
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
            

    def delete_prescription_medication(self):
        while True:
            try:
                self.prescription_id = int(input(
                    "Please enter prescription ID: "))
                
                if not self.validate_login_id(self.prescription_id):
                    print("Please enter valid prescription ID.")
                    continue 
                break

            except ValueError:
                print("Please enter a valid " \
                        "prescription ID using numbers only.")
                continue 

        while True:
            try:
                self.medication_id = int(input(
                    "Please enter medication ID: "))
                
                if not self.validate_login_id(self.medication_id):
                    print("Please enter valid medication ID.")
                    continue 
                break 

            except ValueError:
                print("Please enter a valid " \
                        "medication ID using numbers only.")
                continue 
                
        try:
        # Find the regimen associated with the specified medication.
            cursor.execute("""
                SELECT * FROM prescription_medication
                WHERE prescription_id = ?
                AND medication_id = ?
            """,(self.prescription_id,
                 self.medication_id))
        
        except sqlite3.Error as e:
            print("Unable to search for " \
            "the regimen.", e)
            return 
        
        record = cursor.fetchone()

        if not record:
            print("No regimen was found " \
                    "for this prescription")
            return
        
        
        self.prescription_instructions = record[0]
        self.prescription_id = record[1]
        self.medication_id = record[2]
            
        self.show_prescription_medication_details()

        while True:
            delete = input("Delete " \
                "this prescription medication? (Y/N):").lower()

            if not self.validate_yes_no(delete):
                print("Please enter Y/y or N/n.")
                continue 

            if delete == "n":
                print("Deletion cancelled.")

        # Exit the method because the deletion was cancelled.
                return
        # Exit the confirmation loop and continue with the deletion.
            break 
            
        try:
            cursor.execute("""
                DELETE FROM prescription_medication
                WHERE prescription_id = ?
                AND medication_id = ?
            """,(self.prescription_id,
                self.medication_id))

            conn.commit()

        except sqlite3.Error as e:
            print("Unable to delete " \
                    "the prescription. Please " \
                    "try again.", e)
            return

        print("Prescription medication deleted successfully.")
         

                    
        

        
