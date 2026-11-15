# Holly Hospital System

## Overview

The Holly Hospital System (HHS) was created to overcome possible storage related issues as ever increasing documents can take over vast spaces throughout a hospital. I therefore proposed to create a centralised computerised database management system to store all such valuable information.
The HHS presents itself as a menu driven object-oriented programming application. HHS is built using Python 3 and an SQLite database. It communicates via a terminal to allow the user to input, display all, search, delete and update records. The system entails information on GP, medical practice, consultant, department, patient, appointment, prescription, medication and billing.

## Features
HHS operates via a terminal to allow the user through its main menu and submenus to insert, display all, search, delete and update records.

The program is designed carefully to ensure the user doesn't double book an appointment. The database tables through their unique key combinations and the Python application together each perform their own checks to doubly prevent any double booking appointments from taking place. This means a patient or consultant who already has an appointment booked is prevented from making another booking at the same time and date.

Here an appointment can only have one prescription. In the database a junction table was created to permit a prescription to have several medications each with their own dosage instructions and to permit a medication to appear on many prescriptions. This junction table also prevents the same prescription from holding the same medication twice.

The bill is created after a patient attends an appointment with the consultant. If the patient is given a prescription it would include on it the medication and hence a bill would be generated. Otherwise if no prescription is given to the patient a bill is not generated. The generated bill is shown as "UNPAID" and after the patient has made payment it becomes "PAID". Python uses the bill table to generate a final total cost invoice of the bill. There is another table called bill item table that saves the medication details even if they were deleted in the medication catalog, the medication table. Python uses the bill item table to show a more in depth invoice including the costs per medication and also uses a JOIN. The JOIN makes it possible to combine several tables to display information on patient, what appointment they attended, what department they visited, who the prescribing consultant was, what was prescribed, what GP and medical practice the patient belongs to.

This system includes many sub menus one of which contains reports that make use of JOINs. A JOIN is basically a linkage of two or more tables together to show combinations of information. HHS allows the user to see what medical practice a patient belongs to, what consultant the patient saw at their appointment and all those patients who have or don't have appointments. Also it allows a user to count the medications on a prescription and work out the average cost of a medication.

An option in the main menu exists for the user to access the current date and live time. This feature was added on for better time management practices.

## How to run it

To run HHS install Python 3 and pyfiglet, an extra library which is used to draw the large "HOLLY HOSPITAL" title for this project.

1.  Download the project from GitHub:

    ```
    git clone https://github.com/ukyusufaa/hospital-management-system
    cd hospital-management-system
    ```

2.  Install the extra library:

    ```
    pip install pyfiglet
    ```

3.  Start the program:

    ```
    python3 main.py
    ```

The database file (hospital.db) and all its tables are created automatically the first time the program runs, so there is nothing else to set up.

## Database Design 
HHS has 11 database tables stored in SQLite:

-   gp_surgery: name and address of one medical practice
-   gp: full name of one GP
-   department: name of one department
-   consultant: full name of one consultant
-   medication: name and cost of one medication
-   patient: full name, date of birth, address of one patient and a link to patient GP (gp_id) 
    is optional
-   appointment: one appointment booking between one consultant and one patient that stores
    the time and date as well
-   prescription: one prescription for one appointment
-   prescription_medication: junction table links the prescription and medication tables
    to store a prescription, its medications and their dosage instructions
-   bill: one bill for one appointment storing the total amount for the bill and whether 
    it is "UNPAID" or "PAID"
-   bill_item: one charged medication on a bill with its name and cost

### Relationships

-   One medical practice has many GPs
-   One department has many consultants
-   One GP has many patients (Please note: Not every patient has a GP)
-   Both one consultant and one patient can have many appointments
-   Prescriptions and medications are a many to many relationship and so a junction table
    called prescription_medication is created and this lists the prescription and its medications side by side
-   One appointment has at most one prescription
-   One appointment has at most one bill
-   One bill has many bill items 

### Data rules

-   UNIQUE(consultant_id, appointment_date, appointment_time) A consultant can't be booked
    twice at the same date and time. It prevents a re-booking of the same combination appointment again called double booking
-   UNIQUE(patient_id, appointment_date, appointment_time) A patient can't be booked twice
    at the same date and time. This means it prevents double booking
-   UNIQUE on appointment_id in prescription prevents the same appointment_id from being
    re-used for another prescription_id. So an appointment_id can only be linked to one 
    prescription_id (Please note: Not all appointments have a prescription)
-   UNIQUE on appointment_id in bill means an appointment_id can only be linked to one 
    bill_id (Please note: Not all appointments have a bill)
-   UNIQUE(prescription_id, medication_id) prevents the same pair of relationships. So a 
    prescription cannot contain the same medication_id twice.
-   Foreign keys (switched on with PRAGMA foreign_keys = ON) prevent an ID in one table
    pointing to a primary key ID in another table that doesn't exist. So in such
    a case if patient 999 doesn't exist an appointment cannot be made for patient 999.
    The foreign key also prevents orphan records. This means it prevents a record from being deleted if other records point to it. So if someone tried to delete patient 3 but it had an appointment it would be prevented from doing so. The idea would be to delete the record in the child (foreign key) table first and then delete the record in the parent (primary key) table.
-   CHECK is a rule that is created alongside the table. It enforces what values a column
    will accept so that a complete row can be inserted successfully. In HHS these conditions must be met before a row can be inserted or updated: 
    -   costs must be above 0
    -   payment status is either UNPAID or PAID
    -   dates must be real dates in DD/MM/YYYY format
    -   appointment times must only be between 08:00-18:00 and on the quarter-hour
    -   dosage instructions must be between 1 to 100 characters
