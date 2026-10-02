import pyfiglet
import threading
from database import database
from clock import display_date_time
from patient import Patient
from gp import Gp
from gp_surgery import GpSurgery
from consultant import Consultant
from department import Department
from appointment import Appointment
from appointment_patient import AppointmentPatient
from prescription import Prescription
from prescription_medication import PrescriptionMedication
from medication import Medication
from bill import Bill
from appointment_patient import AppointmentPatient
from colors import(MAIN_MENU_HEADING,ADMIN_MENU,PRACTICE_MENU,
                   GP_MENU,DEPARTMENT_MENU,CONSULTANT_MENU,MEDICATION_MENU,
                   PATIENT_MENU,APPOINTMENT_MENU,A_P_MENU,PRESCRIPTION_MENU,
                   PRESCRIPTION_INSTRUCTIONS_MENU,BILLING_MENU,
                   SUB_MENU_HEADING,SUB_SUB_MENU_HEADING,TREE_SUB,TREE_SUB_SUB,
                   RETURN_GROUP_MENU,RETURN_MAIN_MENU,EXIT,ERROR,RESET)
def menu(database):
    while True:
        # Create and centre the hospital name using PyFiglet.
        # PyFiglet converts normal text into ASCII art and centres each line.
        hospital_name = pyfiglet.figlet_format(
            "HOLLY HOSPITAL",
            font="digital"
        )

        hospital_name = "\n".join(
            line.center(50)
            for line in hospital_name.splitlines()
        )

        print(
            f"{MAIN_MENU_HEADING}"
            f"{hospital_name}"
            f"{RESET}"
        )

        print()
        print("Address: 100 London Rd, Northampton, NN1 1YZ, England, UK".center(50))
        print("Phone: 01604 101010".center(50))
        print("Email:holly-hospital@nhs.net".center(50))
        print()
        print("=== Welcome To The Main Menu of Holly Hospital ===".center(50))
        print()
        print(f"1. {ADMIN_MENU}Hospital Administration{RESET}")
        print("=" *40)
        print(f"2. {PATIENT_MENU}Patient Management{RESET}")
        print("=" *40)
        print(f"3. {APPOINTMENT_MENU}Appointment Management{RESET}")
        print("=" *40)
        print(f"4. {A_P_MENU}Patient & Appointment Information{RESET}")
        print("=" *40)
        print(f"5. {PRESCRIPTION_MENU}Prescription Management{RESET}")
        print("=" *40)
        print(f"6. {BILLING_MENU}Billing Management{RESET}")
        print("=" *40)
        print(f"7. Date & Time")
        print("=" *40)
        print(f"8. {EXIT}Exit{RESET}")
        print("=" *40)

        choice = input("Enter a choice from Main Menu: ")

        if choice == "1":
            hospital_administration(database)

        elif choice == "2":
            patient_management(database)

        elif choice == "3":
            appointment_management(database)

        elif choice == "4":
            appointment_patient_menu(database)

        elif choice == "5":
            prescription_management(database)

        elif choice == "6":
            billing_management(database)

        elif choice == "7":
              stop_event = threading.Event()
              display_date_time(stop_event)

        elif choice == "8":
            print("Exiting Holly Hospital Management System")
            break 

        else:
            print(f"{ERROR}Invalid choice. Please enter a number between 1 and 6.{RESET}")

            input("Press Enter to try again...")

    input("Press Enter to exit Holly Hospital System...")
            
def hospital_administration(database):
    while True:
        print(f"{MAIN_MENU_HEADING}{'+ HOLLY HOSPITAL +'.center(50)}{RESET}")
        print(
                f"{SUB_MENU_HEADING}"
                f"{(TREE_SUB + ' Hospital Administration Menu').center(50)}"
                f"{RESET}"
            )
        print(f"1. {PRACTICE_MENU}Medical Practice Management Of Patient{RESET}")
        print("-" *50)
        print(f"2. {GP_MENU}GP Management Of Patient{RESET}")
        print("-" *50)
        print(f"3. {DEPARTMENT_MENU}Department Management Of Holly Hospital{RESET}")
        print("-" *50)
        print(f"4. {CONSULTANT_MENU}Consultant Management Of Holly Hosptial{RESET}")
        print("-" *50)
        print(f"5. {MEDICATION_MENU}Medication Management Of Holly Hospital{RESET}")
        print("-" *50)
        print(f"6. {RETURN_MAIN_MENU}Return To Main Menu{RESET}")
        print("-" *50)

        choice = input("Enter a choice: ")

        if choice == "1":
            gp_surgery_management(database)

        elif choice == "2":
            gp_management(database)

        elif choice == "3":
            department_management(database)

        elif choice == "4":
            consultant_management(database)

        elif choice == "5":
            medication_management(database)

        elif choice == "6":
            print("Returning to Main Menu")
            break
        
        else:
            print(f"{ERROR}Invalid choice. Please enter a number between 1 and 6.{RESET}")
                        
            input("Press Enter to try again...")


