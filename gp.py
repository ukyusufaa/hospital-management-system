import sqlite3
from database import conn, cursor
from colors import DISPLAY_INFO,GP_MENU,ERROR,RESET

class Gp:

    def __init__(self, first_name = None, surname = None, 
                 surgery_id = None):
        self.first_name = first_name
        self.surname = surname
        self.surgery_id = surgery_id

    def show_details_gp(self):
        print("=" * 30)
        print(f"{DISPLAY_INFO}GP First Name: {self.first_name}{RESET}")
        print(f"{DISPLAY_INFO}GP Last Name: {self.surname}{RESET}")
        print(f"{DISPLAY_INFO}Medical Practice ID: {self.surgery_id}{RESET}")
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
            self.first_name = input(f"{GP_MENU}Enter GP first name: {RESET}")

            if self.first_name == "":
                print(f"{ERROR}First Name is required. Please enter a first name.{RESET}")
                continue

            if not self.validation_name(self.first_name):
                print(f"{ERROR}Please use letters and spaces only.{RESET}")
                continue 
            break 

        while True:
            self.surname = input(f"{GP_MENU}Enter GP last name: {RESET}")

            if self.surname == "":
                print(f"{ERROR}Last name is required. Please enter a last name.{RESET}")
                continue

            if not self.validation_name(self.surname):
                print(f"{ERROR}Please use letters and spaces only.{RESET}")
                continue 
            break 

        while True:
            try:
                self.surgery_id = int(input(f"{GP_MENU}Enter surgery ID: {RESET}"))

                if not self.validate_login_digits(self.surgery_id):
                    print(f"{ERROR}Please enter a valid surgery ID.{RESET}")
                    continue
                break

            except ValueError:
                print(f"{ERROR}Please enter the surgery ID using numbers only.{RESET}")
                continue

        try:
            # Confirm that the selected medical practice exists before creating the GP.
            cursor.execute("""
                SELECT * FROM gp_surgery
                WHERE surgery_id = ?
            """,(self.surgery_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to retrieve the medical practice. " 
                  f"Please try again.{RESET}", e)
            return

        surgery_record = cursor.fetchone()

        if not surgery_record:
            print(f"{ERROR}No medical practice was found with that ID.{RESET}")
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
            print(f"{ERROR}Unable to save the GP. Please try again.{RESET}", e)
            return
            
        print(f"{DISPLAY_INFO}GP created successfully.{RESET}")

        gp_id = cursor.lastrowid
        print(f"{DISPLAY_INFO}GP ID:{gp_id}{RESET}")
        self.show_details_gp()
        return

        # Retrieve and display all GPs stored in the database.
    def display_all_gps(self):
        try:
            cursor.execute("SELECT * FROM gp")

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to retrieve GPs. Please try again.{RESET}", e)
            return
        
        gp_records = cursor.fetchall()

        if not gp_records:
            print(f"{ERROR}No GPs are currently registered.{RESET}")
            return
        
        for gp_record in gp_records:
            gp = Gp(
                gp_record[1],
                gp_record[2],
                gp_record[3]
            )

            print(f"{DISPLAY_INFO}GP ID: {gp_record[0]}{RESET}")
            gp.show_details_gp()
            print()


        # Find a GP using their unique GP ID. 
    def search_gp(self):
        while True:
            try:
                gp_id = int(input(f"{GP_MENU}Enter GP ID:{RESET}"))

                if not self.validate_login_digits(gp_id):
                    print(f"{ERROR}Please enter a valid GP ID.{RESET}")
                    continue
                break

            except ValueError:
                    print(f"{ERROR}Please enter the GP ID using numbers only.{RESET}")
                    continue
        try:     
            cursor.execute("""
            SELECT * FROM gp
            WHERE gp_id = ?
            """,(gp_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to search for the GP. Please try again.{RESET}", e)
            return
        
        gp_record = cursor.fetchone()

        if not gp_record:
            print(f"{ERROR}No GP was found with that ID.{RESET}")
            return
        
        self.first_name = gp_record[1]
        self.surname = gp_record[2]
        self.surgery_id = gp_record[3]

        print(f"{DISPLAY_INFO}GP ID: {gp_record[0]}{RESET}")
        self.show_details_gp()
    

        # Update the details of an existing GP.
    def update_gp(self):
        while True:
            try:
                gp_id = int(input(f"{GP_MENU}Enter GP ID: {RESET}"))

                if not self.validate_login_digits(gp_id):
                    print(f"{ERROR}Please enter a valid GP ID.{RESET}")
                    continue
                break

            except ValueError:
                print(f"{ERROR}Please enter the GP ID using only numbers.{RESET}")
                continue
        try:              
            cursor.execute("""
            SELECT * FROM gp
            WHERE gp_id = ?
            """,(gp_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to retrieve the GP. Please try again.{RESET}", e)
                
        gp_record = cursor.fetchone()

        if not gp_record:
            print(f"{ERROR}No GP was found with that ID.{RESET}")
            return
        
        self.first_name = gp_record[1]
        self.surname = gp_record[2]
        self.surgery_id = gp_record[3]

        print(f"{DISPLAY_INFO}GP ID: {gp_record[0]}{RESET}")
        self.show_details_gp()

        while True:
            update = input(f"{GP_MENU}Update this GPs details? (Y/N): {RESET}").lower()
            
            if not self.validate_yes_no(update):
                print(f"{ERROR}Please enter Y/y or N/n.{RESET}")
                continue

            if update == "n":
                print(f"{DISPLAY_INFO}GP update cancelled.{RESET}")
                return
            break 
        
        while True:
            updated_first_name = input(f"{GP_MENU}Enter new GP first name: {RESET}")
            
            if updated_first_name == "":
                print(f"{ERROR}First name is required. Please enter a first name.{RESET}")
                continue

            if not self.validation_name(updated_first_name):
                print(f"{ERROR}Please use letters and spaces only.{RESET}")
                continue 
            break 
                
        while True:
            updated_surname = input(f"{GP_MENU}Enter new GP last name: {RESET}")
            
            if updated_surname == "":
                print(f"{ERROR}Last name is required. Please enter a last name.{RESET}")
                continue

            if not self.validation_name(updated_surname):
                print(f"{ERROR}Please use letters and spaces only.{RESET}")
                continue 
            break

        while True:
            try:
                updated_surgery_id = int(
                    input(f"{GP_MENU}Enter medical practice ID: {RESET}"))
                
                if not self.validate_login_digits(updated_surgery_id):
                    print(f"{ERROR}Please enter a valid surgery ID.{RESET}")
                    continue
                break
                    
            except ValueError:
                print(f"{ERROR}Please enter the surgery ID using numbers only.{RESET}")
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
            print(f"{ERROR}Unable to update the GP. Please try again.{RESET}", e)
            return
    
        print(f"{DISPLAY_INFO}GP updated successfully.{RESET}")
        

        # Confirm and remove an existing GP from the database.
    def delete_gp(self):
        while True:
            try:
                gp_id = int(input(f"{GP_MENU}Enter GP ID: {RESET}"))

                if not self.validate_login_digits(gp_id):
                    print(f"{ERROR}Please Enter a valid GP ID.{RESET}")
                    continue
                break

            except ValueError:
                    print(f"{ERROR}Please enter the GP ID using numbers only.{RESET}")
                    continue
        try:    
            cursor.execute("""
            SELECT * FROM gp
            WHERE gp_id = ?
            """,(gp_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to retrieve the GP. Please try again.{RESET}", e)
            return
        
        gp_record = cursor.fetchone()

        if not gp_record:
            print(f"{ERROR}No GP was found with that ID.{RESET}")
            return
        
        self.first_name = gp_record[1]
        self.surname = gp_record[2]
        self.surgery_id = gp_record[3]

        print(f"{DISPLAY_INFO}GP ID: {gp_record[0]}{RESET}")
        self.show_details_gp()

        while True:
            delete = input(f"{GP_MENU}Delete this GP? (Y/N): {RESET}").lower()
            
            if not self.validate_yes_no(delete):
                print(f"{ERROR}Please enter Y/y or N/n.{RESET}")
                continue

            if delete == "n":
                print(f"{DISPLAY_INFO}GP deletion cancelled.{RESET}")
                return
            break 
                
        try:
            cursor.execute("""
                DELETE FROM gp
                WHERE gp_id = ?
            """,(gp_id,))

            conn.commit()

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to delete the GP. Please try again.{RESET}", e)
                    
        print(f"{DISPLAY_INFO}GP sucesssfully deleted.{RESET}")
                    
                










