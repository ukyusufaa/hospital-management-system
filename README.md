# Hospital Management System

## 1. Project Overview

The Hospital Management System (HMS) is a menu-driven application developed using Python 3, SQLite, and object-oriented programming (OOP).

The purpose of the project is to manage hospital information through a structured application backed by a relational database. It brings together patient administration, GP management, GP surgery records, consultant management, department management, appointments, medication records, prescriptions, and billing.

The application demonstrates how separate Python modules can work together to manage related information while maintaining database integrity and enforcing business rules.

The system was developed as part of a Python software development portfolio, with a particular focus on practical programming, relational database design, SQL, application structure, data validation, and testing.

**Project status: Completed**

### Main objectives

The project was developed to demonstrate the ability to:

- Design and build a database-driven Python application.
- Apply object-oriented programming principles.
- Organise an application into separate functional modules.
- Create and manage relational SQLite database tables.
- Implement CRUD operations.
- Establish relationships using primary keys and foreign keys.
- Retrieve related records using SQL JOIN operations.
- Implement one-to-many and many-to-many relationships.
- Apply database constraints and business rules.
- Validate user input and handle errors.
- Build a menu-driven console interface.
- Integrate multiple application modules into one working system.
- Use Git and GitHub for source control and project documentation.

---

## 2. System Description

The Hospital Management System provides administrative functions for managing hospital records.

Instead of storing all information in one large table, the application uses a relational database. Different types of information are stored in their own tables and connected through relationships.

For example, a patient record can be associated with appointments, prescriptions, and bills. An appointment can be associated with a patient and a consultant. A consultant can be linked to a department. Prescriptions can be associated with medications through a junction table.

This structure reduces unnecessary duplication and allows the application to retrieve related information when required.

The application is operated through a console-based menu system. Users select the required management function, enter the relevant information, and interact with the database through the associated Python module.

### Core functional areas

The system covers:

1. Patient management.
2. GP management.
3. GP surgery management.
4. Department management.
5. Consultant management.
6. Appointment management.
7. Medication management.
8. Prescription management.
9. Billing and invoice management.

These functions are integrated into the wider application rather than being separate, unrelated programs.

---

## 3. Hospital Administration Menu

The application includes a dedicated Hospital Administration Menu.

This menu provides access to the main administrative functions and allows users to navigate between different areas of the hospital system.

The menu contains the following options:

1. Medical Practice Management of Patient
2. GP Management of Patient
3. Department Management of Holly Hospital
4. Consultant Management of Holly Hospital
5. Medication Management of Holly Hospital
6. Return to Main Menu

### 3.1 Medical Practice Management of Patient

This section provides access to patient administration functions.

Patient information is stored in the database and can be associated with other hospital records through relational database relationships.

Patient management is an important part of the system because patient records are referenced by appointments and other related information.

### 3.2 GP Management of Patient

This section provides access to GP management functions.

GP records are stored separately from patient records. Relationships between patients, GPs, and GP surgeries allow the application to retrieve relevant information without duplicating all GP details in each patient record.

The system also accommodates patients who do not have an assigned GP.

### 3.3 Department Management of Holly Hospital

This section provides access to department management.

Department records are maintained independently and can be associated with consultants. This supports the retrieval of department information when displaying related consultant and appointment records.

### 3.4 Consultant Management of Holly Hospital

This section provides access to consultant management.

Consultants are maintained as separate records and associated with their departments and appointments.

This design allows consultant information to be reused across multiple related records.

### 3.5 Medication Management of Holly Hospital

This section provides access to medication management.

Medication records are maintained in the database and can be referenced by prescriptions and billing-related functionality.

### 3.6 Return to Main Menu

This option allows users to return to the application's main menu.

The menu structure provides a consistent navigation approach across the application.

---

## 4. Main Application Features

### 4.1 Patient Management

The patient management module handles patient records.

Patient information is stored in the SQLite database and can be retrieved when required by other parts of the system.

Patient records form an important part of the relational structure because appointments, prescriptions, and billing information may depend on the associated patient and appointment records.

