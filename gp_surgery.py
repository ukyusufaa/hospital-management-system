import sqlite3

conn = sqlite3.connect("hospital.db")

cursor = conn.cursor()

class GpSurgery:
    def __init__(self,surgery_name,address):
        self.surgery_name = surgery_name
        self.address = address 
    
    def show_gpsurgery_details(self):
        print(f"Surgery Name:{self.surgery_name}")
        print(f"Address:{self.address}")
    
    def validate_surgeryname(self,name):
        for letter in name:
            if not letter.isalpha() and not letter == " ":
                return False
        return True
    
    def validate_id_input(self,number):
        if number < 1:
            return False
        return True
    
    def create_gpsurgery(self):
        while True:
            self.surgery_name = input("Surgery Name:")
            if self.surgery_name == "":
                print("Surgery Name - Do not leave blank!")
                continue
            if not self.validate_surgeryname(self.surgery_name):
                print("For surgery name use alphabet and tap space bar if required")
                continue 
            break

        while True:
            self.address = input("Address:")
            if self.address == "":
                print("Address - Do not leave blank!")
                continue

            if not " " in self.address:
                print("For address tap space bar")
                continue
            
            invalid_char = False
            for character in self.address:
                if character.isalpha() or character.isdigit():
                    continue
                if character in["&", " ", "-", "'", ",", ".", "/"]:
                    continue
                else:
                    invalid_char == True
                    break 
            if invalid_char == True:
                print("Address does not include such a character")
                continue

            digit_in_address = False
            for num in self.address:
                if num.isdigit():
                    digit_in_address = True
                    break 
            if digit_in_address == False:
                print("Address must have a number")
                continue 
            break 

        try:
            cursor.execute("""
            INSERT INTO gp_surgery(
                       surgery_name,
                       address)
            VALUES(?,?)
            """,(self.surgery_name,self.address))

            conn.commit()

        except sqlite3.Error as e:
            print("Database Error", e)
            return

        print("GP Surgery created successfully")
        row = cursor.lastrowid
        print(f"Surgery ID:{row}")
        self.show_gpsurgery_details()
        return

    def display_all_gpsurgery(self):
        try:
            cursor.execute("SELECT * FROM gp_surgery")

        except sqlite3.Erorr as e:
            print("Database Error", e)
            return

        rows = cursor.fetchall()

        if len(rows) == 0:
            print("No GP surgeries found")
            return
        else:
            for row in rows:
                clinic = GpSurgery(
                    row[1],
                    row[2]
                )
                print(row[0])
                clinic.show_gpsurgery_details()
        return
    
    def search_gpsurgery(self):
        while True:
            try:
                surgery_id = int(input("Surgery ID:"))
                if not self.validate_id_input(surgery_id):
                    print("Surgery ID - must be greater than 0")
                    continue 
                break
            except ValueError:
                print("For Surgery ID use only numbers")
                continue
        try:
            cursor.execute("""
            SELECT * FROM gp_surgery
            WHERE surgery_id = ?
            """,(surgery_id,))

        except sqlite3.Error as e:
            print("Database Error", e)
            return

        row = cursor.fetchone()

        if not row:
            print("No GP surgery found")
            return
        else:
            clinic = GpSurgery(row[1],row[2])
            print(row[0])
            clinic.show_gpsurgery_details()
        return
    
    def update_gpsurgery(self):
        while True:
            try:
                surgery_id = int(input("Surgery ID:"))
                if not self.validate_id_input(surgery_id):
                    print("Surgery ID - must be greater than 0")
                    continue 
                break
            except ValueError:
                print("For Surgery ID use only numbers")
                continue
        try:
            cursor.execute("""
            SELECT * FROM gp_surgery
            WHERE surgery_id = ?
            """,(surgery_id,))

        except sqlite3.Error as e:
            print("Database Error", e)
            return

        row = cursor.fetchone()

        if not row:
            print("GP Surgery not found")
            return 
        else:
            gpsurgery = GpSurgery(row[1],row[2])
            print(row[0])
            gpsurgery.show_gpsurgery_details()

            update = input("Are you sure you want to update?")
            if update == "n":
                print("Update - Aborted")
                return
            else:
                while True:
                    new_surgery_name = input("Surgery Name:")
                    if new_surgery_name == "":
                        print("Surgery Name - Do not leave blank!")
                        continue 
                    if not self.validate_surgeryname(new_surgery_name):
                        print("For surgery name use alphabet and tap space bar if required")
                        continue 
                    break
               
                while True:
                    new_address = input("Address:")
                    if new_address == "":
                        print("Address - Do not leave blank!")
                        continue 
    
                    invalid_char = False
                    for character in new_address:
                        if character.isalpha() or character.isdigit():
                            continue
                        if character in["&", " ", "-", "'", ",", ".", "/"]:
                            continue
                        else:
                            invalid_char == True
                            break 
                    if invalid_char == True:
                            print("Address does not include such a character")
                            continue
                
                    digit_in_address = False
                    for num in new_address:
                        if num.isdigit():
                            digit_in_address = True
                            break 
                    if digit_in_address == False:
                        print("Address must have a number")
                        continue 
                    break
                        

            gpsurgery.surgery_name = new_surgery_name
            gpsurgery.address = new_address

            try:
                cursor.execute("""
                    UPDATE gp_surgery
                    SET surgery_name = ?,
                    address = ?
                    WHERE surgery_id = ?
                    """,(gpsurgery.surgery_name,gpsurgery.address,surgery_id))

                conn.commit()

            except sqlite3.Error as e:
                print("Database Error", e)
                return
            
            print("GP Surgery updated sucessfully!")
            return
        
    def delete_gpsurgery(self):
        surgery_id = int(input("Surgery ID:"))
        while True:
            try:
                if surgery_id == "":
                    print("Surgery ID - Do not leave blank!")
                    continue 
                if not self.validate_id_input(surgery_id):
                    print("Surgery ID must greater than 0")
                    continue 
                break
            except ValueError:
                print("For Surgery ID use only numbers")
                continue

        try:
            cursor.execute("""
            SELECT * FROM gp_surgery
            WHERE surgery_id = ?
            """,(surgery_id,))

        except sqlite3.Error as e:
            print("Database Error", e)
            return

        row = cursor.fetchone()

        if not row:
            print("No GP surgery found")
            return
        else:
            gpsurgery = GpSurgery(row[1],row[2])
            print(row[0])
            gpsurgery.show_gpsurgery_details()

            delete = input("Are you sure you want to delete?")
            if delete == "y":

                try:
                    cursor.execute("""
                    DELETE FROM gp_surgery
                    WHERE surgery_id = ?
                    """,(surgery_id,))

                    conn.commit()

                except sqlite3.Error as e:
                    print("Database Error", e)
                    return

                print("GP Surgery deleted sucessfully!")
                return

            else:
                print("Deletion process aborted!")

test = GpSurgery(
        "surgery_name",
        "address"
    )
test.create_gpsurgery()






