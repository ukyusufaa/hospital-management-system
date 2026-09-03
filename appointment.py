# Import SQLite to work with the database.
import sqlite3
import calendar

# Import datetime for appointment date validation.
from datetime import datetime

# Import the shared database connection and cursor from database.py module.
from database import conn, cursor

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

    # Validate the appointment ID is a positive number.
    def validate_login_id(self,number):
        return number >= 1

    # Validate the user's confirmation choice before performing deletion.
    def validate_yes_no(self,option):
        return option in ("y", "n")
    
    def create_appointment(self):
        # Validate the patient ID entered by the user.
        while True:
            try:
                self.patient_id = int(input("Enter the Patient's ID:"))
                if not self.validate_login_id(self.patient_id):
                    print("Please enter a valid patient ID.")
                    continue
                break

            except ValueError:
                print("Please enter the patient ID " \
                        "using numbers only.")
                continue
        try:
        # Find the patient associated with the appointment
            cursor.execute("""
                SELECT * FROM patient
                WHERE patient_id = ?
            """,(self.patient_id,))

        except sqlite3.Error as e:
            print("Unable to find the patient record. " \
                    "Please try again.", e)
            return

        # Retrieve the patient record using fetchone()
        patient_record = cursor.fetchone()

        if not patient_record:
            print("We couldn't find a patient " \
                    "with that ID.")
            return
            
        while True:
            try:
        # Validate the consultant ID entered by the user.
                self.consultant_id = int(input("Enter the Consultant's ID:"))
                if not self.validate_login_id(self.consultant_id):
                    print("Please enter a valid consultant ID.")
                    continue
                break

            except ValueError:
                print("Please enter the consultant ID." \
                        "using numbers only.")
                continue
        try:
        # Find the consultant ID associated with the appointment.
            cursor.execute("""
                SELECT * FROM consultant
                WHERE consultant_id = ?
            """,(self.consultant_id,))

        except sqlite3.Error as e:
            print("Unable to find the consultant record. " \
                    "Please try again.", e)
            return
        # Retrieve the consultant record using fetchone().          
        consultant_record = cursor.fetchone()

        if not consultant_record:
            print("We couldn't find a consultant." \
                    "with that ID.")
            return
    
        while True:
        # Validate the appointment date entered by the user.
            self.appointment_date = (input("Enter the " \
                "appointment date(DD/MM/YYYY):"))
            if self.appointment_date == "":
                print("Please enter an appointment date.")
                continue 
            if len(self.appointment_date) != 10:
                print("The appointment date must be in the " \
                        "format DD/MM/YYYY.")
                continue

            if self.appointment_date[2] != "/" or self.appointment_date[5] != "/":
                print("Please use between the day, " \
                        "month and year.")
                continue

            not_number = False
            for value in self.appointment_date:
                if value == "/":
                    continue 
                if not value.isdigit():
                    not_number = True
                    break 

            if not_number:
                print("Please enter the date using the " \
                        "format DD/MM/YYYY.")
                continue

            day = int(self.appointment_date[0:2])
            month = int(self.appointment_date[3:5])
            year = int(self.appointment_date[6:10])

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

            appointment_date = datetime.strptime(self.appointment_date,"%d/%m/%Y")
            if appointment_date.date() <= datetime.now().date():
                print("Please choose a date from tommorrow onwards.")
                continue
            break

        while True:
        # Validate the appointment time entered by the user.
            self.appointment_time = input("Enter the appointment time (HH:MM):")
            if len(self.appointment_time) != 5:
                print("Please enter the time using the format HH:MM.")
                continue
            if(not self.appointment_time[0:2].isdigit() 
            or not self.appointment_time[3:5].isdigit()):
                print("Please enter the time using the format " \
                        "HH:MM, for example 08:15.")
                continue
            if self.appointment_time[2] != ":":
                print("Please use : between hours and minutes.")
                continue

            hour = int(self.appointment_time[0:2])
            minutes = int(self.appointment_time[3:5])

            if hour < 8 or hour > 18:
                print("Appointments are available between " \
                        "08:00 and 18:00.")
                continue

            if minutes not in (0, 15, 30, 45):
                print("Please choose an appointment time " \
                        "ending in 00, 15, 30 or 45 minutes only.")
                continue
        
             # Check whether the consultant is already booked at this date and time.
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
                    print("Unable to check appointment " \
                        "availability. Please try again.", e)
                    return
        
            # Retrieve any matching appointment.
            matching_appointment1 = cursor.fetchone()

            if matching_appointment1:
                print("The consultant is already booked "
                        "at this date or time.")
                return

            # Check whether the patient is already booked
            try:
                cursor.execute("""
                    SELECT * FROM appointment
                    WHERE patient_id = ?
                    AND appointment_date = ?
                    AND appointment_time = ?
                """,(self.patient_id,
                    self.appointment_date,
                    self.appointment_time))

            except sqlite3.Error as e:
                print("Unable to check appointment " \
                        "availabilty. Please try again.")
                return

            matching_appointment2 = cursor.fetchone()

            if matching_appointment2:
                print("Cannot book this appointment. " \
                    "The patient already has an " \
                    "appointment at this time.")  
                return
            break    
        
        print("The appointment slot is available.")

        try:
        # Insert the new appointment into the database.
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
        # Save the new appointment into the database
            conn.commit()

        except sqlite3.Error as e:
            print("Unable to book the " \
                    "appointment. Please try again.", e)
            return

        print("Appointment booked successfully.")

        # Retrieve the ID automatically generated for the new appointment.
        appointment_id = cursor.lastrowid
        print(f"Appointment ID:{appointment_id}")

        # Display the newly created appointment
        self.show_details_appointment()

    def display_all_appointments(self):
        try:
        # Retrieve all appointments from the database.
            cursor.execute("SELECT * FROM appointment")

        except sqlite3.Error as e:
            print("Unable to retrieve appointments." \
                    "Please try again.", e)
            return

        # Retrieve all appointments records returned by the query.
        appointment_records = cursor.fetchall()

        if not appointment_records:
            print("There are currently no appointments " \
                    "to display.")
            return
        
        # Create and display an Appointment object for each database record.
        for appointment_record in appointment_records:
            appointment = Appointment(
                appointment_record[1],
                appointment_record[2],
                appointment_record[3],
                appointment_record[4]
                )
            print(f"Appointment ID:{appointment_record[0]}")
            appointment.show_details_appointment()

    def search_appointment(self):
        # Validate the appointment ID entered by the user.
        while True:
            try:
                appointment_id = int(input("Appointment ID:"))
                if not self.validate_login_id(appointment_id):
                    print("Please enter a valid appointment ID.")
                    continue
                break
        
            except ValueError:
                print("Please enter the appointment ID using"
                        "numbers only.")
                continue

        try:
        # Search for the appointment ID using its primary key.
            cursor.execute("""
                SELECT * FROM appointment
                WHERE appointment_id = ?
            """,(appointment_id,))

        except sqlite3.Error as e:
            print("Unable to search for the appointment. " \
                    "Please try again.", e)
            return
        
        # Retrieve the matching appointment record.
        appointment_record = cursor.fetchone()

        if not appointment_record:
            print("We couldn't find an appointment " \
                    "with that ID.")
            return
        
        self.patient_id = appointment_record[1]
        self.consultant_id = appointment_record[2]
        self.appointment_date = appointment_record[3]
        self.appointment_time = appointment_record[4]

        print(f"Appointment ID:{appointment_record[0]}")
        self.show_details_appointment()
        return

    def update_appointment(self):
        # Validate the appointment ID entered by the user.
        while True:
            try:
                appointment_id = int(input("Enter the appointment ID:"))
                if not self.validate_login_id(appointment_id):
                    print("Please enter a valid appointment ID.")
                    continue
                break
        
            except ValueError:
                print("Please enter the appointment ID " \
                        "using numbers only.")
                continue

        try:
        # Find the appointment that will be updated.
            cursor.execute("""
                SELECT * FROM appointment
                WHERE appointment_id = ?
            """,(appointment_id,))

        except sqlite3.Error as e:
            print("Unable to retrieve the appointment. " \
                    "Please try again.", e)
            return

        # Retrieve the existing appointment record.
        appointment_record = cursor.fetchone()

        if not appointment_record:
            print("We couldn't find an appointment " \
                    "with that ID.")
            return
        
        self.patient_id = appointment_record[1]
        self.appointment_date = appointment_record[2]
        self.appointment_time = appointment_record[3]
        self.consultant_id = appointment_record[4]

        print(f"Appointment ID:{appointment_record[0]}")
        self.show_details_appointment()

        while True:
         # Confirm whether the user wants to update the appointment.
            update = input("Update "
                    "this appointment? (Y/N): ").lower()
            
            if not self.validate_yes_no(update):
                print("Please enter Y/y for yes " \
                        "or N/n for no.")
                continue

            if update == "n":
                print("Appointment update cancelled.")
                return
            break 

        # Validate the new patient ID
        while True:
            try:
                updated_patient_id = int(input("Enter the Patient's ID:"))

                if not self.validate_login_id(updated_patient_id):
                    print("Please enter a valid patient ID.")
                    continue
                break

            except ValueError:
                print("Please enter the patient ID " \
                        "using numbers only.")
                continue

        # Validate the new consultant ID.
        while True:
            try:
                updated_consultant_id = int(input("Enter the " 
                    "consultant's ID:"))
                    
                if not self.validate_login_id(updated_consultant_id):
                    print("Please enter a valid " \
                            "consultant ID.")
                    continue
                break

            except ValueError:
                print("Please enter the consultant ID " \
                        "using numbers only.")
                continue

        while True:
        # Validate the appointment date entered by the user.
            updated_appointment_date = (input("Enter the " \
                "appointment date(DD/MM/YYYY):"))

            if updated_appointment_date == "":
                print("Please enter an appointment date.")
                continue

            if len(updated_appointment_date) != 10:
                print("The appointment date must be in the " \
                        "format DD/MM/YYYY.")
                continue

            if updated_appointment_date[2] != "/" or updated_appointment_date[5] != "/":
                print("Please use between the day, " \
                        "month and year.")
                continue
    
            not_number = False

            for value in updated_appointment_date:
                if value == "/":
                    continue 
                if not value.isdigit():
                        not_number = True
                        break 
    
            if not_number:
                print("Please enter the date using the " \
                        "format DD/MM/YYYY.")
                continue
    
            day = int(updated_appointment_date[0:2])
            month = int(updated_appointment_date[3:5])
            year = int(updated_appointment_date[6:10])
    
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
    
            appointment_date = datetime.strptime(updated_appointment_date,"%d/%m/%Y")
            if appointment_date.date() <= datetime.now().date():
                print("Please choose a date from tommorrow onwards.")
                continue
            break
    
        while True:
            # Validate the appointment time entered by the user.
            updated_appointment_time = input("Enter the appointment time (HH:MM):")

            if len(updated_appointment_time) != 5:
                print("Please enter the time using the format HH:MM.")
                continue

            if(not updated_appointment_time[0:2].isdigit() 
                or not updated_appointment_time[3:5].isdigit()):
                print("Please enter the time using the format " \
                        "HH:MM, for example 08:15.")
                continue

            if updated_appointment_time[2] != ":":
                print("Please use : between hours and minutes.")
                continue
    
            hour = int(updated_appointment_time[0:2])
            minutes = int(updated_appointment_time[3:5])
    
            if hour < 8 or hour > 18:
                print("Appointments are available between " \
                        "08:00 and 18:00.")
    
            if minutes not in (0, 15, 30, 45):
                print("Please choose an appointment time " \
                        "ending in 00, 15, 30 or 45 minutes only.")
                continue

            # Check that the new consultant, date and time are available.
            try:
                cursor.execute("""
                    SELECT * FROM appointment
                    WHERE consultant_id = ?
                    AND appointment_date = ?
                    AND appointment_time = ?
                    AND appointment_id != ?
                """,(updated_consultant_id,
                    updated_appointment_date,
                    updated_appointment_time,
                    appointment_id))

            except sqlite3.Error as e:
                print("Unable to check appointment " \
                    "availability. Please try again.", e)
                return

            matching_appointment1 = cursor.fetchone()

            if matching_appointment1:
                print("The consultant is already " \
                        "booked at this time or date.")
                return

            # Check whether the patient is already booked
            try:
                cursor.execute("""
                    SELECT * FROM appointment
                    WHERE patient_id = ?
                    AND appointment_date = ?
                    AND appointment_time = ?
                    AND appointment_id != ?
                """,(updated_patient_id,
                    updated_appointment_date,
                    updated_appointment_time,
                    appointment_id))

            except sqlite3.Error as e:
                print("Unable to check appointment " \
                        "availabilty. Please try again.",e)
                return

            matching_appointment2 = cursor.fetchone()

            if matching_appointment2:
                print("Cannot book this appointment. " \
                        "The patient already has an " \
                        "appointment at this time.")  
                return
            break 
             
        print("The appointment slot is available.")  
        try:
        # Update the appointment record in the database.
            cursor.execute("""
                UPDATE appointment
                SET patient_id = ?,
                    appointment_date = ?,
                    appointment_time = ?,
                    consultant_id = ?
                WHERE appointment_id = ?
                """,(updated_patient_id,
                    updated_appointment_date,
                    updated_appointment_time,
                    updated_consultant_id,
                    appointment_id))
                        
        # Save the updated appointment to the database
            conn.commit()

        except sqlite3.Error as e:
            print ("Unable to update the " \
                    "appointment. Please try again.", e)
            return

        print("Appointment updated successfully.")

    def delete_appointment(self):
        # Validate the appointment ID entered by the user.
        while True:
            try:
                appointment_id = int(input("Enter the appointment ID:"))

                if not self.validate_login_id(appointment_id):
                    print("Please enter a valid appointment ID.")
                    continue
                break

            except ValueError:
                print("Please enter the appointment ID " \
                        "using numbers only.")
        try:
        # Find the appointment that will be deleted.
            cursor.execute("""
                SELECT * FROM appointment
                WHERE appointment_id = ?
            """,(appointment_id,))

        except sqlite3.Error as e:
            print("Unable to retrieve the " \
                    "appointment. Please try again.", e)
            return

        # Retrieve the appointment record before deletion
        appointment_record = cursor.fetchone()

        if not appointment_record:
            print("We couldn't find " \
            "an appointment with that ID.")
            return 
        
        self.patient_id = appointment_record[1]
        self.consultant_id = appointment_record[2]
        self.appointment_date = appointment_record[3]
        self.appointment_time = appointment_record[4]

        print(f"Appointment ID: {appointment_record[0]}")
        self.show_details_appointment()

        while True:
        # Confirm that the user wants to delete the appointment.
            delete = input("Delete "
                "this appointment? (Y/N): ").lower()
            
            if not self.validate_yes_no(delete):
                print("Enter Y/y for yes " \
                        "or N/n for no.")
                continue

            if delete == 'n':
                print("Appointment deletion cancelled.")
                return
            break

        # Delete the appointment from the database         
        try:
            cursor.execute("""
                DELETE FROM appointment
                WHERE appointment_id = ?
            """,(appointment_id,))

        # Save the deletion to the database.
            conn.commit()

        except sqlite3.Error as e:
            print("Unable to delete the " \
                    "appointment. Please try again.", e)
            return
                    
        print("Appointment deleted successfully.")
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
        








        
            



            



        



    
        