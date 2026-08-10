import sqlite3

conn = sqlite3.connect("hospital.db")

cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

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
                self.appointment_id = int
                (
                    input("Please enter "/
                          "the appointment ID:")
                )
                if not self.validate_login_id(self.appointment_id):
                    print("Please enter a valid " \
                    "appointment ID.")
                    continue 
                break 

            except ValueError:
                print("Please enter the appointment ID "/
                      "using numbers only.")

        # Find the prescription associated with the prescription.
        
        try:
            cursor.execute("""
            SELECT * FROM prescription
             WHERE appointment_id = ?
            """,(self.appointment_id,))

        except sqlite3.Error as e:
            print("Database Error", e)
            return 

        # Retrieve the prescription because only one is expected.
        prescription_row = cursor.fetchone()
        
        if prescription_row:
    
            self.prescription_id = prescription_row[0]
            print("Prescription found.", prescription_row)
            print("Prescription ID:", self.prescription_id)
        # Find all medications linked through the prescription_medication junction table.
            try:
                cursor.execute("""
                SELECT * FROM prescription_medication
                WHERE prescription_id = ?
                """,(self.prescription_id,))

            except sqlite3.Error as e:
                print("Database Error", e)
                return
        # A prescription contain multiple medications, so fetchall() is used.
            prescription_medication_rows = cursor.fetchall()
            print("Medications linked /"
            "to this prescription",prescription_medication_rows)
         
            if prescription_medication_rows:
                self.total_amount = 0

                for prescription_medication_row in prescription_medication_rows:
                    print("Checking Medication details...",prescription_medication_row)
                
                    self.medication_id = prescription_medication_row[2]

        # Use the medication ID from the junction table to find the medcation details.
                    try:
                        cursor.execute("""
                        SELECT * FROM medication
                        WHERE medication_id = ?
                        """,(self.medication_id,))

                    except sqlite3.Error as e:
                        print("Database Error", e)
                        return

                    medication_row = cursor.fetchone()
                    print("Medication found")

                    if medication_row:
        # Add each medication cost to the bill total.
                        self.medication_cost = medication_row[2]
                        self.total_amount += self.medication_cost
                    else:
                        print("The medication record \
                              could not be found")
                        return 
            else:
                print("No medications are linked "/
                      "to this prescription ")
                return
        else:
            print("No prescription is linked "/ 
                  "to this appointment")
            return
        
        # Set the initial payement status.
        self.payment_status = "UNPAID"

        # Create the Bill object using the calculated details.
        receipt = Bill(
        self.total_amount,
        self.appointment_id,
        self.payment_status
        )

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
            print("Database Error", e)
            return

        print("Bill created successfully")
        bill_number = cursor.lastrowid
        print(f"Bill ID:{bill_number}")

        # Display the newly created bill.
        receipt.show_bill_details()

    def display_all_bills(self):
        try:
        # Retrieve all bills from the database.
            cursor.execute("SELECT * FROM bill")

        except sqlite3.Error as e:
            print("Database Error", e)
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
        cursor.execute("""
        SELECT * FROM bill
        WHERE appointment_id = ?
        """,(self.appointment_id,))

        bill_row = cursor.fetchone()
        if not bill_row:
            print("No bill was found for this appointment")
            return 
        else:
            billing = Bill(
                bill_row[1],
                bill_row[2],
                bill_row[3]
            )
            print(f"Bill ID:{bill_row[0]}")

        # Display the matching bill.
            billing.show_bill_details()
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
        cursor.execute("""
        SELECT * FROM bill
        WHERE appointment_id = ?
        """,(self.appointment_id,))

        bill_row = cursor.fetchone()
        if not bill_row:
            print("Patient bill not found")
            return 
        else:
            billing = Bill(
                bill_row[1],
                bill_row[2],
                bill_row[3]
            )
            print(f"Bill ID:{bill_row[0]}")
            billing.show_bill_details()

            while True:
        # Ask the user whether the bill has been paid.
                bill_paid = input("Has this bill been paid? (Y/N)").lower()
                if not self.validate_yes_no(bill_paid):
                    print("Please enter Y/n for yes "/
                          "or N/n for no")
                    continue
                if bill_paid == 'n':
                    print("The bill remains unpaid")
                else:
        # Update the payment status to PAID
                    billing.payment_status = "PAID"
                    try:
                        cursor.execute("""
                        UPDATE bill
                        SET payment_status = ?
                        WHERE appointment_id = ?
                        """,(billing.payment_status,
                        billing.appointment_id))
        # Save the updated payment status.
                        conn.commit()

                    except sqlite3.Error as e:
                        print("Database Error", e)
                        return

                    print("Bill payment status updated succesfully")
                    print(f"Billing ID:{bill_row[0]}")
        # Display the updated bill
                    billing.show_bill_details()
                    return


        

        
            


        
        
    