Key concepts demonstrated include:

- Database-backed patient records.
- CRUD operations.
- Input validation.
- Primary-key identification.
- Relationships with other hospital records.
- Handling optional GP registration.

A patient does not necessarily have an assigned GP. The database design must therefore allow the relevant GP relationship to be absent without treating the patient record as invalid.

### 4.2 GP Management

The GP management module maintains general practitioner records.

GP information is stored separately from patient information, allowing a GP record to be referenced by related records without duplicating the GP's details.

This supports relational data management and reduces unnecessary duplication.

### 4.3 GP Surgery Management

The GP surgery management module maintains surgery information.

GP records can be associated with their relevant surgeries through database relationships.

Separating GP and surgery information allows the system to retrieve the relevant surgery details when required.

### 4.4 Consultant Management

The consultant management module maintains hospital consultant records.

Consultants are associated with departments and appointments.

This structure supports the retrieval of consultant information when displaying appointment details and related records.

### 4.5 Department Management

The department management module maintains hospital department records.

Consultant and department information is stored in related tables rather than being repeatedly copied into other records.

This demonstrates the use of foreign keys and relational database design.

### 4.6 Appointment Management

The appointment management module handles appointment records.

Appointments connect patients with consultants and provide the basis for retrieving information about scheduled hospital activity.

The appointment functionality uses relational database relationships to associate appointment records with the relevant people and departments.

The system includes database uniqueness constraints designed to prevent conflicting bookings.

The configured rules include:

- A consultant cannot have two appointments at the same date and time.
- A patient cannot have two appointments at the same date and time.

These rules are supported by database constraints rather than relying exclusively on the menu interface to prevent duplicate bookings.

### 4.7 Medication Management

The medication management module maintains medication records.

Medication information can be referenced by prescription-related functionality and billing operations.

Keeping medication records in a separate table allows medication information and costs to be managed independently of individual prescriptions or bills.

### 4.8 Prescription Management

The prescription management module handles prescription records and their relationships with medications.

A prescription can be associated with medication records through the prescription-medication junction table.

This arrangement supports a many-to-many relationship:

- A prescription can reference multiple medications.
- A medication can be referenced by multiple prescriptions.

The junction table represents these relationships without requiring multiple medication columns in the prescription table.

SQL JOIN operations can then retrieve prescription information alongside the associated medication details.

### 4.9 Billing and Invoice Management

The billing module handles bills and invoice display.

Bills are associated with appointments, allowing the system to retrieve the relevant appointment and related hospital information.

Billing functionality includes:

- Associating bills with appointments.
- Storing billing information in the database.
- Recording bill items and their unit costs.
- Calculating totals from associated billing items.
- Retrieving invoice information using SQL queries.
- Displaying relevant patient and appointment details.
- Retrieving consultant and department information.
- Retrieving GP and GP surgery details where available.

The invoice display brings together information from related database tables.

Where a patient has no assigned GP, the application must accommodate that optional relationship rather than treating it as a mandatory requirement.

The billing module demonstrates how relational queries can combine records from multiple tables to produce a single, useful output.

---

## 5. Technologies and Tools

### Python 3

Python is the primary programming language used to implement the application's business logic, menu system, validation, and database interactions.

The code is organised into modules so that different areas of functionality can be maintained separately.

### SQLite

SQLite provides the relational database used to store hospital information.

It supports the creation of tables, constraints, relationships, and SQL queries without requiring a separate database server.

### SQL

SQL is used to interact with the database.

The project demonstrates:

- Retrieving records with `SELECT`.
- Adding records with `INSERT`.
- Modifying records with `UPDATE`.
- Removing records with `DELETE`.
- Filtering records with `WHERE`.
- Retrieving individual and multiple results with `fetchone()` and `fetchall()`.
- Joining related tables.
- Enforcing uniqueness constraints.
- Maintaining referential integrity through foreign keys.

### Object-Oriented Programming

The project uses an object-oriented approach to organise application functionality.

