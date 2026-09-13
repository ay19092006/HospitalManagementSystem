import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(BASE_DIR, "data")
PATIENT_FILE = os.path.join(DATA_FOLDER, "patients.csv")
DOCTOR_FILE = os.path.join(DATA_FOLDER, "doctors.csv")
APPOINTMENT_FILE = os.path.join(DATA_FOLDER, "appointments.csv")
BILL_FILE = os.path.join(DATA_FOLDER, "bills.csv")
PATIENT_HEADERS = [
    "Patient ID",
    "Name",
    "Age",
    "Gender",
    "Phone",
    "Disease",
    "Address"
]
DOCTOR_HEADERS = [
    "Doctor ID",
    "Name",
    "Specialization",
    "Phone",
    "Experience"
]
APPOINTMENT_HEADERS = [
    "Appointment ID",
    "Patient ID",
    "Doctor ID",
    "Date",
    "Time",
    "Status"
]
BILL_HEADERS = [
    "Bill ID",
    "Patient ID",
    "Patient Name",
    "Consultation",
    "Medicine",
    "Room",
    "Total"
]