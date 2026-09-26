import sqlite3
from database import conn, cursor
from colors import DISPLAY_INFO,A_P_MENU,ERROR,RESET


class AppointmentPatient():
    def display_patients_with_appointments(self):
        try:
            cursor.execute("""

                SELECT  patient.first_name,
                        patient.surname,
                        appointment.appointment_date,
                        appointment.appointment_time

                FROM    patient

                INNER JOIN  appointment

                ON  patient.patient_id = appointment.patient_id 

                ORDER BY    substr(appointment.appointment_date,7,4),
                            substr(appointment.appointment_date,4,2),
                            substr(appointment.appointment_date,1,2)
            """)

        except sqlite3.Error as e:
            print(f"{ERROR}Database Error{RESET}",e)
            return 

        rows = cursor.fetchall()

        for row in rows:
            (first_name, surname,
            appointment_date,appointment_time) = row

            print("=" *40)
            print(f"{DISPLAY_INFO}Patient: {first_name} {surname}{RESET}")
            print(f"{DISPLAY_INFO}Date: {appointment_date}{RESET}")
            print(f"{DISPLAY_INFO}Time: {appointment_time}{RESET}")
            print("-"*40)
            print()

    def display_all_patients_with_or_without_appointments(self):
        try:
            cursor.execute("""

                SELECT  patient.first_name,
                        patient.surname,
                        appointment.appointment_date,
                        appointment.appointment_time
            
                FROM    patient

                LEFT JOIN   appointment

                ON  patient.patient_id = appointment.patient_id

                ORDER BY    substr(appointment.appointment_date,7,4),
                            substr(appointment.appointment_date,4,2),
                            substr(appointment.appointment_date,1,2)
            """)

        except sqlite3.Error as e:
            print(f"{ERROR}Database Error{RESET}", e)
            return

        rows = cursor.fetchall()

        for row in rows:
            (first_name,surname,
            appointmemt_date,appointment_time) = row

            print("=" *40)
            print(f"{DISPLAY_INFO}Patient: {first_name} {surname}{RESET}")
            print(f"{DISPLAY_INFO}Date: {appointmemt_date}{RESET}")
            print(f"{DISPLAY_INFO}Time: {appointment_time}{RESET}")
            print("-"*40)
            print()

    def display_all_patients_and_appointments_including_unmatched(self):
        try:
            cursor.execute("""

                SELECT  *

                FROM
                (
            
                    SELECT  patient.first_name,
                            patient.surname,
                            appointment.appointment_date,
                            appointment.appointment_time
                
                    FROM    patient

                    LEFT JOIN  appointment

                    ON  patient.patient_id = appointment.patient_id

                    UNION

                    SELECT  patient.first_name,
                            patient.surname,
                            appointment.appointment_date,
                            appointment.appointment_time
                
                    FROM    appointment

                    LEFT JOIN   patient

                    ON  appointment.patient_id = patient.patient_id
                
                )
                ORDER BY    substr(appointment_date,7,4),
                            substr(appointment_date,4,2),
                            substr(appointment_date,1,2)

            """)

        except sqlite3.Error as e:
            print(f"{ERROR}Database Error{RESET}", e)
            return

        rows = cursor.fetchall()

        for row in rows:
            (first_name, surname, 
             appointment_date, appointment_time) = row

            print("=" * 40)
            print(f"{DISPLAY_INFO}Patient: {first_name} {surname}{RESET}")
            print(f"{DISPLAY_INFO}Date: {appointment_date}{RESET}")
            print(f"{DISPLAY_INFO}Time: {appointment_time}{RESET}")
            print("-"*40)
            print()

    def display_patient_appointment_consultant(self):
        try:
            cursor.execute("""

                SELECT  appointment.appointment_date,
                        appointment.appointment_time,
                        patient.first_name,
                        patient.surname,
                        consultant.first_name,
                        consultant.surname
                
                FROM   appointment

                INNER JOIN   patient
                    ON  appointment.patient_id = patient.patient_id
                            
                INNER JOIN   consultant
                    ON  appointment.consultant_id = consultant.consultant_id
                
                ORDER BY    substr(appointment.appointment_date,7,4),
                            substr(appointment.appointment_date,4,2),
                            substr(appointment.appointment_date,1,2)

            """)

        except sqlite3.Error as e:
            print(f"{ERROR}Database Error{RESET}", e)
            return

        rows = cursor.fetchall()

        for row in rows:
            (appointment_date, appointment_time,
             p_first_name, p_surname,
             c_first_name, c_surname) = row

            print("=" * 40)
            print(f"{DISPLAY_INFO}Date: {appointment_date}{RESET}")
            print(f"{DISPLAY_INFO}Time: {appointment_time}{RESET}")
            print(f"{DISPLAY_INFO}Patient: {p_first_name} {p_surname}{RESET}")
            print(f"{DISPLAY_INFO}Consultant: {c_first_name} {c_surname}{RESET}")
            print("-" *40)
            print()

    def display_patient_appointment_consultant_department(self):
        try:
            cursor.execute("""

                SELECT  appointment.appointment_date,
                        appointment.appointment_time,
                        patient.first_name,
                        patient.surname,
                        consultant.first_name,
                        consultant.surname,
                        department.department_name
            
                FROM   appointment

                INNER JOIN   patient
                    ON  appointment.patient_id = patient.patient_id
                
                INNER JOIN   consultant
                    ON  appointment.consultant_id = consultant.consultant_id
                            
                INNER JOIN   department
                    ON  consultant.department_id = department.department_id
                
                ORDER BY    substr(appointment.appointment_date,7,4),
                            substr(appointment.appointment_date,4,2),
                            substr(appointment.appointment_date,1,2)
            
            """)

        except sqlite3.Error as e:
            print(f"{ERROR}Database Error{RESET}", e)
            return

        rows = cursor.fetchall()

        for row in rows:
            (appointment_date, appointment_time,
             p_first_name, p_surname,
             c_first_name, c_surname,
             department_name) = row

            print("=" * 40)
            print(f"{DISPLAY_INFO}Date: {appointment_date}{RESET}")
            print(f"{DISPLAY_INFO}Time: {appointment_time}{RESET}")
            print(f"{DISPLAY_INFO}Patient: {p_first_name} {p_surname}{RESET}")
            print(f"{DISPLAY_INFO}Consultant: {c_first_name} {c_surname}{RESET}")
            print(f"{DISPLAY_INFO}Department: {department_name}{RESET}")
            print("-" *40)
            print()

    def display_patient_gp_gp_surgery(self):
        try:
            cursor.execute("""

            SELECT  patient.first_name,
                    patient.surname,
                    gp.first_name,
                    gp.surname,
                    gp_surgery.surgery_name,
                    gp_surgery.address
            
            FROM    patient

            INNER JOIN  gp
                ON  patient.gp_id = gp.gp_id
            
            INNER JOIN  gp_surgery
                ON  gp.surgery_id = gp_surgery.surgery_id

        """)

        except sqlite3.Error as e:
            print(f"{ERROR}Database Error{RESET}", e)
            return

        rows = cursor.fetchall()

        for row in rows:
            (p_first_name, p_surname,
             gp_first_name, gp_surname,
             gp_surgery, address) = row

            print("=" *40)
            print(f"{DISPLAY_INFO}Patient: {p_first_name} {p_surname}{RESET}")
            print(f"{DISPLAY_INFO}GP: {gp_first_name} {gp_surname}{RESET}")
            print(f"{DISPLAY_INFO}Medical Practice: {gp_surgery}{RESET}")
            print(f"{DISPLAY_INFO}Practice Address: {address}{RESET}")
            print("-" *40)
            print()

    def display_prescription_medications(self):
        try:
            cursor.execute("""

                SELECT  prescription_medication.prescription_id,
                        prescription_medication.medication_id,
                        medication.medication_name
                
                FROM    prescription_medication

                INNER JOIN  prescription
                    ON  prescription_medication.prescription_id = prescription.prescription_id
                
                INNER JOIN medication
                    ON  prescription_medication.medication_id = medication.medication_id
                
                ORDER BY   prescription_medication.prescription_id,
                           prescription_medication.medication_id
                           
            """)

        except sqlite3.Error as e:
            print(f"{ERROR}Database Error{RESET}", e)
            return 

        rows = cursor.fetchall()

        last_prescription_id = None

        for row in rows:
            (prescription_id,medication_id,
             medication_name) = row

            if prescription_id != last_prescription_id:
                print("=" *40)
                print(f"{DISPLAY_INFO}Prescription ID: {prescription_id}{RESET}")
                print("-" *40)
                print()
                last_prescription_id = prescription_id
            print(f"{DISPLAY_INFO}Medication ID: {medication_id}{RESET}")
            print("=" *40)
            print(f"{DISPLAY_INFO}Medication: {medication_name}{RESET}")
            print("-" *40)
            print()

    def display_advanced_queries(self):
        try:
            cursor.execute("""
                SELECT  prescription_medication.prescription_id,
                    COUNT(prescription_medication.medication_id),
                    SUM(medication.cost),
                    AVG(medication.cost)

                FROM    prescription_medication

                INNER JOIN   medication
                    ON    prescription_medication.medication_id = medication.medication_id

                WHERE   prescription_medication.prescription_id != 5

                GROUP BY   prescription_medication.prescription_id

                HAVING  COUNT(prescription_medication.medication_id) > 1
                   AND  SUM(medication.cost) > 20
                   AND  AVG(medication.cost) > 5
                   
                ORDER BY   prescription_medication.prescription_id
            """)

        except sqlite3.Error as e:
                print(f"{ERROR}Database Error{RESET}", e)
                return

        rows = cursor.fetchall()

        for row in rows:
            (prescription_id,medication_count,
             cost,average) = row

            print(f"{DISPLAY_INFO}Prescription ID: {prescription_id}{ERROR}")
            print("=" *40)
            print(f"{DISPLAY_INFO}Medication Count: {medication_count}{ERROR}")
            print(f"{DISPLAY_INFO}Total: {cost}{ERROR}")
            print(f"{DISPLAY_INFO}Average medication cost: {average}{ERROR}")
            print("-" *40)
            print()

    def display_advanced_queries(self):
        try:
            cursor.execute("""
                SELECT  prescription_medication.prescription_id,
                        COUNT(prescription_medication.medication_id)
                
                FROM    prescription_medication

                GROUP BY   prescription_medication.prescription_id

                HAVING COUNT(prescription_medication.medication_id) > (
                    SELECT COUNT(prescription_medication.medication_id)
                    FROM   prescription_medication
                    WHERE   prescription_id = 5
                )
                
                ORDER BY   prescription_medication.prescription_id
            """)

        except sqlite3.Error as e:
            print(f"{ERROR}Database Error{RESET}", e)

        rows = cursor.fetchall()

        for row in rows:
            prescription_id, medication_count = row
            print("=" *40)
            print(f"{DISPLAY_INFO}Prescription ID: {prescription_id}{RESET}")
            print(f"{DISPLAY_INFO}Medication Count: {medication_count}{RESET}")
            print("-" *40)
            print()
    


                
