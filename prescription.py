# Import SQLite to work with the database
import sqlite3

# Import the shared database connection and cursor from database.py module.
from database import conn, cursor

class Prescription():
        # Store the appointment associated with the prescription.
    def __init__(self,appointment_id = None):
        self.appointment_id = appointment_id

        # Display the prescription details associated with the appointment.
    def show_prescription_details(self):
        print("-" * 30)
        print(f"Appointment ID:{self.appointment_id}")
        print("-" * 30)

        # Validate the appointment ID is a positive number.
    def validate_login_id(self,number):
        if number < 1:
            return False
        return True

        # Validate the user's confirmation choice before performing deletion.
    def validate_yes_no(self,option):
        if option != 'y' and not option =='n':
            return False
        return True

    def create_prescription(self):
        while True:
            try:
        # Request the appointment ID associated with the new prescription.
                self.appointment_id = int(input(
                    "Enter appointment ID: "
                ))
        # Validate that the appointment ID is a positive number
                if not self.validate_login_id(self.appointment_id):
                    print("Enter a valid " \
                    "appointment ID.")
                    continue 
                break 

            except ValueError:
                print("Please enter a valid appointment ID " \
                "using numbers only.")
                continue 

        try:
        # Check whether the appointment already has existing prescription.
            cursor.execute("""
            SELECT * FROM prescription
            WHERE appointment_id = ?
            """,(self.appointment_id,))

        except sqlite3.Error as e:
            print("Unable to search for " \
            "the prescription. Please " \
            "try again.", e)
            return

        # Retrieve the first matching prescription, if one exists.
        searched_row = cursor.fetchone()

        # Prevent duplicate prescriptions from being created for the same appointment.
        if searched_row:
            print("A prescription already exists " \
            "for this appointment.")
            return
        else:
            try:
        # Create a new prescription when no existing prescription was found.
                cursor.execute("""
                INSERT INTO prescription(
                    appointment_id)
                VALUES(?)
                """,(self.appointment_id,))

        # Save the new prescription to the database.
                conn.commit()

            except sqlite3.Error as e:
                print("Unable to create " \
                "the prescription.", e)
                return 

        print("Prescription created successfully.")

        # Retrieve the ID automatically generated for the new prescription.
        row = cursor.lastrowid
        print(f"Prescription ID: {row}")
        self.show_prescription_details()
        return

    def display_all_prescriptions(self):
        try:
        # Retrieve all prescriptions stored in the database.
            cursor.execute("SELECT * FROM prescription")

        except sqlite3.Error as e:
            print("Unable to display the " \
            "prescriptions. Please try again.", e)
            return 

        # Retrieve all rows returned by the query.
        rows = cursor.fetchall()
        if not rows:
            print("No prescriptions are " \
            "currently available.")
        else:
        # Display each prescription returned from the database.
            for row in rows:
                prescription = Prescription(
                    row[1]
                )
                print(f"Prescription ID:{row[0]}")
                prescription.show_prescription_details()
            return

    def search_prescription(self): 
        while True:
            try:
        # Request the appointment ID used to locate the prescription.
                self.appointment_id = int(
                    input("Enter the appointment ID: "))
                if not self.validate_login_id(self.appointment_id):
                    print("Please enter a valid " \
                    "appointment ID.")
                    continue 
                break 
    
            except sqlite3.Error as e:
                print("Appointment ID must " \
                "be in numbers only.")
                continue 

        try:
        # Search for the prescription associated with the specified appointment.
            cursor.execute("""
            SELECT * FROM prescription
            WHERE appointment_id = ?
            """,(self.appointment_id,))
    
        except sqlite3.Error as e:
            print("Unable to search for " \
            "the prescription. Please" \
            "try again.", e)
            return 

        # Retrieve the matching prescription, if one exists.
        row = cursor.fetchone()

        if not row:
        # Handle the case where no prescription exists for the appointment.
            print("No prescription was " \
            "found for this appointment.")
            return 
        else:
            self.appointment_id = row[1]

            print(f"Prescription ID:{row[0]}")
            self.show_prescription_details()
            return
    
    def delete_prescription(self):
        while True:
            try:
        # Request the appointment ID associated with the prescription to be deleted.
                self.appointment_id = int(
                    input("Enter appointment ID:"))
                if not self.validate_login_id(self.appointment_id):
                    print("Please enter a valid " \
                    "appointment ID.")
                    continue 
                break 

            except sqlite3.Error as e:
                print("Appointment ID must " \
                "be in numbers only.")
                continue 
        try:
        # Locate the prescription before attempting deletion.
            cursor.execute("""
            SELECT * FROM prescription
            WHERE appointment_id = ?
            """,(self.appointment_id,))

        except sqlite3.Error as e:
            print("Unable to find the " \
            "prescription. Please try again.", e)
            return 

        row = cursor.fetchone()

        # Stop the deletion if no prescription exists for the appointment.
        if not row:
            print("No prescription was " \
            "found for this appointment.")
            return 
        else:
            self.appointment_id = row[1]

            print(f"Prescription ID:{row[0]}")
            self.show_prescription_details()

            while True:
                delete = input(

        # Confirm the deletion with the user before modifying the database.
                    "Are you sure you want to " 
                    "delete prescription? (Y/N):").lower()
                if not self.validate_yes_no(delete):

        # Validate the user's confirmation choice.
                    print("Please enter Y/y " \
                    "or N/n.")
                    continue 
                if delete == 'n':
                    print("Prescription deletion cancelled.")
                    break 
                else:
                    while True:
                        try:
        # Delete the prescription associated with the specified appointment.
                            cursor.execute("""
                            DELETE FROM prescription
                            WHERE appointment_id = ?
                            """,(self.appointment_id,))

        # Save the deletion to the database.
                            conn.commit()

                        except sqlite3.Error as e:
                            print("Unable to delete " \
                            "the prescription.", e)
                            return 

                        print("Prescription deleted successfully.")
                        return