Classes and methods can group related behaviour and provide a structured way of interacting with different parts of the system.

### Git

Git is used for version control.

It allows changes to the application and its documentation to be tracked through commits.

### GitHub

GitHub hosts the project repository and provides a central location for the source code and documentation.

### Visual Studio Code and WSL Ubuntu

Visual Studio Code is used as the development environment, with the project running in a WSL Ubuntu environment.

The application can be started from the terminal using Python.

---

## 6. Project Structure

The project is organised into separate Python modules.

The main files and their responsibilities are described below.

| File | Responsibility |
|---|---|
| `main.py` | Main application entry point and menu navigation |
| `menu.py` | Menu-driven interface |
| `database.py` | Database connection and configuration |
| `patient.py` | Patient management |
| `gp.py` | GP management |
| `gp_surgery.py` | GP surgery management |
| `consultant.py` | Consultant management |
| `department.py` | Department management |
| `appointment.py` | Appointment management |
| `appointment_patient.py` | Appointment and patient-related functionality |
| `medication.py` | Medication management |
| `prescription.py` | Prescription management |
| `prescription_medication.py` | Prescription-medication relationships |
| `bill.py` | Billing and invoice functionality |
| `colors.py` | Terminal text colours |
| `clock.py` | Date and time-related functionality |

The project directory also contains the README documentation and SQLite database files.

The exact responsibilities of individual modules follow their implemented code. The table describes their principal roles within the application.

---

## 7. Database Architecture

The application uses a relational database to organise hospital information.

Each entity is stored in an appropriate table, with relationships established using keys.

This design supports data consistency and allows the application to retrieve information from multiple related tables.

### 7.1 Primary Keys

A primary key uniquely identifies a record in a table.

For example, a patient identifier can be used to distinguish one patient from another.

Primary keys also provide a stable reference for other tables that need to associate records with that patient.

### 7.2 Foreign Keys

A foreign key references a record in another table.

Foreign keys connect related information, such as an appointment and its patient.

This reduces the need to duplicate the same information in multiple tables.

The database connection enables SQLite foreign-key enforcement so that applicable relationships are checked by the database engine.

### 7.3 One-to-Many Relationships

A one-to-many relationship allows one record to be associated with multiple records in another table.

Examples in this application include:

- One consultant associated with multiple appointments.
- One patient associated with multiple appointments.
- One department associated with multiple consultants, where permitted by the schema.

These relationships are represented through foreign keys.

### 7.4 Many-to-Many Relationships

A many-to-many relationship allows multiple records in one table to be associated with multiple records in another table.

The prescription-medication relationship uses a junction table.

Instead of storing several medication identifiers directly in one prescription record, the relationship is represented by separate rows in the junction table.

This makes the structure more flexible and demonstrates an important relational database design principle.

### 7.5 Optional Relationships

Not every relationship needs to be mandatory.

For example, a patient may not have an assigned GP.

The database and the queries that retrieve patient information must account for this possibility.

Where a related record is optional, suitable SQL joins allow the main record to remain available even when the related record does not exist.

### 7.6 Database Constraints

Database constraints help enforce rules independently of the menu interface.

The project includes uniqueness requirements for appointment bookings.

These include:

- `UNIQUE(consultant_id, appointment_date, appointment_time)`
- `UNIQUE(patient_id, appointment_date, appointment_time)`

The constraints help prevent a consultant or patient from having conflicting appointments at the same date and time.

The actual enforcement depends on the database schema and the configured SQLite connection.

---

## 8. SQL and Relational Queries

SQL is a central part of the project.

The application uses queries to retrieve and manipulate information stored in the database.

### 8.1 SELECT Queries

`SELECT` retrieves data from one or more database tables.

The application uses queries to display records and retrieve the information needed by its management functions.

### 8.2 INSERT Queries

`INSERT` adds new records to database tables.

It is used by database-backed creation operations.

### 8.3 UPDATE Queries

`UPDATE` modifies existing records.

It supports changes to information already stored in the database.

### 8.4 DELETE Queries

