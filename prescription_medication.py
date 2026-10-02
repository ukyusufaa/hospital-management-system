import sqlite3
from colors import DISPLAY_INFO,PRESCRIPTION_INSTRUCTIONS_MENU,ERROR,RESET

class PrescriptionMedication():
        # Store the prescription-medication relationship and associated instructions.
    def __init__(self,database,prescription_instructions = None, 
                 prescription_id = None, medication_id = None):
        self.database = database
        self.prescription_instructions = prescription_instructions
        self.prescription_id = prescription_id
        self.medication_id = medication_id

    def show_prescription_medication_details(self):
        print("=" * 30)
        print(f"{DISPLAY_INFO}Regimen Instructions: {self.prescription_instructions}{RESET}")
        print(f"{DISPLAY_INFO}Prescription ID: {self.prescription_id}{RESET}")
        print(f"{DISPLAY_INFO}Medication ID: {self.medication_id}{RESET}")
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
            self.prescription_instructions = input(f"{PRESCRIPTION_INSTRUCTIONS_MENU}Please " 
                        f"enter the regimen instructions(0-100): ").strip()
            
            if not self.validate_character_length(self.prescription_instructions):
                print(f"{ERROR}Please enter the regimen " 
                      f"instructions between 1 and 100 characters.{RESET}")
                continue 
            break 

        while True:
            try:
                self.prescription_id = int(input(f"{PRESCRIPTION_INSTRUCTIONS_MENU}Please " 
                                                 f"enter the prescription ID: {RESET}"))
                
                if not self.validate_login_id(self.prescription_id):
                    print(f"{ERROR}Please enter a valid prescription ID.{RESET}")
                    continue 
                break 

            except ValueError:
                print(f"{ERROR}Please enter a valid prescription ID " 
                      f"using numbers only.{RESET}")
                continue 

        while True:
                try:
                    self.medication_id = int(input(f"{PRESCRIPTION_INSTRUCTIONS_MENU}Please " 
                                                   f"enter the medication ID: {RESET}"))
                    
                    if not self.validate_login_id(self.medication_id):
                        print(f"{ERROR}Please enter a valid medication ID.{RESET}")
                        continue 
                    break 
    
                except ValueError:
                    print(f"{ERROR}Please enter a valid medication ID " 
                          f"using numbers only.{RESET}")
                    continue

        # Check whether the prescription already contains the medication.
        try:
            self.database.cursor.execute("""
                SELECT * FROM prescription_medication
                WHERE prescription_id = ?
                AND medication_id = ?
            """,(self.prescription_id,
                 self.medication_id))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to check the prescription medication relationship. " 
                  f"Please try again.{e}{RESET}")
            return

        # Check whether a relationship was found.
        relationship = self.database.cursor.fetchone()

        if relationship:
            print(f"{ERROR}This medication is already included on the prescription.{RESET}")
            return

        # Create the prescription-medication relationship.
        try:
            self.database.cursor.execute("""
                INSERT INTO prescription_medication(
                    prescription_instructions,
                    prescription_id,
                    medication_id)
                VALUES(?,?,?)
            """,(self.prescription_instructions,
                self.prescription_id,
                self.medication_id))

        # Save the new prescription-medication record to the database.
            self.database.connection.commit()

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to add the regimen. Please try again.{e}{RESET}")
            return

        print(f"{DISPLAY_INFO}Regimen added successfully.{RESET}")
        print()

        self.show_prescription_medication_details()
    

    def display_all_prescription_medications(self):
        try:
        # Get all prescription-medication records from the database.
            self.database.cursor.execute("SELECT * FROM prescription_medication")

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to display regimens. Please try again.{e}{RESET}")
            return

        records = self.database.cursor.fetchall()

        if not records:
            print(f"{ERROR}No regimens stored in the database.{RESET}")
            return
        
        for record in records:
            prescription_medication = PrescriptionMedication(
                record[0],
                record[1],
                record[2]
            )

            prescription_medication.show_prescription_medication_details()
            print()
            

    def search_prescription_medication(self):
        while True:
            try:
                self.prescription_id = int(input(f"{PRESCRIPTION_INSTRUCTIONS_MENU}Please " 
                                                 f"enter prescription ID: {RESET}"))
                
                if not self.validate_login_id(self.prescription_id):
                    print(f"{ERROR}Please enter valid prescription ID.{RESET}")
                    continue 
                break 

            except ValueError:
                print(f"{ERROR}Please enter a valid prescription ID " 
                      f"using numbers only.{RESET}")
                continue

        while True:
            try:
                self.medication_id = int(input(f"{PRESCRIPTION_INSTRUCTIONS_MENU}Please " 
                                               f"enter medication ID: {RESET}"))
                
                if not self.validate_login_id(self.medication_id):
                    print(f"{ERROR}Please enter valid medication ID.{RESET}")
                    continue 
                break 

            except ValueError:
                print(f"{ERROR}Please enter a valid medication ID using numbers only.{RESET}")
                continue 
        try:
        # Find the prescription-medication record in the database.
            self.database.cursor.execute("""
                SELECT * FROM prescription_medication
                WHERE prescription_id = ?
                AND medication_id = ?
            """,(self.prescription_id,
                 self.medication_id))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to search for the regimen.{e}{RESET}")
            return 

        record = self.database.cursor.fetchone()

        if not record:
            print(f"{ERROR}No regimen was found for this prescription.{RESET}")
            return
        
        self.prescription_instructions = record[0]
        self.prescription_id = record[1]
        self.medication_id = record[2]

        self.show_prescription_medication_details()
        

    def update_prescription_medication(self):
        while True:
            try:
                self.prescription_id = int(input(f"{PRESCRIPTION_INSTRUCTIONS_MENU}Please "
                            f"enter the prescription ID: {RESET}"))
                
                if not self.validate_login_id(self.prescription_id):
                    print(f"{ERROR}Please enter a valid prescription ID.{RESET}")
                    continue 
                break 

            except ValueError:
                print(f"{ERROR}Please enter a valid prescription ID " 
                      f"using numbers only.{RESET}")
                continue 

        while True:
                try:
                    self.medication_id = int(input(f"{PRESCRIPTION_INSTRUCTIONS_MENU}Please " 
                                                   f"enter the medication ID: {RESET}"))
                    
                    if not self.validate_login_id(self.medication_id):
                        print(f"{ERROR}Please enter a valid medication ID.{RESET}")
                        continue 
                    break 
    
                except ValueError:
                    print(f"{ERROR}Please enter a valid " 
                          f"medication ID using numbers only.{RESET}")
                    continue
        try:
        # Find the prescription-medication record in the database.
            self.database.cursor.execute("""
            SELECT * FROM prescription_medication
            WHERE medication_id = ?
            AND prescription_id = ?
            """,(self.medication_id,self.prescription_id))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to find the regimen. Please try again.{e}{RESET}")
            return 

        record = self.database.cursor.fetchone()

        if not record:
            print(f"{ERROR}No regimen was found for this prescription and medication.{RESET}")
            return
        
        self.prescription_instructions = record[0]
        self.prescription_id = record[1]
        self.medication_id = record[2]

        self.show_prescription_medication_details()
        print()

        while True:
            update = input(f"{PRESCRIPTION_INSTRUCTIONS_MENU}Update " 
                           f"the regimen instructions? (Y/N): {RESET}").lower()
            
            if not self.validate_yes_no(update):
                print(f"{ERROR}Please enter Y/y or N/n.{RESET}")
                continue

            if update == 'n':
                print(f"{ERROR}Regimen update cancelled. No changes were made.{RESET}")
                return
            break 
                
        while True:
            updated_prescription_instructions = input(f"{PRESCRIPTION_INSTRUCTIONS_MENU}Please " 
                        f"enter the new regimen instructions (1 - 100 characters): {RESET}")
                
            if not self.validate_character_length(updated_prescription_instructions):
                print(f"{ERROR}Please enter regimen instructions between 1 and " 
                      f"100 characters.{RESET}")
                continue
            break 

        self.prescription_instructions = updated_prescription_instructions

        try:
        # Update the regimen instructions for the selected prescription-medication record.
            self.database.cursor.execute("""
                UPDATE prescription_medication
                SET prescription_instructions = ?
                WHERE prescription_id = ?
                AND medication_id = ?
            """,(self.prescription_instructions,self.prescription_id,
                self.medication_id))

        # Save the updated regimen instructions to the database.
            self.datbase.connection.commit()

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to update the regimen instructions. "
                  f"Please try again.{e}{RESET}")
            return 
                    
        print(f"{DISPLAY_INFO}Regimen instructions updated successfully.{RESET}")
            

    def delete_prescription_medication(self):
        while True:
            try:
                self.prescription_id = int(input(f"{PRESCRIPTION_INSTRUCTIONS_MENU}Please " 
                                                 f"enter prescription ID: {RESET}"))
                
                if not self.validate_login_id(self.prescription_id):
                    print(f"{ERROR}Please enter valid prescription ID.{RESET}")
                    continue 
                break

            except ValueError:
                print(f"{ERROR}Please enter a valid prescription ID " 
                      f"using numbers only.{RESET}")
                continue 

        while True:
            try:
                self.medication_id = int(input(f"{PRESCRIPTION_INSTRUCTIONS_MENU}Please "
                                               f"enter medication ID: {RESET}"))
                
                if not self.validate_login_id(self.medication_id):
                    print(f"{ERROR}Please enter valid medication ID.{RESET}")
                    continue 
                break 

            except ValueError:
                print(f"{ERROR}Please enter a valid " 
                      f"medication ID using numbers only.{RESET}")
                continue 
                
        try:
        # Find the regimen associated with the specified medication.
            self.database.cursor.execute("""
                SELECT * FROM prescription_medication
                WHERE prescription_id = ?
                AND medication_id = ?
            """,(self.prescription_id,
                 self.medication_id))
        
        except sqlite3.Error as e:
            print(f"{ERROR}Unable to search for the regimen.{e}{RESET}")
            return 
        
        record = self.database.cursor.fetchone()

        if not record:
            print(f"{ERROR}No regimen was found for this prescription.{RESET}")
            return
        
        
        self.prescription_instructions = record[0]
        self.prescription_id = record[1]
        self.medication_id = record[2]
            
        self.show_prescription_medication_details()
        print()

        while True:
            delete = input(f"{PRESCRIPTION_INSTRUCTIONS_MENU}Delete "
                           f"this prescription medication? (Y/N): {RESET}").lower()

            if not self.validate_yes_no(delete):
                print(f"{ERROR}Please enter Y/y or N/n.{RESET}")
                continue 

            if delete == "n":
                print(f"{DISPLAY_INFO}Deletion cancelled.{RESET}")

        # Exit the method because the deletion was cancelled.
                return
        # Exit the confirmation loop and continue with the deletion.
            break 
            
        try:
            self.database.cursor.execute("""
                DELETE FROM prescription_medication
                WHERE prescription_id = ?
                AND medication_id = ?
            """,(self.prescription_id,
                self.medication_id))

            self.database.connection.commit()

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to delete the prescription. Please try again.{e}{RESET}")
            return

        print(f"{DISPLAY_INFO}Prescription medication deleted successfully.{RESET}")
         

                    
        

        
