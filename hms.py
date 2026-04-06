"""
Hospital Management System (HMS)
================================
A simple console-based application using Python and SQLite3.
No external libraries needed — just run: python hms.py

Features:
  1. Patient Registration
  2. Doctor Management
  3. Appointment Scheduling
  4. Billing System
  5. Medical History
"""

import sqlite3
from datetime import date

DB_NAME = "hms.db"


# ─── Database Setup ──────────────────────────────────────────────────────────

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


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

    c.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            name           TEXT NOT NULL,
            specialization TEXT NOT NULL,
            phone          TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id  INTEGER NOT NULL,
            date       TEXT NOT NULL,
            time       TEXT NOT NULL,
            status     TEXT DEFAULT 'Scheduled',
            FOREIGN KEY (patient_id) REFERENCES patients(id),
            FOREIGN KEY (doctor_id)  REFERENCES doctors(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id  INTEGER NOT NULL,
            amount      REAL NOT NULL,
            description TEXT,
            status      TEXT DEFAULT 'Unpaid',
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS medical_history (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id  INTEGER NOT NULL,
            diagnosis   TEXT NOT NULL,
            treatment   TEXT,
            medicines   TEXT,
            rec_date    TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    """)

    conn.commit()
    conn.close()


# ─── Helper Functions ────────────────────────────────────────────────────────

def header(title):
    """Print a formatted section header."""
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)


def pause():
    """Wait for user to press Enter."""
    input("\nPress Enter to continue...")


def print_table(headers, rows):
    """Print rows in a neatly formatted table."""
    if not rows:
        print("  (no records found)")
        return

    # calculate column widths
    widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(str(val)))

    # header line
    fmt = "  ".join(f"{{:<{w}}}" for w in widths)
    print("\n  " + fmt.format(*headers))
    print("  " + "  ".join("-" * w for w in widths))

    # data lines
    for row in rows:
        print("  " + fmt.format(*[str(v) for v in row]))


# ─── 1. Patient Management ──────────────────────────────────────────────────

def patient_menu():
    while True:
        header("PATIENT MANAGEMENT")
        print("  1. Add Patient")
        print("  2. View All Patients")
        print("  3. Search Patient")
        print("  4. Update Patient")
        print("  5. Delete Patient")
        print("  6. Back to Main Menu")

        choice = input("\n  Enter choice: ").strip()

        if choice == "1":
            add_patient()
        elif choice == "2":
            view_patients()
        elif choice == "3":
            search_patient()
        elif choice == "4":
            update_patient()
        elif choice == "5":
            delete_patient()
        elif choice == "6":
            break
        else:
            print("  Invalid choice!")


def add_patient():
    header("ADD NEW PATIENT")
    name    = input("  Name    : ").strip()
    age     = input("  Age     : ").strip()
    gender  = input("  Gender  : ").strip()
    phone   = input("  Phone   : ").strip()
    address = input("  Address : ").strip()

    if not name or not age or not gender:
        print("  ✗ Name, Age and Gender are required!")
        return

    try:
        age = int(age)
    except ValueError:
        print("  ✗ Age must be a number!")
        return

    conn = get_connection()
    conn.execute("INSERT INTO patients (name, age, gender, phone, address) VALUES (?,?,?,?,?)",
                 (name, age, gender, phone, address))
    conn.commit()
    conn.close()
    print(f"  ✓ Patient '{name}' added successfully!")


def view_patients():
    header("ALL PATIENTS")
    conn = get_connection()
    rows = conn.execute("SELECT id, name, age, gender, phone, address FROM patients").fetchall()
    conn.close()
    print_table(["ID", "Name", "Age", "Gender", "Phone", "Address"], rows)
    pause()


def search_patient():
    header("SEARCH PATIENT")
    keyword = input("  Enter name or phone: ").strip()
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, name, age, gender, phone, address FROM patients WHERE name LIKE ? OR phone LIKE ?",
        (f"%{keyword}%", f"%{keyword}%")).fetchall()
    conn.close()
    print_table(["ID", "Name", "Age", "Gender", "Phone", "Address"], rows)
    pause()


def update_patient():
    header("UPDATE PATIENT")
    pid = input("  Enter Patient ID: ").strip()
    conn = get_connection()
    patient = conn.execute("SELECT * FROM patients WHERE id=?", (pid,)).fetchone()
    if not patient:
        print("  ✗ Patient not found!")
        conn.close()
        return

    print(f"  Current: {patient[1]}, Age {patient[2]}, {patient[3]}, {patient[4]}, {patient[5]}")
    print("  (Leave blank to keep current value)\n")

    name    = input(f"  Name    [{patient[1]}]: ").strip() or patient[1]
    age     = input(f"  Age     [{patient[2]}]: ").strip() or patient[2]
    gender  = input(f"  Gender  [{patient[3]}]: ").strip() or patient[3]
    phone   = input(f"  Phone   [{patient[4]}]: ").strip() or patient[4]
    address = input(f"  Address [{patient[5]}]: ").strip() or patient[5]

    conn.execute("UPDATE patients SET name=?, age=?, gender=?, phone=?, address=? WHERE id=?",
                 (name, int(age), gender, phone, address, pid))
    conn.commit()
    conn.close()
    print("  ✓ Patient updated!")


def delete_patient():
    header("DELETE PATIENT")
    pid = input("  Enter Patient ID: ").strip()
    confirm = input("  Are you sure? (y/n): ").strip().lower()
    if confirm != "y":
        return
    conn = get_connection()
    conn.execute("DELETE FROM medical_history WHERE patient_id=?", (pid,))
    conn.execute("DELETE FROM bills WHERE patient_id=?", (pid,))
    conn.execute("DELETE FROM appointments WHERE patient_id=?", (pid,))
    conn.execute("DELETE FROM patients WHERE id=?", (pid,))
    conn.commit()
    conn.close()
    print("  ✓ Patient deleted!")


# ─── 2. Doctor Management ───────────────────────────────────────────────────

def doctor_menu():
    while True:
        header("DOCTOR MANAGEMENT")
        print("  1. Add Doctor")
        print("  2. View All Doctors")
        print("  3. Update Doctor")
        print("  4. Delete Doctor")
        print("  5. Back to Main Menu")

        choice = input("\n  Enter choice: ").strip()

        if choice == "1":
            add_doctor()
        elif choice == "2":
            view_doctors()
        elif choice == "3":
            update_doctor()
        elif choice == "4":
            delete_doctor()
        elif choice == "5":
            break
        else:
            print("  Invalid choice!")


def add_doctor():
    header("ADD NEW DOCTOR")
    name = input("  Name           : ").strip()
    spec = input("  Specialization : ").strip()
    phone = input("  Phone          : ").strip()

    if not name or not spec:
        print("  ✗ Name and Specialization are required!")
        return

    conn = get_connection()
    conn.execute("INSERT INTO doctors (name, specialization, phone) VALUES (?,?,?)",
                 (name, spec, phone))
    conn.commit()
    conn.close()
    print(f"  ✓ Doctor '{name}' added successfully!")


def view_doctors():
    header("ALL DOCTORS")
    conn = get_connection()
    rows = conn.execute("SELECT id, name, specialization, phone FROM doctors").fetchall()
    conn.close()
    print_table(["ID", "Name", "Specialization", "Phone"], rows)
    pause()


def update_doctor():
    header("UPDATE DOCTOR")
    did = input("  Enter Doctor ID: ").strip()
    conn = get_connection()
    doc = conn.execute("SELECT * FROM doctors WHERE id=?", (did,)).fetchone()
    if not doc:
        print("  ✗ Doctor not found!")
        conn.close()
        return

    print(f"  Current: {doc[1]}, {doc[2]}, {doc[3]}")
    print("  (Leave blank to keep current value)\n")

    name  = input(f"  Name           [{doc[1]}]: ").strip() or doc[1]
    spec  = input(f"  Specialization [{doc[2]}]: ").strip() or doc[2]
    phone = input(f"  Phone          [{doc[3]}]: ").strip() or doc[3]

    conn.execute("UPDATE doctors SET name=?, specialization=?, phone=? WHERE id=?",
                 (name, spec, phone, did))
    conn.commit()
    conn.close()
    print("  ✓ Doctor updated!")


def delete_doctor():
    header("DELETE DOCTOR")
    did = input("  Enter Doctor ID: ").strip()
    confirm = input("  Are you sure? (y/n): ").strip().lower()
    if confirm != "y":
        return
    conn = get_connection()
    conn.execute("DELETE FROM appointments WHERE doctor_id=?", (did,))
    conn.execute("DELETE FROM doctors WHERE id=?", (did,))
    conn.commit()
    conn.close()
    print("  ✓ Doctor deleted!")


# ─── 3. Appointment Scheduling ──────────────────────────────────────────────

def appointment_menu():
    while True:
        header("APPOINTMENT SCHEDULING")
        print("  1. Book Appointment")
        print("  2. View All Appointments")
        print("  3. Update Appointment Status")
        print("  4. Cancel Appointment")
        print("  5. Back to Main Menu")

        choice = input("\n  Enter choice: ").strip()

        if choice == "1":
            book_appointment()
        elif choice == "2":
            view_appointments()
        elif choice == "3":
            update_appointment_status()
        elif choice == "4":
            cancel_appointment()
        elif choice == "5":
            break
        else:
            print("  Invalid choice!")


def book_appointment():
    header("BOOK APPOINTMENT")

    # show available patients
    conn = get_connection()
    patients = conn.execute("SELECT id, name FROM patients").fetchall()
    doctors  = conn.execute("SELECT id, name, specialization FROM doctors").fetchall()

    if not patients:
        print("  ✗ No patients registered. Add a patient first!")
        conn.close()
        return
    if not doctors:
        print("  ✗ No doctors available. Add a doctor first!")
        conn.close()
        return

    print("\n  Available Patients:")
    for p in patients:
        print(f"    {p[0]}. {p[1]}")

    pid = input("\n  Enter Patient ID: ").strip()

    print("\n  Available Doctors:")
    for d in doctors:
        print(f"    {d[0]}. {d[1]} ({d[2]})")

    did       = input("\n  Enter Doctor ID : ").strip()
    appt_date = input(f"  Date (YYYY-MM-DD) [{date.today()}]: ").strip() or str(date.today())
    appt_time = input("  Time (HH:MM)    : ").strip()

    if not pid or not did or not appt_time:
        print("  ✗ All fields are required!")
        conn.close()
        return

    # check for conflict
    conflict = conn.execute(
        "SELECT id FROM appointments WHERE doctor_id=? AND date=? AND time=? AND status='Scheduled'",
        (did, appt_date, appt_time)).fetchone()

    if conflict:
        print("  ✗ Doctor already has an appointment at that date/time!")
        conn.close()
        return

    conn.execute("INSERT INTO appointments (patient_id, doctor_id, date, time) VALUES (?,?,?,?)",
                 (pid, did, appt_date, appt_time))
    conn.commit()
    conn.close()
    print("  ✓ Appointment booked successfully!")


def view_appointments():
    header("ALL APPOINTMENTS")
    conn = get_connection()
    rows = conn.execute("""
        SELECT a.id, p.name, d.name, a.date, a.time, a.status
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors  d ON a.doctor_id  = d.id
        ORDER BY a.date, a.time
    """).fetchall()
    conn.close()
    print_table(["ID", "Patient", "Doctor", "Date", "Time", "Status"], rows)
    pause()


def update_appointment_status():
    header("UPDATE APPOINTMENT STATUS")
    aid = input("  Enter Appointment ID: ").strip()
    print("  1. Scheduled")
    print("  2. Completed")
    print("  3. Cancelled")
    status_map = {"1": "Scheduled", "2": "Completed", "3": "Cancelled"}
    s = input("  Choose status: ").strip()

    if s not in status_map:
        print("  ✗ Invalid choice!")
        return

    conn = get_connection()
    conn.execute("UPDATE appointments SET status=? WHERE id=?", (status_map[s], aid))
    conn.commit()
    conn.close()
    print("  ✓ Appointment status updated!")


def cancel_appointment():
    header("CANCEL APPOINTMENT")
    aid = input("  Enter Appointment ID: ").strip()
    conn = get_connection()
    conn.execute("UPDATE appointments SET status='Cancelled' WHERE id=?", (aid,))
    conn.commit()
    conn.close()
    print("  ✓ Appointment cancelled!")


# ─── 4. Billing System ──────────────────────────────────────────────────────

def billing_menu():
    while True:
        header("BILLING SYSTEM")
        print("  1. Create Bill")
        print("  2. View All Bills")
        print("  3. Mark Bill as Paid")
        print("  4. View Billing Summary")
        print("  5. Delete Bill")
        print("  6. Back to Main Menu")

        choice = input("\n  Enter choice: ").strip()

        if choice == "1":
            create_bill()
        elif choice == "2":
            view_bills()
        elif choice == "3":
            mark_bill_paid()
        elif choice == "4":
            billing_summary()
        elif choice == "5":
            delete_bill()
        elif choice == "6":
            break
        else:
            print("  Invalid choice!")


def create_bill():
    header("CREATE BILL")
    conn = get_connection()
    patients = conn.execute("SELECT id, name FROM patients").fetchall()

    if not patients:
        print("  ✗ No patients registered!")
        conn.close()
        return

    print("\n  Patients:")
    for p in patients:
        print(f"    {p[0]}. {p[1]}")

    pid    = input("\n  Enter Patient ID  : ").strip()
    amount = input("  Amount (₹)        : ").strip()
    desc   = input("  Description       : ").strip()

    if not pid or not amount:
        print("  ✗ Patient ID and Amount are required!")
        conn.close()
        return

    try:
        amount = float(amount)
    except ValueError:
        print("  ✗ Amount must be a number!")
        conn.close()
        return

    conn.execute("INSERT INTO bills (patient_id, amount, description) VALUES (?,?,?)",
                 (pid, amount, desc))
    conn.commit()
    conn.close()
    print("  ✓ Bill created successfully!")


def view_bills():
    header("ALL BILLS")
    conn = get_connection()
    rows = conn.execute("""
        SELECT b.id, p.name, b.amount, b.description, b.status
        FROM bills b JOIN patients p ON b.patient_id = p.id
        ORDER BY b.id DESC
    """).fetchall()
    conn.close()
    print_table(["ID", "Patient", "Amount", "Description", "Status"], rows)
    pause()


def mark_bill_paid():
    header("MARK BILL AS PAID")
    bid = input("  Enter Bill ID: ").strip()
    conn = get_connection()
    conn.execute("UPDATE bills SET status='Paid' WHERE id=?", (bid,))
    conn.commit()
    conn.close()
    print("  ✓ Bill marked as Paid!")


def billing_summary():
    header("BILLING SUMMARY")
    conn = get_connection()
    total  = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM bills").fetchone()[0]
    paid   = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM bills WHERE status='Paid'").fetchone()[0]
    unpaid = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM bills WHERE status='Unpaid'").fetchone()[0]
    conn.close()
    print(f"\n  Total Billed  : ₹ {total:,.2f}")
    print(f"  Total Paid    : ₹ {paid:,.2f}")
    print(f"  Total Unpaid  : ₹ {unpaid:,.2f}")
    pause()


def delete_bill():
    header("DELETE BILL")
    bid = input("  Enter Bill ID: ").strip()
    confirm = input("  Are you sure? (y/n): ").strip().lower()
    if confirm != "y":
        return
    conn = get_connection()
    conn.execute("DELETE FROM bills WHERE id=?", (bid,))
    conn.commit()
    conn.close()
    print("  ✓ Bill deleted!")


# ─── 5. Medical History ─────────────────────────────────────────────────────

def history_menu():
    while True:
        header("MEDICAL HISTORY")
        print("  1. Add Medical Record")
        print("  2. View All Records")
        print("  3. View Patient History")
        print("  4. Update Record")
        print("  5. Delete Record")
        print("  6. Back to Main Menu")

        choice = input("\n  Enter choice: ").strip()

        if choice == "1":
            add_medical_record()
        elif choice == "2":
            view_all_records()
        elif choice == "3":
            view_patient_history()
        elif choice == "4":
            update_medical_record()
        elif choice == "5":
            delete_medical_record()
        elif choice == "6":
            break
        else:
            print("  Invalid choice!")


def add_medical_record():
    header("ADD MEDICAL RECORD")
    conn = get_connection()
    patients = conn.execute("SELECT id, name FROM patients").fetchall()

    if not patients:
        print("  ✗ No patients registered!")
        conn.close()
        return

    print("\n  Patients:")
    for p in patients:
        print(f"    {p[0]}. {p[1]}")

    pid       = input("\n  Enter Patient ID : ").strip()
    diagnosis = input("  Diagnosis        : ").strip()
    treatment = input("  Treatment        : ").strip()
    medicines = input("  Medicines        : ").strip()
    rec_date  = input(f"  Date [{date.today()}]: ").strip() or str(date.today())

    if not pid or not diagnosis:
        print("  ✗ Patient ID and Diagnosis are required!")
        conn.close()
        return

    conn.execute(
        "INSERT INTO medical_history (patient_id, diagnosis, treatment, medicines, rec_date) VALUES (?,?,?,?,?)",
        (pid, diagnosis, treatment, medicines, rec_date))
    conn.commit()
    conn.close()
    print("  ✓ Medical record added!")


def view_all_records():
    header("ALL MEDICAL RECORDS")
    conn = get_connection()
    rows = conn.execute("""
        SELECT m.id, p.name, m.diagnosis, m.treatment, m.medicines, m.rec_date
        FROM medical_history m JOIN patients p ON m.patient_id = p.id
        ORDER BY m.rec_date DESC
    """).fetchall()
    conn.close()
    print_table(["ID", "Patient", "Diagnosis", "Treatment", "Medicines", "Date"], rows)
    pause()


def view_patient_history():
    header("VIEW PATIENT HISTORY")
    pid = input("  Enter Patient ID: ").strip()
    conn = get_connection()
    patient = conn.execute("SELECT name FROM patients WHERE id=?", (pid,)).fetchone()
    if not patient:
        print("  ✗ Patient not found!")
        conn.close()
        return
    print(f"\n  Medical History for: {patient[0]}")
    rows = conn.execute("""
        SELECT m.id, m.diagnosis, m.treatment, m.medicines, m.rec_date
        FROM medical_history m WHERE m.patient_id = ?
        ORDER BY m.rec_date DESC
    """, (pid,)).fetchall()
    conn.close()
    print_table(["ID", "Diagnosis", "Treatment", "Medicines", "Date"], rows)
    pause()


def update_medical_record():
    header("UPDATE MEDICAL RECORD")
    mid = input("  Enter Record ID: ").strip()
    conn = get_connection()
    rec = conn.execute("SELECT * FROM medical_history WHERE id=?", (mid,)).fetchone()
    if not rec:
        print("  ✗ Record not found!")
        conn.close()
        return

    print(f"  Current: {rec[2]}, {rec[3]}, {rec[4]}, {rec[5]}")
    print("  (Leave blank to keep current value)\n")

    diagnosis = input(f"  Diagnosis  [{rec[2]}]: ").strip() or rec[2]
    treatment = input(f"  Treatment  [{rec[3]}]: ").strip() or rec[3]
    medicines = input(f"  Medicines  [{rec[4]}]: ").strip() or rec[4]
    rec_date  = input(f"  Date       [{rec[5]}]: ").strip() or rec[5]

    conn.execute("UPDATE medical_history SET diagnosis=?, treatment=?, medicines=?, rec_date=? WHERE id=?",
                 (diagnosis, treatment, medicines, rec_date, mid))
    conn.commit()
    conn.close()
    print("  ✓ Record updated!")


def delete_medical_record():
    header("DELETE MEDICAL RECORD")
    mid = input("  Enter Record ID: ").strip()
    confirm = input("  Are you sure? (y/n): ").strip().lower()
    if confirm != "y":
        return
    conn = get_connection()
    conn.execute("DELETE FROM medical_history WHERE id=?", (mid,))
    conn.commit()
    conn.close()
    print("  ✓ Record deleted!")


# ─── Main Menu ───────────────────────────────────────────────────────────────

def main():
    init_db()

    while True:
        header("🏥 HOSPITAL MANAGEMENT SYSTEM")
        print("  1. Patient Management")
        print("  2. Doctor Management")
        print("  3. Appointment Scheduling")
        print("  4. Billing System")
        print("  5. Medical History")
        print("  6. Exit")

        choice = input("\n  Enter choice: ").strip()

        if choice == "1":
            patient_menu()
        elif choice == "2":
            doctor_menu()
        elif choice == "3":
            appointment_menu()
        elif choice == "4":
            billing_menu()
        elif choice == "5":
            history_menu()
        elif choice == "6":
            print("\n  Thank you for using HMS! Goodbye.\n")
            break
        else:
            print("  Invalid choice! Try again.")


if __name__ == "__main__":
    main()
