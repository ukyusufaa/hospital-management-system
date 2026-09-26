import sqlite3
from database import conn, cursor
from colors import DISPLAY_INFO,PRACTICE_MENU,ERROR,RESET

class GpSurgery:
    def __init__(self,surgery_name = None, address = None):
        self.surgery_name = surgery_name
        self.address = address 
    
    def show_gpsurgery_details(self):
        print("=" * 30)
        print(f"{PRACTICE_MENU}Surgery Name:{self.surgery_name}{RESET}")
        print(f"{PRACTICE_MENU}Address:{self.address}{RESET}")
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
            self.surgery_name = input(f"{PRACTICE_MENU}Enter medical practice name: {RESET}")
            if self.surgery_name == "":
                print(f"{ERROR}Medical practice name cannot be blank.{RESET}")
                continue
            if not self.validate_surgeryname(self.surgery_name):
                print(f"{ERROR}Please use letters and spaces only.{RESET}")
                continue 
            break

        while True:
            self.address = input(f"{PRACTICE_MENU}Enter medical practice address: {RESET}")
            if self.address == "":
                print(f"{ERROR}Address cannot be blank.{RESET}")
                continue

            if not " " in self.address:
                print(f"{ERROR}Please enter the full address " 
                        f"including spaces between address details.{RESET}")
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
                print(f"{ERROR}Please enter a valid address using standard charcaters.{RESET}")
                continue

            digit_in_address = False
            for character in self.address:
                if character.isdigit():
                    digit_in_address = True
                    break 
            if digit_in_address == False:
                print(f"{ERROR}Please include a building or " 
                      f"house number in the full address.{RESET}")
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
            print(f"{ERROR}Unable to save the medical practice " 
                    f"details. Please try again.{RESET}", e)
            return

        print(f"{DISPLAY_INFO}Medical practice created successfully.{RESET}")
        print()

        surgery_id = cursor.lastrowid
        print(f"{DISPLAY_INFO}Medical practice ID: {surgery_id}{RESET}")
        self.show_gpsurgery_details()
        

        # Retrieve and display all medical practices stored in the database.
    def display_all_gpsurgery(self):
        try:
            cursor.execute("SELECT * FROM gp_surgery")

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to retrieve medical practices. Please try again.{RESET}", e)
            return

        surgery_rows = cursor.fetchall()

        if len(surgery_rows) == 0:
            print(f"{ERROR}No medical practices are currently registered.{RESET}")
            return
        
        for surgery_row in surgery_rows:
            clinic = GpSurgery(
                surgery_row[1],
                surgery_row[2]
            )

            print(f"{DISPLAY_INFO}Medical practice ID: {surgery_row[0]}{RESET}")
            clinic.show_gpsurgery_details()
            print()
    

        # Find a medical practice using its unique surgery ID.
    def search_gpsurgery(self):
        while True:
            try:
                surgery_id = int(input("Enter medical practice ID:"))
                if not self.validate_id_input(surgery_id):
                    print(f"{ERROR}Please enter a valid medical practice ID.{RESET}")
                    continue 
                break
            except ValueError:
                print(f"{ERROR}Please enter the surgery ID using numbers only.{RESET}")
                continue
        try:
            cursor.execute("""
            SELECT * FROM gp_surgery
            WHERE surgery_id = ?
            """,(surgery_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to search for the medical practice. " 
                  f"Please try again. {RESET}", e)
            return

        surgery = cursor.fetchone()

        if not surgery:
            print(f"{ERROR}No medical practice was found with that ID.{RESET}")
            return
        
        self.surgery_name = surgery[1]
        self.address = surgery[2]

        print(f"{DISPLAY_INFO}Medical practice ID: {surgery[0]}{RESET}")
        self.show_gpsurgery_details()
    

        # Update the details of an existing medical practice.
    def update_gpsurgery(self):
        while True:
            try:
                surgery_id = int(input(f"{PRACTICE_MENU}Enter medical practice ID:{RESET}"))

                if not self.validate_id_input(surgery_id):
                    print(f"{ERROR}Enter a valid medical practice.{RESET}")
                    continue
                break

            except ValueError:
                print(f"{ERROR}Please enter the medical practice ID " 
                      f"using numbers only.{RESET}")
                continue
        try:
            cursor.execute("""
            SELECT * FROM gp_surgery
            WHERE surgery_id = ?
            """,(surgery_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to retrieve the medical practice. "
                  f"Please try again.{RESET}", e)
            return

        surgery = cursor.fetchone()

        if not surgery:
            print(f"{ERROR}GP Surgery not found.{RESET}")
            return 
        
        self.surgery_name = surgery[1]
        self.address = surgery[2]

        print(f"{DISPLAY_INFO}Medical practice ID: {surgery[0]}{RESET}")
        self.show_gpsurgery_details()
        print()

        while True:
            update = input(f"{PRACTICE_MENU}Update " 
                           f"this medical practice? (Y/N): {RESET}").lower()

            if not self.validate_yes_no(update):
                print(f"{ERROR}Please enter Y/y or N/n.{RESET}")
                continue
            
            if update == "n":
                print(f"{DISPLAY_INFO}Medical practice update cancelled.{RESET}")
                return
            break

        while True:
            new_surgery_name = input(f"{DISPLAY_INFO}Enter new medical practice name: {RESET}")

            if new_surgery_name == "":
                print(f"{ERROR}Medical practice name cannot be blank.{RESET}")
                continue

            if not self.validate_surgeryname(new_surgery_name):
                print(f"{ERROR}Please use letters and spaces only.{RESET}")
                continue
            break
               
        while True:
            new_address = input(f"{PRACTICE_MENU}Enter new medical practice address: {RESET}")

            if new_address == "":
                print(f"{ERROR}Address cannot be blank.{RESET}")
                continue

            if not " " in new_address:
                print(f"{ERROR}Please enter the full address " 
                        f"including spaces between address details.{RESET}")
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
                print(f"{ERROR}Please enter a valid address " 
                        f"using the standard characters.{RESET}")
                continue
                
            digit_in_address = False
            for character in new_address:
                if character.isdigit():
                    digit_in_address = True
                    break

            if not digit_in_address:
                print(f"{ERROR}Please include a building " 
                        f"or house number in the address.{RESET}")
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
            print(f"{ERROR}Unable to update the medical practice. Please try again.{RESET}", e)
            return
            
        print(f"{DISPLAY_INFO}Medical practice updated sucessfully.{ERROR}")
        return


        # Confirm and remove an existing medical practice from the database.
    def delete_gpsurgery(self):
        while True:
            try:
                surgery_id = int(input(f"{PRACTICE_MENU}Enter medical practice ID: {RESET}"))

                if surgery_id == "":
                    print(f"{ERROR}Medical practice cannot be blank.{RESET}")
                    continue

                if not self.validate_id_input(surgery_id):
                    print(f"{ERROR}Please enter a valid medical practice ID.{RESET}")
                    continue 
                break

            except ValueError:
                print(f"{ERROR}Please enter the medical " 
                      f"practice ID using numbers only.{RESET}")
                continue

        try:
            cursor.execute("""
            SELECT * FROM gp_surgery
            WHERE surgery_id = ?
            """,(surgery_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to retrieve the medical " 
                  f"practice. Please try again.{RESET}", e)
            return

        surgery = cursor.fetchone()

        if not surgery:
            print(f"{ERROR}No medical practice was found with that ID.{RESET}")
            return
        
        self.surgery_name = surgery[1]
        self.address = surgery[2]

        print(f"{DISPLAY_INFO}Medical practice ID: {surgery[0]}{RESET}")
        self.show_gpsurgery_details()
        print()

        while True:
            delete = input(f"{PRACTICE_MENU}Delete this "
                           f"medical practice?(Y/N): {RESET}").lower()

            if not self.validate_yes_no(delete):
                print(f"{ERROR}Please enter Y/y or N/n.{RESET}")
                continue
            
            if delete == "y":
                try:
                    cursor.execute("""
                    DELETE FROM gp_surgery
                    WHERE surgery_id = ?
                    """,(surgery_id,))

                    conn.commit()

                except sqlite3.Error as e:
                    print(f"{ERROR}Unable to delete the " 
                            f"medical practice. Please try again.{RESET}", e)
                    return

                print(f"{DISPLAY_INFO}Medical practice deleted successfully.{RESET}")
                return
            
            print(f"{DISPLAY_INFO}Medical surgery deletion process cancelled.{RESET}")
            return








