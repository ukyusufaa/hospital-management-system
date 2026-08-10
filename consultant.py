import sqlite3

conn = sqlite3.connect("hospital.db")

cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")
        # Enable foreign key constraints for related database records

class Consultant():
    def __init__(self,first_name = None,surname = None,
                 department_id = None):
        self.first_name = first_name
        self.surname = surname
        self.department_id = department_id
    
    def show_details_consultant(self):
        print("-" * 30)
        print(f"First Name:{self.first_name}")
        print(f"Last Name:{self.surname}")
        print(f"Department ID:{self.department_id}")
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
            self.first_name = input("Enter consultant first name:")
            if self.first_name == "":
                print("First name is required. Do not leave blank.")
                continue 
            if not self.validate_name(self.first_name):
                print("Please use letters and spaces only.")
                continue 
            break 

        while True:
            self.surname = input("Enter consultant last name:")
            if self.surname == "":
                print("Last name is required. Please enter a last name.")
                continue 
            if not self.validate_name(self.surname):
                print("Please use letters and spaces only.")
                continue 
            break 
        
        while True:
            try:
                self.department_id = int(input("Enter department ID:"))
                if not self.validate_login_id(self.department_id):
                    print("Please enter a valid department ID.")
                    continue 
                break 
            except ValueError:
                print("Department ID must contain numbers only")
                continue
        
        specialist = Consultant(
            self.first_name,
            self.surname,
            self.department_id
        )
        
        try:
            # Insert the validated consultant details into the database.
            cursor.execute("""
            INSERT INTO consultant(
                       first_name,
                       surname,
                       department_id)
            VALUES(?,?,?)
            """,(specialist.first_name,specialist.surname,specialist.department_id))

            conn.commit()
        except sqlite3.Error as e:
            print("Unable to save the consultant. " \
            "Please try again.", e)
            return

        print("Consultant created successfully.")
        row = cursor.lastrowid
        print(row)
        self.show_details_consultant()
        return

        # Retrieve and display all consultants stored in the database.
    def display_all_consultants(self):
        try:
        # Retrieve all consultants from the database
            cursor.execute("SELECT * FROM consultant")

        except sqlite3.Error as e:
            print("Unable to retrieve consultants. " \
            "Please try again.", e)
            return
        
        rows = cursor.fetchall()
        if not rows:
            print("No consultants are currently registered.")
            return
        else:
            for row in rows:
                specialist = Consultant(
                    row[1],
                    row[2],
                    row[3]
                )
                print(f"Consultant ID: {row[0]}")
                specialist.show_details_consultant()
            return

        # Find a consultant by their unique consultant ID.
    def search_consultant(self):
        while True:
            try:
                consultant_id = int(input("Enter consultant ID:"))
                if not self.validate_login_id(consultant_id):
                    print("Please enter a valid consultant ID.")
                    continue 
                break 
            except ValueError:
                print("Consultant ID must contain numbers only.")
                continue 
        try:
            cursor.execute("""
            SELECT * FROM consultant
            WHERE consultant_id = ?
            """,(consultant_id,))

        except sqlite3.Error as e:
            print("Unable to search for the consultant. " \
            "Please try again.", e)
            return

        row = cursor.fetchone()
        if not row:
            print("No consultant was found with that ID.")
            return
        else:
            specialist = Consultant(
                row[1],
                row[2],
                row[3]
            )
            print(f"Consultant ID: {row[0]}")
            specialist.show_details_consultant()
            return

        # Find an existing consultant, confirm the change and update their details.
    def update_consultant(self):
        while True:
            try:
                consultant_id = int(input("Enter consultant ID:"))
                if not self.validate_login_id(consultant_id):
                    print("Please enter a valid consultant ID.")
                    continue 
                break 
            except ValueError:
                print("Consultant ID must contain numbers only.")
                continue 
        try:
            cursor.execute("""
            SELECT * FROM consultant
            WHERE consultant_id = ?
            """,(consultant_id,))

        except sqlite3.Error as e:
            print("Unable to retieve the consultant. " \
            "Please try again.", e)
        
        row = cursor.fetchone()
        if not row:
            print("No consultant was found with that ID.")
            return
        else:
            specialist = Consultant(
                row[1],
                row[2],
                row[3]
            )
        print(f"Consultant ID: {row[0]}")
        specialist.show_details_consultant()

        while True:
            update = input("Update this consultant?(Y/N):").lower()
            if not self.validate_yes_no(update):
                print("Please enter Y/y or N/n.")
                continue
            if update == "n":
                print("Consultant update cancelled")
                return
            else:
                while True:
                    updated_first_name = input(
                        "Enter new consultant " 
                        "first name: "
                    )
                    if updated_first_name == "":
                        print("First name is required. " \
                        "Please enter a first name.")
                        continue 
                    if not self.validate_name(updated_first_name):
                        print("Please use letters " \
                        "and spaces only")
                        continue
                    break

                while True:
                    updated_surname = input(
                        "Enter new consultant "
                        "last name: "
                    )
                    if updated_surname == "":
                        print("Last name is required. " \
                        "Please enter a last name.")
                        continue 
                    if not self.validate_name(updated_surname):
                        print("Please use letters " \
                        "spaces only.")
                        continue 
                    break 
                    
                while True:
                    try:
                        updated_department_id = int(
                            input("Enter new "
                            "department ID:")
                        )
                        if not self.validate_login_id(updated_department_id):
                            print("Please enter a valid " \
                            "department ID.")
                            continue
                        break
    
                    except ValueError:
                        print("Department ID must contain numbers only.")
                        continue
            
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
                    print("Unable to update the consultant. " \
                    "Please try again.", e)
                    return
                
                print("Consultant updated successfully")
                return

        # Find a consultant, confirm deletion, and remove the record from the database.
    def delete_consultant(self):
        while True:
            try:
                consultant_id = int(input("Enter consultant ID:"))
                if not self.validate_login_id(consultant_id):
                    print("Please enter a valid consultant ID")
                    continue 
                break 
            except ValueError:
                print("Consultant ID must contain" \
                "numbers only.")
                continue 
        try:
            cursor.execute("""
            SELECT * FROM consultant
            WHERE consultant_id = ?
            """,(consultant_id,))

        except sqlite3.Error as e:
            print("Unable to retieve " \
            "the consultant. " \
            "Please try again", e)
            return
        
        row = cursor.fetchone()
        if not row:
            print("No consultant was found " \
            "with that ID.")
            return
        else:
            specialist = Consultant(
            row[1],
            row[2],
            row[3]
            )
            print(f"Consultant ID: {row[0]}")
            specialist.show_details_consultant()

            while True:
                delete = input(
                    "Delete this "
                    "consultant?(Y/N):"
                ).lower()
                if not self.validate_yes_no(delete):
                    print("Please enter Y/y or N/n.")
                    continue 
                if delete == "n":
                    print("Consultant deletion cancelled")
                    return
                else:
                    try:
                        cursor.execute("""
                        DELETE FROM consultant
                        WHERE consultant_id = ?
                        """,(consultant_id,))

                        conn.commit()

                    except sqlite3.Error as e:
                        print("Unable to delete " \
                        "the consultant. " \
                        "Please try again.", e)
                        return
                    
                    print("Consultant deleted successfully")
                    return
        
    
        