-   Triggers are set inside the database and every time a rule is broken they prevent an
    insert, update or delete by firing automatically. Let's look at a few examples: a patient's date of birth cannot be in the future, so a trigger blocks it when a patient is added or updated. An appointment date rule states an appointment can only be booked tomorrow or later. So a trigger blocks today's date or a past date. In another example a trigger blocks a bill item from being deleted. This is to ensure a bill always adds up to what the patient was charged (the total amount).   
-   Bills are saved as one transaction. This means we make one commit at the end after the
    individual bill items have tallied the bill. If anything goes wrong while saving the bill or its items nothing is saved, a rollback enforces the program to undo any changes. This ensures the final total always matches the costs of all the items on the bill. Without this, an early commit could create a partial bill. A second bill would be prevented because of the UNIQUE rule applied on appointment_id.

## What I learned

### Class
A class is a template, a blueprint and an object is built from it. The class contains vital
information on:
-   Attributes: the object data
-   Methods: the object actions and behaviours

Here is an example:

``` 
class Patient():
```

Here is the blueprint defined. Patient objects will now be created using the Class Patient.

### Constructor and self
I will explain with an example:

```
def __init__(self, database, first_name=None, surname=None,
             dob=None, address=None, gp_id=None):
```

At the start we initialise the object using the init method.

| Parameter | Purpose |
|---|---|
| self | Refers to the current object |
| database | Database connection or database handler |
| first_name | Patient's first name |
| surname | Patient's surname |
| dob | Date of birth |
| address | Patient's address |
| gp_id | Associated GP's ID |

Except self and database all the above parameters have a default value of None. We are permitted to create an object without them too. Self refers to the current object and database here is the shared database we are using throughout the program. So we are allowed to proceed onwards from here, here we can create the object.

```
self.first_name = first_name
self.surname = surname
self.dob = dob
```

Here self.first_name is the instance attribute belonging to the object self. The first_name is a parameter received by the method. These two must not be intermingled or confused as the same thing as they are not. An example below will further clarify this.
Suppose we create another object:

```
patient1 = Patient(database, "John", "Smith")
```

Here is an opportunity to explain what 'self' is as well. Basically self refers to the current object in this case it is patient1. Now let's show you what I previously intended to clarify.

```
self.first_name = "John"
self.surname = "Smith"
self.dob = None
self.address = None
self.gp_id = None
```

As you can clearly see the Parameter side is filled with values. The self here refers to data stored in patient1.

During my program I learned to understand what an object can hold. Here is an example of a Department object.

The first row's data is stored in an object as self.department_name = "Cardiology". One object can only hold one department. To hold the other rows, a for loop creates a new object for each row.

| department_id | department_name |
|---|---|
| 1 | Cardiology |
| 2 | Neurology |
| 3 | Oncology |

Now each object can hold its own self.department_name data, as shown below:

-   Object 1 holds Cardiology.
-   Object 2 holds Neurology.
-   Object 3 holds Oncology.

### Validation
Validation checks are used to ensure the user input is in accordance with business rules and therefore acceptable before it is stored as saved data in the database.
The various checks include whether the user only entered a number for an ID or whether a name only contains letters and spaces. A While True loop is used to keep asking until true before the next user input likewise is checked in the same manner. There are certain steps and stages the user must successfully complete before a record can be successfully inserted into the database as row, here is an example, validating an appointment date (future date):

| Stage | Check | Example |
|---|---|---|
| Shape | 10 characters with / separators | 26/01/2027 passes |
| Content | Digits in the correct positions | 2a/01/2027 fails |
| Meaning | A real date, and in the future | 14/10/2026 fails (in the past) |

So here the shape is that the user must enter exactly 10 characters and use separators. The content is that only digits are in the correct positions. Meaning is that it must be a future date and not a past date, in this case of an appointment date. The checks work like a staircase: when you climb the stairs you step on each step in order, and likewise these checks work together. The digit check would only take place after the length test has passed, and the future date check would only occur after the digit test has passed.

Besides these validations other stricter checks are used too:
For example these user inputs would fail:

1.  31/02/2027 - February doesn't have 31 days
2.  29/02/2027 - February isn't a leap year in 2027
3.  32/01/2027 - No month has 32 days
4.  31/14/2027 - No year has 14 months
5.  aa/'@-wi - Incorrect user inputs and separators are used

The above checks ensure the program does what is supposed to do and these work using loops, the user breaks free from the loop only when such checks are passed.

The program also uses try/except to catch out two different types of errors in this program, they are called ValueError and sqlite3.Error.

The ValueError is a python error. It happens when a value the program wasn't expecting is typed in by the user. For example:

When asked for an ID the user types "abc".
The code then runs:

```
int("abc")
```

Now here is the problem these letters "abc" are not a number, so a ValueError is raised by Python. So the ID validators loop the user back to enter the ID once again. This of course continues as explained previously until the correct value is entered.
The second kind is a database error called sqlite3.Error. This happens when a database rule is broken. Take a look at this example below where the SQL commands here are refused by SQLite:

-   UNIQUE: booking a consultant twice at the same date and time
-   FOREIGN KEY: an appointment for patient 999, or deleting a department that still has
    consultants
-   CHECK: a medication cost of -5
-   Trigger: a date of birth in the future

Python checks the input first and catches a ValueError, then the database checks last and raises a sqlite3.Error if a rule is broken. This ensures incorrect data is stopped twice.





