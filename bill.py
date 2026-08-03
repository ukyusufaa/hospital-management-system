import sqlite3

conn = sqlite3.connect("hospital.db")

cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

class Bill():
    def __init__(self, appointment_id, total_amount):
        self.appointment_id = appointment_id
        self.total_amount = total_amount
        self.payment_status = "Unpaid"

    def show_bill_details(self):
        print(f"Appointment ID:{self.appointment_id}")
        print(f"Total Amount:{self.total_amount}")

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
            # This table connects one prescription to its medication ID's.
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

        receipt = Bill(
        self.appointment_id,
        self.total_amount
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
    
appointment_id = int(input("Appointment ID:"))
test = Bill(
    appointment_id,
    0
    )
test.create_bill()
        

        
            


        
        
    