import sqlite3
from database import conn, cursor

class Bill():
    def __init__(self, total_amount = None, 
                 appointment_id = None, payment_status = None):
        self.total_amount = total_amount
        self.appointment_id = appointment_id
        self.payment_status = payment_status

    def show_bill_details(self):
        print("-" * 30)
        print(f"Total Amount:{self.total_amount}")
        print(f"Appointment ID:{self.appointment_id}")
        print("-" * 30)

    def validate_login_id(self,number):
        return number >= 1

    def validate_yes_no(self,choice):
        return choice in ('n', 'y')

    def validate_bill(self,amount):
        return amount >= 0 and amount == round(amount, 2)
            
    def create_bill(self):
        # Validate the appointment ID entered by user.
        while True:
            try:
                self.appointment_id = int(input("Please enter "
                    "the appointment ID: "))
                
                if not self.validate_login_id(self.appointment_id):
                    print("Please enter a valid " \
                    "appointment ID.")
                    continue 
                break 

            except ValueError:
                print("Please enter the appointment ID " \
                      "using numbers only.")
                continue

        # Find the prescription associated with the appointment.
        try:
            cursor.execute("""
            SELECT * FROM prescription
             WHERE appointment_id = ?
            """,(self.appointment_id,))

        except sqlite3.Error as e:
            print("Unable to find the prescription. " \
            "Please try again.", e)
            return 

        # Get the prescription row from the database.
        prescription_row = cursor.fetchone()

        if not prescription_row:
            print("No prescription is linked to " \
            "this appointment.")
            return

        # If prescription found.
        # prescription_id was not created in __init__.
        # We create the object attribute here using self and store the ID from the database row.
        self.prescription_id = prescription_row[0]
        print("Prescription ID:", self.prescription_id)

        # Find all medications linked through the prescription_medication junction table.
        try:
            cursor.execute("""
                SELECT * FROM prescription_medication
                WHERE prescription_id = ?
            """,(self.prescription_id,))

        except sqlite3.Error as e:
            print("Unable to retrieve the " \
            "prescription medications. Please " \
            "try again.", e)
            return

        # A prescription can contain multiple medications, so fetchall() is used.
        prescription_medication_rows = cursor.fetchall()
    
        if not prescription_medication_rows:
            print("No medications are linked " \
            "to this prescription.")
            return

        # Start the bill total at zero.
        self.total_amount = 0

        # Go through each medication linked to this prescription.
        for prescription_medication_row in prescription_medication_rows:

        # Get the medication ID from the junction table.
        # Store the medication ID in the Bill object.
            self.medication_id = prescription_medication_row[2]

        # Use the medication ID stored in the Bill object.
        try:
            cursor.execute("""
                SELECT * FROM medication
                WHERE medication_id = ?
            """,(self.medication_id,))

        except sqlite3.Error as e:
            print("Unable to retrieve the " \
            "medications. Please try again.", e)
            return

        # Get the one mataching medication from the the database.
        medication_row = cursor.fetchone()
    
        if not medication_row:
            print("Medication not found in the database.")

        # Add each medication cost to the bill total.
        self.medication_cost = medication_row[2]
        self.total_amount += self.medication_cost

        # Set the initial payement status.
        self.payment_status = "UNPAID"

        # Insert the calculated bill into the database.
        try:
            cursor.execute("""
                INSERT INTO bill(
                    appointment_id,
                    total_amount,
                    payment_status)
                VALUES(?,?,?)
            """,(self.appointment_id,
                 self.total_amount,
                 self.payment_status))
        # Save the transaction to the database.
            conn.commit()

        except sqlite3.Error as e:
            print("Unable to create the bill. " \
            "Please try again.", e)
            return

        print("Bill created successfully.")
        bill_id = cursor.lastrowid
        print(f"Bill ID:{bill_id}")

        # Display the newly created bill.
        self.show_bill_details()

    def display_all_bills(self):
        try:
        # Retrieve all bills from the database.
            cursor.execute("SELECT * FROM bill")

        except sqlite3.Error as e:
            print("Unable to retrieve bills. " \
            "Please try again.", e)
            return

        bill_rows = cursor.fetchall()
        if not bill_rows:
            print("No bills are " \
            "are currently recorded")
            return
        
        for bill_row in bill_rows:
        # Create a Bill object for each database record.
            billing = Bill(
                bill_row[1],
                bill_row[2],
                bill_row[3]
            )
            print(f"Bill ID:{bill_row[0]}")
            billing.show_bill_details()

    def search_bill(self):
        while True:
            try:
                self.appointment_id = int(input("Pleaae enter the "/
                "Appointment ID:"))

                if not self.validate_login_id(self.appointment_id):
                    print("Please enter a valid appointment ID")
                    continue
                break 

            except ValueError:
                print("Please enter the appointment ID " \
                "using numbers only")
                continue 

        # Search for a bill using the appointment ID.
        try:
            cursor.execute("""
            SELECT * FROM bill
            WHERE appointment_id = ?
            """,(self.appointment_id,))

        except sqlite3.Error as e:
            print("Unable to search for the bill. " \
            "Please try again.", e)
            return

        bill_row = cursor.fetchone()

        if not bill_row:
            print("No bill was found for this appointment.")
            return 
        
        self.total_amount = bill_row[1]
        self.appointment_id = bill_row[2]
        self.payment_status = bill_row[3]

        print(f"Bill ID:{bill_row[0]}")

        # Display the matching bill.
        self.show_bill_details()
        

    def bill_update(self):
        while True:
            try:
                self.appointment_id = int(input("Please enter the appointment ID:"))
                if not self.validate_login_id(self.appointment_id):
                    print("Please enter a valid appointment ID")
                    continue
                break 

            except ValueError:
                print("Please enter the appointment ID " \
                    "using numbers only.")
                continue 

        # Find the bill associated with the appointment.
        try:
            cursor.execute("""
            SELECT * FROM bill
            WHERE appointment_id = ?
            """,(self.appointment_id,))

        except sqlite3.Error as e:
            print("Unable to retrieve the bill. " \
            "Please try again.", e)
            return

        bill_row = cursor.fetchone()
        if not bill_row:
            print("Patient bill not found.")
            return 
        
        self.total_amount = bill_row[1]
        self.appointment_id = bill_row[2]
        self.payment_status = bill_row[3]

        print(f"Bill ID:{bill_row[0]}")
    
        self.show_bill_details()

        while True:
        # Ask the user whether the bill has been paid.
            bill_paid = input("Has this bill been paid? (Y/N)").lower()
            if not self.validate_yes_no(bill_paid):
                print("Please enter Y/y for yes " \
                      "or N/n for no.")
                continue

            if bill_paid == 'n':
                    print("The bill remains unpaid.")
                    return
                
        # Update the payment status to PAID
            self.payment_status = "PAID"

            try:
                cursor.execute("""
                    UPDATE bill
                    SET payment_status = ?
                    WHERE appointment_id = ?
                """,(self.payment_status,
                    self.appointment_id))
                
        # Save the updated payment status.
                conn.commit()

            except sqlite3.Error as e:
                print("Unable to update the bill. " \
                    "Please try again.", e)
                return

            print("Bill payment status updated successfully.")

            print(f"Billing ID:{bill_row[0]}")

        # Display the updated bill
            self.show_bill_details()
                    


        

        
            


        
        
    