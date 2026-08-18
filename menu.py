from patient import Patient
from gp import Gp
from gp_surgery import GpSurgery
from consultant import Consultant
from department import Department
from appointment import Appointment
from prescription import Prescription
from prescription_medication import PrescriptionMedication
from medication import Medication
from bill import Bill

def menu():
    while True:
        print("=== Holly Hospital ===".center(50))
        print("=== Welcome to the Main Menu ===".center(50))
        print("1. Hospital Administration")
        print("2. Patient Management")
        print("3. Appointment Management")
        print("4. Prescription Management")
        print("5. Billing Management")
        print("6. Exit")

        choice = input("Enter a choice from Main Menu: ")

        if choice == "1":
            hospital_administration()

        elif choice == "2":
            patient_management()

        elif choice == "3":
            appointment_management()

        elif choice == "4":
            prescription_management()

        elif choice == "5":
            billing_management()

        elif choice == "6":
            print("Exiting Holly Hospital Management System")
            break 

        else:
            print("\nInvalid choice. Please enter " \
            "a number between 1 and 6.")

            input("Press Enter to try again...")

    input("Press Enter to exit Holly Hospital System...")
            
def hospital_administration():
    while True:
        print("--- Holly Hospital ---".center(50))
        print("--- Hospital Administration Menu ---".center(50))
        print("1. Patient Medical Practice Management")
        print("2. Patient GP Management")
        print("3. Department Management")
        print("4. Consultant Management")
        print("5. Medication Management")
        print("6. Return to Main Menu")

        choice = input("Enter a choice: ")

        if choice == "1":
            gp_surgery_management()

        elif choice == "2":
            gp_management()

        elif choice == "3":
            department_management()

        elif choice == "4":
            consultant_management()

        elif choice == "5":
            medication_management()

        elif choice == "6":
            print("Returning to Main Menu")
            break
        
        else:
            print("\nInvalid choice. Please enter " \
            "a number between 1 and 6.")
                        
            input("Press Enter to try again...")

    input("Press Enter to return to the Main Menu...")

def gp_surgery_management():
    while True:
        print("--- Holly Hospital ---".center(50)) 
        print("--- Patient ---".center(50)) 
        print("--- Medical Practice Menu ---".center(50))
        print("1. Insert Medical Practice")
        print("2. Search Medical Practice")
        print("3. Update Medical Practice")
        print("4. Delete Medical Practice")
        print("5. Display All Patient Medical Practices")
        print("6. Return to Hospital Patient Menu")

        choice = input("Enter a choice: ")

        if choice == "1":
            gpsurgery = GpSurgery()
            gpsurgery.create_gpsurgery()

        elif choice == "2":
            gpsurgery = GpSurgery()
            gpsurgery.search_gpsurgery()

        elif choice == "3":
            gpsurgery = GpSurgery()
            gpsurgery.update_gpsurgery()

        elif choice == "4":
            gpsurgery = GpSurgery()
            gpsurgery.delete_gpsurgery()

        elif choice == "5":
            gpsurgery = GpSurgery()
            gpsurgery.display_all_gpsurgery()

        elif choice == "6":
            print("Returning to Hospital Administration Menu...")
            break 

        else:
            print("\nInvalid choice. Please enter " \
            "a number between 1 and 6.")
            
            input("Press Enter to try again...")

    input("Press Enter to return to the Hospital Administration Menu...")

def gp_management():
    while True:
        print("--- Holly Hospital ---".center(50)) 
        print("--- Patient ---".center(50))
        print("--- GP Menu ---".center(50))
        print("1. Insert GP")
        print("2. Search GP")
        print("3. Update GP")
        print("4. Delete GP")
        print("5. Display All Patient GP's")
        print("6. Return to Hospital Patient Menu ")

        choice = input("Enter a choice: ")

        if choice == "1":
            gp = Gp()
            gp.create_gp()

        elif choice == "2":
            gp = Gp()
            gp.search_gp()

        elif choice == "3":
            gp = Gp()
            gp.update_gp()

        elif choice == "4":
            gp = Gp()
            gp.delete_gp()

        elif choice == "5":
            gp = Gp()
            gp.display_all_gps()

        elif choice == "6":
            print("Returning to Hospital Administration Menu")
            break 
        else:
            print("\nInvalid choice. Please enter " \
            "a number between 1 and 6.")
            
            input("Press Enter to try again...")

    input("Press Enter to return to the Hospital Administration Menu...")

