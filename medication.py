import sqlite3

conn = sqlite3.connect("hospital.db")

cursor = conn.cursor()

class Medication():
    def __init__(self,medication_name = None, cost = None):
        self.medication_name = medication_name
        self.cost = cost
    
    def show_medication_details(self):
        print("-" * 30)
        print(f"Medication Name:{self.medication_name}")
        print(f"Cost:{self.cost}")
        print("-" * 30)

        # Validate IDs to ensure they are positive integers.
    def validate_login_id(self,number):
        if number < 1:
            return False
        return True

        # Validate medication names using letters, numbers and spaces.
    def validate_medication_name(self,name):
        for letter in name:
            if(not letter.isalpha()
            and not letter.isdigit()
            and not letter == " "):
                return False
        return True

        # Validate medication cost as positive values with two decimal places.
    def validate_medication_cost(self,cost):
        if cost <=0 or cost != round(cost,2):
            return False
        return True

        # Collect and validate medication details before saving the record.
    def create_medication(self):
        while True:
            self.medication_name = input("Enter medication " \
            "name and strength (for example: Paracetamol 500mg):")
            if self.medication_name == "":
                print("Medication Name is required. Please enter " \
                "a medication name and strength.")
                continue

            letter_found = False
            for character in self.medication_name:
                if character.isalpha():
                    letter_found = True
                    break 
            if letter_found == False:
                print("Please enter the medication name.")
                continue

            number_found = False
            for character in self.medication_name:
                if character.isdigit():
                    number_found = True
                    break 
            if number_found == False:
                print("Please include the medication strength.")
                continue

            space_found = False
            for charcater in self.medication_name:
                if charcater == " ":
                    space_found = True
                    break 
            if space_found == False:
                print("Please enter the medication name " \
                "and its strength separated by a space.")
                continue

            if not self.validate_medication_name(self.medication_name):
                print("Please use letters, numbers and " \
                "spaces only.")
                continue 
            break

        while True:
            try:
                self.cost = float(input("Enter medication cost: "))
                if not self.validate_medication_cost(self.cost):
                    print("Medication cost must be greater " \
                    "than £0:00 and have no more than " \
                    "2 decimal places.")
                    continue 
                break 
            except ValueError:
                print("Please enter the medication cost as " \
                "a number (decimal).")
                continue

        meds = Medication(
        self.medication_name,
        self.cost
        )

        try:
            # Insert the validated medication details into the database.
            cursor.execute("""
            INSERT INTO medication(
                    medication_name,
                    cost)
            VALUES(?,?)
            """,(meds.medication_name, meds.cost))

            conn.commit()

        except sqlite3.Error as e:
            print("Unable to save the medication. " \
            "Please try again.", e)
            return

        print("Medication created successfully.")
        row = cursor.lastrowid
        print(f"Medication ID: {row}")
        meds.show_medication_details()
        return


        # Retrieve and display all medications stored in the database.
    def display_all_medications(self):
        cursor.execute("SELECT * FROM medication")

        rows = cursor.fetchall()
        if not rows:
            print("No medications are " \
            "currently registered.")
            return 
        else:
            for row in rows:
                meds = Medication(
                    row[1],
                    row[2]
                )
                print(f"Medication ID: {row[0]}")
                meds.show_medication_details()
            return

        # Find a medication using its unique medication ID.
    def search_medication(self):
        while True:
            try:
                medication_id = int(input(
                    "Enter medication ID: "
                ))
                if not self.validate_login_id(medication_id):
                    print("Please enter a valid " \
                    "medication ID.")
                    continue 
                break 
            except ValueError:
                print("Please enter the medication ID " \
                "using numbers only.")
                continue 
        try: 
            cursor.execute("""
            SELECT * FROM medication
            WHERE medication_id = ?
            """,(medication_id,))

        except sqlite3.Error as e:
            print("Unable to search for the " \
            "medication. Please try again.", e)
            return

        row = cursor.fetchone()
        if not row:
            print("No medication was found " \
            "with that ID.")
            return
        else:
            meds = Medication(
                row[1],
                row[2]
            )
            print(f"Medication ID: {row[0]}")
            meds.show_medication_details()
            return

        # Update the details of an existing medication.
    def update_medication(self):
        while True:
            try:
                medication_id = int(input("Enter medication ID:"))
                if not self.validate_login_id(medication_id):
                    print("Please enter a valid medication ID.")
                    continue 
                break 
            except ValueError:
                print("Please enter the medication ID " \
                "using numbers only.")
                continue 
        try:
            cursor.execute("""
            SELECT * FROM medication
            WHERE medication_id = ?
            """,(medication_id,))

        except sqlite3.Error as e:
            print("Unable to retrieve the " \
            "medication. Please try again.", e)
            return

        row = cursor.fetchone()
        if not row:
            print("No medication was " \
            "found with that ID.")
            return 
        else:
            meds = Medication(
                row[1],
                row[2]
            )
            print(f"(Medication ID: {row[0]}")
            meds.show_medication_details()
            
            update = input("Update this medication?").lower()
            if update == "y":
                while True:
                    new_medication_name = input
                    (
                        "Enter new "
                        "medication name and strength: "
                    )
                    if new_medication_name == "":
                        print("Medication name is " \
                        "required. Please enter " \
                        "a medication name and strength.")
                        continue
                    if not self.validate_medication_name(new_medication_name):
                        print("Please use letters, " \
                        "numbers and spaces only.")
                        continue 
                    break

                while True:
                    try:
                        new_cost = float(input
                        (
                            "Enter new medication " \
                            "cost (£): "

                        ))
                        if not self.validate_medication_cost(new_cost):
                            print("Medication cost must be " \
                            "greater than £0:00 and have " \
                            "no more than 2 decimal places.")
                            continue 
                        break 
                    except ValueError:
                        print("Please enter the medication " \
                        "cost as a number.")
                        continue
                
                meds.medication_name = new_medication_name
                meds.cost = new_cost

                try:
                    cursor.execute("""
                    UPDATE medication
                    SET medication_name = ?,
                        cost = ?
                    WHERE medication_id = ?
                    """,(meds.medication_name,meds.cost,medication_id))

                    conn.commit()

                except sqlite3.Error as e:
                    print("Unable to update " \
                    "the medication. Please " \
                    "try again.", e)
                    return
                
                print("Medication updated successfully.")
                return
            else:
                print("Medication update cancelled.")
                return

        # Confirm and remove an existing medication from the database.
    def delete_medication(self):
        while True:
            try:
                medication_id = int(input("Enter medication ID:"))
                if not self.validate_login_id(medication_id):
                    print("Please enter a valid medication ID.")
                    continue 
                break 
            except ValueError:
                print("Please enter the medication ID " \
                "using numbers only.")
                continue 
        try:
            cursor.execute("""
            SELECT * FROM medication
            WHERE medication_id = ?
            """,(medication_id,))

        except sqlite3.Error as e:
            print("Unable to retrieve the " \
            "medication. Please try again.", e)
            return

        row = cursor.fetchone()
        if not row:
            print("No medication was found " \
            "with that ID.")
            return
        else:
            meds = Medication(
                row[1],
                row[2]
                )
            print(f"Medication ID:{row[0]}")
            meds.show_medication_details()

            delete = input(
                "Delete this medication? (Y/N): "
            ).lower()
            if delete == "y":

                try:
                    cursor.execute("""
                    DELETE FROM medication
                    WHERE medication_id = ?
                    """,(medication_id,))

                    conn.commit()

                except sqlite3.Error as e:
                    print("Unable to delete " \
                    "the medication. Please" \
                    "try again.", e)
                    return 
                
                print("Medication deleted successfully.")
                return
            else:
                print("Medication deletion cancelled.")
                return


        
    