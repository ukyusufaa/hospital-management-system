import sqlite3
from datetime import datetime

conn = sqlite3.connect("hospital.db")

cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

class Appointment():

    def __init__(self, patient_id = None, appointment_date = None, 
                 appointment_time = None, consultant_id = None):
        
        self.patient_id = patient_id
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.consultant_id = consultant_id

    def show_details_appointment(self):
        print("-" * 30)
        print(f"Patient ID:{self.patient_id}")
        print(f"Appointment Date:{self.appointment_date}")
        print(f"Appointment Time:{self.appointment_time}")
        print(f"Consultant ID:{self.consultant_id}")
        print("-" * 30)

    def validate_user_login(self,number):
        if number < 1:
            return False
        return True

    def validate_yes_no(self,option):
        if option != 'y' and option != 'n':
            return False
        return True
    
    def create_appointment(self):
        while True:
            try:
                self.patient_id = int(input("Patient ID:"))
                if not self.validate_user_login(self.patient_id):
                    print("Patient ID must be greater than 0")
                    continue
                break

            except ValueError:
                print("For Patient ID use numbers")
                continue
        try:
            cursor.execute("""
            SELECT * FROM patient
            WHERE patient_id = ?
            """,(self.patient_id,))

        except sqlite3.Error as e:
            print("Database error:", e)
            return
            
        row = cursor.fetchone()
        if not row:
            print("Patient not found")
            return
            
        while True:
            try:
                self.consultant_id = int(input("Consultant ID:"))
                if not self.validate_user_login(self.consultant_id):
                    print("Consultant ID must be greater than 0")
                    continue
                break

            except ValueError:
                print("For Consultant ID use only numbers")
                continue
        try:
            cursor.execute("""
            SELECT * FROM consultant
            WHERE consultant_id = ?
            """,(self.consultant_id,))

        except sqlite3.Error as e:
            print("Database Error", e)
            return
                    
        row = cursor.fetchone()
        if not row:
            print("Consultant not found")
            return
    
        while True:
            self.appointment_date = (input("Appointment Date(MM/DD/YYYY):"))
            if self.appointment_date == "":
                print("Appointment Date - Do not leave blank")
                continue 
            if len(self.appointment_date) != 10:
                print("Appointment Date - Invalid length")
                continue
            if self.appointment_date[2] != "/" or self.appointment_date[5] != "/":
                print("Appointment Date - Invalid character entered")
                continue

            not_number = False
            for value in self.appointment_date:
                if value == "/":
                    continue 
                if not value.isdigit():
                    not_number = True
                    continue

            if not_number == True:
                print("Appointment Date - Use this format only (MM/DD/YYYY)")
                continue

            if(int(self.appointment_date[0:2]) < 1
                or int(self.appointment_date[0:2])) > 31:
                print("Appointment Date - Invalid day")
                continue
            if(int(self.appointment_date[3:5]) < 1 
               or int(self.appointment_date[3:5])) > 12:
                print("Appointment Date - Invalid month")
                continue 
            if(int(self.appointment_date[6:10]) < 1900 
            or int(self.appointment_date[6:10])) > datetime.now().year:
                print("Appointment Date - Invalid year")
                continue

            if(int(self.appointment_date[0:2]) > 30 
               and int(self.appointment_date[3:5])) in [4,6,9,11]:
                print("Appointment Day- Invalid day entered for this month")
                continue

            if(
                int(self.appointment_date[0:2]) > 29 
                and int(self.appointment_date[3:5]) == 2
                and
                (
                    int(self.appointment_date[6:10]) % 400 == 0
                    or
                    (
                        int(self.appointment_date[6:10]) % 4 == 0
                        and
                        int(self.appointment_date[6:10]) % 100 != 0
                    )
                )
            ):
                print("Appointment Date - LEAP YEAR - Invalid day entered for February")
                continue 

            if(
                int(self.appointment_date[0:2]) > 28
                and int(self.appointment_date[3:5]) == 2
                and
                (
                    int(self.appointment_date[6:10]) % 400 != 0
                    and
                    (
                        int(self.appointment_date[6:10]) % 4 != 0
                        or 
                        int(self.appointment_date[6:10]) % 100 == 0
                    )
                )
            ):
                print("Appointment Date - NOT A LEAP YEAR - Invalid day entered for February")
                continue

            appointment_date = datetime.strptime(self.appointment_date,"%d/%m/%Y")
            if appointment_date.date() <= datetime.now().date():
                print("Appointment Date - must be TOMMORROW or LATER & only the CURRENT YEAR.")
                continue
            break

        while True:
            self.appointment_time = input("Appointment Time(HH:MM):")
            if len(self.appointment_time) != 5:
                print("Appointment Time - Character length invalid for time")
                continue
            if(not self.appointment_time[0:2].isdigit() 
            or not self.appointment_time[3:5].isdigit()):
                print("Appointment Time - must be HH:MM (e.g. 01:10)")
                continue
            if self.appointment_time[2] != ":":
                print("Appointment Time - must use ':' between hours and minutes ")
                continue
            if(int(self.appointment_time[0:2]) < 8 
            or int(self.appointment_time[0:2]) > 18):
                print("Appointment Time - Hour used must not be out of appointment hours")
                continue
            minutes = int(self.appointment_time[3:5])
            if(
                minutes < 0 or minutes >= 60
                    or
                    (
                        minutes != 00
                        and minutes != 15
                        and minutes != 30
                        and minutes != 45
                    )
                ):
                    print("Appointment Time - Minutes used must be set minutes")
                    continue
            break

        try:
            cursor.execute("""
            SELECT * FROM appointment
            WHERE consultant_id = ? 
                AND appointment_date = ? 
                AND appointment_time = ?
            
            """,(self.consultant_id,
                self.appointment_date,
                self.appointment_time))

        except sqlite3.Error as e:
            print("Database Error", e)
            return

        row = cursor.fetchone()
        if row:
            print("Appointment unavailable - Please choose another booking")
        else:
            print("Appointment available - Please book")

            try:
                cursor.execute("""
                INSERT INTO appointment(
                        patient_id,
                        consultant_id,
                        appointment_date,
                        appointment_time
                        )
                VALUES(?,?,?,?)
                """,(self.patient_id,
                    self.consultant_id,
                    self.appointment_date,
                    self.appointment_time))

                conn.commit()

            except sqlite3.Error as e:
                print("Database Error", e)
                return

            print("Appointment successfully booked")
            row = cursor.lastrowid
            print(f"Appointment ID:{row}")
            self.show_details_appointment

    def display_all_appointments(self):
        try:
            cursor.execute("SELECT * FROM appointment")

        except sqlite3.Error as e:
            print("Database Error", e)
            return

        rows = cursor.fetchall()
        if not rows:
            print("No appointments found")
            return
        else:
            for row in rows:
                patient_appointment = Appointment(
                    row[1],
                    row[2],
                    row[3],
                    row[4]
                    )
                print(f"Appointment ID:{row[0]}")
                patient_appointment.show_details_appointment()

    def search_appointment(self):
        while True:
            try:
                appointment_id = int(input("Appointment ID:"))
                if not self.validate_user_login(appointment_id):
                    print("Appointment ID must be greater than 0")
                    continue
                break
        
            except ValueError:
                print("For Appointment ID use numbers")
                continue

        try:
            cursor.execute("""
            SELECT * FROM appointment
            WHERE appointment_id = ?
            """,(appointment_id,))

        except sqlite3.Error as e:
            print("Database Error", e)
            return

        row = cursor.fetchone()
        if not row:
            print("Appointment not found")
            return
        else:
            patient_appointment = Appointment(
                row[1],
                row[2],
                row[3],
                row[4]
                )
            print(f"Appointment ID:{row[0]}")
            patient_appointment.show_details_appointment()
            return

    def update_appointment(self):
        while True:
            try:
                appointment_id = int(input("Appointment ID:"))
                if not self.validate_user_login(appointment_id):
                    print("Appointment ID must be greater than 0")
                    continue
                break
        
            except ValueError:
                print("For Appointment ID use numbers")
                continue

        try:
            cursor.execute("""
            SELECT * FROM appointment
            WHERE appointment_id = ?
            """,(appointment_id,))

        except sqlite3.Error as e:
            print("Database Error", e)
            return

        row = cursor.fetchone()
        if not row:
            print("Appointment not found")
            return
        else:
            patient_appointment = Appointment(
                row[1],
                row[2],
                row[3],
                row[4]
                )
            print(f"Appointment ID:{row[0]}")
            patient_appointment.show_details_appointment()

            while True:
                update = input("Do you want to update appointment?(Y/N)").lower()
                if not self.validate_yes_no(update):
                    print("Enter either Y or N to proceed")
                    continue
                if update == "n":
                    print("Appointment - Update aborted")
                    break 
                else:
                    while True:
                        try:
                            updated_patient_id = int(input("Patient ID:"))
                            if not self.validate_user_login(updated_patient_id):
                                print("Patient ID must be greater than 0")
                                continue
                            break 
                        except ValueError:
                            print("Paient ID must be numbers")
                            continue

                    while True:
                        try:
                            updated_consultant_id = int(input("Consultant ID:"))
                            if not self.validate_user_login(updated_consultant_id):
                                print("Consultant ID must be greater than 0")
                                continue
                            break 
                        except ValueError:
                            print("Consultant ID must be numbers")
                            continue

                    while True:
                        updated_appointment_date = input("Date(DD/MM/YYYY):")
                        not_number = False
                        for user_input in updated_appointment_date:
                            if user_input == "/":
                                continue
                            if not user_input.isdigit():
                                not_number = True
                                continue
                        if not_number == True:
                            print("Appointment Date - Use this format only(DD/MM/YYYY)")
                            continue
                        if updated_appointment_date == "":
                            print("Appointment Date - Do not leave blank")
                            continue
                        if len(updated_appointment_date) != 10:
                            print("Appointment Date - Invalid length")
                            continue
                        if(updated_appointment_date[2] != "/" 
                           or updated_appointment_date[5] != "/"):
                            print("Appointment Date - Invalid character used")
                            continue
                        if(int(updated_appointment_date[0:2]) < 1
                           or int(updated_appointment_date[0:2]) > 31):
                            print("Appointment Date - Invalid day")
                            continue
                        if(int(updated_appointment_date[3:5]) < 1
                            or int(updated_appointment_date[3:5]) > 12):
                            print("Appointment Date - Invalid month")
                            continue
                        if(int(updated_appointment_date[6:10]) < 1900
                            or int(updated_appointment_date[6:10]) > datetime.now().year):
                            print("Appointment Date - Invalid year")
                            continue
                  
                        if(
                            int(updated_appointment_date[0:2]) > 29 
                            and int(updated_appointment_date[3:5]) == 2
                            and
                            (
                                int(updated_appointment_date[6:10]) % 400 == 0
                                or
                                (
                                    int(updated_appointment_date[6:10]) % 4 == 0
                                    and
                                    int(updated_appointment_date[6:10]) % 100 != 0
                                )
                            )
                        ):
                            print("Appointment Date - LEAP YEAR - Invalid day used "
                            "for February")
                            continue 
            
                        if(
                            int(updated_appointment_date[0:2]) > 28
                            and int(updated_appointment_date[3:5]) == 2
                            and
                            (
                                int(updated_appointment_date[6:10]) % 400 != 0
                                and
                                (
                                    int(updated_appointment_date[6:10]) % 4 != 0
                                    or 
                                    int(updated_appointment_date[6:10]) % 100 == 0
                                )
                            )
                        ):
                            print("Appointment Date - NOT A LEAP YEAR - Invalid for day" 
                            "used for February")
                            continue

                        appointment_date = datetime.strptime(
                            patient_appointment.appointment_date,"%d/%m/%Y")
                        if appointment_date.date() <= datetime.now().date():
                            print("Appointment date must be tommorrow or later.")
                            continue 
                        break
                

                    while True:
                        updated_appointment_time = input("Appointment Time(HR:MM):")
                        if updated_appointment_time == "":
                            print("Do not leave blank!")
                            continue
                        if len(updated_appointment_time) != 5:
                           print("Invalid input - Time digit length incorrect")
                           continue
                        if(not updated_appointment_time[0:2].isdigit() 
                        or not updated_appointment_time[3:5].isdigit()):
                           print("Invalid input - Enter time using correct format (HR:MM)")
                           continue
                        if updated_appointment_time[2] != ":":
                           print("Invalid input - Wrong separator used between hour and mins")
                           continue
                        if(int(updated_appointment_time[0:2]) < 8 
                        or int(updated_appointment_time[0:2]) > 18):
                           print("Invalid input -Incorrect appointment hour")
                           continue
                        minutes = int(updated_appointment_time[3:5])
                        if(
                           minutes < 0 or minutes >= 60
                               or
                               (
                                   minutes != 00
                                   and minutes != 15
                                   and minutes != 30
                                   and minutes != 45
                               )
                           ):
                               print("Invalid input - Incorrect appointment minutes")
                               continue
                        break 
                
                patient_appointment.patient_id = updated_patient_id
                patient_appointment.consultant_id = updated_consultant_id
                patient_appointment.appointment_date = updated_appointment_date
                patient_appointment.appointment_time = updated_appointment_time

                try:
                    cursor.execute("""
                    SELECT * FROM appointment
                    WHERE consultant_id = ?
                    AND appointment_date = ?
                    AND appointment_time = ?
                    """,(patient_appointment.consultant_id,
                        patient_appointment.appointment_date,
                        patient_appointment.appointment_time))

                except sqlite3.Error as e:
                    print("Database Error", e)
                    return

                row = cursor.fetchone()
                if row:
                    print("Appointment unavailable - choose another appointment time/date")
                else:
                    try:
                        cursor.execute("""
                        UPDATE appointment
                        SET patient_id = ?,
                        consultant_id = ?,
                        appointment_date = ?,
                        appointment_time = ?
                        """,(patient_appointment.patient_id,
                         patient_appointment.consultant_id,
                         patient_appointment.appointment_date,
                         patient_appointment.appointment_time))

                        conn.commit()

                    except sqlite3.Error as e:
                        print ("Database Error", e)
                        return

                    print("Appointment successfully updated")

    def delete_appointment(self):
        while True:
            try:
                appointment_id = int(input("Appointment ID:"))
                if not self.validate_user_login(appointment_id):
                    print("Appointment ID must be greater than 0")
                    continue
                break
            except ValueError:
                print("Appointment ID must be numbers")
        try:
            cursor.execute("""
            SELECT * FROM appointment
            WHERE appointment_id = ?
            """,(appointment_id,))

        except sqlite3.Error as e:
            print("Database Error", e)
            return

        row = cursor.fetchone()
        if not row:
            print("No appointment found")
            return 
        else:
            patient_appointment = Appointment(
                row[1],
                row[2],
                row[3],
                row[4]
                )
            print(row[0])
            patient_appointment.show_details_appointment()

            while True:
                delete = input("Are you sure you want to delete this appointment(Y/N)?").lower()
                if not self.validate_yes_no(delete):
                    print("Enter either Y or N to proceed")
                    continue
                if delete == 'n':
                    print("Appointment - delete process aborted")
                    break 
                else:
                    try:
                        cursor.execute("""
                        DELETE FROM appointment
                        WHERE appointment_id = ?
                        """,(appointment_id,))

                        conn.commit()

                    except sqlite3.Error as e:
                        print("Database Error", e)
                        return
                    
                print("Appointment deleted sucessfully")
                return

    def appointment_prescription_join(self):
        try:
            cursor.execute("""
                SELECT *
                FROM appointment
                INNER JOIN prescription
                ON appointment.appointment_id =
            prescription.appointment_id
            """)

        except sqlite3.Error as e:
            print("Database Error", e)
            return

        rows = cursor.fetchall()

        for row in rows:
                print(row)
        








        
            



            



        



    
        