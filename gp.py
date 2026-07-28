import sqlite3

conn = sqlite3.connect("hospital.db")
conn.execute("PRAGMA foreign_keys = ON;")
cursor = conn.cursor()

class Gp:

    def __init__(self, first_name, surname, surgery_id):
        self.first_name = first_name
        self.surname = surname
        self.surgery_id = surgery_id

    def show_details_gp(self):
        print("-" * 30)
        print(f"First Name: {self.first_name}")
        print(f"Last Name: {self.surname}")
        print(f"Surgery ID: {self.surgery_id}")
        print("-" * 30)

    def validation_name(self,name):
            for letter in name:
                if not letter.isalpha() and not letter == " ":
                    return False
            return True

    def validate_login_digits(self,number):
            if number < 1:
                return False
            return True
        
    def validate_yes_no(self,choice):
            if choice != 'y' and choice != 'n':
                return False
            return True

    def create_gp(self):
        while True:
            self.first_name = input("GP First Name:")
            if self.first_name == "":
                print("GP First Name - Do not leave blank!")
                continue
            if not self.validation_name(self.first_name):
                print("First Name - Use alphabet and tap space bar if required")
                continue 
            break 

        while True:
            self.surname = input("GP Last Name:")
            if self.surname == "":
                print("GP Last Name - Do not leave blank!")
                continue 
            if not self.validation_name(self.surname):
                print("GP Last Name - Use alphabet and tap space bar if required")
                continue 
            break 

        while True:
            try:
                self.surgery_id = int(input("Surgery ID: "))
                if not self.validate_login_digits(self.surgery_id):
                    print("Surgery ID must be greater than 0")
                    continue
                break 
            except ValueError:
                print("For Surgery ID use only numbers")
                continue

        try:
            cursor.execute("""
            SELECT * FROM gp_surgery
            WHERE surgery_id = ?
            """,(self.surgery_id,))

        except sqlite3.Error as e:
            print("Database Error", e)
            return

        row = cursor.fetchone()
        if not row:
            print("No GP surgery found")
            return
        else:
            try:
                cursor.execute("""
                INSERT INTO gp 
                        (first_name, 
                        surname, 
                        surgery_id)
                VALUES (?,?,?)
                """, (self.first_name, self.surname, self.surgery_id))

                conn.commit()

            except sqlite3.Error as e:
                print("Database Error", e)
                return
            
        print("GP inserted successfully")
        row = cursor.lastrowid
        print(f"GP ID:{row}")
        self.show_details_gp()
        return

    def display_all_gps(self):
        try:
            cursor.execute("SELECT * FROM patient")

        except sqlite3.Error as e:
                print("Database Error", e)
                return
        
        rows = cursor.fetchall()
        if not rows:
            print("No patients found")
            return
        else:
            for row in rows:
                dr = Gp(
                    row[1],
                    row[2],
                    row[3]
                )
            print(row[0])
            dr.show_patient_details()
            return
            
    def search(self):
        while True:
            try:
                gp_id = int(input("GP ID:"))
                if not self.validate_login_digits(gp_id):
                    print("GP ID must be greater than 0")
                    continue
                break 
            except ValueError:
                    print("For GP ID use only numbers")
                    continue
        try:     
            cursor.execute("""
            SELECT * FROM gp
            WHERE gp_id = ?
            """,(gp_id,))

        except sqlite3.Error as e:
            print("Database Error", e)
            return
        
        row = cursor.fetchone()
        if not row:
            print("Patient not found")
            return
        else:
            dr = Gp(
                row[1],
                row[2],
                row[3]
                )
        print(row[0])
        dr.show_patient_details()
        return

    def update_gp(self):
        while True:
            try:
                gp_id = int(input("GP ID:"))
                if not self.validate_login_digits(gp_id):
                    print("GP ID must be greater than 0")
                    continue
                break 
            except ValueError:
                print("For GP ID use only numbers")
                continue
        try:              
            cursor.execute("""
            SELECT * FROM gp
            WHERE gp_id = ?
            """,(gp_id,))

        except sqlite3.Error as e:
            print("Database Error", e)
                
        row = cursor.fetchone()
        if not row:
            print("GP not found")
            return
        else:
            dr = Gp(
                row[1],
                row[2],
                row[3]
                )
        print(row[0])
        dr.show_details_gp()

        while True:
            update = input("Do you want to update this GP's details?(y/n)").lower()
            if not self.validate_yes_no(update):
                print("Invalid input")
                continue
            if update == "n":
                print("Update aborted")
                return
            else:
                while True:
                    updated_first_name = input("GP First Name:")
                    if updated_first_name == "":
                        print("GP First Name - Do not leave name blank!")
                        continue
                    if not self.validation_name(updated_first_name):
                        print("First Name - Use alphabet and tap space bar if required")
                        continue 
                    break 
                
                while True:
                    updated_surname = input("Last Name:")
                    if updated_surname == "":
                        print("Last Name - Do not leave blank!")
                        continue 
                    if not self.validation_name(updated_surname):
                        print("Last Name - Use alphabet and tap space bar if required")
                        continue 
                    break

                while True:
                    try:
                        updated_surgery_id = int(input("Surgery ID:"))
                        if not self.validate_login_id(updated_surgery_id):
                            continue
                        break
                    
                    except ValueError:
                        print("For Surgery ID use only numbers")
                        continue
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
                      gp_id))#

                conn.commit()

            except sqlite3.Error as e:
                print("Database Error", e)
                return
    
            print("GP updated successfully")
            return

    def delete_gp(self):
        while True:
            try:
                gp_id = int(input("GP ID:"))
                if not self.validate_login_digits(gp_id):
                    print("GP ID must be greater than 0")
                    continue
                break 
            except ValueError:
                    print("For GP ID use only numbers")
                    continue
        try:    
            cursor.execute("""
            SELECT * FROM gp
            WHERE gp_id = ?
            """,(gp_id,))

        except sqlite3.Error as e:
            print("Database Error", e)
        
        row = cursor.fetchone()
        if not row:
            print("GP not found")
        else:
            dr = Gp(
                row[1],
                row[2],
                row[3]
            )
        print(row[0])
        dr.show_details_gp()

        while True:
                delete = input("Are you sure you want to delete?").lower()
                if not self.validate_yes_no(delete):
                    continue 
                if delete == "n":
                    print("GP not deleted - aborted")
                    return
                else:
                    try:
                        cursor.execute("""
                        DELETE FROM gp
                        WHERE gp_id = ?
                        """,(gp_id,))

                        conn.commit()

                    except sqlite3.Error as e:
                        print("Database Error", e)
                        return
                    
                    print("GP sucesssfully deleted")
                    return










