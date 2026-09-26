import sqlite3
from database import conn, cursor
from colors import DISPLAY_INFO,MEDICATION_MENU,ERROR,RESET

class Medication():
    def __init__(self,medication_name = None, cost = None):
        self.medication_name = medication_name
        self.cost = cost
    
    def show_medication_details(self):
        print("=" * 30)
        print(f"{DISPLAY_INFO}Medication Name:{self.medication_name}{RESET}")
        print(f"{DISPLAY_INFO}Cost:{self.cost}{RESET}")
        print("-" * 30)

        # Validate IDs to ensure they are positive integers.
    def validate_login_id(self,number):
        if number < 1:
            return False
        return True

        # Validate medication names using letters, numbers and spaces.
    def validate_medication_name(self,name):
       return all(
           character.isalpha()
           or character.isdigit()
           or character == " "
           for character in name
       )

        # Validate medication cost as positive values with two decimal places.
    def validate_medication_cost(self,cost):
        return cost > 0 and cost == round(cost,2)

        # Collect and validate medication details before saving the record.
    def create_medication(self):
        while True:
            self.medication_name = input(f"{MEDICATION_MENU}Enter medication " 
                    f"name and strength (for example: Paracetamol 500mg): {RESET}")
            
            if self.medication_name == "":
                print(f"{ERROR}Medication Name is required. Please enter " 
                        f"a medication name and strength.{RESET}")
                continue

            if not any(character.isalpha()
                       for character in self.medication_name):
                print(f"{ERROR}Please enter the medication name.{RESET}")
                continue

            if not any(character.isdigit()
                       for character in self.medication_name):
                print(f"{ERROR}Please enter a medication strength.{RESET}")
                continue

            if not any(character == " "
                       for character in self.medication_name):
                print(f"{ERROR}Please enter the medication name " 
                        f"and its strength separated by a space.{RESET}")
                continue
            
            if not self.validate_medication_name(self.medication_name):
                print(f"{ERROR}Please use letters, numbers and spaces only.{RESET}")
                continue 
            break

        while True:
            try:
                self.cost = float(input(f"{MEDICATION_MENU}Enter medication cost: {RESET}"))

                if not self.validate_medication_cost(self.cost):
                    print(f"{ERROR}Medication cost must be greater " 
                            f"than £0:00 and have no more than 2 decimal places.{RESET}")
                    continue 
                break

            except ValueError:
                print(f"{ERROR}Please enter the medication cost as a number (decimal).{RESET}")
                continue

        try:
            # Insert the validated medication details into the database.
            cursor.execute("""
                INSERT INTO medication(
                    medication_name,
                    cost)
                VALUES(?,?)
            """,(self.medication_name, self.cost))

            conn.commit()

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to save the medication. Please try again.{RESET}", e)
            return

        print(f"{DISPLAY_INFO}Medication created successfully.{RESET}")

        medication_id = cursor.lastrowid
        print(f"{DISPLAY_INFO}Medication ID: {medication_id}{RESET}")
        self.show_medication_details()


        # Retrieve and display all medications stored in the database.
    def display_all_medications(self):
        cursor.execute("SELECT * FROM medication")

        medication_rows = cursor.fetchall()

        if not medication_rows :
            print(f"{ERROR}No medications are currently registered.{RESET}")
            return 
        
        for medication_row in medication_rows:
            medication = Medication(
                medication_row[1],
                medication_row[2]
                )
            
            print(f"{DISPLAY_INFO}Medication ID: {medication_row[0]}{RESET}")
            medication.show_medication_details()
            print()
        

        # Find a medication using its unique medication ID.
    def search_medication(self):
        while True:
            try:
                medication_id = int(input(f"{MEDICATION_MENU}Enter medication ID: {RESET}"))
                
                if not self.validate_login_id(medication_id):
                    print(f"{ERROR}Please enter a valid medication ID.{RESET}")
                    continue 
                break 

            except ValueError:
                print(f"{ERROR}Please enter the medication ID using numbers only.{RESET}")
                continue 
        try: 
            cursor.execute("""
                SELECT * FROM medication
                WHERE medication_id = ?
            """,(medication_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to search for the medication. Please try again.{RESET}", e)
            return

        medication_row = cursor.fetchone()

        if not medication_row:
            print(f"{ERROR}No medication was found with that ID.{RESET}")
            return
        
        self.medication_name = medication_row[1]
        self.cost = medication_row[2]
        
        print(f"{DISPLAY_INFO}Medication ID: {medication_row[0]}{RESET}")
        self.show_medication_details()
    

        # Update the details of an existing medication.
    def update_medication(self):
        while True:
            try:
                medication_id = int(input(f"{MEDICATION_MENU}Enter medication ID: {RESET}"))

                if not self.validate_login_id(medication_id):
                    print(f"{ERROR}Please enter a valid medication ID.{RESET}")
                    continue 
                break

            except ValueError:
                print(f"{ERROR}Please enter the medication ID using numbers only.{RESET}")
                continue 
        try:
            cursor.execute("""
            SELECT * FROM medication
            WHERE medication_id = ?
            """,(medication_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to retrieve the medication. Please try again.{RESET}", e)
            return

        medication_row = cursor.fetchone()

        if not medication_row:
            print(f"{ERROR}No medication was found with that ID.{RESET}")
            return 
        
        self.medication_name = medication_row[1]
        self.cost = medication_row[2]

        print(f"{DISPLAY_INFO}Medication ID: {medication_row[0]}{RESET}")
        self.show_medication_details()
        print()
            
        update = input(f"{MEDICATION_MENU}Update this medication? (Y/N): {RESET}").lower()
        
        if update == "y":
            while True:
                new_medication_name = input(f"{MEDICATION_MENU}Enter new medication " 
                                            f"name and strength: {RESET}").strip()
                
                if not any(character.isalpha()
                        for character in new_medication_name):
                    print(f"{ERROR}Please enter the medication name.{RESET}")
                    continue

                if not any(character.isdigit()
                       for character in new_medication_name):
                    print(f"{ERROR}Please enter a medication strength.{RESET}")
                    continue

                if not any(character == " "
                       for character in new_medication_name):
                    print(f"{ERROR}Please enter the medication name " 
                            f"and its strength separated by a space.{RESET}")
                    continue

                if not self.validate_medication_name(new_medication_name):
                    print(f"{ERROR}Please use letters, " 
                            f"numbers and spaces only.{RESET}")
                    continue 
                break

            while True:
                try:
                    new_cost = float(input(f"{MEDICATION_MENU}Enter new medication" 
                                           f"cost (£): {RESET}"))
                    
                    if not self.validate_medication_cost(new_cost):
                        print(f"{ERROR}Medication cost must be greater than £0:00 and have " 
                                f"no more than 2 decimal places.{RESET}")
                        continue 
                    break

                except ValueError:
                    print(f"{ERROR}Please enter the medication cost as a number.{RESET}")
                    continue
                
            self.medication_name = new_medication_name
            self.cost = new_cost

            try:
                cursor.execute("""
                    UPDATE medication
                    SET medication_name = ?,
                        cost = ?
                    WHERE medication_id = ?
                """,(self.medication_name, self.cost, medication_id))

                conn.commit()

            except sqlite3.Error as e:
                print(f"{ERROR}Unable to update the medication. Please try again.{RESET}", e)
                return
                
            print(f"{DISPLAY_INFO}Medication updated successfully.{RESET}")
        else:   
            print(f"{DISPLAY_INFO}Medication update cancelled.{RESET}")
            

        # Confirm and remove an existing medication from the database.
    def delete_medication(self):
        while True:
            try:
                medication_id = int(input(f"{MEDICATION_MENU}Enter medication ID: {RESET}"))

                if not self.validate_login_id(medication_id):
                    print(f"{ERROR}Please enter a valid medication ID.{RESET}")
                    continue 
                break

            except ValueError:
                print(f"{ERROR}Please enter the medication ID using numbers only.{RESET}")
                continue 
        try:
            cursor.execute("""
                SELECT * FROM medication
                WHERE medication_id = ?
            """,(medication_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to retrieve the medication. Please try again.{RESET}", e)
            return

        medication_row = cursor.fetchone()

        if not medication_row:
            print(f"{ERROR}No medication was found with that ID.{RESET}")
            return
        
        self.medication_name = medication_row[1]
        self.cost = medication_row[2]

        print(f"{DISPLAY_INFO}Medication ID:{medication_row[0]}{RESET}")
        self.show_medication_details()
        print()

        delete = input(f"{MEDICATION_MENU}Delete this medication? (Y/N): {RESET}").lower()

        if delete == "y":

            try:
                cursor.execute("""
                    DELETE FROM medication
                    WHERE medication_id = ?
                """,(medication_id,))

                conn.commit()

            except sqlite3.Error as e:
                print(f"{ERROR}Unable to delete the medication. Please try again.{RESET}", e)
                return 
                
            print(f"{DISPLAY_INFO}Medication deleted successfully.{RESET}")
            
        else:
            print(f"{DISPLAY_INFO}Medication deletion cancelled.{RESET}")
                


        
    