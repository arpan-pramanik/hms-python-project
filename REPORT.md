# Hospital Management System

## A Mini Project Report

---

**Submitted by:**
- **Name:** [Your Name]
- **Roll No:** [Your Roll Number]
- **Branch:** [Your Branch, e.g., Computer Science & Engineering]
- **Semester:** [e.g., 4th Semester]

**Guided by:**
- **Faculty Name:** [Guide's Name]
- **Designation:** [e.g., Assistant Professor]

**Institution:**
[Your College Name]
[University Name]
[Year: 2025–2026]

---

## Certificate

This is to certify that the project titled **"Hospital Management System"** has been successfully completed by **[Your Name]**, Roll No. **[Your Roll Number]**, in partial fulfillment of the requirements for the degree of **[Your Degree]** in **[Your Branch]** during the academic year **2025–2026**.

| | |
|---|---|
| **Project Guide** | **Head of Department** |
| [Faculty Name] | [HOD Name] |
| Date: ____________ | Date: ____________ |

---

## Acknowledgement

I would like to express my sincere gratitude to my project guide **[Faculty Name]** for their continuous support and guidance throughout the development of this project. I am also thankful to the **Head of the Department** and all the faculty members for providing the necessary resources and encouragement.

I extend my thanks to my classmates and friends for their valuable suggestions and support during the project.

---

## Abstract

The **Hospital Management System (HMS)** is a console-based application developed using **Python** and **SQLite3**. It is designed to simplify and automate the daily operations of a hospital or clinic, including patient registration, doctor management, appointment scheduling, billing, and medical history tracking.

The system provides a menu-driven interface that is easy to use and does not require any external libraries or complex setup. All data is stored persistently in an SQLite database file. The application demonstrates practical usage of database operations (CRUD), input validation, and modular programming in Python.

---

## Table of Contents

1. [Introduction](#chapter-1--introduction)
2. [Literature Review](#chapter-2--literature-review)
3. [System Requirements](#chapter-3--system-requirements)
4. [System Design](#chapter-4--system-design)
5. [Implementation](#chapter-5--implementation)
6. [Testing & Output](#chapter-6--testing--output)
7. [Conclusion & Future Scope](#chapter-7--conclusion--future-scope)
8. [References](#references)

---

## Chapter 1 — Introduction

### 1.1 Background

Hospitals handle large volumes of data daily — patient records, doctor schedules, appointments, billing, and medical histories. Managing all of this manually on paper is slow, error-prone, and inefficient. A computerized system can streamline these tasks, reduce human errors, and make information retrieval faster.

### 1.2 Problem Statement

Small clinics and hospitals often lack access to expensive hospital management software. There is a need for a **simple, lightweight, and cost-free** system that can handle basic hospital operations without requiring complex infrastructure.

### 1.3 Objective

The objective of this project is to develop a **console-based Hospital Management System** that:

- Allows registration and management of patients and doctors.
- Enables scheduling of appointments with automatic conflict detection.
- Tracks billing with payment status and financial summaries.
- Maintains medical history records for every patient.
- Stores all data persistently using SQLite3.
- Runs as a single Python file with zero external dependencies.

### 1.4 Scope

This project covers the following modules:

| # | Module | Description |
|---|---|---|
| 1 | Patient Management | Register, search, update, and delete patients |
| 2 | Doctor Management | Add and manage doctor profiles |
| 3 | Appointment Scheduling | Book, view, update, and cancel appointments |
| 4 | Billing System | Create bills, track payments, view summary |
| 5 | Medical History | Record diagnoses, treatments, and prescriptions |

---

## Chapter 2 — Literature Review

### 2.1 Existing Systems

Most existing hospital management systems are either:

- **Enterprise software** (e.g., Epic, Cerner) — expensive, complex, designed for large hospitals.
- **Web-based applications** — require server setup, deployment, and maintenance.
- **Spreadsheet-based** — lack relational data support and prone to errors.

### 2.2 Motivation

There is a gap for a **simple, single-file, zero-cost** solution suitable for learning purposes and small clinics. Python's built-in `sqlite3` module makes it possible to build a fully functional database-driven application without any installation overhead.

### 2.3 Technology Justification

| Technology | Reason |
|---|---|
| **Python** | Easy to learn, readable syntax, large standard library |
| **SQLite3** | Built-in with Python, serverless, file-based, supports SQL |
| **Console Interface** | No GUI framework needed, runs on any terminal |

---

## Chapter 3 — System Requirements

### 3.1 Hardware Requirements

| Component | Minimum Requirement |
|---|---|
| Processor | Any modern CPU (Intel/AMD) |
| RAM | 512 MB |
| Storage | 10 MB free space |
| Display | Any terminal/console |

### 3.2 Software Requirements

| Component | Requirement |
|---|---|
| Operating System | Windows / Linux / macOS |
| Python | Version 3.6 or higher |
| Database | SQLite3 (bundled with Python) |
| IDE (optional) | VS Code, PyCharm, or any text editor |

### 3.3 Functional Requirements

- The system shall allow adding, editing, and deleting patient records.
- The system shall allow adding, editing, and deleting doctor records.
- The system shall allow booking appointments and prevent double-booking.
- The system shall allow creating, viewing, and managing bills.
- The system shall allow recording and viewing patient medical history.

### 3.4 Non-Functional Requirements

- The system shall respond to user input within 1 second.
- The system shall store data persistently across sessions.
- The system shall validate all user inputs before saving.

---

## Chapter 4 — System Design

### 4.1 System Architecture

```
┌──────────────────────────────────────┐
│           User (Terminal)            │
└──────────────┬───────────────────────┘
               │ Input / Output
               ▼
┌──────────────────────────────────────┐
│         Application Layer            │
│  (Python — Menu + Business Logic)    │
└──────────────┬───────────────────────┘
               │ SQL Queries
               ▼
┌──────────────────────────────────────┐
│          Database Layer              │
│      (SQLite3 — hms.db file)         │
└──────────────────────────────────────┘
```

The system follows a **two-tier architecture**:
1. **Application Layer** — handles user interaction, input validation, and business logic.
2. **Database Layer** — stores and retrieves data using SQL queries.

### 4.2 Database Design (ER Diagram)

```
┌────────────┐       ┌────────────────┐       ┌────────────┐
│  patients  │       │  appointments  │       │  doctors   │
├────────────┤       ├────────────────┤       ├────────────┤
│ *id (PK)   │──1:N─→│ *id (PK)       │←─N:1──│ *id (PK)   │
│  name      │       │  patient_id(FK)│       │  name      │
│  age       │       │  doctor_id(FK) │       │  speciali- │
│  gender    │       │  date          │       │   zation   │
│  phone     │       │  time          │       │  phone     │
│  address   │       │  status        │       └────────────┘
└─────┬──────┘       └────────────────┘
      │
      │ 1:N
      ▼
┌────────────────┐   ┌──────────────────┐
│    bills       │   │ medical_history  │
├────────────────┤   ├──────────────────┤
│ *id (PK)       │   │ *id (PK)         │
│  patient_id(FK)│   │  patient_id (FK) │
│  amount        │   │  diagnosis       │
│  description   │   │  treatment       │
│  status        │   │  medicines       │
└────────────────┘   │  rec_date        │
                     └──────────────────┘
```

### 4.3 Data Flow Diagram (Level 0)

```
                    ┌──────────┐
   Patient Data ──→ │          │ ──→ Stored Records
   Doctor Data  ──→ │   HMS    │ ──→ Appointment Confirmations
   Appointments ──→ │  System  │ ──→ Bills & Summaries
   Bill Info    ──→ │          │ ──→ Medical Reports
                    └──────────┘
```

### 4.4 Module Design

```
main()
 ├── patient_menu()
 │    ├── add_patient()
 │    ├── view_patients()
 │    ├── search_patient()
 │    ├── update_patient()
 │    └── delete_patient()
 │
 ├── doctor_menu()
 │    ├── add_doctor()
 │    ├── view_doctors()
 │    ├── update_doctor()
 │    └── delete_doctor()
 │
 ├── appointment_menu()
 │    ├── book_appointment()
 │    ├── view_appointments()
 │    ├── update_appointment_status()
 │    └── cancel_appointment()
 │
 ├── billing_menu()
 │    ├── create_bill()
 │    ├── view_bills()
 │    ├── mark_bill_paid()
 │    ├── billing_summary()
 │    └── delete_bill()
 │
 └── history_menu()
      ├── add_medical_record()
      ├── view_all_records()
      ├── view_patient_history()
      ├── update_medical_record()
      └── delete_medical_record()
```

---

## Chapter 5 — Implementation

### 5.1 Database Initialization

The database and all tables are created automatically when the application starts:

```python
def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT NOT NULL,
            age      INTEGER NOT NULL,
            gender   TEXT NOT NULL,
            phone    TEXT,
            address  TEXT
        )
    """)
    # Similar CREATE TABLE statements for doctors,
    # appointments, bills, and medical_history
    conn.commit()
    conn.close()
```

### 5.2 Adding a Patient (Create Operation)

```python
def add_patient():
    name    = input("  Name    : ").strip()
    age     = input("  Age     : ").strip()
    gender  = input("  Gender  : ").strip()
    phone   = input("  Phone   : ").strip()
    address = input("  Address : ").strip()

    # Validation
    if not name or not age or not gender:
        print("  Name, Age and Gender are required!")
        return

    conn = get_connection()
    conn.execute(
        "INSERT INTO patients (name, age, gender, phone, address) "
        "VALUES (?,?,?,?,?)",
        (name, int(age), gender, phone, address)
    )
    conn.commit()
    conn.close()
    print("  Patient added successfully!")
```

### 5.3 Appointment Conflict Detection

Before booking an appointment, the system checks for existing bookings:

```python
conflict = conn.execute(
    "SELECT id FROM appointments "
    "WHERE doctor_id=? AND date=? AND time=? AND status='Scheduled'",
    (doctor_id, appt_date, appt_time)
).fetchone()

if conflict:
    print("  Doctor already has an appointment at that time!")
    return
```

### 5.4 Billing Summary

```python
def billing_summary():
    conn = get_connection()
    total  = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM bills").fetchone()[0]
    paid   = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM bills WHERE status='Paid'").fetchone()[0]
    unpaid = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM bills WHERE status='Unpaid'").fetchone()[0]
    conn.close()
    print(f"  Total Billed : ₹ {total:,.2f}")
    print(f"  Total Paid   : ₹ {paid:,.2f}")
    print(f"  Total Unpaid : ₹ {unpaid:,.2f}")
```

### 5.5 Formatted Table Display

A reusable helper function prints any dataset in a neatly aligned table:

```python
def print_table(headers, rows):
    widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(str(val)))

    fmt = "  ".join(f"{{:<{w}}}" for w in widths)
    print(fmt.format(*headers))
    print("  ".join("-" * w for w in widths))
    for row in rows:
        print(fmt.format(*[str(v) for v in row]))
```

---

## Chapter 6 — Testing & Output

### 6.1 Test Cases

| # | Test Case | Input | Expected Output | Result |
|---|---|---|---|---|
| 1 | Add patient with valid data | Name: John, Age: 30, Gender: Male | Patient added successfully | ✅ Pass |
| 2 | Add patient with missing name | Name: (blank) | Validation error shown | ✅ Pass |
| 3 | Add patient with invalid age | Age: "abc" | "Age must be a number" error | ✅ Pass |
| 4 | Add doctor | Name: Dr. Smith, Spec: Cardiology | Doctor added successfully | ✅ Pass |
| 5 | Book appointment | Patient 1, Doctor 1, 2026-04-07, 10:00 | Appointment booked | ✅ Pass |
| 6 | Double-book same doctor | Same doctor, same date, same time | Conflict error shown | ✅ Pass |
| 7 | Create bill | Patient 1, ₹500 | Bill created | ✅ Pass |
| 8 | Mark bill paid | Bill ID 1 | Status changed to Paid | ✅ Pass |
| 9 | View billing summary | — | Correct totals displayed | ✅ Pass |
| 10 | Add medical record | Patient 1, Diagnosis: Flu | Record added | ✅ Pass |

### 6.2 Sample Output

**Main Menu:**
```
==================================================
  🏥 HOSPITAL MANAGEMENT SYSTEM
==================================================
  1. Patient Management
  2. Doctor Management
  3. Appointment Scheduling
  4. Billing System
  5. Medical History
  6. Exit

  Enter choice:
```

**Viewing Patients:**
```
==================================================
  ALL PATIENTS
==================================================

  ID  Name         Age  Gender  Phone       Address
  --  ----         ---  ------  -----       -------
  1   John Doe     30   Male    9876543210  Mumbai
  2   Jane Smith   25   Female  8765432109  Delhi
```

**Billing Summary:**
```
==================================================
  BILLING SUMMARY
==================================================

  Total Billed  : ₹ 5,500.00
  Total Paid    : ₹ 3,000.00
  Total Unpaid  : ₹ 2,500.00
```

---

## Chapter 7 — Conclusion & Future Scope

### 7.1 Conclusion

The Hospital Management System was successfully developed as a console-based Python application. It demonstrates the practical application of:

- **Database management** using SQLite3 with SQL queries.
- **Modular programming** with well-organized functions.
- **Input validation** to ensure data integrity.
- **CRUD operations** across all five modules.
- **Conflict detection** in appointment scheduling.

The system fulfills all the stated objectives and can serve as a functional tool for small clinics or as a learning project for understanding database-driven applications.

### 7.2 Limitations

- No graphical user interface (console only).
- No user authentication or role-based access.
- No report generation (PDF/print).
- Single-user system (no concurrent access).

### 7.3 Future Scope

| Enhancement | Description |
|---|---|
| **Login System** | Add admin, doctor, and receptionist roles with passwords |
| **GUI Version** | Build a graphical interface using Tkinter or Flask |
| **PDF Reports** | Generate printable bills and medical reports |
| **Notifications** | SMS/email reminders for upcoming appointments |
| **Analytics Dashboard** | Charts for revenue, patient trends, doctor workload |
| **Data Export** | Export records to CSV or Excel |
| **Cloud Deployment** | Host as a web application for remote access |

---

## References

1. Python Official Documentation — https://docs.python.org/3/
2. SQLite3 Python Module — https://docs.python.org/3/library/sqlite3.html
3. SQLite Official Website — https://www.sqlite.org/
4. "Automate the Boring Stuff with Python" by Al Sweigart
5. GeeksforGeeks — Python SQLite Tutorial — https://www.geeksforgeeks.org/python-sqlite/
