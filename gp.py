import sqlite3
from database import conn, cursor

class Gp:

    def __init__(self, first_name = None, surname = None, 
                 surgery_id = None):
        self.first_name = first_name
        self.surname = surname
        self.surgery_id = surgery_id

    def show_details_gp(self):
        print("-" * 30)
        print(f"GP First Name: {self.first_name}")
        print(f"GP Last Name: {self.surname}")
        print(f"Medical Practice ID: {self.surgery_id}")
        print("-" * 30)

        # Validate names using letters and spaces only.
    def validation_name(self,name):
            for letter in name:
                if not letter.isalpha() and not letter == " ":
                    return False
            return True

        # Validate IDs to ensure they are positive integers.
    def validate_login_digits(self,number):
            if number < 1:
                return False
            return True

        # Validate Y/N responses. 
    def validate_yes_no(self,choice):
            if choice != 'y' and choice != 'n':
                return False
            return True

        # Collect and validate GP details before saving the record.
    def create_gp(self):
        while True:
            self.first_name = input("Enter GP first name:")

            if self.first_name == "":
                print("First Name is required. " \
                        "Please enter a first name.")
                continue

            if not self.validation_name(self.first_name):
                print("Please use letters and " \
                        "spaces only.")
                continue 
            break 

        while True:
            self.surname = input("Enter GP last name:")

            if self.surname == "":
                print("Last name is required. " \
                        "Please enter a last name.")
                continue

            if not self.validation_name(self.surname):
                print("Please use letters and " \
                        "spaces only.")
                continue 
            break 

        while True:
            try:
                self.surgery_id = int(input("Enter surgery ID: "))

                if not self.validate_login_digits(self.surgery_id):
                    print("Please enter a valid surgery ID.")
                    continue
                break

            except ValueError:
                print("Please enter the surgery ID " \
                        "using numbers only.")
                continue

        try:
            # Confirm that the selected medical practice exists before creating the GP.
            cursor.execute("""
                SELECT * FROM gp_surgery
                WHERE surgery_id = ?
            """,(self.surgery_id,))

        except sqlite3.Error as e:
            print("Unable to retrieve the " \
                    "medical practice. " \
                    "Please try again.", e)
            return

        surgery_record = cursor.fetchone()

        if not surgery_record:
            print("No medical practice was found " \
                    "with that ID.")
            return
        
        try:
        # Insert the validated GP details into the database.
            cursor.execute("""
                INSERT INTO gp 
                    (first_name, 
                    surname, 
                    surgery_id)
                VALUES (?,?,?)
            """, (self.first_name, self.surname, self.surgery_id))

            conn.commit()

        except sqlite3.Error as e:
            print("Unable to save the GP. " \
                    "Please try again.", e)
            return
            
        print("GP created successfully")

        gp_id = cursor.lastrowid
        print(f"GP ID:{gp_id}")
        self.show_details_gp()
        return

        # Retrieve and display all GPs stored in the database.
    def display_all_gps(self):
        try:
            cursor.execute("SELECT * FROM gp")

        except sqlite3.Error as e:
            print("Unable to retrieve GPs. " \
                    "Please try again.", e)
            return
        
        gp_records = cursor.fetchall()

        if not gp_records:
            print("No GPs are currently " \
                    "registered.")
            return
        
        for gp_record in gp_records:
            gp = Gp(
                gp_record[1],
                gp_record[2],
                gp_record[3]
            )

            print(f"GP ID: {gp_record[0]}")
            gp.show_details_gp()


        # Find a GP using their unique GP ID. 
    def search_gp(self):
        while True:
            try:
                gp_id = int(input("Enter GP ID:"))

                if not self.validate_login_digits(gp_id):
                    print("Please enter a valid GP ID.")
                    continue
                break

            except ValueError:
                    print("Please enter the GP ID " 
                            "using numbers only.")
                    continue
        try:     
            cursor.execute("""
            SELECT * FROM gp
            WHERE gp_id = ?
            """,(gp_id,))

        except sqlite3.Error as e:
            print("Unable to search for " \
                    "the GP. Please try again.", e)
            return
        
        gp_record = cursor.fetchone()

        if not gp_record:
            print("No GP was found " \
                    "with that ID.")
            return
        
        self.first_name = gp_record[1]
        self.surname = gp_record[2]
        self.surgery_id = gp_record[3]

        print(f"GP ID: {gp_record[0]}")
        self.show_details_gp()
    

        # Update the details of an existing GP.
    def update_gp(self):
        while True:
            try:
                gp_id = int(input("Enter GP ID:"))

                if not self.validate_login_digits(gp_id):
                    print("Please enter a valid GP ID.")
                    continue
                break

            except ValueError:
                print("Please enter the GP ID using " \
                        "only numbers.")
                continue
        try:              
            cursor.execute("""
            SELECT * FROM gp
            WHERE gp_id = ?
            """,(gp_id,))

        except sqlite3.Error as e:
            print("Unable to retrieve the GP. " \
                    "Please try again.", e)
                
        gp_record = cursor.fetchone()

        if not gp_record:
            print("No GP was found " \
                    "with that ID.")
            return
        
        self.first_name = gp_record[1]
        self.surname = gp_record[2]
        self.surgery_id = gp_record[3]

        print(f"GP ID: {gp_record[0]}")
        self.show_details_gp()

        while True:
            update = input("Update " 
                "this GPs details? (Y/N): ").lower()
            
            if not self.validate_yes_no(update):
                print("Please enter Y/y " \
                        "or N/n.")
                continue

            if update == "n":
                print("GP update cancelled.")
                return
            break 
        
        while True:
            updated_first_name = input(
                "Enter new GP first name: ")
            
            if updated_first_name == "":
                print("First name is required. " \
                        "Please enter a first name.")
                continue

            if not self.validation_name(updated_first_name):
                print("Please use letters " \
                        "and spaces only.")
                continue 
            break 
                
        while True:
            updated_surname = input(
                "Enter new GP last name: ")
            
            if updated_surname == "":
                print("Last name is required. " \
                    "Please enter a last name.")
                continue

            if not self.validation_name(updated_surname):
                print("Please use letters and " \
                    "spaces only.")
                continue 
            break

        while True:
            try:
                updated_surgery_id = int(
                    input("Enter medical " \
                            "practice ID: "))
                
                if not self.validate_login_digits(updated_surgery_id):
                    print("Please enter a valid "
                            "surgery ID.")
                    continue
                break
                    
            except ValueError:
                print("Please enter the surgery ID " \
                        "using numbers only.")
                continue

        self.first_name = updated_first_name
        self.surname = updated_surname
        self.surgery_id = updated_surgery_id

        try:
            cursor.execute("""
                UPDATE gp
                SET first_name = ?,
                    surname = ?,
                    surgery_id = ?
                WHERE gp_id = ?
            """, (self.first_name,
                    self.surname,
                    self.surgery_id,
                    gp_id))

            conn.commit()

        except sqlite3.Error as e:
            print("Unable to update the GP." \
                    "Please try again.", e)
            return
    
        print("GP updated successfully.")
        

        # Confirm and remove an existing GP from the database.
    def delete_gp(self):
        while True:
            try:
                gp_id = int(input("Enter GP ID:"))

                if not self.validate_login_digits(gp_id):
                    print("Please Enter a valid GP ID.")
                    continue
                break

            except ValueError:
                    print("Please enter the GP ID " \
                            "using numbers only.")
                    continue
        try:    
            cursor.execute("""
            SELECT * FROM gp
            WHERE gp_id = ?
            """,(gp_id,))

        except sqlite3.Error as e:
            print("Unable to retrieve the GP. " \
                    "Please try again.", e)
            return
        
        gp_record = cursor.fetchone()

        if not gp_record:
            print("No GP was found " \
                    "with that ID.")
            return
        
        self.first_name = gp_record[1]
        self.surname = gp_record[2]
        self.surgery_id = gp_record[3]

        print(f"GP ID: {gp_record[0]}")
        self.show_details_gp()

        while True:
            delete = input("Delete " 
                        "this GP? (Y/N): ").lower()
            
            if not self.validate_yes_no(delete):
                print("Please enter Y/y " \
                        "or N/n.")
                continue

            if delete == "n":
                print("GP deletion cancelled.")
                return
            break 
                
        try:
            cursor.execute("""
                DELETE FROM gp
                WHERE gp_id = ?
            """,(gp_id,))

            conn.commit()

        except sqlite3.Error as e:
            print("Unable to delete the GP. " \
                    "Please try again.", e)
                    
        print("GP sucesssfully deleted.")
                    
                