def department_management():
    while True:
        print("--- Holly Hospital ---".center(50))
        print("--- Department Menu ---".center(50))
        print("1. Insert Department")
        print("2. Search Department")
        print("3. Update Department")
        print("4. Delete Department")
        print("5. Display All Hospital Departments")
        print("6. Return to Main Menu")

        choice = input("Enter a choice: ")

        if choice == "1":
            department = Department()
            department.create_department()

        elif choice == "2":
            department = Department()
            department.search_department()

        elif choice == "3":
            department = Department()
            department.update_department()

        elif choice == "4":
            department = Department()
            department.delete_department()

        elif choice == "5":
            department = Department()
            department.display_all_departments()

        elif choice == "6":
            print("Returning to Main Menu")
            break

        else:
            print("\nInvalid choice. Please enter " \
            "a number between 1 and 6.")
                        
            input("Press Enter to try again...")

    input("Press Enter to return to the Hospital Administration Menu...")
            
def consultant_management():
    while True:
        print("--- Holly Hospital ---".center(50))
        print("--- Consultant Menu ---".center(50))
        print("1. Insert Consultant")
        print("2. Search Consultant")
        print("3. Update Consultant")
        print("4. Delete Consultant")
        print("5. Display All Hospital Consultants")
        print("6. Return to Main Menu")

        choice = input("Enter a choice: ")

        if choice == "1":
            consultant = Consultant()
            consultant.create_consultant()

        elif choice == "2":
            consultant = Consultant()
            consultant.search_consultant()

        elif choice == "3":
            consultant = Consultant()
            consultant.update_consultant()

        elif choice == "4":
            consultant = Consultant()
            consultant.delete_consultant()

        elif choice == "5":
            consultant = Consultant()
            consultant.display_all_consultants()

        elif choice == "6":
            print("Returning to Main Menu")
            break 

        else:
            print("\nInvalid choice. Please enter " \
            "a number between 1 and 6.")
            
            input("Press Enter to try again...")

    input("Press Enter to return to the Hospital Administration Menu...")

def medication_management():
    while True:
        print("--- Holly Hospital ---".center(50))
        print("--- Medication Menu ---".center(50))
        print("1. Insert Medication")
        print("2. Search Medication")
        print("3. Update Medication")
        print("4. Delete Medication")
        print("5. Display All Hospital Medications")
        print("6. Return to Main Menu")

        choice = input("Enter a choice: ")

        if choice == "1":
            medication = Medication()
            medication.create_medication()

        elif choice == "2":
            medication = Medication ()
            medication.search_medication()

        elif choice == "3":
            medication = Medication()
            medication.update_medication()

        elif choice == "4":
            medication = Medication()
            medication.delete_medication()

        elif choice == "5":
            medication = Medication()
            medication.display_all_medications()

        elif choice == "6":
            print("Returning to Main Menu")
            break

        else:
            print("\nInvalid choice. Please enter " \
            "a number between 1 and 6.")
                        
            input("Press Enter to try again...")

    input("Press Enter to return to the Hospital Administration Menu...")

def patient_management():
    while True:
        print("--- Holly Hospital ---".center(50)) 
        print("--- Patient Menu ---".center(50))
        print("1. Insert Patient Data")
        print("2. Search Patient Data")
        print("3. Update Patient Data")
        print("4. Delete Patient Data")
        print("5. Display All Patients Data")
        print("6. Return to Main Menu")

        choice = input("Enter a choice: ")


        if choice == "1":
            patient = Patient()
            patient.create_patient()

        elif choice == "2":
            patient = Patient()
            patient.search_patient()

        elif choice == "3":
            patient = Patient()
            patient.update_patient()

        elif choice == "4":
            patient = Patient()
            patient.delete_patient()

        elif choice == "5":
            patient = Patient()
            patient.display_all_patients()

        elif choice == "6":
            print("Returning to Main Menu")
            break

        else:
            print("\nInvalid choice. Please enter " \
            "a number between 1 and 6.")
            
            input("Press Enter to try again...")

    input("Press Enter to return to the Main Menu...")