`DELETE` removes records where the relevant operation and database constraints permit it.

Deletion must take account of relationships with other records.

For example, related appointments or bills may affect whether a particular record can safely be removed.

### 8.5 WHERE Clauses

`WHERE` filters records according to specified conditions.

Filtering allows the application to retrieve records matching an identifier or another relevant value.

### 8.6 JOIN Operations

JOIN operations combine information from related tables.

They are particularly useful when the application needs to display information that is stored across multiple entities.

For example, an invoice may require information from the bill, appointment, patient, consultant, and department tables.

Rather than duplicating all these details in the bill table, SQL joins retrieve the relevant information when required.

### 8.7 INNER JOIN and LEFT JOIN

An `INNER JOIN` returns rows where the join conditions match in both tables.

A `LEFT JOIN` preserves rows from the left-hand table even when no matching record exists in the right-hand table.

This distinction matters when a relationship is optional.

For example, using an `INNER JOIN` to retrieve a patient together with a GP would exclude a patient who has no assigned GP.

A suitable `LEFT JOIN` allows the patient record to remain available while the GP columns contain `NULL`.

### 8.8 fetchone() and fetchall()

The application uses Python's SQLite interface to retrieve query results.

- `fetchone()` retrieves one result row.
- `fetchall()` retrieves all remaining result rows.

Choosing the appropriate method depends on whether the operation expects one record or multiple records.

These methods are part of the integration between Python and the SQLite database.

---

## 9. Business Rules and Data Integrity

Business rules define conditions that the application must respect when managing information.

The project combines application logic with database constraints to maintain consistent records.

### NHS Number Uniqueness

An NHS number must be unique within the patient records.

This prevents two patient records from sharing the same NHS number.

### Appointment Uniqueness

The configured appointment constraints prevent a consultant or patient from having two appointments at the same date and time.

### Optional GP Registration

A patient may exist without an assigned GP.

The application must handle this situation when retrieving and displaying related information.

### Prescription-Medication Relationships

Prescription and medication relationships are represented through the junction table.

This avoids the need to store multiple medication relationships in a single prescription column.

### Billing Relationships

Bills are associated with appointments, allowing the application to retrieve related appointment information when displaying invoices.

### Referential Integrity

Foreign keys help maintain valid relationships between database records.

Where applicable, the database prevents operations that would violate the configured foreign-key rules.

### Input Validation

Input validation helps ensure that user-supplied values meet the requirements of the relevant operation.

Validation is important because database constraints alone do not cover every possible business rule or user-interface requirement.

### Exception Handling

Exception handling allows the application to deal with certain errors without terminating unexpectedly.

It is particularly relevant to database operations and user input.

The precise validation and exception-handling behaviour is determined by the implementation of each module.

---

## 10. Application Workflow

The application follows a menu-driven workflow.

### Step 1: Start the Application

The user launches the application through `main.py`.

### Step 2: Display the Main Menu

The main menu provides access to the application's management areas.

### Step 3: Select a Management Function

The user chooses the required function, such as patient management, GP management, appointments, prescriptions, or billing.

### Step 4: Process the Requested Operation

The relevant module handles the operation and interacts with the database as necessary.

### Step 5: Validate Input and Apply Rules

The application validates user input and applies the relevant business rules and database constraints.

### Step 6: Execute Database Operations

The application performs the required database queries to create, retrieve, update, or delete records.

### Step 7: Display Results

The application displays the resulting information through the console interface.

For example, the billing module retrieves related records and displays the invoice information.

### Step 8: Return to Navigation

The user can continue using the available menu functions or return to the main menu.

This workflow separates navigation, application functionality, and database operations into more manageable parts.

---

## 11. Billing and Invoice Workflow

Billing is an important example of how the application combines several related tables.

### 11.1 Bill Association

A bill is associated with an appointment.

The appointment identifier provides a link to the appointment record.

### 11.2 Retrieving Related Information

When an invoice is displayed, the application retrieves the associated information required for the invoice.

This can include:

