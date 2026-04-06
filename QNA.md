# 🎓 HMS — Viva / Q&A Preparation

---

## 1. What is your project?

This is a **Hospital Management System (HMS)** — a console-based Python application that helps manage day-to-day hospital operations. It covers five core modules:

- **Patient Registration** — store and manage patient details.
- **Doctor Management** — maintain a directory of doctors and their specializations.
- **Appointment Scheduling** — book patient-doctor appointments with conflict detection.
- **Billing System** — generate bills, track payments, and view financial summaries.
- **Medical History** — record diagnoses, treatments, and prescribed medicines for each patient.

The entire application runs in a single Python file (`hms.py`) using **SQLite3** as the database — no external libraries or installations are needed.

---

## 2. Which data structures are used?

| Data Structure | Where It's Used | Why |
|---|---|---|
| **Lists** | Storing rows fetched from the database (`fetchall()` returns a list of tuples) | Easy iteration for displaying records in tables |
| **Tuples** | Each database row is returned as a tuple | Immutable, memory-efficient representation of a record |
| **Dictionaries** | `status_map` in appointment status update (`{"1": "Scheduled", ...}`) | Fast key-based lookup for mapping user input to values |
| **Strings** | All user input handling, SQL queries, formatted output | Core data type for text processing |
| **SQLite Tables (Relational)** | `patients`, `doctors`, `appointments`, `bills`, `medical_history` | Persistent storage with relationships via foreign keys |

### Why SQLite instead of plain files?

- Supports **structured queries** (SQL) — easy to search, filter, and join data.
- **ACID compliant** — data is safe even if the program crashes.
- **Foreign keys** — enforces relationships (e.g., a bill must belong to an existing patient).
- Built into Python — no installation needed.

---

## 3. How does billing work?

The billing module works in these steps:

1. **Create a Bill** — the user selects a patient (by ID), enters the amount and a description. The bill is saved with status `Unpaid`.
2. **View Bills** — all bills are displayed in a table showing patient name, amount, description, and payment status.
3. **Mark as Paid** — the user enters a Bill ID and its status changes from `Unpaid` → `Paid`.
4. **Billing Summary** — shows three totals:
   - Total Billed (sum of all bills)
   - Total Paid (sum of paid bills)
   - Total Unpaid (sum of unpaid bills)
5. **Delete Bill** — removes a bill record after confirmation.

### SQL used behind the scenes:

```sql
-- Creating a bill
INSERT INTO bills (patient_id, amount, description) VALUES (?, ?, ?);

-- Marking as paid
UPDATE bills SET status = 'Paid' WHERE id = ?;

-- Summary calculation
SELECT COALESCE(SUM(amount), 0) FROM bills;                    -- total
SELECT COALESCE(SUM(amount), 0) FROM bills WHERE status='Paid';  -- paid
SELECT COALESCE(SUM(amount), 0) FROM bills WHERE status='Unpaid'; -- unpaid
```

---

## 4. Future improvements?

- **Login System** — add admin/doctor/receptionist roles with password authentication.
- **GUI Interface** — build a graphical version using Tkinter or a web framework like Flask.
- **PDF Reports** — generate printable bills and medical reports using a library like `reportlab`.
- **Appointment Reminders** — send SMS or email reminders using APIs.
- **Search & Filters** — advanced search across all modules (by date range, specialization, etc.).
- **Prescription Module** — dedicated module for managing medicines and dosages.
- **Dashboard / Analytics** — show graphs for patient count, revenue trends, doctor workload.
- **Data Export** — export records to CSV or Excel for external analysis.
- **Multi-user Support** — allow concurrent usage over a network using a client-server architecture.
- **Audit Log** — track who made what changes and when for accountability.

---

## 5. What is SQLite? Why did you choose it?

SQLite is a **lightweight, serverless, file-based relational database**. It stores the entire database in a single file (`hms.db`).

**Why we chose it:**
- Comes **built-in with Python** (`import sqlite3`) — zero setup.
- Perfect for **small-to-medium projects** and desktop apps.
- Supports **SQL queries**, joins, and foreign keys.
- No separate database server needed.

---

## 6. What is CRUD?

CRUD stands for the four basic operations on data:

| Letter | Operation | Example in HMS |
|--------|-----------|----------------|
| **C** | Create | Adding a new patient |
| **R** | Read | Viewing all doctors |
| **U** | Update | Editing a medical record |
| **D** | Delete | Removing a bill |

Every module in this project implements full CRUD operations.

---

## 7. How does appointment conflict detection work?

Before booking, the system checks if the selected doctor already has a `Scheduled` appointment at the same date and time:

```sql
SELECT id FROM appointments
WHERE doctor_id = ? AND date = ? AND time = ? AND status = 'Scheduled';
```

If a row is found → **conflict** → booking is rejected.  
If no row is found → **slot is free** → appointment is created.

---

## 8. What are foreign keys and how are they used?

A **foreign key** links a column in one table to the primary key of another table, ensuring data consistency.

In our project:
- `appointments.patient_id` → references `patients.id`
- `appointments.doctor_id` → references `doctors.id`
- `bills.patient_id` → references `patients.id`
- `medical_history.patient_id` → references `patients.id`

This means you **cannot** create a bill for a patient that doesn't exist.

---

## 9. What Python concepts are used in this project?

- **Functions** — each feature is a separate function (modular design)
- **Loops** — `while True` for menus, `for` for iterating over records
- **Conditionals** — `if/elif/else` for menu choices and validation
- **String formatting** — f-strings for output display
- **Exception handling** — `try/except` for validating numeric input
- **Modules** — `sqlite3` for database, `datetime` for dates
- **File I/O (via SQLite)** — persistent data storage

---

## 10. How do you handle input validation?

- **Required fields** — checked with `if not variable` before saving.
- **Numeric validation** — age and amount use `try/except ValueError`.
- **Date defaults** — if user leaves date blank, today's date is used.
- **Delete confirmation** — asks `Are you sure? (y/n)` before deleting.
- **Conflict checks** — appointments are validated against existing bookings.