def appointment_management():
    while True:
        print("--- Holly Hospital ---".center(50))
        print("--- Appointment Menu ---".center(50))
        print("1. Insert Appointment")
        print("2. Search Appointment")
        print("3. Update Appointment")
        print("4. Delete Appointment")
        print("5. Display All Hospital Appointments")
        print("6. Return to Main Menu")

        choice = input("Enter a choice: ")

        if choice == "1":
            appointment = Appointment()
            appointment.create_appointment()

        elif choice == "2":
            appointment = Appointment ()
            appointment.search_appointment()

        elif choice == "3":
            appointment = Appointment()
            appointment.update_appointment()

        elif choice == "4":
            appointment = Appointment()
            appointment.delete_appointment()

        elif choice == "5":
            appointment = Appointment()
            appointment.display_all_appointments()

        elif choice == "6":
            print("Returning to Main Menu")
            break

        else:
            print("\nInvalid choice. Please enter " \
            "a number between 1 and 6.")
                        
            input("Press Enter to try again...")

    input("Press Enter to return to the Main Menu...")

def prescription_management():
    while True:
        print("--- Holly Hospital ---".center(50))
        print("--- Prescription Menu ---".center(50))
        print("1. Insert Prescription")
        print("2. Search Prescription")
        print("3. Delete Prescription")
        print("4. Display All Hospital Prescriptions")
        print("5. Prescription Instructions Management")
        print("6. Return to Main Menu")

        choice = input("Enter a choice: ")

        if choice == "1":
            prescription = Prescription()
            prescription.create_prescription()

        elif choice == "2":
            prescription = Prescription()
            prescription.search_prescription()

        elif choice == "3":
            prescription = Prescription()
            prescription.delete_prescription()

        elif choice == "4":
            prescription = Prescription()
            prescription.display_all_prescriptions()

        elif choice == "5":
            prescription_instructions_management()

        elif choice == "6":
            print("Returning to Main Menu")
            break

        else:
            print("\nInvalid choice. Please enter " \
            "a number between 1 and 6.")
                        
            input("Press Enter to try again...")

    input("Press Enter to return to the Main Menu...")

def prescription_instructions_management():
    while True:
        print("--- Holly Hospital ---".center(50))
        print("--- Prescription ---".center(50))
        print("--- Instructions Menu ---".center(50))
        print("1. Insert Prescription Instructions")
        print("2. Search Prescription Instructions")
        print("3. Update Prescription Instructions")
        print("4. Display All Hospital Prescription Instructions")
        print("5. Delete Prescription Instructions")
        print("6. Return to Hospital Prescription Menu")

        choice = input("Enter a choice: ")

        if choice == "1":
            instructions = PrescriptionMedication()
            instructions.create_prescription_medication()

        elif choice == "2":
            instructions = PrescriptionMedication()
            instructions.search_prescription_medication()

        elif choice == "3":
            instructions = PrescriptionMedication()
            instructions.update_prescription_medication()

        elif choice == "4":
            instructions = PrescriptionMedication()
            instructions.display_all_prescription_medications()

        elif choice == "5":
            instructions = PrescriptionMedication()
            instructions.delete_prescription_medication()

        elif choice == "6":
            print("Returning to Prescription Menu")
            break 

        else:
            print("\nInvalid choice. Please enter " \
            "a number between 1 and 5.")
                        
            input("Press Enter to try again...")

    input("Press Enter to return to the Prescription Menu...")

def billing_management():
    while True:
        print("--- Holly Hospital ---".center(50))
        print("--- Billing Menu ---".center(50))
        print("1. Insert Billing")
        print("2. Search Billing")
        print("3. Update Billing")
        print("4. Display All Hospital Billings")
        print("5. Return to Main Menu")

        choice = input("Enter a choice:")

        if choice == "1":
            bill = Bill()
            bill.create_bill()

        elif choice == "2":
            bill = Bill()
            bill.search_bill()

        elif choice == "3":
            bill = Bill()
            bill.bill_update()

        elif choice == "4":
            bill = Bill()
            bill.display_all_bills()

        elif choice == "5":
            print("Returning to Main Menu")
            break 

        else:
            print("\nInvalid choice. Please enter " \
            "a number between 1 and 5.")
                        
            input("Press Enter to try again...")

    input("Press Enter to return to the Main Menu...")









