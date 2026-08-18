import sqlite3 
from datetime import datetime
from database import conn, cursor

class Patient():
    def __init__(self, first_name = None, surname = None, 
                 dob = None, address = None, 
                 gp_id = None):
        self.first_name = first_name
        self.surname = surname
        self.dob = dob
        self.address = address
        self.gp_id = gp_id
    
    def show_patient_details(self):
        print("-" * 30)
        print(f"First Name:{self.first_name}")
        print(f"Last Name:{self.surname}")
        print(f"Date of Birth:{self.dob}")
        print(f"Address:{self.address}")
        print(f"GP ID:{self.gp_id}")
        print("-" * 30)

        # Validate patient names using letters and spaces.
    def validation_name(self,name):
        for letter in name:
            if not letter.isalpha() and not letter == " ":
                return False
        return True

        # Validate IDs to ensure they are postive integers.
    def validate_login_digits(self,number):
        if number < 1:
            return False
        return True

        # Validate confirmation changes.
    def validate_yes_no(self,choice):
        if choice != 'y' and choice != 'n':
            return False
        return True

        # Collect and validate patient details before creating the record.
    def create_patient(self):
        while True:
            self.first_name = input("Enter first name: ")
            if self.first_name == "":
                print("First name is required.")
                continue
            if not self.validation_name(self.first_name):
                print("Please use letters and spaces only.")
                continue 
            break 

        while True:
            self.surname = input("Enter last name: ")
            if self.surname == "":
                print("Last name is required.")
                continue 
            if not self.validation_name(self.surname):
                print("Please use letters and spaces only.")
                continue 
            break 

        while True:
            
            invalid_dob = False

            self.dob = input("Enter date of birth (DD/MM/YYYY):")
            if len(self.dob) != 10:
                print("Date of birth must be DD/MM/YYYYY.")
                continue 
            if self.dob[2] != "/" or self.dob[5] != "/":
                print("Date of birth must use / as "
                "a separator.")
                continue
            for value in self.dob:
                if value == "/":
                    continue
                if not value.isdigit():
                    invalid_dob = True
                    print("Date of birth must contain " \
                    "numbers and / only.")
                    continue

            if invalid_dob == True:
                print("Date of birth must use "
                "the format (DD/MM/YYYY).")
                continue

            if int(self.dob[0:2]) < 1 or int(self.dob[0:2]) > 31:
                print("Please enter a valid day.")
                continue 
            if int(self.dob[3:5]) < 1 or int(self.dob[3:5]) > 12:
                print("Please enter a valid month. ")
                continue 
            if int(self.dob[6:10]) < 1900 or int(self.dob[6:10]) > datetime.now().year:
                print("Please enter a valid year.")
                continue 
            if int(self.dob[0:2]) > 30 and int(self.dob[3:5]) in [4,6,9,11]:
                print("This month does not contain " \
                "that many days.")
                continue 
            if(
                int(self.dob[0:2]) > 29 
                and int(self.dob[3:5]) == 2 
                and 
                (
                    int(self.dob[6:10]) % 400 == 0
                    or
                    (
                        int(self.dob[6:10]) % 4 == 0
                        and
                        int(self.dob[6:10]) % 100 != 0
                    )
                )
            ):
                print("This is a leap year. February has " \
                "a maximum of 29 days.")
                continue
            
            if(
                int(self.dob[0:2]) > 28 
                and int(self.dob[3:5]) == 2 
                and 
                (
                    int(self.dob[6:10]) % 400 != 0
                    and
                    (
                        int(self.dob[6:10]) % 4 != 0
                        or
                        int(self.dob[6:10]) % 100 == 0
                    )
                )
            ):
                print("This is not a leap year. February " \
                "has a maximum of 28 days.")
                continue 
            break

        while True:
            self.address = input("Enter address: ")
            if self.address == "":
                print("Address is required.")
                continue
            
            if not " " in self.address:
                print("Please enter the address using " \
                "spaces between address parts.")
                continue

            invalid_char = False
            for character in self.address:
                if character.isalpha() or character.isdigit():
                    continue
                if character in [".", ",", "'", "-", "/", "&", " "]:
                    continue
                else:
                    invalid_char = True
                    break 
            if invalid_char == True:
                print("Please enter a valid address.")
                continue
            
            digit_in_address = False
            for character in self.address:
                if character.isdigit():
                    digit_in_address = True
                    break
            if digit_in_address == False:
                print("Address must contain a house " \
                "or building number.")
                continue
            break
    
        while True:
            gp = input(
                "Does the patient have " 
                "a GP? (Y/N): ").lower()
            if not self.validate_yes_no(gp):
                print("Enter Y/y " \
                "or N/n.")
                continue
            if gp == "y":
                try:
                    self.gp_id = int(input("Enter GP ID:"))
                    if not self.validate_login_digits(self.gp_id):
                        print("Please use a valid GP ID.")
                        continue
                except ValueError:
                    print("Please enter the GP ID " \
                    "using numbers only.")
                    continue 

                try:
                    cursor.execute("""
                    SELECT * FROM gp
                    WHERE gp_id = ?
                    """,(self.gp_id,))

                except sqlite3.Error as e:
                    print("Unable to verify the " \
                    "GP record. Please try again.",e)
                    return

                row = cursor.fetchone()
                if not row:
                    print("No GP was found " \
                    "with that ID.")
                    continue 
                break
            
            else:
                self.gp_id = None 
                break

        try:
        # Insert the validated patient details into the database.
            cursor.execute("""
            INSERT INTO patient(
                first_name,
                surname,
                dob,
                address,
                gp_id)
            VALUES(?,?,?,?,?)
            """,(self.first_name,self.surname,self.dob,self.address,self.gp_id))

            conn.commit()

        except sqlite3.Error as e:
            print("Unable to create " \
            "the patient.", e)
            return
        
        print("Patient created successfully.")
        row = cursor.lastrowid
        print(f"Patient ID: {row}")
        self.show_patient_details()
        return

        # Retrieve and display all registered patients.
    def display_all_patients(self):
        try:
            cursor.execute("SELECT * FROM patient")

        except sqlite3.Error as e:
            print("Unable to retrieve " \
            "patient records. Please " \
            "try again.", e)
            return

        rows = cursor.fetchall()
        if not rows:
            print("No patients are " \
            "currently registered.")
            return
        else:
            for row in rows:
                sick = Patient(
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5]
                    )
                print(f"Patient ID: {row[0]}")
                sick.show_patient_details()
            return

        # Find a patient using their unique patient ID.
    def search_patient(self):
        while True:
            try:
                patient_id = int(input("Enter patient ID:"))
                if not self.validate_login_digits(patient_id):
                    print("Please enter a valid " \
                    "patient ID.")
                    continue
                break 
            except ValueError:
                print("Please enter the patient ID " \
                "using numbers only.")
                continue
        try:
            cursor.execute("""
            SELECT * FROM patient
            WHERE patient_id = ?
            """,(patient_id,))

        except sqlite3.Error as e:
            print("Unable to search the " \
            "patient records. Please " \
            "try again.", e)
            return

        row = cursor.fetchone()
        if not row:
            print("No patient was found " \
            "with that ID.")
            return
        else:
            sick = Patient(
                row[1],
                row[2],
                row[3],
                row[4],
                row[5]
            )
            print(f"Patient ID: {row[0]}")
            sick.show_patient_details()
            return

        # Update the details of an existing patient.
    def update_patient(self):
        while True:
            try:
                patient_id = int(input("Enter patient ID: "))
                if not self.validate_login_digits(patient_id):
                    print("Please enter a valid " \
                    "patient ID.")
                    continue
                break 
            except ValueError:
                print("Please enter the patient ID " \
                "using numbers only.")
                continue
        try:
            cursor.execute("""
            SELECT * FROM patient
            WHERE patient_id = ?
            """,(patient_id,))

        except sqlite3.Error as e:
            print("Unable to retrieve the " \
            "patient record for updating. " \
            "Please try again.", e)
            return

        row = cursor.fetchone()
        if not row:
            print("No patient was found " \
            "with that ID.")
            return
        else:
            sick = Patient(
                row[1],
                row[2],
                row[3],
                row[4],
                row[5]
            )
            print(f"Patient ID: {row[0]}")
            sick.show_patient_details()

            while True:
                update = input("Update " 
                    "this patients details? (Y/N): ").lower()
                if not self.validate_yes_no(update):
                    print("Please enter Y/y " \
                    "or N/n.")
                    continue
                
                if update == "n":
                    print("Update aborted")
                    return
                else:
                    while True:
                        updated_first_name = input("Enter new "
                            "first name: ")
                        if updated_first_name == "":
                            print("First name is required.")
                            continue
                        if not self.validation_name(updated_first_name):
                            print("Please use letters"
                            " and spaces only.")
                            continue 
                        break 
            
                    while True:
                        updated_surname = input("Enter new "
                            "last name:")
                        if updated_surname == "":
                            print("Last name is required.")
                            continue 
                        if not self.validation_name(updated_surname):
                            print("Please use letters " \
                            "and spaces only.")
                            continue 
                        break 

                    while True:
                        updated_dob = input("Date of Birth(DD/MM/YYYY):")
                        if len(updated_dob) != 10:
                            print("Date of birth must be DD/MM/YYYYY.")
                            continue 
                        if updated_dob[2] != "/" or updated_dob[5] != "/":
                            print("Date of birth must use "
                                  "a separator.")
                            continue
                    
                        no_digits = False
                        for user_input in updated_dob:
                            if user_input == "/":
                                continue 
                            if not user_input.isdigit():
                                no_digits = True
                                print("Date of birth "
                                "must contain numbers "
                                "and / only.")
                        
                        if no_digits == True:
                            print("Date of birth must " \
                            "use the format (DD/MM/YYYY).")
                            continue

                        if int(updated_dob[0:2]) < 1 or int(updated_dob[0:2]) > 31:
                            print("Please enter a valid day.")
                            continue 

                        if int(updated_dob[3:5]) < 1 or int(updated_dob[3:5]) > 12:
                            print("Please enter a valid month.")
                            continue

                        if int(updated_dob[6:10]) < 1900 or int(updated_dob[6:10]) > datetime.now().year:
                            print("Please enter a valid year.")
                            continue

                        if int(updated_dob[0:2]) > 30 and int(updated_dob[3:5]) in [4,6,9,11]:
                            print("This month does not contain " \
                            "this many days.")
                            continue

                        if(
                            int(updated_dob[0:2]) > 29 
                            and int(updated_dob[3:5]) == 2
                            and
                            (
                                int(updated_dob[6:10]) % 400 == 0
                                or
                                (
                                    int(updated_dob[6:10]) % 4 == 0
                                    and
                                    int(updated_dob[6:10]) % 100 != 0
                                )
                            )
                        ):
                            print("This is a leap. February " \
                            "has a maximum of 29 days.")
                            continue 

                        if(
                            int(updated_dob[0:2]) > 28 
                            and int(updated_dob[3:5]) == 2 
                            and 
                            (
                                int(updated_dob[6:10]) % 400 != 0
                                and
                                (
                                    int(updated_dob[6:10]) % 4 != 0
                                    or
                                    int(updated_dob[6:10]) % 100 == 0
                                )
                            )
                        ):
                            print("This is not a leap year. " \
                            "February has a maximum of 28 days.")
                            continue 
                        break
                    
                    while True:
                        updated_address = input("Enter address:")
                        if updated_address == "":
                            print("Address is required.")
                            continue

                        if not " " in updated_address:
                            print("Please enter the address " \
                            "using spaces betweeen " \
                            "address parts.")
                            continue
                        
                        not_allowed_input = False
                        for character in updated_address:
                            if character.isalpha() or character.isdigit():
                                continue
                            if character in ["&", "-", "'", ",", ".", "/", " "]:
                                continue 
                            else:
                                not_allowed_input = True
                                break
                        if not_allowed_input == True:
                            print("Please enter a valid address.")
                            continue

                        house_number = False
                        for char in updated_address:
                            if char.isdigit():
                                house_number = True
                                break
                        if house_number == False:
                            print("Address must contain " \
                            "a house or building number.")
                            continue
                        break 
                    
                    while True:
                        gp = input("Does the patient "
                            "have a GP? (Y/N): ").lower()
                        if not self.validate_yes_no(gp):
                            print("Please enter Y/y " \
                                "or N/n.")
                            continue
                        if gp == "y":
                            while True:
                                try:
                                    updated_gp_id = int(input(
                                        "Enter GP ID: "))
                                    if not self.validate_login_digits(updated_gp_id):
                                        print("Please enter a " \
                                        "valid GP ID.")
                                        continue 
                                
                                except ValueError:
                                    print("Please enter the " \
                                    "GP ID using numbers only.")
                                    continue 

                                try:
                                    cursor.execute("""
                                    SELECT * FROM gp
                                    WHERE gp_id = ?
                                    """,(updated_gp_id,))

                                except sqlite3.Error as e:
                                    print("Unable to verify " \
                                    "the GP record. Please " \
                                    "try again.")

                                row = cursor.fetchone()
                                if not row:
                                    print("No GP was found " \
                                    "with that ID.")
                                    continue
                                break
                            break
                        else:
                            updated_gp_id = None
                            break 

                sick.first_name = updated_first_name
                sick.surname = updated_surname
                sick.dob = updated_dob
                sick.address = updated_address
                sick.gp_id = updated_gp_id

                try:
                    cursor.execute("""
                        UPDATE patient
                        SET first_name = ?,
                        surname = ?,
                        dob = ?,
                        address = ?,
                        gp_id = ?
                    WHERE patient_id =?
                        """,(sick.first_name,
                        sick.surname,
                        sick.dob,
                        sick.address,
                        sick.gp_id,
                        patient_id
                        ))
                
                    conn.commit()

                except sqlite3.Error as e:
                    print("Unable to update the " \
                    "patient record. Please try again.",e)
                    return

                print("Patient updated successfully.")
                return

        # Confirm and remove an existing patient from the database.
    def delete_patient(self):
        while True:
            try:
                patient_id = int(input("Enter patient ID:"))
                if not self.validate_login_digits(patient_id):
                    print("Please enter a " \
                    "valid patient ID.")
                    continue
                break 
            except ValueError:
                print("Please enter the patient " \
                "ID using numbers only.")
                continue

        try:
            cursor.execute("""
            SELECT * FROM patient
            WHERE patient_id = ?
            """,(patient_id,))

        except sqlite3.Error as e:
            print("Unable to retrieve " \
            "the patient record. Please " \
            "try again.", e)
            return

        row = cursor.fetchone()
        if not row:
            print("No patient was " \
            "found with that ID.")
            return
        else:
            sick = Patient(
                row[1],
                row[2],
                row[3],
                row[4],
                row[5]
            )
            print(f"Patient ID: {row[0]}")
            sick.show_patient_details()
            
            while True:
                delete = input("Delete " 
                    "this patient? (Y/N): ").lower()
                if not self.validate_yes_no(delete):
                    print("Please enter Y/y " \
                    "or N/n.")
                    continue
                if delete == "n":
                    print("Patient deletion " \
                    "cancelled.")
                    return
                else:
                    try:
                        cursor.execute("""
                        DELETE FROM patient
                        WHERE patient_id = ?
                        """,(patient_id,))

                        conn.commit()

                    except sqlite3.Error as e:
                        print("Unable to delete " \
                        "the patient record." \
                        "Please try again.", e)
                        return
                    
                    print("Patient deleted successfully.")
                    return

        
        


            
                

                    


                


        
            
            

                