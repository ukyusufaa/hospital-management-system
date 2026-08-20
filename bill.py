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
        if number < 1:
            return False
        return True 

    def validate_yes_no(self,choice):
        if not choice == 'y' and not choice == 'n':
            return False
        return True

    def validate_bill(self,amount):
        if amount < 0 or amount != round(amount,2):
            return False
        return True
            
    def create_bill(self):
        # Validate the appointment ID entered by user.
        while True:
            try:
                self.appointment_id = int(input("Please enter "
                    "the appointment ID:"))
                if not self.validate_login_id(self.appointment_id):
                    print("Please enter a valid " \
                    "appointment ID.")
                    continue 
                break 

            except ValueError:
                print("Please enter the appointment ID "/
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

        # Check if a prescription was found.
        if prescription_row:
        
        # The prescription_id was not created in __init__.
        # We create the object attribute here using self and store the ID from the database row.
            self.prescription_id = prescription_row[0]

        # self.prescription_id can be used by other methods and queries for this bill object.
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
        # A prescription contain multiple medications, so fetchall() is used.
            prescription_medication_rows = cursor.fetchall()
            print("Medications linked /"
            "to this prescription",prescription_medication_rows)

        # Check that the prescription has at least one medication.
            if prescription_medication_rows:

        # Start the bill total at zero.
                self.total_amount = 0

        # Go through each medication linked to this prescription.
                for prescription_medication_row in prescription_medication_rows:
                    print("Checking Medication details...",prescription_medication_row)

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
                    print("Medication found")

        # Check if a medication was found.
                    if medication_row:
        # Add each medication cost to the bill total.
                        self.medication_cost = medication_row[2]
                        self.total_amount += self.medication_cost
                    else:
                        print("Medication not found " \
                        "in the database.")
                        return 
            else:
                print("No medications are linked " \
                "to this prescription.")
                return
        else:
            print("No prescription is linked "/ 
                  "to this appointment")
            return
        
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
        bill_number = cursor.lastrowid
        print(f"Bill ID:{bill_number}")

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
        else:
            for bill_row in bill_rows:
        # Create a Bill object for each database record.
                billing = Bill(
                    bill_row[1],
                    bill_row[2],
                    bill_row[3]

                )
                print(f"Bill ID:{bill_row[0]}")
                billing.show_bill_details()
            return

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
            print("No bill was found for this appointment")
            return 
        else:
            self.total_amount = bill_row[1]
            self.appointment_id = bill_row[2]
            self.payment_status = bill_row[3]
            print(f"Bill ID:{bill_row[0]}")

        # Display the matching bill.
            self.show_bill_details()
            return

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
        else:
            self.total_amount = bill_row[1]
            self.appointment_id = bill_row[2]
            self.payment_status = bill_row[3]

            print(f"Bill ID:{bill_row[0]}")
            print(f"Bill ID:{bill_row[0]}")
            self.show_bill_details()

            while True:
        # Ask the user whether the bill has been paid.
                bill_paid = input("Has this bill been paid? (Y/N)").lower()
                if not self.validate_yes_no(bill_paid):
                    print("Please enter Y/n for yes "/
                          "or N/n for no")
                    continue
                if bill_paid == 'n':
                    print("The bill remains unpaid.")
                    return
                else:
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
                    return


        

        
            


        
        
    