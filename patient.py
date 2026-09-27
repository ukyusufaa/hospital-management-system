import sqlite3
import calendar 
from datetime import datetime
from database import conn, cursor
from colors import DISPLAY_INFO,PATIENT_MENU,ERROR,RESET


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
        print("=" * 30)
        print(f"{DISPLAY_INFO}First Name:{self.first_name}{RESET}")
        print(f"{DISPLAY_INFO}Last Name:{self.surname}{RESET}")
        print(f"{DISPLAY_INFO}Date of Birth:{self.dob}{RESET}")
        print(f"{DISPLAY_INFO}Address:{self.address}{RESET}")
        print(f"{DISPLAY_INFO}GP ID:{self.gp_id}{RESET}")
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
            self.first_name = input(f"{PATIENT_MENU}Enter first name: {RESET}")

            if self.first_name == "":
                print(f"{ERROR}First name is required.{RESET}")
                continue

            if not self.validation_name(self.first_name):
                print(f"{ERROR}Please use letters and spaces only.{RESET}")
                continue 
            break 

        while True:
            self.surname = input(f"{PATIENT_MENU}Enter last name: {RESET}")

            if self.surname == "":
                print(f"{ERROR}Last name is required.{RESET}")
                continue

            if not self.validation_name(self.surname):
                print(f"{ERROR}Please use letters and spaces only.{RESET}")
                continue 
            break 

        while True:
            invalid_dob = False

            self.dob = input(f"{PATIENT_MENU}Enter date of birth (DD/MM/YYYY): {RESET}")

            if len(self.dob) != 10:
                print(f"{ERROR}Date of birth must be DD/MM/YYYYY.{RESET}")
                continue

            if self.dob[2] != "/" or self.dob[5] != "/":
                print(f"{ERROR}Date of birth must use a separator.{RESET}")
                continue

            for value in self.dob:
                if value == "/":
                    continue

                if not value.isdigit():
                    invalid_dob = True
                    break 

            if invalid_dob:
                print(f"{ERROR}Date of birth must use the format (DD/MM/YYYY).{RESET}")
                continue

            day = int(self.dob[0:2])
            month = int(self.dob[3:5])
            year = int(self.dob[6:10])

            if day < 1 or day > 31:
                print(f"{ERROR}Please enter a valid day.{RESET}")
                continue 

            if month < 1 or month > 12:
                print(f"{ERROR}Please enter a valid month.{RESET}")
                continue 

            if year < 1900:
                print(f"{ERROR}Please enter a valid year.{RESET}")
                continue 

            days_in_month = calendar.monthrange(year, month)[1]
            
            if day > days_in_month:
                print(f"{ERROR}Please enter a valid date.{RESET}")
                continue
            break

        while True:
            self.address = input(f"{PATIENT_MENU}Enter address: {RESET}")

            if self.address == "":
                print(f"{ERROR}Address is required.{RESET}")
                continue
            
            if not " " in self.address:
                print(f"{ERROR}Please enter the address using spaces between " 
                      f"address parts.{RESET}")
                continue

            if not all(
                character.isalpha()
                or character.isdigit()
                or character in [".", ",", "'", "-", "/", "&", " "]
                for character in self.address):
                    print(f"{ERROR}Please enter a valid address.{RESET}")
                    continue

            if not any(character.isdigit() for character in self.address):
                print(f"{ERROR}Address must contain a house or building number.{RESET}")
                continue
            break
    
        while True:
            gp = input(f"{PATIENT_MENU}Does the patient have a GP? (Y/N):  {RESET}").lower()
            
            if not self.validate_yes_no(gp):
                print(f"{ERROR}Enter Y/y or N/n.{RESET}")
                continue

            if gp == "n":
                self.gp_id = None
                break

            try:
                self.gp_id = int(input(f"{PATIENT_MENU}Enter GP ID: {RESET}"))

                if not self.validate_login_digits(self.gp_id):
                    print(f"{ERROR}Please use a valid GP ID.{RESET}")
                    continue
                

            except ValueError:
                print(f"{ERROR}Please enter the GP ID using numbers only.{RESET}")
                continue 

            try:
                cursor.execute("""
                SELECT * FROM gp
                    WHERE gp_id = ?
                """,(self.gp_id,))

            except sqlite3.Error as e:
                    print(f"{ERROR}Unable to verify the GP record. Please try again.{e}{RESET}")
                    return

            gp_record = cursor.fetchone()

            if not gp_record:
                print(f"{ERROR}No GP was found with that ID.{RESET}")
                return
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
            print(f"{ERROR}Unable to create the patient.{e}{RESET}")
            return
        
        print(f"{DISPLAY_INFO}Patient created successfully.{RESET}")
        print()

        patient_id = cursor.lastrowid
        print(f"{DISPLAY_INFO}Patient ID: {patient_id}{RESET}")
        self.show_patient_details()
        

        # Retrieve and display all registered patients.
    def display_all_patients(self):
        try:
            cursor.execute("SELECT * FROM patient")

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to retrieve patient records. Please try again.{e}{RESET}")
            return

        patient_records = cursor.fetchall()

        if not patient_records:
            print(f"{ERROR}No patients are currently registered.{RESET}")
            return
        
        for patient_record in patient_records:
            patient = Patient(
                patient_record[1],
                patient_record[2],
                patient_record[3],
                patient_record[4],
                patient_record[5]
            )

            print(f"{DISPLAY_INFO}Patient ID: {patient_record[0]}{RESET}")
            patient.show_patient_details()
            print()
        

        # Find a patient using their unique patient ID.
    def search_patient(self):
        while True:
            try:
                patient_id = int(input(f"{PATIENT_MENU}Enter patient ID: {RESET}"))

                if not self.validate_login_digits(patient_id):
                    print(f"{ERROR}Please enter a valid patient ID.{RESET}")
                    continue
                break

            except ValueError:
                print(f"{ERROR}Please enter the patient ID using numbers only.{RESET}")
                continue
        try:
            cursor.execute("""
                SELECT * FROM patient
                WHERE patient_id = ?
            """,(patient_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to search the patient records. Please try again.{e}{RESET}")
            return

        patient_record = cursor.fetchone()

        if not patient_record:
            print(f"{ERROR}No patient was found with that ID.{RESET}")
            return
        
        self.first_name = patient_record[1]
        self.surname = patient_record[2]
        self.dob = patient_record[3]
        self.address = patient_record[4]
        self.gp = patient_record[5]

        print(f"{DISPLAY_INFO}Patient ID: {patient_record[0]}{RESET}")
        self.show_patient_details()
        

        # Update the details of an existing patient.
    def update_patient(self):
        while True:
            try:
                patient_id = int(input(f"{PATIENT_MENU}Enter patient ID: {RESET}"))

                if not self.validate_login_digits(patient_id):
                    print(f"{ERROR}Please enter a valid patient ID.{RESET}")
                    continue
                break 

            except ValueError:
                print(f"{ERROR}Please enter the patient ID using numbers only.{RESET}")
                continue
        try:
            cursor.execute("""
                SELECT * FROM patient
                WHERE patient_id = ?
            """,(patient_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to retrieve the patient record for updating. "
                  f"Please try again.{e}{RESET}")
            return

        patient_record = cursor.fetchone()

        if not patient_record:
            print(f"{ERROR}No patient was found with that ID.{RESET}")
            return
        
        self.first_name = patient_record[1]
        self.surname = patient_record[2]
        self.dob = patient_record[3]
        self.address = patient_record[4]
        self.gp = patient_record[5]

        print(f"{DISPLAY_INFO}Patient ID: {patient_record[0]}{RESET}")
        self.show_patient_details()
        print()

        while True:
            update = input(f"{PATIENT_MENU}Update " 
                           f"this patients details? (Y/N): {RESET}").lower()
            
            if not self.validate_yes_no(update):
                print(f"{ERROR}Please enter Y/y or N/n.{RESET}")
                continue
                
            if update == "n":
                print(f"{DISPLAY_INFO}Update aborted.{RESET}")
                return
            break 
            
        while True:
            updated_first_name = input(f"{PATIENT_MENU}Enter first name: {RESET}")
    
            if updated_first_name == "":
                print(f"{ERROR}First name is required.{RESET}")
                continue
    
            if not self.validation_name(updated_first_name):
                print(f"{ERROR}Please use letters and spaces only.{RESET}")
                continue 
            break 
    
        while True:
            updated_surname = input(f"{PATIENT_MENU}Enter last name: {RESET}")
    
            if updated_surname == "":
                print(f"{ERROR}Last name is required.{RESET}")
                continue
    
            if not self.validation_name(updated_surname):
                print(f"{ERROR}Please use letters and spaces only.{RESET}")
                continue 
            break 
    
        while True:
            invalid_dob = False
    
            updated_dob = input(f"{PATIENT_MENU}Enter date of birth (DD/MM/YYYY): {RESET}")
    
            if len(updated_dob) != 10:
                print(f"{ERROR}Date of birth must be DD/MM/YYYYY.{RESET}")
                continue
    
            if updated_dob[2] != "/" or updated_dob[5] != "/":
                print(f"{ERROR}Date of birth must use / as a separator.{RESET}")
                continue
    
            for value in updated_dob:
                if value == "/":
                    continue
    
                if not value.isdigit():
                    invalid_dob = True
                break 
    
            if invalid_dob:
                print(f"{ERROR}Date of birth must use the format (DD/MM/YYYY).{RESET}")
                continue
    
            day = int(self.dob[0:2])
            month = int(self.dob[3:5])
            year = int(self.dob[6:10])
    
            if day < 1 or day > 31:
                print(f"{ERROR}Please enter a valid day.{RESET}")
                continue 
    
            if month < 1 or month > 12:
                print(f"{ERROR}Please enter a valid month.{RESET}")
                continue 
    
            if year < 1900:
                print(f"{ERROR}Please enter a valid year.{RESET}")
                continue 
    
            days_in_month = calendar.monthrange(year, month)[1]
                
            if day > days_in_month:
                print(f"{ERROR}Please enter a valid date.{RESET}")
                continue
            break
    
        while True:
            updated_address = input(f"{PATIENT_MENU}Enter address: {RESET}")
    
            if updated_address == "":
                print(f"{ERROR}Address is required.{RESET}")
                continue
                
            if not " " in self.address:
                print(f"{ERROR}Please enter the address using " 
                      f"spaces between address parts.{RESET}")
                continue
    
            if not all(
                character.isalpha()
                or character.isdigit()
                or character in [".", ",", "'", "-", "/", "&", " "]
                for character in self.address):
                    print(f"{ERROR}Please enter a valid address.{RESET}")
                    continue
    
            if not any(character.isdigit() for character in self.address):
                print(f"{ERROR}Address must contain a house or building number.{RESET}")
                continue
            break

        while True:
            gp = input(f"{PATIENT_MENU}Does the patient have a GP? (Y/N): {RESET}").lower()
                    
            if not self.validate_yes_no(gp):
                print(f"{ERROR}Enter Y/y or N/n.{RESET}")
                continue
        
            if gp == "n":
                self.gp_id = None
                break
            
            try:
                updated_gp_id = int(input(f"{PATIENT_MENU}Enter GP ID: {RESET}"))
        
                if not self.validate_login_digits(updated_gp_id):
                    print(f"{ERROR}Please use a valid GP ID.{RESET}")
                    continue
        
            except ValueError:
                print(f"{ERROR}Please enter the GP ID using numbers only.{RESET}")
                continue 
        
            try:
                cursor.execute("""
                    SELECT * FROM gp
                    WHERE gp_id = ?
                """,(updated_gp_id,))
        
            except sqlite3.Error as e:
                print(f"{ERROR}Unable to verify the GP record. Please try again.{e}{RESET}")
                return
        
            gp_record = cursor.fetchone()
        
            if not gp_record:
                print(f"{ERROR}No GP was found with that ID.{RESET}")
                continue 
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
            print(f"{ERROR}Unable to update the patient record. Please try again.{e}{RESET}")
            return

        print(f"{DISPLAY_INFO}Patient updated successfully.{RESET}")
        

        # Confirm and remove an existing patient from the database.
    def delete_patient(self):
        while True:
            try:
                patient_id = int(input(f"{PATIENT_MENU}Enter patient ID: {RESET}"))

                if not self.validate_login_digits(patient_id):
                    print(f"{ERROR}Please enter a valid patient ID.{RESET}")
                    continue

            except ValueError:
                print(f"{ERROR}Please enter the patient ID using numbers only.{RESET}")
                continue

            try:
                cursor.execute("""
                    SELECT * FROM patient
                    WHERE patient_id = ?
            """,(patient_id,))

            except sqlite3.Error as e:
                print(f"{ERROR}Unable to retrieve the patient record. "
                      f"Please try again.{e}{RESET}")
                return

            patient_record = cursor.fetchone()

            if not patient_record:
                print(f"{ERROR}No patient was found with that ID.{RESET}")
                continue 
            break
        
        self.first_name = patient_record[1]
        self.surname = patient_record[2]
        self.dob = patient_record[3]
        self.address = patient_record[4]
        self.gp = patient_record[5]

        print(f"{DISPLAY_INFO}Patient ID: {patient_record[0]}{RESET}")
        self.show_patient_details()
        print()
            
        while True:
            delete = input(f"{PATIENT_MENU}Delete this patient? (Y/N): {RESET}").lower()
            
            if not self.validate_yes_no(delete):
                print(f"{ERROR}Please enter Y/y or N/n.{RESET}")
                continue

            if delete == "n":
                print(f"{DISPLAY_INFO}Patient deletion cancelled.{RESET}")
                return
            break
                
        try:
            cursor.execute("""
                DELETE FROM patient
                WHERE patient_id = ?
            """,(patient_id,))

            conn.commit()

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to delete the patient record. Please try again.{e}{RESET}")
            return
                    
        print(f"{DISPLAY_INFO}Patient deleted successfully.{RESET}")


        
        


            
                

                    


                


        
            
            

                