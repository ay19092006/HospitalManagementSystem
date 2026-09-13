import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from core.config import (
    APPOINTMENT_FILE,
    APPOINTMENT_HEADERS,
    PATIENT_FILE,
    DOCTOR_FILE
)
from core.database import (
    read_csv,
    write_csv,
    append_csv,
    generate_id
)
from core.utils import validate_date

class Appointments:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(
            parent,
            bg="#F4F7FB"
        )
        self.selected_id = None
        self.create_ui()
        self.load_appointments()

    def create_ui(self):
        tk.Label(
            self.frame,
            text="Appointment Management",
            font=("Arial", 24, "bold"),
            bg="#F4F7FB",
            fg="#1F2937"
        ).pack(
            anchor="w",
            padx=30,
            pady=(25, 5)
        )
        tk.Label(
            self.frame,
            text="Schedule and manage patient appointments",
            font=("Arial", 11),
            bg="#F4F7FB",
            fg="#6B7280"
        ).pack(
            anchor="w",
            padx=30,
            pady=(0, 15)
        )
        form = tk.Frame(
            self.frame,
            bg="white",
            highlightbackground="#E5E7EB",
            highlightthickness=1
        )
        form.pack(
            fill="x",
            padx=30,
            pady=5
        )
        self.patient_var = tk.StringVar()
        self.doctor_var = tk.StringVar()
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.time_var = tk.StringVar(value="10:00")
        self.add_field(
            form,
            "Patient ID",
            self.patient_var,
            0,
            0
        )
        self.add_field(
            form,
            "Doctor ID",
            self.doctor_var,
            0,
            2
        )
        self.add_field(
            form,
            "Date (YYYY-MM-DD)",
            self.date_var,
            0,
            4
        )
        self.add_field(
            form,
            "Time",
            self.time_var,
            2,
            0
        )
        buttons = tk.Frame(
            form,
            bg="white"
        )
        buttons.grid(
            row=4,
            column=0,
            columnspan=6,
            padx=10,
            pady=(0, 15),
            sticky="w"
        )
        self.make_button(
            buttons,
            "Add Appointment",
            self.add_appointment,
            "#2563EB"
        )
        self.make_button(
            buttons,
            "Cancel Appointment",
            self.cancel_appointment,
            "#DC2626"
        )
        self.make_button(
            buttons,
            "Clear",
            self.clear_form,
            "#6B7280"
        )
        table_frame = tk.Frame(
            self.frame,
            bg="white"
        )
        table_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20
        )
        self.tree = ttk.Treeview(
            table_frame,
            columns=APPOINTMENT_HEADERS,
            show="headings"
        )
        widths = {
            "Appointment ID": 120,
            "Patient ID": 110,
            "Doctor ID": 110,
            "Date": 130,
            "Time": 100,
            "Status": 130
        }
        for column in APPOINTMENT_HEADERS:
            self.tree.heading(
                column,
                text=column
            )
            self.tree.column(
                column,
                width=widths.get(column, 120),
                anchor="center"
            )
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(
            yscrollcommand=scrollbar.set
        )
        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )
        scrollbar.pack(
            side="right",
            fill="y"
        )
        self.tree.bind(
            "<ButtonRelease-1>",
            self.select_appointment
        )

    def add_field(
        self,
        parent,
        label,
        variable,
        row,
        column
    ):
        tk.Label(
            parent,
            text=label,
            bg="white",
            fg="#374151",
            font=("Arial", 10, "bold")
        ).grid(
            row=row,
            column=column,
            padx=10,
            pady=(15, 5),
            sticky="w"
        )
        tk.Entry(
            parent,
            textvariable=variable,
            width=25,
            font=("Arial", 10)
        ).grid(
            row=row + 1,
            column=column,
            padx=10,
            pady=(0, 15),
            sticky="w"
        )

    def make_button(
        self,
        parent,
        text,
        command,
        color
    ):
        tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=15,
            pady=7,
            cursor="hand2"
        ).pack(side="left", padx=5)

    def add_appointment(self):
        patient_id = self.patient_var.get().strip()
        doctor_id = self.doctor_var.get().strip()
        date = self.date_var.get().strip()
        time = self.time_var.get().strip()
        patients = read_csv(PATIENT_FILE)
        doctors = read_csv(DOCTOR_FILE)
        patient_exists = any(
            p["Patient ID"] == patient_id
            for p in patients
        )
        doctor_exists = any(
            d["Doctor ID"] == doctor_id
            for d in doctors
        )
        if not patient_exists:
            messagebox.showwarning(
                "Validation",
                "Patient ID does not exist."
            )
            return
        if not doctor_exists:
            messagebox.showwarning(
                "Validation",
                "Doctor ID does not exist."
            )
            return
        if not validate_date(date):
            messagebox.showwarning(
                "Validation",
                "Date must be in YYYY-MM-DD format."
            )
            return
        appointment_id = generate_id(
            "A",
            APPOINTMENT_FILE,
            "Appointment ID"
        )
        row = {
            "Appointment ID": appointment_id,
            "Patient ID": patient_id,
            "Doctor ID": doctor_id,
            "Date": date,
            "Time": time,
            "Status": "Scheduled"
        }
        append_csv(
            APPOINTMENT_FILE,
            APPOINTMENT_HEADERS,
            row
        )
        messagebox.showinfo(
            "Success",
            f"Appointment added successfully.\nAppointment ID: {appointment_id}"
        )
        self.clear_form()
        self.load_appointments()

    def cancel_appointment(self):
        if not self.selected_id:
            messagebox.showwarning(
                "Selection",
                "Please select an appointment."
            )
            return
        records = read_csv(APPOINTMENT_FILE)
        for record in records:
            if record["Appointment ID"] == self.selected_id:
                if record["Status"] == "Cancelled":
                    messagebox.showinfo(
                        "Information",
                        "This appointment is already cancelled."
                    )
                    return
                record["Status"] = "Cancelled"
                break
        write_csv(
            APPOINTMENT_FILE,
            APPOINTMENT_HEADERS,
            records
        )
        messagebox.showinfo(
            "Success",
            "Appointment cancelled successfully."
        )
        self.clear_form()
        self.load_appointments()

    def clear_form(self):
        self.selected_id = None
        self.patient_var.set("")
        self.doctor_var.set("")
        self.date_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.time_var.set("10:00")
        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def load_appointments(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        records = read_csv(APPOINTMENT_FILE)
        for record in records:
            self.tree.insert(
                "",
                "end",
                values=[
                    record.get(column, "")
                    for column in APPOINTMENT_HEADERS
                ]
            )

    def select_appointment(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(
            selected[0],
            "values"
        )
        if not values:
            return
        self.selected_id = values[0]
        self.patient_var.set(values[1])
        self.doctor_var.set(values[2])
        self.date_var.set(values[3])
        self.time_var.set(values[4])