def gp_surgery_management(database):
    while True:
        print(f"{MAIN_MENU_HEADING}{'+ HOLLY HOSPITAL +'.center(50)}{RESET}")
        print(f"{SUB_MENU_HEADING}{TREE_SUB} Hospital Administration Menu{RESET}")
        print(f"{SUB_SUB_MENU_HEADING}{TREE_SUB_SUB} Medical Practice Of Patient Menu{RESET}")
        print("*" *50)
        print(f"1. {PRACTICE_MENU}Insert Medical Practice{RESET}")
        print("*" *50)
        print(f"2. {PRACTICE_MENU}Search Medical Practice{RESET}")
        print("*" *50)
        print(f"3. {PRACTICE_MENU}Update Medical Practice{RESET}")
        print("*" *50)
        print(f"4. {PRACTICE_MENU}Delete Medical Practice{RESET}")
        print("*" *50)
        print(f"5. {PRACTICE_MENU}Display All Patient Medical Practices{RESET}")
        print("*" *50)
        print(f"6. {RETURN_GROUP_MENU}Return To Hospital Administration Menu{RESET}")
        print("*" *50)

        choice = input("Enter a choice: ")

        if choice == "1":
            gpsurgery = GpSurgery(database)
            gpsurgery.create_gpsurgery()

        elif choice == "2":
            gpsurgery = GpSurgery(database)
            gpsurgery.search_gpsurgery()

        elif choice == "3":
            gpsurgery = GpSurgery(database)
            gpsurgery.update_gpsurgery()

        elif choice == "4":
            gpsurgery = GpSurgery(database)
            gpsurgery.delete_gpsurgery()

        elif choice == "5":
            gpsurgery = GpSurgery(database)
            gpsurgery.display_all_gpsurgery()

        elif choice == "6":
            print("Returning to Hospital Administration Menu...")
            break 

        else:
            print(f"{ERROR}Invalid choice. Please enter a number between 1 and 6.{RESET}")
            
            input("Press Enter to try again...")


def gp_management():
    while True:
        print(f"{MAIN_MENU_HEADING}{'+ HOLLY HOSPITAL +'.center(50)}{RESET}") 
        print(f"{SUB_MENU_HEADING}{TREE_SUB} Hospital Administration Menu{RESET}")
        print(f"{SUB_SUB_MENU_HEADING}{TREE_SUB_SUB} GP Of Patient Menu{RESET}")
        print("*" *45)
        print(f"1. {GP_MENU}Insert GP{RESET}")
        print("*" *45)
        print(f"2. {GP_MENU}Search GP{RESET}")
        print("*" *45)
        print(f"3. {GP_MENU}Update GP{RESET}")
        print("*" *45)
        print(f"4. {GP_MENU}Delete GP{RESET}")
        print("*" *45)
        print(f"5. {GP_MENU}Display All Patient GP's{RESET}")
        print("*" *45)
        print(f"6. {RETURN_GROUP_MENU}Return To Hospital Administration Menu{RESET}")
        print("*" *45)

        choice = input("Enter a choice: ")

        if choice == "1":
            gp = Gp(database)
            gp.create_gp()

        elif choice == "2":
            gp = Gp(database)
            gp.search_gp()

        elif choice == "3":
            gp = Gp(database)
            gp.update_gp()

        elif choice == "4":
            gp = Gp(database)
            gp.delete_gp()

        elif choice == "5":
            gp = Gp(database)
            gp.display_all_gps()

        elif choice == "6":
            print("Returning to Hospital Administration Menu")
            break 
        else:
            print(f"{ERROR}Invalid choice. Please enter a number between 1 and 6.{RESET}")
            
            input("Press Enter to try again...")


