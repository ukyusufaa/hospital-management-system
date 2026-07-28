import sqlite3

conn = sqlite3.connect("hospital.db")

cursor = conn.cursor()

class Department():
    def __init__(self, department_name):
        self.department_name = department_name
    
    def show_department_details(self):
        print(f"Department Name:{self.department_name}")
    
    def validate_department_name(self,name):
        for letter in name:
            if not letter.isalpha() and letter != " ":
                return False
        return True
    
    def validate_id_input(self,number):
            if number < 1:
                return False
            return True          

    def create_department(self):
        while True:
            self.department_name = input("Department Name:")
            if self.department_name == "":
                print("Department Name - Do not leave blank!")
                continue 
            if not self.validate_department_name(self.department_name):
                print("For department name use alphabet and tap space bar if required")
                continue 
            break 

        dept = Department(
            self.department_name
        )

        try:
            cursor.execute("""
            INSERT INTO department(
                       department_name)
            VALUES(?)             
            """,(dept.department_name,))

            conn.commit()

        except sqlite3.Error as e:
            print("Database Error", e)
            return
        
        print("Department inserted at Medina Hospital successfully")
        row = cursor.lastrowid
        print(row)
        self.show_department_details()
        return
    
    def display_all_departments(self):
        try:
            cursor.execute("SELECT * FROM department")

        except sqlite3.Error as e:
            print("Database Error", e)
            return

        rows = cursor.fetchall()

        if not rows:
            print("No Departments found")
            return
        else:
            for row in rows: 
                new_dept = Department(
                row[1]
                )
                print(row[0])
                new_dept.show_department_details()
        return
    
    def search_department(self):
        while True:
            try:
                department_id = int(input("Department ID:"))
                if not self.validate_id_input(department_id):
                    print("Department ID - must be greater than 0")
                    continue 
                break
            except ValueError:
                print("For Department ID use only numbers")
                return

        try:
            cursor.execute("""
            SELECT * FROM department
            WHERE department_id = ?
            """,(department_id,))

        except sqlite3.Error as e:
            print("Database Error", e)
            return

        row = cursor.fetchone()
        if not row:
            print ("No department found")
            return
        else:
            dept = Department(
                row[1]
            )
            print(row[0])
            dept.show_department_details()
            return
    
    def update_department(self):
        while True:
            try:
                department_id = int(input("Department ID:"))
                if not self.validate_id_input(department_id):
                    print("Department ID - must be greater than 0")
                    continue 
                break 
            except ValueError:
                print("For Department ID use only numbers")
                continue 

        try:
            cursor.execute("""
            SELECT * FROM department
            WHERE department_id = ?
            """,(department_id,))

        except sqlite3.Error as e:
            print("Database Error", e)
            return

        row = cursor.fetchone()
        if not row:
            print("No such department")
            return
        else:
            dept = Department(
                row[0]
            )
            print(row[0])
            dept.show_department_details()

            update = input("Are you sure you want to update?")
            if update == "y":
                while True:
                    new_dept_name = input("Department Name:")
                    if new_dept_name == "":
                        print("Department Name - Do not leave blank!")
                        continue 
                    if not self.validate_department_name(new_dept_name):
                        continue 
                    break 

                dept.department_name = new_dept_name

                try:
                    cursor.execute("""
                    UPDATE department
                    SET department_name = ?
                    WHERE department_id = ?
                    """,(dept.department_name,department_id))

                    conn.commit()

                except sqlite3.Error as e:
                    print("Database Error", e)
                    return

                print("Department updated successfully")
                return
            else:
                print("Update process aborted")
                return

    def delete_department(self):
            while True:
                try:
                    department_id = int(input("Department ID:"))
                    if not self.validate_id_input(department_id):
                        print("Department ID - must be greater than 0")
                        continue 
                    break 
                except ValueError:
                    print("For Department ID use only numbers")
                    continue

            try:
                cursor.execute("""
                SELECT * FROM department
                WHERE department_id = ?
                """,(department_id,))

            except sqlite3.Error as e:
                print("Database Error", e)
                return
    
            row = cursor.fetchone()
            if not row:
                print("No such department found")
                return
            else:
                dept = Department(
                    row[1]
                )
                print(row[0])
                dept.show_department_details()
    
                delete = input("Are you sure you want to delete?")
                if delete == "y":

                    try:
                        cursor.execute("""
                        DELETE FROM department
                        WHERE department_id = ?
                        """,(department_id,))
    
                        conn.commit()

                    except sqlite3.Error as e:
                        print("Database Error", e)
                        return
    
                    print("Department deleted successfully")
                    return
                else:
                    print("Delete process aborted")
                    return
        
                        
test = Department(
    "department"
    )

test.create_department()

            
