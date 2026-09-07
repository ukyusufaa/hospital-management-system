import sqlite3

from database import conn, cursor

class AppointmentPatient():
    def display_appointment_details(self):
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
            print("Database Error",e)
            return 

        rows = cursor.fetchall()

        for row in rows:
            (first_name, surname,
            appointment_date,appointment_time) = row

            print(f"Patient: {first_name} {surname}")
            print(f"Date: {appointment_date}")
            print(f"Time: {appointment_time}")
            print("-"*40)

    def display_all_patients_with_appointments(self):
        try:
            cursor.execute("""

                SELECT  patient.first_name,
                        patient.surname,
                        appointment.appointment_date,
                        appointment.appointment_time
            
                FROM    patient

                LEFT JOIN   appointment

                ON  patient.patient_id = appointment.patient_id
        
            """)

        except sqlite3.Error as e:
            print("Database Error", e)
            return

        rows = cursor.fetchall()

        for row in rows:
            (first_name,surname,
            appointmemt_date,appointment_time) = row

            print(f"Patient: {first_name} {surname}")
            print(f"Date: {appointmemt_date}")
            print(f"Time: {appointment_time}")
            print("-"*40)

    def display_all_patients_and_appointments(self):
        try:
            cursor.execute("""

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

            """)

        except sqlite3.Error as e:
            print("Database Error", e)
            return

        rows = cursor.fetchall()

        for row in rows:
            (first_name, surname, 
             appointment_date, appointment_time) = row

            print(f"Patient: {first_name} {surname}")
            print(f"Date: {appointment_date}")
            print(f"Time: {appointment_time}")
            print("-"*40)
