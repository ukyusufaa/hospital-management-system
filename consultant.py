import sqlite3
from database import conn, cursor
from colors import DISPLAY_INFO,CONSULTANT_MENU,ERROR,RESET

class Consultant():
    def __init__(self,first_name = None,surname = None,
                 department_id = None):
        self.first_name = first_name
        self.surname = surname
        self.department_id = department_id
    
    def show_details_consultant(self):
        print("=" * 30)
        print(f"{DISPLAY_INFO}First Name:{self.first_name}{RESET}")
        print(f"{DISPLAY_INFO}Last Name:{self.surname}{RESET}")
        print(f"{DISPLAY_INFO}Department ID:{self.department_id}{RESET}")
        print("-" * 30)
    
    def validate_login_id(self,number):
        if number < 1:
            return False
        return True
    
    def validate_name(self,name):
        # validate that names contain letters and spaces only.
        for letter in name:
            if not letter.isalpha() and not letter == " ":
                return False
        return True
    
    def validate_yes_no(self,selected):
        if selected != 'y' and selected != 'n':
            return False
        return True

        # Collect and validate consultant details before saving the record.
    def create_consultant(self):
        while True:
            self.first_name = input(f"{CONSULTANT_MENU}Enter consultant first name: {RESET}")

            if self.first_name == "":
                print(f"{ERROR}First name is required. Do not leave blank.{RESET}")
                continue

            if not self.validate_name(self.first_name):
                print(f"{ERROR}Please use letters and spaces only.{RESET}")
                continue 
            break 

        while True:
            self.surname = input(f"{CONSULTANT_MENU}Enter consultant last name: {RESET}")

            if self.surname == "":
                print(f"{ERROR}Last name is required. Please enter a last name.{RESET}")
                continue

            if not self.validate_name(self.surname):
                print(f"{ERROR}Please use letters and spaces only.{RESET}")
                continue 
            break 
        
        while True:
            try:
                self.department_id = int(input(f"{CONSULTANT_MENU}Enter " 
                                               f"department ID: {RESET}"))

                if not self.validate_login_id(self.department_id):
                    print(f"{ERROR}Please enter a valid department ID.{RESET}")
                    continue 
                break

            except ValueError:
                print(f"{ERROR}Department ID must contain numbers only.{RESET}")
                continue
        
        try:
            # Insert the validated consultant details into the database.
            cursor.execute("""
                INSERT INTO consultant(
                    first_name,
                    surname,
                    department_id)
                VALUES(?,?,?)
            """,(self.first_name,self.surname,self.department_id))

            conn.commit()

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to save the consultant. Please try again.{RESET}", e)
            return

        print(f"{DISPLAY_INFO}Consultant created successfully.{RESET}")
        print()

        consultant_id = cursor.lastrowid
        print(f"{DISPLAY_INFO}Consultant ID: {consultant_id}{RESET}")
        print()

        self.show_details_consultant()


    def display_all_consultants(self):
        # Retrieve all consultants from the database.
        try:
            cursor.execute("SELECT * FROM consultant")

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to retrieve consultants. Please try again.{RESET}", e)
            return
        
        consultant_rows = cursor.fetchall()

        if not consultant_rows:
            print(f"{ERROR}No consultants are currently registered.{RESET}")
            return
        
        for consultant_row in consultant_rows:
            specialist = Consultant(
                consultant_row[1],
                consultant_row[2],
                consultant_row[3]
            )

            print(f"{DISPLAY_INFO}Consultant ID: {consultant_row[0]}{RESET}")
            print()

            specialist.show_details_consultant()

        
    def search_consultant(self):
        # Find a consultant by their unique consultant ID.
        while True:
            try:
                consultant_id = int(input(f"{CONSULTANT_MENU}Enter consultant ID: {RESET}"))
                if not self.validate_login_id(consultant_id):
                    print(f"{ERROR}Please enter a valid consultant ID.{RESET}")
                    continue 
                break 
            except ValueError:
                print(f"{ERROR}Consultant ID must contain numbers only.{RESET}")
                continue 
        try:
            cursor.execute("""
                SELECT * FROM consultant
                WHERE consultant_id = ?
            """,(consultant_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to search for the consultant. Please try again.{RESET}", e)
            return

        consultant_row = cursor.fetchone()
        if not consultant_row:
            print(f"{ERROR}No consultant was found with that ID.{RESET}")
            return
        
        self.first_name = consultant_row[1]
        self.surname = consultant_row[2]
        self.department_id = consultant_row[3]

        print(f"{DISPLAY_INFO}Consultant ID: {consultant_row[0]}{RESET}")
        print()

        self.show_details_consultant()
        return


        # Find an existing consultant, confirm the change and update their details.
    def update_consultant(self):
        while True:
            try:
                consultant_id = int(input(f"{CONSULTANT_MENU}Enter consultant ID: {RESET}"))

                if not self.validate_login_id(consultant_id):
                    print(f"{ERROR}Please enter a valid consultant ID.{RESET}")
                    continue 
                break 
            except ValueError:
                print(f"{ERROR}Consultant ID must contain numbers only.{RESET}")
                continue 
        try:
            cursor.execute("""
                SELECT * FROM consultant
                WHERE consultant_id = ?
            """,(consultant_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to retrieve the consultant. Please try again.{RESET}", e)
            return
        
        consultant_row = cursor.fetchone()

        if not consultant_row:
            print(f"{ERROR}No consultant was found with that ID.{RESET}")
            return
        
        self.first_name = consultant_row[1]
        self.surname = consultant_row[2]
        self.department_id = consultant_row[3]

        print(f"{ERROR}Consultant ID: {consultant_row[0]}{RESET}")
        print()

        self.show_details_consultant()

        while True:
            update = input(f"{CONSULTANT_MENU}Update "
                           f"this consultant?(Y/N): {RESET}").lower()
            
            if not self.validate_yes_no(update):
                print(f"{ERROR}Please enter Y/y or N/n.{RESET}")
                continue

            if update == "n":
                print(f"{DISPLAY_INFO}Consultant update cancelled.{RESET}")
                print()
                return
            break 
            
        while True:
            updated_first_name = input(f"{CONSULTANT_MENU}Enter new consultant " 
                                       f"first name: {RESET}")

            if updated_first_name == "":
                print(f"{CONSULTANT_MENU}First name is required. "
                      f"Please enter a first name.{RESET}")
                continue

            if not self.validate_name(updated_first_name):
                print(f"{CONSULTANT_MENU}Please use letters and spaces only.{RESET}")
                continue
            break

        while True:
                updated_surname = input(f"{CONSULTANT_MENU}Enter new consultant "
                                        f"last name: {RESET}")

                if updated_surname == "":
                    print(f"{ERROR}Last name is required. Please enter a last name.{RESET}")
                    continue

                if not self.validate_name(updated_surname):
                    print(f"{ERROR}Please use letters spaces only.{RESET}")
                    continue 
                break 
                    
        while True:
            try:
                updated_department_id = int(input(f"{CONSULTANT_MENU}Enter new "
                                                  f"department ID: {RESET}"))

                if not self.validate_login_id(updated_department_id):
                    print(f"{ERROR}Please enter a valid department ID.{RESET}")
                    continue
                break
    
            except ValueError:
                print(f"{ERROR}Department ID must contain numbers only.{RESET}")
                    
        self.first_name = updated_first_name
        self.surname = updated_surname
        self.department_id = updated_department_id

        try:
            cursor.execute("""
                UPDATE consultant
                SET first_name = ?,
                    surname = ?,
                    department_id = ?
                WHERE consultant_id = ?
            """,(self.first_name,self.surname,self.department_id, consultant_id))

            conn.commit()

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to update the consultant. " 
                    f"Please try again.{RESET}", e)
            return
        
        print()       
        print("Consultant updated successfully.")
            

        # Find a consultant, confirm deletion, and remove the record from the database.
    def delete_consultant(self):
        while True:
            try:
                consultant_id = int(input(f"{CONSULTANT_MENU}Enter consultant ID: {RESET}"))

                if not self.validate_login_id(consultant_id):
                    print(f"{ERROR}Please enter a valid consultant ID.{RESET}")
                    continue 
                break

            except ValueError:
                print(f"{ERROR}Consultant ID must contain " 
                        f"numbers only.{RESET}")
                continue 
        try:
            cursor.execute("""
                SELECT * FROM consultant
                WHERE consultant_id = ?
            """,(consultant_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to retieve the consultant. Please try again{RESET}", e)
            return
        
        consultant_row = cursor.fetchone()
        if not consultant_row:
            print(f"{ERROR}No consultant was found with that ID.{RESET}")
            return
        
        self.first_name = consultant_row[1]
        self.surname = consultant_row[2]
        self.department_id = consultant_row[3]

        print(f"{DISPLAY_INFO}Consultant ID: {consultant_row[0]}{RESET}")
        print()

        self.show_details_consultant()

        while True:
            delete = input(f"{CONSULTANT_MENU}Delete this consultant? (Y/N): {RESET}").lower()
            
            if not self.validate_yes_no(delete):
                print(f"{ERROR}Please enter Y/y or N/n.{RESET}")
                continue 

            if delete == "n":
                print(f"{DISPLAY_INFO}Consultant deletion cancelled.{RESET}")
                return
            break

        try:
            cursor.execute("""
                DELETE FROM consultant
                WHERE consultant_id = ?
            """,(consultant_id,))

            conn.commit()
            
        except sqlite3.Error as e:
            print(f"{ERROR}Unable to delete the consultant. Please try again.{RESET}", e)
            return
                    
        print(f"{DISPLAY_INFO}Consultant deleted successfully.{RESET}")
        
        
    
        