- Patient details.
- Appointment details.
- Consultant information.
- Department information.
- GP information, when available.
- GP surgery information, when available.
- Bill items and their unit costs.

### 11.3 Bill Items

Individual billing items are stored separately from the main bill record.

This allows a bill to contain multiple items without requiring a fixed set of item columns in the bill table.

### 11.4 Calculating the Total

The invoice total is calculated from the associated billing items and their costs.

The calculation depends on the billing data stored for the relevant bill.

### 11.5 Displaying the Invoice

The billing module combines the retrieved information into a readable terminal invoice.

This demonstrates the practical use of relational queries to produce a single output from multiple database entities.

### 11.6 Handling Missing Optional Information

A patient may not have an assigned GP or an associated surgery.

In such cases, the invoice display should handle missing optional information appropriately instead of treating the absence of a GP as a missing patient record.

---

## 12. Error Handling and Validation

The application uses validation and exception handling to improve reliability.

Validation checks whether user-supplied information meets the requirements of the relevant operation.

Database constraints provide an additional layer of protection for rules that can be enforced at the database level.

Exception handling allows the application to respond to certain errors during execution.

These techniques help distinguish between invalid input, unsuccessful database operations, and legitimate situations where optional information is absent.

A missing optional GP relationship, for example, is different from a missing bill or an invalid foreign-key reference.

This distinction is important when debugging database-driven applications.

---

## 13. Testing and Debugging

Testing was an important part of completing the system.

Individual functions and the integration between modules needed to be checked to confirm that the application behaved as expected.

### 13.1 Functional Testing

Functional testing checks whether a management function performs its intended operation.

Relevant areas include:

- Patient management.
- GP management.
- GP surgery management.
- Consultant management.
- Department management.
- Appointment management.
- Medication management.
- Prescription management.
- Billing and invoice display.

### 13.2 Database Testing

Database testing checks whether records are stored and retrieved correctly.

It also checks whether relationships between records behave as intended.

### 13.3 Constraint Testing

Constraint testing checks that configured database rules prevent invalid combinations of records.

Appointment uniqueness is one example.

### 13.4 Validation Testing

Validation testing checks how the application responds to unsuitable user input.

The exact cases depend on the validation implemented in each module.

### 13.5 Integration Testing

Integration testing checks whether different modules work together correctly.

For example, billing relies on relationships between bills, appointments, patients, and other associated records.

Prescription management similarly relies on the relationship between prescriptions and medications.

### 13.6 Debugging

Debugging involved investigating application behaviour, reviewing SQL queries, checking database relationships, and correcting implementation issues.

This process helped reinforce the importance of distinguishing between Python-level problems, SQL query problems, and database design issues.

---

## 14. Installation and Setup

### Requirements

The application requires:

- Python 3.
- SQLite support through Python's built-in `sqlite3` module.
- Git, if cloning the repository.
- A terminal or command-line environment.

Visual Studio Code and WSL Ubuntu were used during development, but the application can be run in another compatible Python environment with the appropriate setup.

### Step 1: Clone the Repository

Clone the GitHub repository:

```bash
git clone <your-github-repository-url>
```

Replace the placeholder with the actual repository URL.

### Step 2: Navigate to the Project Directory

```bash
cd hospital-management-system
```

The directory name should match the name used when cloning the repository.

### Step 3: Check the Python Installation

```bash
python3 --version
```

This displays the installed Python version.

### Step 4: Start the Application

```bash
python3 main.py
```

The main application menu should appear.

### Step 5: Initialise the Database

The database connection and configuration are handled by `database.py`.

Follow the initialisation process implemented by the project to ensure that the required tables exist before using the application.

If the repository contains an existing SQLite database, use it according to the project's configuration.

**Important:** Do not delete the database file simply to restart the application. Deleting it may remove stored records. Database resets should only be performed when intentionally resetting test data or rebuilding the database.

---

## 15. Running the Application in WSL Ubuntu

The project was developed using Visual Studio Code with WSL Ubuntu.

A typical workflow is:

