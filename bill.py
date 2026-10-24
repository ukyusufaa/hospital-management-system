import sqlite3
from colors import (DISPLAY_INFO,BILLING_MENU,UNPAID_STATUS,
MEDICATION_COST,TOTAL_AMOUNT,PAID_STATUS,ERROR,RESET)

class Bill():
    def __init__(self, database, total_amount = None, 
                 appointment_id = None, payment_status = None):
        self.database = database
        self.total_amount = total_amount
        self.appointment_id = appointment_id
        self.payment_status = payment_status

    def show_bill_details(self):
        print("=" * 40)
        print(f"Total Amount:{DISPLAY_INFO} £{self.total_amount:.2f}{RESET}")
        print(f"Appointment ID:{DISPLAY_INFO} {self.appointment_id}{RESET}")
        if self.payment_status == "PAID":
            print(f"Payment Status:{PAID_STATUS} {self.payment_status}{RESET}")
        else:
            print(f"Payment Status:{UNPAID_STATUS} {self.payment_status}{RESET}")

        try:
            self.database.cursor.execute("""
                SELECT medication_id, medication_name, unit_cost
                FROM bill_item
                WHERE bill_id = (
                    SELECT bill_id
                    FROM bill
                    WHERE appointment_id = ?
                )
            """, (self.appointment_id,))

            bill_items = self.database.cursor.fetchall()

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to retrieve bill items. {e}{RESET}")
            print("=" * 40)
            return

        print("-" * 40)
        print(f"Medication Charges: ")

        if bill_items:
            for item in bill_items:
                medication_id, medication_name, unit_cost = item
                print(f"Medication ID:{DISPLAY_INFO} {medication_id}{RESET}")
                print(f"Medication Name:{DISPLAY_INFO} {medication_name}{RESET}")
                print(f"Medication Cost:{DISPLAY_INFO} £{unit_cost:.2f}{RESET}")
                print("-" * 40)
        else:
            print(f"{DISPLAY_INFO}No medication items recorded.{RESET}")
        print("=" * 40)

    
    def show_invoice(self):
        try:
            self.database.cursor.execute("""
                SELECT
                    bill.bill_id,
                    bill.payment_status,
                    date('now'),
                    appointment.appointment_id,
                    patient.patient_id,
                    patient.first_name,
                    patient.surname,
                    patient.address,
                    consultant.first_name,
                    consultant.surname,
                    department.department_name,
                    gp.first_name,
                    gp.surname,
                    gp_surgery.surgery_name,
                    gp_surgery.address

                FROM bill
                INNER JOIN appointment
                    ON bill.appointment_id = appointment.appointment_id
                INNER JOIN patient
                    ON appointment.patient_id = patient.patient_id
                INNER JOIN consultant
                    ON appointment.consultant_id = consultant.consultant_id
                INNER JOIN department
                    ON consultant.department_id = department.department_id
                INNER JOIN gp
                    ON patient.gp_id = gp.gp_id
                INNER JOIN gp_surgery
                    ON gp.surgery_id = gp_surgery.surgery_id
                WHERE bill.appointment_id = ?
                """, (self.appointment_id,))

            invoice = self.database.cursor.fetchone()

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to retrieve invoice. {e}{RESET}")
            return

        if invoice is None:
            print(f"{ERROR}No invoice found for this appointment.{RESET}")
            return
    
        (   
            bill_id,
            payment_status,
            invoice_date,
            appointment_id,
            patient_id,
            patient_first_name,
            patient_surname,
            patient_address,
            consultant_first_name,
            consultant_surname,
            department_name,
            gp_first_name,
            gp_surname,
            surgery_name,
            surgery_address
        
        ) = invoice

        try:
            self.database.cursor.execute("""
                SELECT
                    bill_item.medication_name,
                    bill_item.unit_cost
                FROM bill
                    LEFT JOIN bill_item
                        ON bill_item.bill_id = bill.bill_id
                    WHERE bill.appointment_id = ?
                    """, (self.appointment_id,))
        
            bill_items = self.database.cursor.fetchall()
        
        except sqlite3.Error as e:
            print(f"{ERROR}Unable to retrieve invoice. {e}{RESET}")
            return
        
        if not bill_items:
            print(f"{ERROR}No invoice found for this appointment.{RESET}")
            return

        print()
        print("*" * 50)
        print("                 HOLLY HOSPITAL")
        print("*" * 50)
        print("                 Hospital Invoice")
        print()


        print("=" * 50)
        print(f"Bill ID:{DISPLAY_INFO} BILL-{bill_id:03d}{RESET}")
        
        if payment_status == "PAID":
            print(f"Payment Status:{PAID_STATUS} {payment_status}{RESET}")
        else:
            print(f"Payment Status:{UNPAID_STATUS} {payment_status}{RESET}")

        print(f"Invoice Date:{DISPLAY_INFO} {invoice_date}{RESET}")
        print(f"Appointment ID:{DISPLAY_INFO} {appointment_id}{RESET}")
        print()

        for item in bill_items:
            medication_name, medication_cost = item
            print("*" *50)
            print("BILL ITEM DETAILS")
            print(f"Medication:{DISPLAY_INFO} {medication_name}{RESET}")
            print(f"Medication Cost:{DISPLAY_INFO} {MEDICATION_COST} £{medication_cost:.2f}{RESET}")
            print("*" * 50)
            print()

        print("/" *50)
        print(f"TOTAL AMOUNT:{DISPLAY_INFO} {TOTAL_AMOUNT} £{self.total_amount:.2f}{RESET}")
        print("/" * 50)
        print()

        print("PATIENT DETAILS")
        print(f"Patient ID:{DISPLAY_INFO} {patient_id}{RESET}")
        print(f"Patient:{DISPLAY_INFO} {patient_first_name} {patient_surname}{RESET}")
        print(f"Patient Address:{DISPLAY_INFO} {patient_address}{RESET}")
        print()

        print("CONSULTANT DETAILS")
        print(f"Hospital Consultant:{DISPLAY_INFO} {consultant_first_name} " 
              f"{consultant_surname}{RESET}")
        print()

        print("DEPARTMENT DETAILS")
        print(f"Hospital Department:{DISPLAY_INFO} {department_name}{RESET}")
        print()

        print("GP AND MEDICAL CLINIC")
        print(f"GP:{DISPLAY_INFO} {gp_first_name} {gp_surname}{RESET}")
        print(f"Medical Clinic:{DISPLAY_INFO} {surgery_name}{RESET}")
        print(f"Medical Clinic Address:{DISPLAY_INFO} {surgery_address}{RESET}")

        print("-" * 50)

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
            self.database.cursor.execute("""
                SELECT * FROM appointment
                WHERE appointment_id = ?
            """, (self.appointment_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to find the appointment.{e}{RESET}")
            return

        appointment_record = self.database.cursor.fetchone()

        if not appointment_record:
            print(f"{ERROR}This appointment does not exist.{RESET}")
            return
        
        print(f"{DISPLAY_INFO}The Appointment exists{RESET}")

        print(f"Appointment ID:{DISPLAY_INFO} {appointment_record[0]}{RESET}")

        # Find the bill linked to this appointment.
        try:
            self.database.cursor.execute("""
                SELECT * FROM bill
                WHERE appointment_id = ?
            """,(self.appointment_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to find the bill linked to this appointment.{RESET}")
            return

        bill_record = self.database.cursor.fetchone()

        if bill_record:
            print(f"{ERROR}This appointment already has an existing bill.{RESET}")
            return

        print(f"{DISPLAY_INFO}This appointment does not have a previous bill.{RESET}")

        # Find the one prescription associated with the one appointment.
        try:
            self.database.cursor.execute("""
                SELECT * FROM prescription
                WHERE appointment_id = ?
            """,(self.appointment_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to find the prescription. Please try again.{e}{RESET}")
            return 

        prescription_record = self.database.cursor.fetchone()

        if not prescription_record:
            print(f"{ERROR}No prescription is linked to this appointment.{RESET}")
            return

        print(f"{DISPLAY_INFO}A prescription linked to this appointment found.{RESET}")

        # prescription_id was not created in __init__.
        # We create the object attribute here using self and store the ID from the database row.
        
        self.prescription_id = prescription_record[0]
        print(f"Prescription ID:{DISPLAY_INFO} {self.prescription_id}{RESET}")
        print()

        try:
        # This junction table contains prescription_id, medication_id
            self.database.cursor.execute("""
                SELECT * FROM prescription_medication
                WHERE prescription_id = ?
            """,(self.prescription_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to retrieve the prescription medications. Please " 
                    f"try again.{e}{RESET}")
            return

        # A prescription can contain multiple medications, so fetchall() is used.
        prescription_medication_rows = self.database.cursor.fetchall()
    
        if not prescription_medication_rows:
            print(f"{DISPLAY_INFO}No medications are linked to this prescription.{RESET}")
            return

        print(f"{DISPLAY_INFO}The medication/medications " 
              f"linked to this prescription found.{RESET}")
        print()

        # Create empty list
        # Start the bill total at zero.
        bill_items = []
        self.total_amount = 0

        for prescription_medication_row in prescription_medication_rows:
            self.medication_id = prescription_medication_row[2]

            print(f"Medication ID:{DISPLAY_INFO} {self.medication_id}{RESET}")

            try:
                self.database.cursor.execute("""
                    SELECT * FROM medication
                    WHERE medication_id = ?
                """,(self.medication_id,))

            except sqlite3.Error as e:
                print(f"{ERROR}Unable to retrieve the " 
                        f"medications. Please try again.{e}{RESET}")
                return

            medication_record = self.database.cursor.fetchone()

            if not medication_record:
                print(f"{ERROR}No Medication found.{RESET}")
                return
        
            print(f"{DISPLAY_INFO}Medication{medication_record}{RESET}")

        
            self.total_amount += medication_record[2]

            bill_items.append({
                "medication_id": medication_record[0],
                "medication_name": medication_record[1],
                "unit_cost": medication_record[2]
            })

        # Set the initial payement status.
        self.payment_status = "UNPAID"

        # Insert the calculated bill into the database.
        try:
            self.database.cursor.execute("""
                INSERT INTO bill (
                    appointment_id,
                    total_amount,
                    payment_status
                )
                VALUES (?, ?, ?)
            """, (
                self.appointment_id,
                self.total_amount,
                self.payment_status
            ))

            # Get the ID of the newly created bill.
            bill_id = self.database.cursor.lastrowid

            # Save each medication as a separate bill item.
            for item in bill_items:
                self.database.cursor.execute("""
                    INSERT INTO bill_item (
                        bill_id,
                        medication_id,
                        medication_name,
                        unit_cost
                    )
                    VALUES (?, ?, ?, ?)
                """, (
                    bill_id,
                    item["medication_id"],
                    item["medication_name"],
                    item["unit_cost"]
                ))

            # Save the bill and its items together.
            self.database.connection.commit()

        except sqlite3.Error as e:
            # Undo any incomplete database changes.
            self.database.connection.rollback()
            print(
                f"{ERROR}Unable to create the bill. "
                f"Please try again. {e}{RESET}"
            )
            return

        print(f"Bill ID:{DISPLAY_INFO} {bill_id}{RESET}")
        print()

        # Display the newly created bill.
        self.show_bill_details()
        return
      
    def display_all_bills(self):
        try:
        # Retrieve all bills from the database.
            self.database.cursor.execute("SELECT * FROM bill")

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to retrieve bills. Please try again.{e}{RESET}")
            return

        bill_rows = self.database.cursor.fetchall()

        if not bill_rows:
            print(f"{ERROR}No bills are are currently recorded.{RESET}")
            return
        
        for bill_row in bill_rows:
        # Create a Bill object for each database record.
            billing = Bill(
                self.database,
                bill_row[1],
                bill_row[2],
                bill_row[3]
            )
            print(f"Bill ID:{DISPLAY_INFO} {bill_row[0]}{RESET}")
            billing.show_bill_details()

        while True:
            try:
                choice = input(f"{DISPLAY_INFO}Would you like more information " 
                        f"on a particular bill? (Y/N){RESET}").lower()
                if not self.validate_yes_no(choice):
                    print(f"{ERROR}Please enter Y/y for yes or N/n for no.{RESET}")
                    continue
            
                if choice == 'n':
                    print("Goodbye")
                    return
                
                self.appointment_id = int(input(f"{BILLING_MENU}Please enter "
                                    f"the appointment_id: {RESET}"))
                                
                if not self.validate_login_id(self.appointment_id):
                    print(f"{ERROR}Please enter a valid appointment ID.{RESET}")
                    continue 
                break
                            
            except ValueError:
                    print(f"{ERROR}Please enter the appointment ID using numbers only.{RESET}")
                    continue
        try:
            self.database.cursor.execute("""
                SELECT * FROM bill
                WHERE appointment_id = ?
            """,(self.appointment_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to find the bill linked to this appointment.{RESET}")
            return

        bill_record = self.database.cursor.fetchone()

        if not bill_record:
            print(f"{ERROR}This appointment ID does not exist.{RESET}")
            return

        self.bill_id = bill_record[0]
        self.total_amount = bill_record[1]
        self.appointment_id = bill_record[2]
        self.payment_status = bill_record[3]

        self.show_invoice()
        return


    def search_bill(self):
        while True:
            try:
                self.appointment_id = int(input(f"{BILLING_MENU}Please enter the " 
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
            self.database.cursor.execute("""
            SELECT * FROM bill
            WHERE appointment_id = ?
            """,(self.appointment_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to search for the bill. Please try again.{e}{RESET}")
            return

        bill_row = self.database.cursor.fetchone()

        if not bill_row:
            print()
            print(f"{ERROR}No bill was found for this appointment.{RESET}")
            return 
        self.bill_id = bill_row[0]
        self.total_amount = bill_row[1]
        self.appointment_id = bill_row[2]
        self.payment_status = bill_row[3]

        # Display the matching bill.
        self.show_invoice()
        

    def bill_update(self):
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

        # Find the bill associated with the appointment.
        try:
            self.database.cursor.execute("""
            SELECT * FROM bill
            WHERE appointment_id = ?
            """,(self.appointment_id,))

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to retrieve the bill. Please try again.{e}{RESET}")
            return

        bill_row = self.database.cursor.fetchone()
        if not bill_row:
            print(f"{ERROR}Patient bill not found.{RESET}")
            return 
        
        self.total_amount = bill_row[1]
        self.appointment_id = bill_row[2]
        self.payment_status = bill_row[3]

        print(f"Bill ID:{DISPLAY_INFO} {bill_row[0]}{RESET}")
        print()
    
        self.show_bill_details()
        print()

        try:
            self.database.cursor.execute("""
                SELECT
                    patient.patient_id,
                    patient.first_name,
                    patient.surname
                FROM bill
                    INNER JOIN appointment
                        ON bill.appointment_id = appointment.appointment_id
                    INNER JOIN patient
                        ON appointment.patient_id = patient.patient_id
                WHERE bill.appointment_id = ?
                    """, (self.appointment_id,))
        
            bill_listed = self.database.cursor.fetchone()
        
        except sqlite3.Error as e:
                print(f"{ERROR}Unable to retrieve invoice. {e}{RESET}")
                return
        
        if  bill_listed is None:
            print(f"{ERROR}No invoice found for this appointment.{RESET}")
            return
            
        (   
            patient_id,
            patient_first_name,
            patient_surname

        ) = bill_listed

        if self.payment_status == "PAID":
            print(
                    f"{PAID_STATUS}Bill paid already\n"
                    f"Bill ID: {bill_row[0]}\n"
                    f"Patient ID: {patient_id}\n"
                    f"Patient: {patient_first_name} {patient_surname}\n"
                    f"Payment Status: PAID{RESET}"
                )
            return
        
        while True:
        # Ask the user whether the bill has been paid.
            bill_paid = input(f"{DISPLAY_INFO}Does to patient wish to pay " 
                              f"this bill? (Y/N){RESET}").lower()
            if not self.validate_yes_no(bill_paid):
                print(f"{ERROR}Please enter Y/y for yes or N/n for no.{RESET}")
                continue

            if bill_paid == 'n':
                print(
                    f"{UNPAID_STATUS}Bill not paid \n"
                    f"Bill ID: {bill_row[0]}\n"
                    f"Patient ID: {patient_id}\n"
                    f"Patient: {patient_first_name} {patient_surname}\n"
                    f"Payment Status: UNPAID{RESET}"
                    )
                return
            break
                
        # Update the payment status to PAID
        self.payment_status = "PAID"

        try:
            self.database.cursor.execute("""
                UPDATE bill
                SET payment_status = ?
                WHERE appointment_id = ?
            """,(self.payment_status,
                self.appointment_id))
                
        # Save the updated payment status.
            self.database.connection.commit()

        except sqlite3.Error as e:
            print(f"{ERROR}Unable to update the bill. Please try again.{e}{RESET}")
            return

        print(
            f"{PAID_STATUS}Bill Payment Successful\n"
            f"Bill ID: {bill_row[0]}\n"
            f"Patient ID: {patient_id}\n"
            f"Patient: {patient_first_name} {patient_surname}\n"
            f"Payment Status: PAID{RESET}"
        )
        print()

        # Display the updated bill
        self.show_bill_details()
        return


        

        
            


        
        
    