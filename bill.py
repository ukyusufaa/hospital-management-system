import sqlite3
from database import conn, cursor
from colors import DISPLAY_INFO,BILLING_MENU,ERROR,RESET

class Bill():
    def __init__(self, total_amount = None, 
                 appointment_id = None, payment_status = None):
        self.total_amount = total_amount
        self.appointment_id = appointment_id
        self.payment_status = payment_status

    def show_bill_details(self):
        print("=" * 30)
        print(f"{DISPLAY_INFO}Total Amount:{self.total_amount}{RESET}")
        print(f"{DISPLAY_INFO}Appointment ID:{self.appointment_id}{RESET}")
        print(f"{DISPLAY_INFO}Payment Status: {self.payment_status}{RESET}")
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
                self.appointment_id = int(input(f"{BILLING_MENU}Please enter "
                                                f"the appointment ID: {RESET}"))
                
                if not self.validate_login_id(self.appointment_id):
                    print(f"{ERROR}Please enter a valid appointment ID.{RESET}")
                    continue 
                break
            except ValueError:
                print(f"{ERROR}Please enter the appointment ID using numbers only.{RESET}")
                continue
        try:
            cursor.execute("""
                SELECT * FROM appointment
                WHERE appointment_id = ?
            """, (self.appointment_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to find the appointment.{RESET}")
            return

        appointment_record = cursor.fetchone()

        if not appointment_record:
            print(f"{ERROR}This appointment does not exist.{RESET}")
            return
        
        print(f"{DISPLAY_INFO}The Appointment exists{RESET}")

        print(f"{DISPLAY_INFO}Appointment ID: {appointment_record[0]}{RESET}")

        # Find the one prescription associated with the one appointment.
        try:
            cursor.execute("""
                SELECT * FROM prescription
                WHERE appointment_id = ?
            """,(self.appointment_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to find the prescription. Please try again.{RESET}", e)
            return 

        # Get the one prescription details from the database.
        prescription_record = cursor.fetchone()

        if not prescription_record:
            print(f"{ERROR}No prescription is linked to this appointment.{RESET}")
            return

        print(f"{DISPLAY_INFO}A prescription linked to this appointment found.{RESET}")

        # If the one prescription linked to one appointment exists.
        # prescription_id was not created in __init__.
        # We create the object attribute here using self and store the ID from the database row.
        
        self.prescription_id = prescription_record[0]
        print(f"{DISPLAY_INFO}Prescription ID: {RESET}", self.prescription_id)
        print()

        # Find all the medications listed on this one prescription.
        # Remember this one prescription is linked to one appointment.
        try:
        # This junction table contains prescription_id, medication_id together so linking them.
            cursor.execute("""
                SELECT * FROM prescription_medication
                WHERE prescription_id = ?
            """,(self.prescription_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to retrieve the prescription medications. Please " 
                    f"try again.{RESET}", e)
            return

        # A prescription can contain multiple medications, so fetchall() is used.
        prescription_medication_rows = cursor.fetchall()
    
        if not prescription_medication_rows:
            print(f"{DISPLAY_INFO}No medications are linked to this prescription.{RESET}")
            return

        print(f"{DISPLAY_INFO}The medication/medications " 
              f"linked to this prescription found.{RESET}")
        print()

        # If Medications are found.
        # Start the bill total at zero.
        self.total_amount = 0

        # Go through each medication linked to this prescription.
        for prescription_medication_row in prescription_medication_rows:

            # Get the medication ID from the junction table.
            # Store the medication ID in the Bill object.
            self.medication_id = prescription_medication_row[2]

            # Display each medication ID linked to this one prescription.
            print(f"{DISPLAY_INFO}Medication ID: {self.medication_id}{RESET}")

            # Use the medication ID stored in the Bill object.
            try:
                cursor.execute("""
                    SELECT * FROM medication
                    WHERE medication_id = ?
                """,(self.medication_id,))

            except sqlite3.Error as e:
                print(f"{ERROR}Unable to retrieve the " 
                        f"medications. Please try again.{RESET}", e)
                return

            # Retrieve all matching medication records.
            medication_rows = cursor.fetchall()

            if not medication_rows:
                print(f"{ERROR}No Medication found.{RESET}")
                return
        
            # From the medication table show all the medications and their details. 
            # Show medication_id, name, cost of each medication.
            print(f"{DISPLAY_INFO}Medication{RESET}",medication_rows)

            # Retrieve row(medication) and its cost at index 2 from the many medication rows.
            # Add each medication cost to the bill total.
            for row in medication_rows:
                self.total_amount += row[2]

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
            print(f"{ERROR}Unable to create the bill. Please try again.{RESET}", e)
            return

        print(f"{DISPLAY_INFO}Bill created successfully.{RESET}")

        bill_id = cursor.lastrowid
        print(f"{DISPLAY_INFO}Bill ID: {bill_id}{RESET}")
        print()

        # Display the newly created bill.
        self.show_bill_details()
        return
      
    def display_all_bills(self):
        try:
        # Retrieve all bills from the database.
            cursor.execute("SELECT * FROM bill")

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to retrieve bills. Please try again.{RESET}", e)
            return

        bill_rows = cursor.fetchall()
        if not bill_rows:
            print(f"{ERROR}No bills are are currently recorded.{RESET}")
            return
        
        for bill_row in bill_rows:
        # Create a Bill object for each database record.
            billing = Bill(
                bill_row[1],
                bill_row[2],
                bill_row[3]
            )
            print(f"{DISPLAY_INFO}Bill ID:{bill_row[0]}{RESET}")
            billing.show_bill_details()
            print()

    def search_bill(self):
        while True:
            try:
                self.appointment_id = int(input(f"{DISPLAY_INFO}Please enter the " 
                                                f"Appointment ID: {RESET}"))

                if not self.validate_login_id(self.appointment_id):
                    print(f"{ERROR}Please enter a valid appointment ID.{RESET}")
                    continue
                break 

            except ValueError:
                print(f"{ERROR}EPlease enter the appointment ID using numbers only.{RESET}")
                continue 

        # Search for a bill using the appointment ID.
        try:
            cursor.execute("""
            SELECT * FROM bill
            WHERE appointment_id = ?
            """,(self.appointment_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to search for the bill. Please try again.{RESET}", e)
            return

        bill_row = cursor.fetchone()

        if not bill_row:
            print()
            print(f"{ERROR}No bill was found for this appointment.{RESET}")
            return 
        
        self.total_amount = bill_row[1]
        self.appointment_id = bill_row[2]
        self.payment_status = bill_row[3]

        print(f"{DISPLAY_INFO}Bill ID: {bill_row[0]}{RESET}")
        print()

        # Display the matching bill.
        self.show_bill_details()
        

    def bill_update(self):
        while True:
            try:
                self.appointment_id = int(input(f"{DISPLAY_INFO}Please enter " 
                                                f"the appointment ID:"))
                if not self.validate_login_id(self.appointment_id):
                    print(f"{ERROR}Please enter a valid appointment ID.{RESET}")
                    continue
                break 

            except ValueError:
                print(f"{ERROR}Please enter the appointment ID using numbers only.{RESET}")
                continue 

        # Find the bill associated with the appointment.
        try:
            cursor.execute("""
            SELECT * FROM bill
            WHERE appointment_id = ?
            """,(self.appointment_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to retrieve the bill. Please try again.{RESET}", e)
            return

        bill_row = cursor.fetchone()
        if not bill_row:
            print(f"{ERROR}Patient bill not found.{RESET}")
            return 
        
        self.total_amount = bill_row[1]
        self.appointment_id = bill_row[2]
        self.payment_status = bill_row[3]

        print(f"{DISPLAY_INFO}Bill ID:{bill_row[0]}{RESET}")
        print()
    
        self.show_bill_details()
        print()

        while True:
        # Ask the user whether the bill has been paid.
            bill_paid = input(f"{DISPLAY_INFO}Has this bill been paid? (Y/N)").lower()
            if not self.validate_yes_no(bill_paid):
                print(f"{ERROR}Please enter Y/y for yes or N/n for no.{RESET}")
                continue

            if bill_paid == 'n':
                    print(f"{DISPLAY_INFO}The bill remains unpaid.{RESET}")
                    return
            break
                
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
            print(f"{ERROR}Unable to update the bill. Please try again.{RESET}", e)
            return

        print(f"{DISPLAY_INFO}Bill payment status updated successfully.{RESET}")

        print(f"{DISPLAY_INFO}Billing ID: {bill_row[0]}{RESET}")
        print()

        # Display the updated bill
        self.show_bill_details()
        return


        

        
            


        
        
    