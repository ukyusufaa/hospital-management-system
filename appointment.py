# Import SQLite to work with the database.
import sqlite3

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

    def validate_user_login(self,number):
        if number < 1:
            return False
        return True

    def validate_yes_no(self,option):
        if option != 'y' and option != 'n':
            return False
        return True
    
    def create_appointment(self):
        # Validate the patient ID entered by the user.
        while True:
            try:
                self.patient_id = int(input("Enter the Patient's ID:"))
                if not self.validate_user_login(self.patient_id):
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
        row = cursor.fetchone()
        if not row:
            print("We couldn't find a patient " \
            "with that ID.")
            return
            
        while True:
            try:
        # Validate the consultant ID entered by the user.
                self.consultant_id = int(input("Enter the Consultant's ID:"))
                if not self.validate_user_login(self.consultant_id):
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
        row = cursor.fetchone()
        if not row:
            print("We couldn't find a consultant." \
            "with that ID.")
            return
    
        while True:
        # Validate the appointment date entered by the user.
            self.appointment_date = (input("Enter the " \
            "appointment date(MM/DD/YYYY):"))
            if self.appointment_date == "":
                print("Please enter an appointment date.")
                continue 
            if len(self.appointment_date) != 10:
                print("The appointment date must be in the " \
                "format DD/MM/YYYY.")
                continue
            if self.appointment_date[2] != "/" or self.appointment_date[5] != "/":
                print("Please use / between the day, " \
                "month and year.")
                continue

            not_number = False
            for value in self.appointment_date:
                if value == "/":
                    continue 
                if not value.isdigit():
                    not_number = True
                    continue

            if not_number == True:
                print("Please enter the date using the " \
                "format DD/MM/YYYY.")
                continue

            if(int(self.appointment_date[0:2]) < 1
                or int(self.appointment_date[0:2])) > 31:
                print("Please enter a valid day.")
                continue
            if(int(self.appointment_date[3:5]) < 1 
               or int(self.appointment_date[3:5])) > 12:
                print("Please enter a valid month.")
                continue 
            if(int(self.appointment_date[6:10]) < 1900 
            or int(self.appointment_date[6:10])) > datetime.now().year:
                print("Please enter a valid year.")
                continue

            if(int(self.appointment_date[0:2]) > 30 
               and int(self.appointment_date[3:5])) in [4,6,9,11]:
                print("That month does not have that many days. " \
                "Please enter valid date.")
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
                print("February has only 29 days in a leap year. " \
                "Please enter a valid date.")
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
                print("February only has 28 days this year. " \
                "Please enter a valid date.")
                continue

            appointment_date = datetime.strptime(self.appointment_date,"%d/%m/%Y")
            if appointment_date.date() <= datetime.now().date():
                print("Please choose a date from tommorrow onwards " \
                "within the current year.")
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
            if(int(self.appointment_time[0:2]) < 8 
            or int(self.appointment_time[0:2]) > 18):
                print("Appointments are available between " \
                "08:00 and 18:00.")
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
                    print("Please choose an appointment time ending " \
                    "in 00, 15, 30 or 45 minutes.")
                    continue
            break
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
        row = cursor.fetchone()
        if row:
            print("That appointment slot is already booked. " \
            "Please choose another date or time.")
        else:
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
            row = cursor.lastrowid
            print(f"Appointment ID:{row}")
        # Display the newly created appointment
            self.show_details_appointment

    def display_all_appointments(self):
        try:
        # Retrieve all appointments from the database.
            cursor.execute("SELECT * FROM appointment")

        except sqlite3.Error as e:
            print("Unable to retrieve appointments." \
            "Please try again.", e)
            return

        # Retrieve all appointments records returned by the query.
        rows = cursor.fetchall()
        if not rows:
            print("There are currently no appointments " \
            "to display.")
            return
        else:
        # Create and display an Appointment object for each database record.
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
        # Validate the appointment ID entered by the user.
        while True:
            try:
                appointment_id = int(input("Appointment ID:"))
                if not self.validate_user_login(appointment_id):
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
        row = cursor.fetchone()
        if not row:
            print("We couldn't find an appointment " \
            "with that ID.")
            return
        else:
            self.patient_id = row[1]
            self.consultant_id = row[2]
            self.appointment_date = row[3]
            self.appointment_time = row[4]
            print(f"Appointment ID:{row[0]}")
            self.show_details_appointment()
            return

    def update_appointment(self):
        # Validate the appointment ID entered by the user.
        while True:
            try:
                appointment_id = int(input("Enter the appointment ID:"))
                if not self.validate_user_login(appointment_id):
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
        row = cursor.fetchone()
        if not row:
            print("We couldn't find an appointment " \
            "with that ID.")
            return
        else:
            self.patient_id = row[1]
            self.consultant_id = row[2]
            self.appointment_date = row[3]
            self.appointment_time = row[4]

            print(f"Appointment ID:{row[0]}")
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

                else:
        # Validate the new patient ID
                    while True:
                        try:
                            updated_patient_id = int(input
                                                     ("Enter the " 
                                                      "Patient's ID:")
                                                     )
                            if not self.validate_user_login(updated_patient_id):
                                print("Please enter a valid " \
                                "patient ID.")
                                continue
                            break 
                        except ValueError:
                            print("Please enter the patient ID " \
                            "using numbers only.")
                            continue

        # Validate the new consultant ID.
                    while True:
                        try:
                            updated_consultant_id = int(
                                input("Enter the " 
                                      "consultant's ID:")
                                )
                            if not self.validate_user_login(updated_consultant_id):
                                print("Please enter a valid " \
                                "consultant ID.")
                                continue
                            break 
                        except ValueError:
                            print("Please enter the consultant ID " \
                            "using numbers only.")
                            continue

        # Validate the new appointment date.
                    while True:
                        updated_appointment_date = input(
                            "Enter the new "
                            "appointment date(DD/MM/YYYY):"
                            )
                        not_number = False
                        for user_input in updated_appointment_date:
                            if user_input == "/":
                                continue
                            if not user_input.isdigit():
                                not_number = True
                                continue
                        if not_number == True:
                            print("Please enter the appointment " \
                            "date using the format (DD/MM/YYYY).")
                            continue
                        if updated_appointment_date == "":
                            print("Please enter an " \
                            "appointment date.")
                            continue
                        if len(updated_appointment_date) != 10:
                            print("The appointment date must be " \
                            "in the format DD/MM/YYYY.")
                            continue
                        if(updated_appointment_date[2] != "/" 
                           or updated_appointment_date[5] != "/"):
                            print("Please use / between the day, " \
                            "month and year.")
                            continue
                        if(int(updated_appointment_date[0:2]) < 1
                           or int(updated_appointment_date[0:2]) > 31):
                            print("Please enter a valid day.")
                            continue
                        if(int(updated_appointment_date[3:5]) < 1
                            or int(updated_appointment_date[3:5]) > 12):
                            print("Please enter a valid month.")
                            continue
                        if(int(updated_appointment_date[6:10]) < 1900
                            or int(updated_appointment_date[6:10]) > datetime.now().year):
                            print("Please enter a valid year.")
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
                            print("February only has 29 days in a leap year. " \
                            "Please enter a valid date.")
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
                            print("February has only 28 days this year. " \
                            "Please enter a valid date.")
                            continue

                        appointment_date = datetime.strptime(
                            self.appointment_date,"%d/%m/%Y")
                        if appointment_date.date() <= datetime.now().date():
                            print("Please choose a date from tommorrow. " \
                            "onwards.")
                            continue 
                        break

        # Validate the new appointment time.
                    while True:
                        updated_appointment_time = input("Enter the new "
                                                         "appointment " 
                                                         "time(HR:MM).:"
                                                         )
                        if updated_appointment_time == "":
                            print("Please enter an appointment time.")
                            continue
                        if len(updated_appointment_time) != 5:
                           print("Please enter the time " /
                                  "using the format HH:MM.")
                           continue
                        if(not updated_appointment_time[0:2].isdigit() 
                        or not updated_appointment_time[3:5].isdigit()):
                           print("Please enter the time " \
                           "using the format HH:MM.")
                           continue
                        if updated_appointment_time[2] != ":":
                           print("Please use : between hours " \
                           "and minutes.")
                           continue
                        if(int(updated_appointment_time[0:2]) < 8 
                        or int(updated_appointment_time[0:2]) > 18):
                           print("Appointments are available " \
                           "between 08:00 and 18:00.")
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
                               print("Please choose an appointment " \
                               "time ending in 00, 15, 30, 45 " \
                               "minutes.")
                               continue
                        break 
    
                self.patient_id = updated_patient_id
                self.consultant_id = updated_consultant_id
                self.appointment_date = updated_appointment_date
                self.appointment_time = updated_appointment_time

                try:
        # Check that the new consultant, date and time are available.
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

                row = cursor.fetchone()
                if row:
                    print("The appointment slot is " \
                    "already booked. Please choose " \
                    "another date or time.")
                else:
                    try:
        # Update the appointment record in the database.
                        cursor.execute("""
                        UPDATE appointment
                        SET patient_id = ?,
                        consultant_id = ?,
                        appointment_date = ?,
                        appointment_time = ?
                        WHERE appointment_id = ?
                        """,(self.patient_id,
                         self.consultant_id,
                         self.appointment_date,
                         self.appointment_time,
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
                if not self.validate_user_login(appointment_id):
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
        row = cursor.fetchone()
        if not row:
            print("We couldn't find " \
            "an appointment with that ID.")
            return 
        else:
            self.patient_id = row[1]
            self.consultant_id = row[2]
            self.appointment_date = row[3]
            self.appointment_time = row[4]

            print(f"Appointment ID: {row[0]}")
            self.show_details_appointment()

            while True:
        # Confirm that the user wants to delete the appointment.
                delete = input("Delete "
                    "this appointment? (Y/N): ").lower()
                if not self.validate_yes_no(delete):
                    print("Please Y/y for yes " \
                    "or N/n for no.")
                    continue
                if delete == 'n':
                    print("Appointment deletion cancelled.")
                    break 
                else:
                    try:
        # Delete the appointment from the database
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
        








        
            



            



        



    
        