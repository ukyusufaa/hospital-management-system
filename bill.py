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
        print(f"Total Amount:{self.total_amount}")
        print(f"Appointment ID:{self.appointment_id}")

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
        # Get and validate appointment ID from user
        while True:
            try:
                self.appointment_id = int(input("Appointment ID:"))
                if not self.validate_login_id(self.appointment_id):
                    print("Appointment ID must be greater than 0")
                    continue 
                break 

            except ValueError:
                print("Appointment ID must be numbers")

        # Search the prescription table using the appointment ID.
        # We need to discover which prescription 
            # belongs to this appointment.
        
        try:
            cursor.execute("""
            SELECT * FROM prescription
             WHERE appointment_id = ?
            """,(self.appointment_id,))

        except sqlite3.Error as e:
            print("Database Error", e)
            return 

        # Only one prescription is expected for this appointment,
            # therefore fetchone is used.

        prescription_row = cursor.fetchone()
        # If no row is returned, the appointment has
            # no prescription.
        # So a bill based on medication cannot be created.
       
        if prescription_row:
            # Extract the prescription ID from the returned
                # prescription row.
            # This ID becomes the link to the prescription_medication table.
            self.prescription_id = prescription_row[0]
            print("PRESCRIPTION:", prescription_row)
            print("PRESCRIPTION ID:", self.prescription_id)
            # Search the prescription_medication junction table.
            # This table connects prescription to medication ID/ID's.
            try:
                cursor.execute("""
                SELECT * FROM prescription_medication
                WHERE prescription_id = ?
                """,(self.prescription_id,))

            except sqlite3.Error as e:
                print("Database Error", e)
                return
            # One prescription can contain several medications.
            # Therfore fetchall() is required here.

            prescription_medication_rows = cursor.fetchall()
            print("ROWS:",prescription_medication_rows)
            # An empty list means prescription exist, but there are
                # no medications attached to it.
         
            if prescription_medication_rows:
                # Go through every prescription_medication row.
                # Each row represents a medication linked to 
                    # this prescription
                
                self.total_amount = 0

                for prescription_medication_row in prescription_medication_rows:
                    print("LOOP: ",prescription_medication_row)
                    # Extract the medication ID from the junction-table row.
                    # This ID will now be used to find the 
                        # actual medication.
                    self.medication_id = prescription_medication_row[2]
                    # Search the medication table using the medication ID.
                    # The Junction table gives us the relationship;
                        # the medication table contains the actual
                        # medication details.
                    try:
                        # Search for the single medication in the 
                            # medication table
                        cursor.execute("""
                        SELECT * FROM medication
                        WHERE medication_id = ?
                        """,(self.medication_id,))

                    except sqlite3.Error as e:
                        print("Database Error", e)
                        return

                    # Get the single medication using fethchone().
                    medication_row = cursor.fetchone()
                    print(medication_row)

                    # Check whether a medication was actually found
                    if medication_row:
                        self.medication_cost = medication_row[2]
                        self.total_amount += self.medication_cost
                    else:
                        print("Medication record not found")
                        return 
            else:
                print("No medications found for this prescription ")
                return
        else:
            print("No prescription found for this appointment")
            return

        self.payment_status = "UNPAID"

        receipt = Bill(
        self.total_amount,
        self.appointment_id,
        self.payment_status
        )

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

            conn.commit()

        except sqlite3.Error as e:
            print("Database Error", e)
            return

        print("Bill inserted succesfully")
        bill_number = cursor.lastrowid
        print(f"Bill ID:{bill_number}")
        receipt.show_bill_details()

    def display_all_bills(self):
        try:
            cursor.execute("SELECT * FROM bill")

        except sqlite3.Error as e:
            print("Database Error", e)
            return

        bill_rows = cursor.fetchall()
        if not bill_rows:
            print("No patient bills founds")
            return
        else:
            for bill_row in bill_rows:
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
                self.appointment_id = int(input("Appointment ID:"))
                if not self.validate_login_id(self.appointment_id):
                    print("Appointment ID must be greater than 0")
                    continue
                break 

            except ValueError:
                print("Appointment ID must be numbers")
                continue 

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
            return

    def bill_update(self):
        while True:
            try:
                self.appointment_id = int(input("Appointment ID:"))
                if not self.validate_login_id(self.appointment_id):
                    print("Appointment ID must be greater than 0")
                    continue
                break 

            except ValueError:
                print("Appointment ID must be numbers")
                continue 

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
                bill_paid = input("Has the bill been paid(Y/N)?").lower()
                if not self.validate_yes_no(bill_paid):
                    print("Enter either Y or N to proceed")
                    continue
                if bill_paid == 'n':
                    print("Bill not paid")
                    return
                else:
                    billing.payment_status = "PAID"
                    try:
                        cursor.execute("""
                        UPDATE bill
                        SET payment_status = ?
                        WHERE appointment_id = ?
                        """,(billing.payment_status,
                        billing.appointment_id))

                        conn.commit()

                    except sqlite3.Error as e:
                        print("Database Error", e)
                        return

                    print("Bill Updated succesfully")
                    print(f"Billing ID:{bill_row[0]}")
                    billing.show_bill_details()
                    return


        

        
            


        
        
    