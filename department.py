import sqlite3
from database import conn, cursor

class Department():
    def __init__(self, department_name = None):
        self.department_name = department_name
    
    def show_department_details(self):
        print("-" * 30)
        print(f"Department Name:{self.department_name}")
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
            self.department_name = input("Enter department name: ")

            if self.department_name == "":
                print("Department Name is required. " \
                        "Please enter a department name.")
                continue 

            if not self.validate_department_name(self.department_name):
                print("Please use letters and " \
                        "spaces only.")
                continue 
            break 

        try:
            # Insert the validated department into the database.
            cursor.execute("""
                INSERT INTO department(
                       department_name)
                VALUES(?)             
            """,(self.department_name,))

            conn.commit()

        except sqlite3.Error as e:
            print("Unable to save the department. " \
                    "Please try again.", e)
            return
        
        print("Department created successfully")

        department_id = cursor.lastrowid
        print(f"Department ID: {department_id}")

        self.show_department_details()
        

        # Retrieve and display all departments stored in the database.
    def display_all_departments(self):
        try:
            cursor.execute("SELECT * FROM department")

        except sqlite3.Error as e:
            print("Unable to retrieve departments." \
                    "Please try again.", e)
            return

        departments = cursor.fetchall()

        if not departments:
            print("No departments are " \
                    "currently registered")
            return
        
        for department in departments:
            new_dept = Department(department[1])

            print(f"Department ID:{department[0]}")
            new_dept.show_department_details()


        # Find a department using its unique department ID.
    def search_department(self):
        while True:
            try:
                department_id = int(input("Enter department ID:"))
                if not self.validate_id_input(department_id):
                    print("Please enter a valid " \
                            "department ID.")
                    continue 
                break

            except ValueError:
                print("For Department ID " \
                        "must contain numbers only.")
                return

        try:
            cursor.execute("""
                SELECT * FROM department
                WHERE department_id = ?
            """,(department_id,))

        except sqlite3.Error as e:
            print("Unable to search " \
            "for the department. " \
            "Please try again.", e)
            return

        department = cursor.fetchone()

        if not department:
            print ("No department was found " \
                    "with that ID.")
            return
        
        self.department_name = department[1]
            
        print(f"Department ID:{department[0]}")
        self.show_department_details()
    

        # Update the details of an existing department.
    def update_department(self):
        while True:
            try:
                department_id = int(input("Enter department ID:"))
                if not self.validate_id_input(department_id):
                    print("Please enter a valid " \
                    "department ID.")
                    continue 
                break

            except ValueError:
                print("Department ID must " \
                "contain numbers only.")
                continue 

        try:
            cursor.execute("""
                SELECT * FROM department
                WHERE department_id = ?
            """,(department_id,))

        except sqlite3.Error as e:
            print("Unable to retrieve the " \
            "department. Please try again.", e)
            return

        department = cursor.fetchone()

        if not department:
            print("No department was found " \
            "with that ID.")
            return
        
        self.department_name = department[1]
            
        print(f"Department ID:{department[0]}")

        self.show_department_details()

        update = input("Update " 
                "this department? (Y/N): ").lower()
        
        if update == "y":
            while True:
                new_dept_name = input(
                    "Enter new department name: ")
                
                if new_dept_name == "":
                    print("Department name is required. " \
                    "Please enter a department name.")
                    continue

                if not self.validate_department_name(new_dept_name):
                    print("Please use letters " \
                    "and spaces only.")
                    continue 
                break 

            self.department_name = new_dept_name

            try:
                cursor.execute("""
                    UPDATE department
                    SET department_name = ?
                    WHERE department_id = ?
                """,(self.department_name,department_id))

                conn.commit()

            except sqlite3.Error as e:
                print("Unable to update the " \
                "department. Please try again.", e)
                return

            print("Department updated successfully.")
            return
        
        print("Department update cancelled.")
        

        # Confirm and remove an existing department from the database.
    def delete_department(self):
        while True:
            try:
                department_id = int(input("Enter department ID: "))

                if not self.validate_id_input(department_id):
                    print("Please enter a valid " \
                    "department ID.")
                    continue 
                break 

            except ValueError:
                print("Department ID use only numbers.")
                continue

        try:
            cursor.execute("""
                SELECT * FROM department
                WHERE department_id = ?
            """,(department_id,))

        except sqlite3.Error as e:
            print("Unable to retrieve the " \
            "department. Please try again.", e)
            return
    
        department = cursor.fetchone()

        if not department:
            print("No department was found " \
            "with that ID.")
            return
            
        self.department_name = department[1]
                
        print(f"Department ID:{department[0]}")
        self.show_department_details()
    
        delete = input("Delete " 
            "this department? (Y/N): ").lower()
        
        if delete == "y":
            try:
                cursor.execute("""
                    DELETE FROM department
                    WHERE department_id = ?
                """,(department_id,))

                conn.commit()

            except sqlite3.Error as e:
                print("Unable to delete the " \
                "department. Please try again.", e)
                return
    
            print("Department deleted successfully.")
            return
            
        print("Department deletion cancelled.")
        return
                    


            