def department_management(database):
    while True:
        print(f"{MAIN_MENU_HEADING}{'+ HOLLY HOSPITAL +'.center(50)}{RESET}")
        print(f"{SUB_MENU_HEADING}{TREE_SUB} Hospital Administration Menu{RESET}")
        print(f"{SUB_SUB_MENU_HEADING}{TREE_SUB_SUB} Department Of Holly Hospital Menu{RESET}")
        print("*" *50)
        print(f"1. {DEPARTMENT_MENU}Insert Department{RESET}")
        print("*" *50)
        print(f"2. {DEPARTMENT_MENU}Search Department{RESET}")
        print("*" *50)
        print(f"3. {DEPARTMENT_MENU}Update Department{RESET}")
        print("*" *50)
        print(f"4. {DEPARTMENT_MENU}Delete Department{RESET}")
        print("*" *50)
        print(f"5. {DEPARTMENT_MENU}Display All Hospital Departments{RESET}")
        print("*" *50)
        print(f"6. {RETURN_GROUP_MENU}Return To Hospital Administration Menu{RESET}")
        print("*" *50)

        choice = input("Enter a choice: ")

        if choice == "1":
            department = Department(database)
            department.create_department()

        elif choice == "2":
            department = Department(database)
            department.search_department()

        elif choice == "3":
            department = Department(database)
            department.update_department()

        elif choice == "4":
            department = Department(database)
            department.delete_department()

        elif choice == "5":
            department = Department(database)
            department.display_all_departments()

        elif choice == "6":
            print("Returning to Hospital Administration Menu")
            break

        else:
            print(f"{ERROR}Invalid choice. Please enter a number between 1 and 6.{RESET}")
                        
            input("Press Enter to try again...")

            
def consultant_management(database):
    while True:
        print(f"{MAIN_MENU_HEADING}{'+ HOLLY HOSPITAL +'.center(50)}{RESET}")
        print(f"{SUB_MENU_HEADING}{TREE_SUB} Hospital Administration Menu{RESET}")
        print(f"{SUB_SUB_MENU_HEADING}{TREE_SUB_SUB} Consultant of Holly Hospital Menu{RESET}")
        print("*" *50)
        print(f"1. {CONSULTANT_MENU}Insert Consultant{RESET}")
        print("*" *50)
        print(f"2. {CONSULTANT_MENU}Search Consultant{RESET}")
        print("*" *50)
        print(f"3. {CONSULTANT_MENU}Update Consultant{RESET}")
        print("*" *50)
        print(f"4. {CONSULTANT_MENU}Delete Consultant{RESET}")
        print("*" *50)
        print(f"5. {CONSULTANT_MENU}Display All Hospital Consultants{RESET}")
        print("*" *50)
        print(f"6. {RETURN_GROUP_MENU}Return To Hospital Administration Menu{RESET}")
        print("*" *50)

        choice = input("Enter a choice: ")

        if choice == "1":
            consultant = Consultant(database)
            consultant.create_consultant()

        elif choice == "2":
            consultant = Consultant(database)
            consultant.search_consultant()

        elif choice == "3":
            consultant = Consultant(database)
            consultant.update_consultant()

        elif choice == "4":
            consultant = Consultant(database)
            consultant.delete_consultant()

        elif choice == "5":
            consultant = Consultant(database)
            consultant.display_all_consultants()

        elif choice == "6":
            print("Returning to Hospital Administration Menu")
            break 

        else:
            print(f"{ERROR}Invalid choice. Please enter a number between 1 and 6.{RESET}")
            
            input("Press Enter to try again...")


