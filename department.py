import sqlite3
from colors import DISPLAY_INFO,DEPARTMENT_MENU,ERROR,RESET

class Department():
    def __init__(self,database,department_name = None):
        self.database = database
        self.department_name = department_name
    
    def show_department_details(self):
        print("=" * 30)
        print(f"{DISPLAY_INFO}Department Name:{self.department_name}{RESET}")
        print("-" * 30)

        # Validate department names using letters and spaces only.
    def validate_department_name(self,name):
        for letter in name:
            if not letter.isalpha() and letter != " ":
                return False
        return True
    
    def validate_id_input(self,number):
        if number < 1:
            return False
        return True          

        # Collect and validate department details before saving the record.
    def create_department(self):
        while True:
            self.department_name = input(f"{DEPARTMENT_MENU}Enter department name: {RESET}")

            if self.department_name == "":
                print(f"{ERROR}Department Name is required. " 
                        f"Please enter a department name.{RESET}")
                continue 

            if not self.validate_department_name(self.department_name):
                print(f"{ERROR}Please use letters and spaces only.{RESET}")
                continue 
            break 

        try:
            # Insert the validated department into the database.
            self.database.cursor.execute("""
                INSERT INTO department(
                       department_name)
                VALUES(?)             
            """,(self.department_name,))

            self.database.connection.commit()

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to save the department. Please try again.{e}{RESET}")
            return
        
        print(f"{DISPLAY_INFO}Department created successfully.{RESET}")
        print()

        department_id = self.database.cursor.lastrowid
        print(f"{DISPLAY_INFO}Department ID: {department_id}{RESET}")
        print()

        self.show_department_details()
        

        # Retrieve and display all departments stored in the database.
    def display_all_departments(self):
        try:
            self.datbase.cursor.execute("SELECT * FROM department")

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to retrieve departments. Please try again.{e}{RESET}")
            return

        departments = self.database.cursor.fetchall()

        if not departments:
            print(f"{ERROR}No departments are currently registered.{RESET}")
            return
        
        for department in departments:
            new_dept = Department(department[1])

            print(f"{DISPLAY_INFO}Department ID:{department[0]}{RESET}")
            new_dept.show_department_details()
            print()


        # Find a department using its unique department ID.
    def search_department(self):
        while True:
            try:
                department_id = int(input(f"{DEPARTMENT_MENU}Enter department ID: {RESET}"))
                if not self.validate_id_input(department_id):
                    print(f"{ERROR}Please enter a valid department ID.{RESET}")
                    continue 
                break

            except ValueError:
                print(f"{ERROR}Department ID must contain numbers only.{RESET}")
                return

        try:
            self.database.cursor.execute("""
                SELECT * FROM department
                WHERE department_id = ?
            """,(department_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to search for the department. Please try again.{e}{RESET}")
            return

        department = self.database.cursor.fetchone()

        if not department:
            print (f"{ERROR}No department was found with that ID.{RESET}")
            return
        
        self.department_name = department[1]
            
        print(f"{DISPLAY_INFO}Department ID:{department[0]}{RESET}")
        print()
        self.show_department_details()
    

        # Update the details of an existing department.
    def update_department(self):
        while True:
            try:
                department_id = int(input(f"{DEPARTMENT_MENU}Enter department ID: {RESET}"))
                if not self.validate_id_input(department_id):
                    print(f"{ERROR}Please enter a valid department ID.{RESET}")
                    continue 
                break

            except ValueError:
                print(f"{ERROR}Department ID must contain numbers only.{RESET}")
                continue 

        try:
            self.database.cursor.execute("""
                SELECT * FROM department
                WHERE department_id = ?
            """,(department_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to retrieve the department. Please try again.{e}{RESET}")
            return

        department = self.database.cursor.fetchone()

        if not department:
            print(f"{ERROR}No department was found with that ID.{RESET}")
            return
        
        self.department_name = department[1]
            
        print(f"{DISPLAY_INFO}Department ID:{department[0]}{RESET}")
        print()
        self.show_department_details()
        print()

        update = input(f"{DEPARTMENT_MENU}Update this department? (Y/N): {RESET}").lower()
        
        if update == "y":
            while True:
                new_dept_name = input(f"{DEPARTMENT_MENU}Enter new department name: {RESET}")
                
                if new_dept_name == "":
                    print(f"{ERROR}Department name is required. "
                          f"Please enter a department name.{RESET}")
                    continue

                if not self.validate_department_name(new_dept_name):
                    print(f"{ERROR}Please use letters and spaces only.{RESET}")
                    continue 
                break 

            self.department_name = new_dept_name

            try:
                self.database.cursor.execute("""
                    UPDATE department
                    SET department_name = ?
                    WHERE department_id = ?
                """,(self.department_name,department_id))

                self.database.connection.commit()

            except sqlite3.Error as e:
                print(f"{ERROR}Unable to update the department. Please try again.{e}{RESET}")
                return

            print(f"{DISPLAY_INFO}Department updated successfully.{RESET}")
            print()
            return
        
        print(f"{DISPLAY_INFO}Department update cancelled.{RESET}")
        

        # Confirm and remove an existing department from the database.
    def delete_department(self):
        while True:
            try:
                department_id = int(input(f"{DEPARTMENT_MENU}Enter department ID: {RESET}"))

                if not self.validate_id_input(department_id):
                    print(f"{ERROR}Please enter a valid department ID.{RESET}")
                    continue 
                break 

            except ValueError:
                print(f"{ERROR}Department ID use only numbers.{RESET}")
                continue

        try:
            self.database.cursor.execute("""
                SELECT * FROM department
                WHERE department_id = ?
            """,(department_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to retrieve the department. Please try again.{e}{RESET}")
            return
    
        department = self.database.cursor.fetchone()

        if not department:
            print(f"{ERROR}No department was found with that ID.{RESET}")
            return
            
        self.department_name = department[1]
                
        print(f"{DISPLAY_INFO}Department ID:{department[0]}{RESET}")
        print()
        self.show_department_details()
        print()
    
        delete = input(f"{DEPARTMENT_MENU}Delete this department? (Y/N): {RESET}").lower()
        
        if delete == "y":
            try:
                self.database.cursor.execute("""
                    DELETE FROM department
                    WHERE department_id = ?
                """,(department_id,))

                self.database.connection.commit()

            except sqlite3.Error as e:
                print(f"{ERROR}Unable to delete the department. Please try again.{e}{RESET}")
                return
    
            print(f"{DISPLAY_INFO}Department deleted successfully.{RESET}")
            print()
            return
            
        print(f"{DISPLAY_INFO}Department deletion cancelled.{RESET}")
        return
                    


            
