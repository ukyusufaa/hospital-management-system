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
        return number >= 1

        # Validate the user's confirmation choice before performing deletion.
    def validate_yes_no(self,option):
        return option in ("y", "n")

    def create_prescription(self):
        # Get and validate the appointment ID.
        while True:
            try:
                self.appointment_id = int(input(
                    "Enter appointment ID: "))
                
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

        # Check whether a prescription already exists.
        try:
            cursor.execute("""
            SELECT * FROM prescription
                WHERE appointment_id = ?
            """,(self.appointment_id,))

        except sqlite3.Error as e:
            print("Unable to search for " \
                    "the prescription. Please " \
                    "try again.", e)
            return

        # Retrieve the prescription, if one exists.
        prescription_record = cursor.fetchone()

        # Prevent duplicate prescriptions from being created for the same appointment.
        if prescription_record:
            print("A prescription already exists " \
                    "for this appointment.")
            return
        
        # Create the prescription.
        try:
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

        # Retrieve the ID automatically generated for the new prescription.
        prescription_id = cursor.lastrowid

        print("Prescription created successfully.")
        print(f"Prescription ID: {prescription_id}")

        # Display the prescription stored in this object.
        self.show_prescription_details()
        

    def display_all_prescriptions(self):
        # Retrieve all prescriptions from the database.
        try:
            cursor.execute("SELECT * FROM prescription")

        except sqlite3.Error as e:
            print("Unable to display the " \
                    "prescriptions. Please try again.", e)
            return 

        # Retrieve all queried rows.
        prescription_records = cursor.fetchall()

        if not prescription_records:
            print("No prescriptions are " \
                    "currently available.")
            return
        
        # Create an object for each database record
        for prescription_record in prescription_records:
            prescription = Prescription(prescription_record[1])

            print(f"Prescription ID:{prescription_record[0]}")
            prescription.show_prescription_details()

    def search_prescription(self):
        # Get and validate the appointment ID.
        while True:
            try:
                self.appointment_id = int(
                    input("Enter the appointment ID: "))
                if not self.validate_login_id(self.appointment_id):
                    print("Please enter a valid " \
                            "appointment ID.")
                    continue 
                break 
    
            except ValueError:
                print("Appointment ID must " \
                        "be in numbers only.")
                continue 

        # Search for the prescription linked to the appointment.
        try:
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
        prescription_record = cursor.fetchone()

        if not prescription_record:
        # Handle the case where no prescription exists for the appointment.
            print("No prescription was " \
                    "found for this appointment.")
            return 

        # Store the database value in the current object.
        self.appointment_id = prescription_record[1]

        print(f"Prescription ID:{prescription_record[0]}")
        self.show_prescription_details()
            
    def delete_prescription(self):
        # Get and validate the appointment ID.
        while True:
            try:
                self.appointment_id = int(input(
                    "Enter appointment ID:"))
                
                if not self.validate_login_id(self.appointment_id):
                    print("Please enter a valid " \
                            "appointment ID.")
                    continue 
                break 

            except ValueError:
                print("Appointment ID must " \
                        "be in numbers only.")
                continue

         # Locate the prescription before attempting deletion.
        try:
            cursor.execute("""
                SELECT * FROM prescription
                WHERE appointment_id = ?
            """,(self.appointment_id,))

        except sqlite3.Error as e:
            print("Unable to find the " \
                    "prescription. Please try again.", e)
            return
        
        prescription_record = cursor.fetchone()

        # Stop the deletion if no prescription exists for the appointment.
        if not prescription_record:
            print("No prescription was " \
                    "found for this appointment.")
            return
        
        self.appointment_id = prescription_record[1]

        print(f"Prescription ID:{prescription_record[0]}")
        self.show_prescription_details()

        while True:
            delete = input(
                "Are you sure you want to " 
                "delete prescription? (Y/N):").lower()

            if not self.validate_yes_no(delete):
            # Validate the user's confirmation choice.
                print("Please enter Y/y " \
                "or N/n.")
                continue 
            
            if delete == 'n':
                print("Prescription deletion cancelled.")
                return
            
            break

        # Delete the prescription associated with the specified appointment.
        try:
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
        