def medication_management(database):
    while True:
        print(f"{MAIN_MENU_HEADING}{'+ HOLLY HOSPITAL +'.center(50)}{RESET}")
        print(f"{SUB_MENU_HEADING}{TREE_SUB} Hospital Administration Menu{RESET}")
        print(f"{SUB_SUB_MENU_HEADING}{TREE_SUB_SUB} Medication of Holly Hospital Menu{RESET}")
        print("*" *50)
        print(f"1. {MEDICATION_MENU}Insert Medication{RESET}")
        print("*" *50)
        print(f"2. {MEDICATION_MENU}Search Medication{RESET}")
        print("*" *50)
        print(f"3. {MEDICATION_MENU}Update Medication{RESET}")
        print("*" *50)
        print(f"4. {MEDICATION_MENU}Delete Medication{RESET}")
        print("*" *50)
        print(f"5. {MEDICATION_MENU}Display All Hospital Medications{RESET}")
        print("*" *50)
        print(f"6. {RETURN_GROUP_MENU}Return to Hospital Administration Menu{RESET}")
        print("*" *50)

        choice = input("Enter a choice: ")

        if choice == "1":
            medication = Medication(database)
            medication.create_medication()

        elif choice == "2":
            medication = Medication (database)
            medication.search_medication()

        elif choice == "3":
            medication = Medication(database)
            medication.update_medication()

        elif choice == "4":
            medication = Medication(database)
            medication.delete_medication()

        elif choice == "5":
            medication = Medication(database)
            medication.display_all_medications()

        elif choice == "6":
            print("Returning to Hospital Administration Menu")
            break

        else:
            print(f"{ERROR}Invalid choice. Please enter a number between 1 and 6.{RESET}")
                        
            input("Press Enter to try again...")


def patient_management(database):
    while True:
        print(f"{MAIN_MENU_HEADING}{'+ HOLLY HOSPITAL +'.center(50)}{RESET}")
        print(
                f"{SUB_MENU_HEADING}"
                f"{(TREE_SUB + ' Patient Menu').center(50)}"
                f"{RESET}"
            )
        print("*" *40)
        print(f"1. {PATIENT_MENU}Insert Patient Data{RESET}")
        print("*" *40)
        print(f"2. {PATIENT_MENU}Search Patient Data{RESET}")
        print("*" *40)
        print(f"3. {PATIENT_MENU}Update Patient Data{RESET}")
        print("*" *40)
        print(f"4. {PATIENT_MENU}Delete Patient Data{RESET}")
        print("*" *40)
        print(f"5. {PATIENT_MENU}Display All Patients Data{RESET}")
        print("*" *40)
        print(f"6. {RETURN_MAIN_MENU}Return to Main Menu{RESET}")
        print("*" *40)

        choice = input("Enter a choice: ")


        if choice == "1":
            patient = Patient(database)
            patient.create_patient()

        elif choice == "2":
            patient = Patient(database)
            patient.search_patient()

        elif choice == "3":
            patient = Patient(database)
            patient.update_patient()

        elif choice == "4":
            patient = Patient(database)
            patient.delete_patient()

        elif choice == "5":
            patient = Patient(database)
            patient.display_all_patients()

        elif choice == "6":
            print("Returning to Main Menu")
            break

        else:
            print(f"{ERROR}Invalid choice. Please enter a number between 1 and 6.{RESET}")
            
            input("Press Enter to try again...")


def appointment_management(database):
    while True:
        print(f"{MAIN_MENU_HEADING}{'+ HOLLY HOSPITAL +'.center(50)}{RESET}")
        print(
                f"{SUB_MENU_HEADING}"
                f"{(TREE_SUB + ' Appointment Menu').center(50)}"
                f"{RESET}"
            )
        print("*" *45)
        print(f"1. {APPOINTMENT_MENU}Insert Appointment{RESET}")
        print("*" *45)
        print(f"2. {APPOINTMENT_MENU}Search Appointment{RESET}")
        print("*" *45)
        print(f"3. {APPOINTMENT_MENU}Update Appointment{RESET}")
        print("*" *45)
        print(f"4. {APPOINTMENT_MENU}Delete Appointment{RESET}")
        print("*" *45)
        print(f"5. {APPOINTMENT_MENU}Display All Hospital Appointments{RESET}")
        print("*" *45)
        print(f"6. {RETURN_MAIN_MENU}Return to Main Menu{RESET}")
        print("*" *45)

        choice = input("Enter a choice: ")

        if choice == "1":
            appointment = Appointment(database)
            appointment.create_appointment()

        elif choice == "2":
            appointment = Appointment(database)
            appointment.search_appointment()

        elif choice == "3":
            appointment = Appointment(database)
            appointment.update_appointment()

        elif choice == "4":
            appointment = Appointment(database)
            appointment.delete_appointment()

        elif choice == "5":
            appointment = Appointment(database)
            appointment.display_all_appointments()

        elif choice == "6":
            print("Returning to Main Menu")
            break

        else:
            print(f"{ERROR}Invalid choice. Please enter a number between 1 and 6.{RESET}")
                        
            input("Press Enter to try again...")