1. Open the project in Visual Studio Code.
2. Connect to the WSL Ubuntu environment.
3. Open the integrated terminal.
4. Navigate to the project directory.
5. Run the application using Python.

Example:

```bash
cd ~/python/hospital-management-system
python3 main.py
```

This assumes that the project is located at the directory shown above.

The application then runs in the terminal.

---

## 16. Version Control and GitHub

Git is used to track changes to the project.

GitHub hosts the repository and makes the project available for portfolio review.

### Check the Working Tree

```bash
git status
```

This shows whether files have been modified, staged, or committed.

### Stage the README

```bash
git add README.md
```

This stages the documentation file.

### Commit the Documentation

```bash
git commit -m "Add complete hospital management system documentation"
```

This creates a commit containing the staged README changes.

### Push to GitHub

```bash
git push
```

This pushes the commit to the configured remote repository.

These commands update the documentation without requiring changes to the application's Python modules.

---

## 17. Project Achievements

The completed Hospital Management System demonstrates practical experience in combining Python programming with relational database technology.

Key achievements include:

- Building a menu-driven hospital management application.
- Organising functionality into separate Python modules.
- Managing hospital records through SQLite.
- Implementing CRUD operations.
- Establishing primary-key and foreign-key relationships.
- Designing a junction table for prescription-medication relationships.
- Using SQL JOIN operations to retrieve related information.
- Applying uniqueness constraints to appointment bookings.
- Supporting optional GP registration.
- Integrating prescription and medication records.
- Implementing billing and invoice display.
- Calculating invoice totals from associated billing items.
- Applying input validation and exception handling.
- Debugging database queries and application behaviour.
- Maintaining the project using Git and GitHub.

The project demonstrates how a collection of individual modules can be integrated into one coherent application.

---

## 18. Learning Outcomes

Developing this application provided practical experience in several areas of software development.

### Python Programming

The project strengthened understanding of functions, classes, methods, modules, control flow, validation, and exception handling.

### Object-Oriented Design

Separating application functionality into modules helped establish clearer responsibilities and a more maintainable structure.

### Relational Database Design

The project demonstrated why related information should be represented through appropriate tables and relationships.

### SQL

Working with SQL queries reinforced the use of filtering, data manipulation, joins, and database constraints.

### Python and SQLite Integration

The application demonstrates how Python can interact with a relational database to store, retrieve, and modify information.

### Application Integration

The project required separate management functions to work together using consistent database relationships.

### Testing and Debugging

Investigating errors in the application helped develop a more systematic approach to identifying the cause of a problem.

### Version Control

Git and GitHub provide a way to track changes and present the completed project as part of a software development portfolio.

---

## 19. Limitations and Intended Use

This project is an educational portfolio application.

It demonstrates software development and database concepts, but it is not intended for use as a production hospital information system.

Real-world healthcare software requires additional security controls, access management, audit logging, privacy protections, clinical safety processes, backup and recovery arrangements, and applicable regulatory compliance.

The application should therefore be treated as a learning and demonstration project rather than software suitable for managing real patient care.

---

## 20. Future Development

The current project is considered complete within its defined scope.

Possible extensions, if pursued in a future version, could include:

- A graphical user interface.
- User authentication and role-based access control.
- Expanded reporting and analytics.
- Additional search and filtering functionality.
- Automated testing.
- More comprehensive audit logging.
- Enhanced database backup and recovery procedures.

These are potential extensions, not requirements for the completed version described in this documentation.

---

## 21. Conclusion

The Hospital Management System is a completed Python and SQLite project that brings together hospital administration, patient records, appointments, prescriptions, medication management, and billing.

Its modular design separates different areas of functionality, while its relational database connects the information required by the application.

The project demonstrates practical use of object-oriented programming, CRUD operations, SQL queries, primary keys, foreign keys, junction tables, database constraints, input validation, exception handling, and application integration.

It also demonstrates the importance of understanding how application logic and database design work together.

The completed system forms part of a Python software development portfolio and provides a foundation for developing more advanced database-driven applications.

---

## Author

Developed as part of a Python software development portfolio.