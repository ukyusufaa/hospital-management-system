import sqlite3
from database import conn, cursor

class GpSurgery:
    def __init__(self,surgery_name = None, address = None):
        self.surgery_name = surgery_name
        self.address = address 
    
    def show_gpsurgery_details(self):
        print("-" * 30)
        print(f"Surgery Name:{self.surgery_name}")
        print(f"Address:{self.address}")
        print("-" * 30)

        # Validate surgery names using letters and spaces.
    def validate_surgeryname(self,name):
        for letter in name:
            if (not letter.isalpha() and not letter == " "
                and not letter == '&'):
                return False
        return True

    def validate_yes_no(self,selected):
        if selected != 'y' and selected != 'n':
            return False
        return True

        # Validate IDs to ensure they are positive integers.
    def validate_id_input(self,number):
        if number < 1:
            return False
        return True

    # Collect and validate surgery details before saving the record.
    def create_gpsurgery(self):
        while True:
            self.surgery_name = input("Enter medical practice name:")
            if self.surgery_name == "":
                print("Medical practice name cannot be blank.")
                continue
            if not self.validate_surgeryname(self.surgery_name):
                print("Please use letters and spaces only.")
                continue 
            break

        while True:
            self.address = input("Enter medical practice address:")
            if self.address == "":
                print("Address cannot be blank.")
                continue

            if not " " in self.address:
                print("Please enter the full address " \
                        "including spaces between address " \
                            "details.")
                continue
            
            invalid_char = False
            for character in self.address:
                if character.isalpha() or character.isdigit():
                    continue
                if character in["&", " ", "-", "'", ",", ".", "/"]:
                    continue
                else:
                    invalid_char = True
                    break 
            if invalid_char == True:
                print("Please enter a valid address " \
                        "using standard charcaters.")
                continue

            digit_in_address = False
            for character in self.address:
                if character.isdigit():
                    digit_in_address = True
                    break 
            if digit_in_address == False:
                print("Please include a building or house " \
                        "number in the full address.")
                continue 
            break 

        try:
        # Insert the validated medical practice details into the database.
            cursor.execute("""
            INSERT INTO gp_surgery(
                       surgery_name,
                       address)
            VALUES(?,?)
            """,(self.surgery_name,self.address))

            conn.commit()

        except sqlite3.Error as e:
            print("Unable to save the medical practice " \
                    "details. Please try again.", e)
            return

        print("Medical practice created successfully.")

        surgery_id = cursor.lastrowid
        print(f"Medical practice ID: {surgery_id}")
        self.show_gpsurgery_details()
        

        # Retrieve and display all medical practices stored in the database.
    def display_all_gpsurgery(self):
        try:
            cursor.execute("SELECT * FROM gp_surgery")

        except sqlite3.Error as e:
            print("Unable to retrieve medical practices." \
                    "Please try again.", e)
            return

        surgery_rows = cursor.fetchall()

        if len(surgery_rows) == 0:
            print("No medical practices are " \
                    "currently registered.")
            return
        
        for surgery_row in surgery_rows:
            clinic = GpSurgery(
                surgery_row[1],
                surgery_row[2]
            )

            print(f"Medical practice ID: {surgery_row[0]}")
            clinic.show_gpsurgery_details()
    

        # Find a medical practice using its unique surgery ID.
    def search_gpsurgery(self):
        while True:
            try:
                surgery_id = int(input("Enter medical practice ID:"))
                if not self.validate_id_input(surgery_id):
                    print("Please enter a valid medical " \
                    "practice ID.")
                    continue 
                break
            except ValueError:
                print("Please enter the surgery ID " \
                        "using numbers only.")
                continue
        try:
            cursor.execute("""
            SELECT * FROM gp_surgery
            WHERE surgery_id = ?
            """,(surgery_id,))

        except sqlite3.Error as e:
            print("Unable to search for the " \
                    "medical practice. " \
                        "Please try again.", e)
            return

        surgery = cursor.fetchone()

        if not surgery:
            print("No medical practice was found. " \
                    "with that ID.")
            return
        
        self.surgery_name = surgery[1]
        self.address = surgery[2]

        print(f"Medical practice ID: {surgery[0]}")
        self.show_gpsurgery_details()
    

        # Update the details of an existing medical practice.
    def update_gpsurgery(self):
        while True:
            try:
                surgery_id = int(input("Enter medical practice ID:"))

                if not self.validate_id_input(surgery_id):
                    print("Enter a valid medical practice.")
                    continue
                break

            except ValueError:
                print("Please enter the medical practice ID " \
                        "using numbers only.")
                continue
        try:
            cursor.execute("""
            SELECT * FROM gp_surgery
            WHERE surgery_id = ?
            """,(surgery_id,))

        except sqlite3.Error as e:
            print("Unable to retrieve the " \
                    "medical practice. Please try again.", e)
            return

        surgery = cursor.fetchone()

        if not surgery:
            print("GP Surgery not found.")
            return 
        
        self.surgery_name = surgery[1]
        self.address = surgery[2]

        print(f"Medical practice ID: {surgery[0]}")
        self.show_gpsurgery_details()

        while True:
            update = input("Update " 
                "this medical practice? (Y/N):").lower()

            if not self.validate_yes_no(update):
                print("Please enter Y/y or N/n.")
                continue
            
            if update == "n":
                print("Medical practice update cancelled.")
                return
            break

        while True:
            new_surgery_name = input(
                "Enter new medical practice name: ")

            if new_surgery_name == "":
                print("Medical practice name cannot be blank.")
                continue

            if not self.validate_surgeryname(new_surgery_name):
                print("Please use letters and spaces only.")
                continue
            break
               
        while True:
            new_address = input("Enter new medical practice address: ")

            if new_address == "":
                print("Address cannot be blank.")
                continue

            if not " " in new_address:
                print("Please enter the full address " \
                        "including spaces between address details.")
                continue
    
            invalid_char = False
            for character in new_address:
                if character.isalpha() or character.isdigit():
                    continue
                if character in["&", " ", "-", "'", ",", ".", "/"]:
                    continue
                else:
                    invalid_char = True
                    break

            if invalid_char:
                print("Please enter a valid address " \
                        "using the standard characters.")
                continue
                
            digit_in_address = False
            for character in new_address:
                if character.isdigit():
                    digit_in_address = True
                    break

            if not digit_in_address:
                print("Please include a building " \
                        "or house number in the address.")
                continue 
            break
                        
        self.surgery_name = new_surgery_name
        self.address = new_address

        try:
            cursor.execute("""
                UPDATE gp_surgery
                SET surgery_name = ?,
                    address = ?
                WHERE surgery_id = ?
            """,(self.surgery_name, self.address,surgery_id))

            conn.commit()

        except sqlite3.Error as e:
            print("Unable to update the medical " \
                    "practice. Please try again.", e)
            return
            
        print("Medical practice updated sucessfully!")
        return


        # Confirm and remove an existing medical practice from the database.
    def delete_gpsurgery(self):
        while True:
            try:
                surgery_id = int(input("Enter medical practice ID: "))

                if surgery_id == "":
                    print("Medical practice cannot be blank.")
                    continue

                if not self.validate_id_input(surgery_id):
                    print("Please enter a " \
                            "valid medical practice ID.")
                    continue 
                break

            except ValueError:
                print("Please enter the medical " \
                        "practice ID using numbers only.")
                continue

        try:
            cursor.execute("""
            SELECT * FROM gp_surgery
            WHERE surgery_id = ?
            """,(surgery_id,))

        except sqlite3.Error as e:
            print("Unable to retrieve the " \
            "medical practice. Please try again.", e)
            return

        surgery = cursor.fetchone()

        if not surgery:
            print("No medical practice was " \
                    "found with that ID.")
            return
        
        self.surgery_name = surgery[1]
        self.address = surgery[2]

        print(f"Medical practice ID: {surgery[0]}")
        self.show_gpsurgery_details()

        while True:
            delete = input("Delete " 
                "this medical practice?(Y/N): ").lower()

            if not self.validate_yes_no(delete):
                print("Please enter Y/y or N/n.")
                continue
            
            if delete == "y":
                try:
                    cursor.execute("""
                    DELETE FROM gp_surgery
                    WHERE surgery_id = ?
                    """,(surgery_id,))

                    conn.commit()

                except sqlite3.Error as e:
                    print("Unable to delete the " \
                            "medical practice. Please try again.", e)
                    return

                print("Medical practice deleted " \
                        "successfully.")
                return
            
            print("Medical surgery deletion " \
                    "process cancelled.")
            return