def appointment_patient_menu(database):
    while True:
        print(f"{MAIN_MENU_HEADING}{'+ HOLLY HOSPITAL +'.center(50)}{RESET}")
        print()
        print(
                f"{SUB_MENU_HEADING}"
                f"{(TREE_SUB + 'Patient & Appointment Information').center(50)}"
                f"{RESET}"
            )
        print("*" *80)
        print(f"1. {A_P_MENU}Patients with Appointments(INNER JOIN).{RESET}")
        print("*" *80)
        print(f"2. {A_P_MENU}All Patients, including those " 
              f"without Appointments(LEFT JOIN).{RESET}")
        print("*" *80)
        print(f"3. {A_P_MENU}All Patients and Appointments Including "
              f"Unmatched(FULL OUTER JOIN).{RESET}")
        print("*" *80)
        print(f"4. {A_P_MENU}Patient, Appointment & Consultant Information.{RESET}")
        print("*" *80)
        print(f"5. {A_P_MENU}Patient, Appointment, Consultant & "
              f"Department Information.{RESET}")
        print("*" *80)
        print(f"6. {A_P_MENU}Patient, GP & Medical Practice.{RESET}")
        print("*" *80)
        print(f"7. {A_P_MENU}Prescription & Medication Data "
              f"(MANY TO MANY DATABASE RELATIONSHIP).{RESET}")
        print("*" *80)
        print(f"8. {A_P_MENU}Prescription Medication Statistics(Advanced SQL Queries).{RESET}")
        print("*" *80)
        print(f"9. {A_P_MENU}Advanced Prescription Searches(Advanced SQL Subqueries).{RESET}")
        print("*" *80)
        print(f"10. {RETURN_MAIN_MENU}Return to Main Menu.{RESET}")
        print("*" *80)

        choice = input("Enter choice: ")

        if choice == "1":
            appointment_patient = AppointmentPatient(database)
            appointment_patient.display_patients_with_appointments()

        elif choice == "2":
            appointment_patient = AppointmentPatient(database)
            appointment_patient.display_all_patients_with_or_without_appointments()

        elif choice == "3":
            appointment_patient = AppointmentPatient(database)
            appointment_patient.display_all_patients_and_appointments_including_unmatched()

        elif choice == "4":
            appointment_patient = AppointmentPatient(database)
            appointment_patient.display_patient_appointment_consultant()

        elif choice == "5":
            appointment_patient = AppointmentPatient(database)
            appointment_patient.display_patient_appointment_consultant_department()

        elif choice == "6":
            appointment_patient = AppointmentPatient(database)
            appointment_patient.display_patient_gp_gp_surgery()

        elif choice == "7":
            appointment_patient = AppointmentPatient(database)
            appointment_patient.display_prescription_medications()

        elif choice == "8":
            appointment_patient = AppointmentPatient(database)
            appointment_patient.display_advanced_queries()

        elif choice == "9":
            appointment_patient = AppointmentPatient(database)
            appointment_patient.display_advanced_queries()

        elif choice == "10":
            print("Returning to the main menu.")
            break

        else:
            print(f"{ERROR}Invalid choice. Please enter a number between 1 and 9.{RESET}")
                                    
            input("Press Enter to try again...")


def prescription_management(database):
    while True:
        print(f"{MAIN_MENU_HEADING}{'+ HOLLY HOSPITAL +'.center(50)}{RESET}")
        print(
                f"{SUB_MENU_HEADING}"
                f"{(TREE_SUB + ' Prescription Menu').center(50)}"
                f"{RESET}"
            )
        print("*" *45)
        print(f"1. {PRESCRIPTION_MENU}Insert Prescription{RESET}")
        print("*" *45)
        print(f"2. {PRESCRIPTION_MENU}Search Prescription{RESET}")
        print("*" *45)
        print(f"3. {PRESCRIPTION_MENU}Delete Prescription{RESET}")
        print("*" *45)
        print(f"4. {PRESCRIPTION_MENU}Display All Hospital Prescriptions{RESET}")
        print("*" *45)
        print(f"5. {PRESCRIPTION_MENU}Prescribe The Medication{RESET}")
        print("*" *45)
        print(f"6. {RETURN_MAIN_MENU}Return to Main Menu{RESET}")
        print("*" *45)

        choice = input("Enter a choice: ")

        if choice == "1":
            prescription = Prescription(database)
            prescription.create_prescription()

        elif choice == "2":
            prescription = Prescription(database)
            prescription.search_prescription()

        elif choice == "3":
            prescription = Prescription(database)
            prescription.delete_prescription()

        elif choice == "4":
            prescription = Prescription(database)
            prescription.display_all_prescriptions()

        elif choice == "5":
            prescription_instructions_management(database)

        elif choice == "6":
            print("Returning to Main Menu")
            break

        else:
            print(f"{ERROR}Invalid choice. Please enter a number between 1 and 6.{RESET}")
                        
            input("Press Enter to try again...")


