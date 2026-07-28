import sqlite3 
from datetime import datetime

conn = sqlite3.connect("hospital.db")

cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

class Patient():
    def __init__(self, first_name, surname, dob, address, gp_id):
        self.first_name = first_name
        self.surname = surname
        self.dob = dob
        self.address = address
        self.gp_id = gp_id
    
    def show_patient_details(self):
        print(f"First Name:{self.first_name}")
        print(f"Last Name:{self.surname}")
        print(f"Date of Birth:{self.dob}")
        print(f"Address:{self.address}")
        print(f"GP ID:{self.gp_id}")
    
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
    
    def create_patient(self):
        while True:
            self.first_name = input("First Name:")
            if self.first_name == "":
                print("First Name - Do not leave name blank!")
                continue
            if not self.validation_name(self.first_name):
                print("First Name - Use alphabet and tap space bar if required")
                continue 
            break 

        while True:
            self.surname = input("Last Name:")
            if self.surname == "":
                print("Last Name - Do not leave blank!")
                continue 
            if not self.validation_name(self.surname):
                print("Last Name - Use alphabet and tap space bar if required")
                continue 
            break 

        while True:
            
            invalid_dob = False

            self.dob = input("Date of Birth(DD/MM/YYYY):")
            if len(self.dob) != 10:
                print("Date of Birth - Invalid length")
                continue 
            if self.dob[2] != "/" or self.dob[5] != "/":
                print("Date of Birth - Invalid character used")
                continue
            for value in self.dob:
                if value == "/":
                    continue
                if not value.isdigit():
                    invalid_dob = True
                    print("Date of Birth - Use only numbers and this character /")
                    continue

            if invalid_dob == True:
                print("Date of birth - must be in this format(DD/MM/YYYY)")
                continue

            if int(self.dob[0:2]) < 1 or int(self.dob[0:2]) > 31:
                print("Date of Birth - Invalid day entered")
                continue 
            if int(self.dob[3:5]) < 1 or int(self.dob[3:5]) > 12:
                print("Date of Birth - Invalid month entered")
                continue 
            if int(self.dob[6:10]) < 1900 or int(self.dob[6:10]) > datetime.now().year:
                print("Date of Birth - Invalid year entered")
                continue 
            if int(self.dob[0:2]) > 30 and int(self.dob[3:5]) in [4,6,9,11]:
                print("Date of Birth - This month does not have this many days")
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
                print("Date of Birth - IT'S A LEAP YEAR - February only has 29 days")
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
                print("Date of Birth - IT'S NOT A LEAP YEAR - February only has 28 days")
                continue 
            break

        while True:
            self.address = input("Address:")
            if self.address == "":
                print("Address - Do not leave blank!")
                continue
            
            if not " " in self.address:
                print("Address - Must use space")
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
                print("Address - must be correctly entered")
                continue
            
            digit_in_address = False
            for character in self.address:
                if character.isdigit():
                    digit_in_address = True
                    break
            if digit_in_address == False:
                print("Address - must have a number")
                continue
            break
    
        while True:
            gp = input("Does the patient have a GP:(Y/N)").lower()
            if not self.validate_yes_no(gp):
                print("Enter either Y or N to proceed")
                continue
            if gp == "y":
                try:
                    self.gp_id = int(input("GP ID:"))
                    if not self.validate_login_digits(self.gp_id):
                        print("GP ID must be greater than 0")
                        continue
                except ValueError:
                    print("For GP ID use only numbers")
                    continue 

                try:
                    cursor.execute("""
                    SELECT * FROM gp
                    WHERE gp_id = ?
                    """,(self.gp_id,))

                except sqlite3.Error as e:
                    print("Database Error",e)
                    return

                row = cursor.fetchone()
                if not row:
                    print("No GP found")
                    continue 
                break
            
            else:
                self.gp_id = None 
                break

        try:
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
            print("Database Error", e)
            return
        
        print("Patient inserted sucessfully")
        row = cursor.lastrowid
        print(f"Patient ID:{row}")
        self.show_patient_details()
        return

    def display_all_patients(self):
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
                sick = Patient(
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5]
                    )
                print(row[0])
                sick.show_patient_details()
            return
    
    def search_patient(self):
        while True:
            try:
                patient_id = int(input("Patient ID:"))
                if not self.validate_login_digits(patient_id):
                    print("Patient ID must be greater than 0")
                    continue
                break 
            except ValueError:
                print("For Patient ID use only numbers")
                continue
        try:
            cursor.execute("""
            SELECT * FROM patient
            WHERE patient_id = ?
            """,(patient_id,))

        except sqlite3.Error as e:
            print("Database Error", e)
            return

        row = cursor.fetchone()
        if not row:
            print("Patient not found")
            return
        else:
            sick = Patient(
                row[1],
                row[2],
                row[3],
                row[4],
                row[5]
            )
            print(row[0])
            sick.show_patient_details()
            return
    
    def update_patient(self):
        while True:
            try:
                patient_id = int(input("Patient ID:"))
                if not self.validate_login_digits(patient_id):
                    print("Patient ID must be greater than 0")
                    continue
                break 
            except ValueError:
                print("For Patient ID use only numbers")
                continue
        try:
            cursor.execute("""
            SELECT * FROM patient
            WHERE patient_id = ?
            """,(patient_id,))

        except sqlite3.Error as e:
            print("Database Error", e)
            return

        row = cursor.fetchone()
        if not row:
            print("Patient not found")
            return
        else:
            sick = Patient(
                row[1],
                row[2],
                row[3],
                row[4],
                row[5]
            )
            print(row[0])
            sick.show_patient_details()

            while True:
                update = input("Do you want to update this patients details?(Y/N)").lower()
                if not self.validate_yes_no(update):
                    print("Enter either Y or N to proceed")
                    continue
                
                if update == "n":
                    print("Update aborted")
                    return
                else:
                    while True:
                        updated_first_name = input("First Name:")
                        if updated_first_name == "":
                            print("First Name - Do not leave name blank!")
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
                        updated_dob = input("Date of Birth(DD/MM/YYYY):")
                        if len(updated_dob) != 10:
                            print("Date of Birth - Invalid length")
                            continue 
                        if updated_dob[2] != "/" or updated_dob[5] != "/":
                            print("Date of Birth - Invalid character used")
                            continue
                    
                        no_digits = False
                        for user_input in updated_dob:
                            if user_input == "/":
                                continue 
                            if not user_input.isdigit():
                                no_digits = True
                                print("Date of Birth - has numbers and /")
                        
                        if no_digits == True:
                            print("Date of Birth - must be in this format(DD/MM/YYYY) ")
                            continue

                        if int(updated_dob[0:2]) < 1 or int(updated_dob[0:2]) > 31:
                            print("Date of Birth - Invalid day entered")
                            continue 

                        if int(updated_dob[3:5]) < 1 or int(updated_dob[3:5]) > 12:
                            print("Date of Birth - Invalid month entered")
                            continue

                        if int(updated_dob[6:10]) < 1900 or int(updated_dob[6:10]) > datetime.now().year:
                            print("Date of Birth - Invalid year entered")
                            continue

                        if int(updated_dob[0:2]) > 30 and int(updated_dob[3:5]) in [4,6,9,11]:
                            print("Date of Birth - This month does not have this many days")
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
                            print("Date of Birth - IT'S A LEAP YEAR - February only has 29 days")
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
                            print("Date of Birth - IT'S NOT A LEAP YEAR - February only has 28 days")
                            continue 
                        break
                    
                    while True:
                        updated_address = input("Address:")
                        if updated_address == "":
                            print("Address - Do not leave blank")
                            continue

                        if not " " in self.address:
                            print("Address - Must use space")
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
                            print("Address - must be correctly entered")
                            continue

                        house_number = False
                        for char in updated_address:
                            if char.isdigit():
                                house_number = True
                                break
                        if house_number == False:
                            print("Address - must have a number")
                            continue
                        break 
                    
                    while True:
                        gp = input("Does the patient have a GP?(y/n):").lower()
                        if not self.validate_yes_no(gp):
                            print("Does the patient have a GP:(Y/N")
                            continue
                        if gp == "y":
                            while True:
                                try:
                                    updated_gp_id = int(input("GP ID:"))
                                    if not self.validate_login_digits(updated_gp_id):
                                        print("GP ID must be greater than 0")
                                        continue 
                                
                                except ValueError:
                                    print("For GP ID use only numbers!")
                                    continue 

                                cursor.execute("""
                                SELECT * FROM gp
                                WHERE gp_id = ?
                                """,(updated_gp_id,))

                                row = cursor.fetchone()
                                if not row:
                                    print("No patient found")
                                    continue
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
                    print("Database Error",e)
                    return

                print("Patient updated sucessfully")
                return
    
    def delete_patient(self):
        while True:
            try:
                patient_id = int(input("Patient ID:"))
                if not self.validate_login_digits(patient_id):
                    print("GP ID must be greater than 0")
                    continue
                break 
            except ValueError:
                print("GP ID must be numbers")
                continue

        try:
            cursor.execute("""
            SELECT * FROM patient
            WHERE patient_id = ?
            """,(patient_id,))

        except sqlite3.Error as e:
            print("Database Error", e)
            return

        row = cursor.fetchone()
        if not row:
            print("Patient not found")
            return
        else:
            sick = Patient(
                row[1],
                row[2],
                row[3],
                row[4],
                row[5]
            )
            print(row[0])
            sick.show_patient_details()
            
            while True:
                delete = input("Do you want to delete this patient?(y/n):")
                if not self.validate_yes_no(delete):
                    print("Enter either Y or N to proceed")
                    continue
                if delete == "n":
                    print("Delete aborted")
                    return
                else:
                    try:
                        cursor.execute("""
                        DELETE FROM patient
                        WHERE patient_id = ?
                        """,(patient_id,))

                        conn.commit()

                    except sqlite3.Error as e:
                        print("Database Error", e)
                        return
                    
                    print("Patient sucessfully deleted")
                    return
                
test = Patient(
    "first_name",
    "surname",
    "dob",
    "address",
    "gp_id"
    )
test.create_patient()
        
        


            
                

                    


                


        
            
            

                