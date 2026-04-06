# 🏥 Hospital Management System (HMS)

A simple **console-based** Hospital Management System built with Python and SQLite3.  
No external libraries needed — just run it!

---

## How to Run

```bash
python hms.py
```

> The database file `hms.db` is auto-created on first run.

---

## Features

| # | Module                  | What You Can Do                                              |
|---|-------------------------|--------------------------------------------------------------|
| 1 | **Patient Management**  | Add, view, search, update, delete patients                   |
| 2 | **Doctor Management**   | Add, view, update, delete doctors                            |
| 3 | **Appointment Scheduling** | Book appointments (with conflict detection), update status, cancel |
| 4 | **Billing System**      | Create bills, mark paid, view summary, delete bills          |
| 5 | **Medical History**     | Add records, view all / per-patient history, update, delete  |

---

## Menu Structure

```
MAIN MENU
├── 1. Patient Management
│   ├── Add / View / Search / Update / Delete
├── 2. Doctor Management
│   ├── Add / View / Update / Delete
├── 3. Appointment Scheduling
│   ├── Book / View / Update Status / Cancel
├── 4. Billing System
│   ├── Create / View / Mark Paid / Summary / Delete
├── 5. Medical History
│   ├── Add / View All / View by Patient / Update / Delete
└── 6. Exit
```

---

## Database Tables

| Table              | Key Columns                                      |
|--------------------|--------------------------------------------------|
| `patients`         | id, name, age, gender, phone, address             |
| `doctors`          | id, name, specialization, phone                   |
| `appointments`     | id, patient_id, doctor_id, date, time, status     |
| `bills`            | id, patient_id, amount, description, status       |
| `medical_history`  | id, patient_id, diagnosis, treatment, medicines, date |

---

## Tech Stack

- **Python 3** (standard library only)
- **SQLite3** — lightweight embedded database
- No `pip install` needed

---

## Project Files

```
hms/
├── hms.py      ← entire application (single file)
├── hms.db      ← database (auto-created)
└── README.md   ← this file
```