def prescription_instructions_management(database):
    while True:
        print(f"{MAIN_MENU_HEADING}{'+ HOLLY HOSPITAL +'.center(50)}{RESET}")
        print(f"{SUB_MENU_HEADING}{TREE_SUB} Hospital Administration Menu{RESET}")
        print(f"{SUB_SUB_MENU_HEADING}{TREE_SUB_SUB} Prescribe Medication Menu{RESET}")
        print("*" *80)
        print(f"1. {PRESCRIPTION_INSTRUCTIONS_MENU}Insert Prescription Instructions{RESET}")
        print("*" *80)
        print(f"2. {PRESCRIPTION_INSTRUCTIONS_MENU}Search Prescription Instructions{RESET}")
        print("*" *80)
        print(f"3. {PRESCRIPTION_INSTRUCTIONS_MENU}Update Prescription Instructions{RESET}")
        print("*" *80)
        print(
                f"4. {PRESCRIPTION_INSTRUCTIONS_MENU}Display All "
                f"Hospital Prescription Instructions{RESET}"
                )
        print("*" *80)
        print(f"5. {PRESCRIPTION_INSTRUCTIONS_MENU}Delete Prescription Instructions{RESET}")
        print("*" *80)
        print(f"6. {RETURN_GROUP_MENU}Return to Hospital Prescription Menu{RESET}")
        print("*" *80)

        choice = input("Enter a choice: ")

        if choice == "1":
            instructions = PrescriptionMedication(database)
            instructions.create_prescription_medication()

        elif choice == "2":
            instructions = PrescriptionMedication(database)
            instructions.search_prescription_medication()

        elif choice == "3":
            instructions = PrescriptionMedication(database)
            instructions.update_prescription_medication()

        elif choice == "4":
            instructions = PrescriptionMedication(database)
            instructions.display_all_prescription_medications()

        elif choice == "5":
            instructions = PrescriptionMedication(database)
            instructions.delete_prescription_medication()

        elif choice == "6":
            print("Returning to Prescription Menu")
            break 

        else:
            print(f"{ERROR}Invalid choice. Please enter a number between 1 and 5.{RESET}")
                        
            input("Press Enter to try again...")


def billing_management(database):
    while True:
        print(f"{MAIN_MENU_HEADING}{'+ HOLLY HOSPITAL +'.center(50)}{RESET}")
        print(
                f"{SUB_MENU_HEADING}"
                f"{(TREE_SUB + ' Billing Menu').center(50)}"
                f"{RESET}"
            )
        print("*" *45)
        print(f"1. {BILLING_MENU}Insert Billing{RESET}")
        print("*" *45)
        print(f"2. {BILLING_MENU}Search Billing{RESET}")
        print("*" *45)
        print(f"3. {BILLING_MENU}Update Billing{RESET}")
        print("*" *45)
        print(f"4. {BILLING_MENU}Display All Hospital Billings{RESET}")
        print("*" *45)
        print(f"5. {RETURN_MAIN_MENU}Return to Main Menu{RESET}")
        print("*" *45)

        choice = input("Enter a choice:")

        if choice == "1":
            bill = Bill(database)
            bill.create_bill()

        elif choice == "2":
            bill = Bill(database)
            bill.search_bill()

        elif choice == "3":
            bill = Bill(database)
            bill.bill_update()

        elif choice == "4":
            bill = Bill(database)
            bill.display_all_bills()

        elif choice == "5":
            print("Returning to Main Menu")
            break 

        else:
            print(f"{ERROR}Invalid choice. Please enter a number between 1 and 5.{RESET}")
                        
            input("Press Enter to try again...")










