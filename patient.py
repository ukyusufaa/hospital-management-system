import sqlite3
import calendar 
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
                    break 

            if invalid_dob:
                print("Date of birth must use "
                "the format (DD/MM/YYYY).")
                continue

            day = int(self.dob[0:2])
            month = int(self.dob[3:5])
            year = int(self.dob[6:10])

            if day < 1 or day > 31:
                print("Please enter a valid day.")
                continue 

            if month < 1 or month > 12:
                print("Please enter a valid month.")
                continue 

            if year < 1900:
                print("Please enter a valid year.")
                continue 

            days_in_month = calendar.monthrange(year, month)[1]
            
            if day > days_in_month:
                print("Please enter a valid date.")
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

            if not all(
                character.isalpha()
                or character.isdigit()
                or character in [".", ",", "'", "-", "/", "&", " "]
                for character in self.address):
                    print("Please enter a valid address.")
                    continue

            if not any(character.isdigit() for character in self.address):
                print("Address must contain a house "
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

                gp_record = cursor.fetchone()

                if not gp_record:
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

        patient_id = cursor.lastrowid
        print(f"Patient ID: {patient_id}")
        self.show_patient_details()
        

        # Retrieve and display all registered patients.
    def display_all_patients(self):
        try:
            cursor.execute("SELECT * FROM patient")

        except sqlite3.Error as e:
            print("Unable to retrieve " \
            "patient records. Please " \
            "try again.", e)
            return

        patient_records = cursor.fetchall()

        if not patient_records:
            print("No patients are " \
            "currently registered.")
            return
        
        for patient_record in patient_records:
            patient = Patient(
                patient_record[1],
                patient_record[2],
                patient_record[3],
                patient_record[4],
                patient_record[5]
            )

            print(f"Patient ID: {patient_record[0]}")
            patient.show_patient_details()
        

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

        patient_record = cursor.fetchone()

        if not patient_record:
            print("No patient was found " \
                    "with that ID.")
            return
        
        self.first_name = patient_record[1]
        self.surname = patient_record[2]
        self.dob = patient_record[3]
        self.address = patient_record[4]
        self.gp = patient_record[5]

        print(f"Patient ID: {patient_record[0]}")
        self.show_patient_details()
        

        # Update the details of an existing patient.
    def update_patient(self):
        while True:
            try:
                patient_id = int(input("Enter patient ID: "))

                if not self.validate_login_digits(patient_id):
                    print("Please enter a valid patient ID.")
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

        patient_record = cursor.fetchone()

        if not patient_record:
            print("No patient was found " \
                    "with that ID.")
            return
        
        self.first_name = patient_record[1]
        self.surname = patient_record[2]
        self.dob = patient_record[3]
        self.address = patient_record[4]
        self.gp = patient_record[5]

        print(f"Patient ID: {patient_record[0]}")
        self.show_patient_details()

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
            break 
            
        while True:
            updated_first_name = input("Enter first name: ")
    
            if updated_first_name == "":
                print("First name is required.")
                continue
    
            if not self.validation_name(updated_first_name):
                print("Please use letters and spaces only.")
                continue 
            break 
    
        while True:
            updated_surname = input("Enter last name: ")
    
            if updated_surname == "":
                print("Last name is required.")
                continue
    
            if not self.validation_name(updated_surname):
                print("Please use letters and spaces only.")
                continue 
            break 
    
        while True:
            invalid_dob = False
    
            updated_dob = input("Enter date of birth (DD/MM/YYYY):")
    
            if len(updated_dob) != 10:
                print("Date of birth must be DD/MM/YYYYY.")
                continue
    
            if updated_dob[2] != "/" or updated_dob[5] != "/":
                print("Date of birth must use / as "
                        "a separator.")
                continue
    
            for value in updated_dob:
                if value == "/":
                    continue
    
                if not value.isdigit():
                    invalid_dob = True
                break 
    
            if invalid_dob:
                print("Date of birth must use "
                        "the format (DD/MM/YYYY).")
                continue
    
            day = int(self.dob[0:2])
            month = int(self.dob[3:5])
            year = int(self.dob[6:10])
    
            if day < 1 or day > 31:
                print("Please enter a valid day.")
                continue 
    
            if month < 1 or month > 12:
                print("Please enter a valid month.")
                continue 
    
            if year < 1900:
                print("Please enter a valid year.")
                continue 
    
            days_in_month = calendar.monthrange(year, month)[1]
                
            if day > days_in_month:
                print("Please enter a valid date.")
                continue
            break
    
        while True:
            updated_address = input("Enter address: ")
    
            if updated_address == "":
                print("Address is required.")
                continue
                
            if not " " in self.address:
                print("Please enter the address using " \
                        "spaces between address parts.")
                continue
    
            if not all(
                character.isalpha()
                or character.isdigit()
                or character in [".", ",", "'", "-", "/", "&", " "]
                for character in self.address):
                    print("Please enter a valid address.")
                    continue
    
            if not any(character.isdigit() for character in self.address):
                print("Address must contain a house "
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
                    updated_gp_id = int(input("Enter GP ID:"))
        
                    if not self.validate_login_digits(updated_gp_id):
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
                    """,(updated_gp_id,))
        
                except sqlite3.Error as e:
                    print("Unable to verify the " \
                            "GP record. Please try again.",e)
                    return
        
                gp_record = cursor.fetchone()
        
                if not gp_record:
                    print("No GP was found " \
                            "with that ID.")
                    continue 
                break

            else:
                updated_gp_id = None 
                break
        
          
        self.first_name = updated_first_name
        self.surname = updated_surname
        self.dob = updated_dob
        self.address = updated_address
        self.gp_id = updated_gp_id

        try:
            cursor.execute("""
                UPDATE patient
                SET first_name = ?,
                    surname = ?,
                    dob = ?,
                    address = ?,
                    gp_id = ?
                WHERE patient_id =?
            """,(self.first_name,
                self.surname,
                self.dob,
                self.address,
                self.gp_id,
                patient_id))
                
            conn.commit()

        except sqlite3.Error as e:
            print("Unable to update the " \
                    "patient record. Please try again.",e)
            return

        print("Patient updated successfully.")
        

        # Confirm and remove an existing patient from the database.
    def delete_patient(self):
        while True:
            try:
                patient_id = int(input("Enter patient ID: "))

                if not self.validate_login_digits(patient_id):
                    print("Please enter a " \
                            "valid patient ID.")
                    continue

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

            patient_record = cursor.fetchone()

            if not patient_record:
                print("No patient was " \
                    "found with that ID.")
                continue 
            break
        
        self.first_name = patient_record[1]
        self.surname = patient_record[2]
        self.dob = patient_record[3]
        self.address = patient_record[4]
        self.gp = patient_record[5]

        print(f"Patient ID: {patient_record[0]}")
        self.show_patient_details()
            
        while True:
            delete = input("Delete " 
                        "this patient? (Y/N): ").lower()
            
            if not self.validate_yes_no(delete):
                print("Please enter Y/y or N/n.")
                continue

            if delete == "n":
                print("Patient deletion cancelled.")
                return
            break
                
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


        
        


            
                

                    


                


        
            
            

                