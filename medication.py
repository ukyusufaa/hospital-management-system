import sqlite3
from database import conn, cursor

class Medication():
    def __init__(self,medication_name = None, cost = None):
        self.medication_name = medication_name
        self.cost = cost
    
    def show_medication_details(self):
        print("-" * 30)
        print(f"Medication Name:{self.medication_name}")
        print(f"Cost:{self.cost}")
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
            self.medication_name = input("Enter medication " \
                    "name and strength (for example: Paracetamol 500mg): ")
            
            if self.medication_name == "":
                print("Medication Name is required. Please enter " \
                        "a medication name and strength.")
                continue

            if not any(character.isalpha()
                       for character in self.medication_name):
                print("Please enter the medication name.")
                continue

            if not any(character.isdigit()
                       for character in self.medication_name):
                print("Please enter a medication strength.")
                continue

            if not any(character == " "
                       for character in self.medication_name):
                print("Please enter the medication name " \
                        "and its strength separated by a space.")
                continue
            
            if not self.validate_medication_name(self.medication_name):
                print("Please use letters, numbers and " \
                        "spaces only.")
                continue 
            break

        while True:
            try:
                self.cost = float(input("Enter medication cost: "))

                if not self.validate_medication_cost(self.cost):
                    print("Medication cost must be greater " \
                            "than £0:00 and have no more than " \
                            "2 decimal places.")
                    continue 
                break

            except ValueError:
                print("Please enter the medication cost as " \
                        "a number (decimal).")
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
            print("Unable to save the medication. " \
                    "Please try again.", e)
            return

        print("Medication created successfully.")

        medication_id = cursor.lastrowid
        print(f"Medication ID: {medication_id}")
        self.show_medication_details()


        # Retrieve and display all medications stored in the database.
    def display_all_medications(self):
        cursor.execute("SELECT * FROM medication")

        medication_rows = cursor.fetchall()

        if not medication_rows :
            print("No medications are " \
            "currently registered.")
            return 
        
        for medication_row in medication_rows:
            medication = Medication(
                medication_row[1],
                medication_row[2]
                )
            
            print(f"Medication ID: {medication_row[0]}")
            medication.show_medication_details()
        

        # Find a medication using its unique medication ID.
    def search_medication(self):
        while True:
            try:
                medication_id = int(input(
                    "Enter medication ID: "))
                
                if not self.validate_login_id(medication_id):
                    print("Please enter a valid " \
                            "medication ID.")
                    continue 
                break 

            except ValueError:
                print("Please enter the medication ID " \
                        "using numbers only.")
                continue 
        try: 
            cursor.execute("""
                SELECT * FROM medication
                WHERE medication_id = ?
            """,(medication_id,))

        except sqlite3.Error as e:
            print("Unable to search for the " \
                    "medication. Please try again.", e)
            return

        medication_row = cursor.fetchone()

        if not medication_row:
            print("No medication was found " \
                    "with that ID.")
            return
        
        self.medication_name = medication_row[1]
        self.cost = medication_row[2]
        
        print(f"Medication ID: {medication_row[0]}")
        self.show_medication_details()
    

        # Update the details of an existing medication.
    def update_medication(self):
        while True:
            try:
                medication_id = int(input("Enter medication ID: "))

                if not self.validate_login_id(medication_id):
                    print("Please enter a valid medication ID.")
                    continue 
                break

            except ValueError:
                print("Please enter the medication ID " \
                "using numbers only.")
                continue 
        try:
            cursor.execute("""
            SELECT * FROM medication
            WHERE medication_id = ?
            """,(medication_id,))

        except sqlite3.Error as e:
            print("Unable to retrieve the " \
            "medication. Please try again.", e)
            return

        medication_row = cursor.fetchone()

        if not medication_row:
            print("No medication was " \
                    "found with that ID.")
            return 
        
        self.medication_name = medication_row[1]
        self.cost = medication_row[2]

        print(f"(Medication ID: {medication_row[0]}")
        self.show_medication_details()
            
        update = input("Update " 
                    "this medication? (Y/N): ").lower()
        
        if update == "y":
            while True:
                new_medication_name = input(
                    "Enter new medication name and strength: ").strip()
                
                if not any(character.isalpha()
                        for character in new_medication_name):
                    print("Please enter the medication name.")
                    continue

                if not any(character.isdigit()
                       for character in new_medication_name):
                    print("Please enter a medication strength.")
                    continue

                if not any(character == " "
                       for character in new_medication_name):
                    print("Please enter the medication name " \
                            "and its strength separated by a space.")
                    continue

                if not self.validate_medication_name(new_medication_name):
                    print("Please use letters, " \
                            "numbers and spaces only.")
                    continue 
                break

            while True:
                try:
                    new_cost = float(input(
                            "Enter new medication " \
                            "cost (£): "))
                    
                    if not self.validate_medication_cost(new_cost):
                        print("Medication cost must be " \
                                "greater than £0:00 and have " \
                                "no more than 2 decimal places.")
                        continue 
                    break

                except ValueError:
                    print("Please enter the medication " \
                            "cost as a number.")
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
                print("Unable to update " \
                        "the medication. Please " \
                        "try again.", e)
                return
                
            print("Medication updated successfully.")
        else:   
            print("Medication update cancelled.")
            

        # Confirm and remove an existing medication from the database.
    def delete_medication(self):
        while True:
            try:
                medication_id = int(input("Enter medication ID: "))

                if not self.validate_login_id(medication_id):
                    print("Please enter a valid medication ID.")
                    continue 
                break

            except ValueError:
                print("Please enter the medication ID " \
                        "using numbers only.")
                continue 
        try:
            cursor.execute("""
                SELECT * FROM medication
                WHERE medication_id = ?
            """,(medication_id,))

        except sqlite3.Error as e:
            print("Unable to retrieve the " \
            "medication. Please try again.", e)
            return

        medication_row = cursor.fetchone()

        if not medication_row:
            print("No medication was found " \
                "with that ID.")
            return
        
        self.medication_name = medication_row[1]
        self.cost = medication_row[2]

        print(f"Medication ID:{medication_row[0]}")
        self.show_medication_details()

        delete = input("Delete "
            "this medication? (Y/N): ").lower()

        if delete == "y":

            try:
                cursor.execute("""
                    DELETE FROM medication
                    WHERE medication_id = ?
                """,(medication_id,))

                conn.commit()

            except sqlite3.Error as e:
                print("Unable to delete " \
                    "the medication. Please" \
                    "try again.", e)
                return 
                
            print("Medication deleted successfully.")
            
        else:
            print("Medication deletion cancelled.")
                


        
    