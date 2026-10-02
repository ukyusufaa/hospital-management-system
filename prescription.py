# Import SQLite to work with the database
import sqlite3
from colors import DISPLAY_INFO,PRESCRIPTION_MENU,ERROR,RESET

class Prescription():
        # Store the appointment associated with the prescription.
    def __init__(self,database,appointment_id = None):
        self.database = database
        self.appointment_id = appointment_id

        # Display the prescription details associated with the appointment.
    def show_prescription_details(self):
        print("=" * 30)
        print(f"{DISPLAY_INFO}Appointment ID:{self.appointment_id}{RESET}")
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
                self.appointment_id = int(input(f"{PRESCRIPTION_MENU}Enter " 
                                                f"appointment ID: {RESET}"))
                
        # Validate that the appointment ID is a positive number
                if not self.validate_login_id(self.appointment_id):
                    print(f"{ERROR}Enter a valid appointment ID.{RESET}")
                    continue 
                break 

            except ValueError:
                print(f"{ERROR}Please enter a valid appointment ID using numbers only.{RESET}")
                continue 

        # Check whether a prescription already exists.
        try:
            self.database.cursor.execute("""
            SELECT * FROM prescription
                WHERE appointment_id = ?
            """,(self.appointment_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to search for the prescription. Please try again.{e}{RESET}")
            return

        # Retrieve the prescription, if one exists.
        prescription_record = self.database.cursor.fetchone()

        # Prevent duplicate prescriptions from being created for the same appointment.
        if prescription_record:
            print(f"{ERROR}A prescription already exists for this appointment.{RESET}")
            return
        
        # Create the prescription.
        try:
            self.database.cursor.execute("""
                INSERT INTO prescription(
                appointment_id)
                VALUES(?)
            """,(self.appointment_id,))

        # Save the new prescription to the database.
            self.database.connection.commit()

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to create the prescription.{e}{RESET}")
            return 

        # Retrieve the ID automatically generated for the new prescription.
        prescription_id = self.database.cursor.lastrowid

        print(f"{DISPLAY_INFO}Prescription created successfully.{RESET}")
        print()
        print(f"{DISPLAY_INFO}Prescription ID: {prescription_id}{RESET}")

        # Display the prescription stored in this object.
        self.show_prescription_details()
        

    def display_all_prescriptions(self):
        # Retrieve all prescriptions from the database.
        try:
            self.database.cursor.execute("SELECT * FROM prescription")

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to display the prescriptions. Please try again.{e}{RESET}")
            return 

        # Retrieve all queried rows.
        prescription_records = self.database.cursor.fetchall()

        if not prescription_records:
            print(f"{ERROR}No prescriptions are currently available.{RESET}")
            return
        
        # Create an object for each database record
        for prescription_record in prescription_records:
            prescription = Prescription(prescription_record[1])

            print(f"{DISPLAY_INFO}Prescription ID:{prescription_record[0]}{RESET}")
            prescription.show_prescription_details()
            print()

    def search_prescription(self):
        # Get and validate the appointment ID.
        while True:
            try:
                self.appointment_id = int(input(f"{PRESCRIPTION_MENU}Enter " 
                                                f"the appointment ID: {RESET}"))
                if not self.validate_login_id(self.appointment_id):
                    print(f"{ERROR}Please enter a valid appointment ID.{RESET}")
                    continue 
                break 
    
            except ValueError:
                print(f"{ERROR}Appointment ID must be in numbers only.{RESET}")
                continue 

        # Search for the prescription linked to the appointment.
        try:
            self.database.cursor.execute("""
                SELECT * FROM prescription
                WHERE appointment_id = ?
            """,(self.appointment_id,))
    
        except sqlite3.Error as e:
            print(f"{ERROR}Unable to search for the prescription. Please try again.{e}{RESET}")
            return 

        # Retrieve the matching prescription, if one exists.
        prescription_record = self.database.cursor.fetchone()

        if not prescription_record:
        # Handle the case where no prescription exists for the appointment.
            print(f"{ERROR}No prescription was found for this appointment.{RESET}")
            return 

        # Store the database value in the current object.
        self.appointment_id = prescription_record[1]

        print(f"{DISPLAY_INFO}Prescription ID:{prescription_record[0]}{RESET}")
        self.show_prescription_details()
            
    def delete_prescription(self):
        # Get and validate the appointment ID.
        while True:
            try:
                self.appointment_id = int(input(f"{PRESCRIPTION_MENU}Enter " 
                                                f"appointment ID: {RESET}"))
                
                if not self.validate_login_id(self.appointment_id):
                    print(f"{ERROR}Please enter a valid appointment ID.{RESET}")
                    continue 
                break 

            except ValueError:
                print(f"{ERROR}Appointment ID must be in numbers only.{RESET}")
                continue

         # Locate the prescription before attempting deletion.
        try:
            self.database.cursor.execute("""
                SELECT * FROM prescription
                WHERE appointment_id = ?
            """,(self.appointment_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to find the prescription. Please try again.{e}{RESET}")
            return
        
        prescription_record = self.database.cursor.fetchone()

        # Stop the deletion if no prescription exists for the appointment.
        if not prescription_record:
            print(f"{ERROR}No prescription was found for this appointment.{RESET}")
            return
        
        self.appointment_id = prescription_record[1]

        print(f"{DISPLAY_INFO}Prescription ID:{prescription_record[0]}{RESET}")
        self.show_prescription_details()
        print()

        while True:
            delete = input(f"{PRESCRIPTION_MENU}Are you sure you want to " 
                           f"delete prescription? (Y/N): {RESET}").lower()

            if not self.validate_yes_no(delete):
            # Validate the user's confirmation choice.
                print(f"{ERROR}Please enter Y/y or N/n.{RESET}")
                continue 
            
            if delete == 'n':
                print(f"{DISPLAY_INFO}Prescription deletion cancelled.{RESET}")
                return
            
            break

        # Delete the prescription associated with the specified appointment.
        try:
            self.database.cursor.execute("""
                DELETE FROM prescription
                WHERE appointment_id = ?
            """,(self.appointment_id,))

        # Save the deletion to the database.
            self.database.connection.commit()

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to delete the prescription.{RESET}", e)
            return 

        print(f"{DISPLAY_INFO}Prescription deleted successfully.{RESET}")
        


