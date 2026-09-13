import tkinter as tk
from tkinter import ttk, messagebox
from core.config import (
    PATIENT_FILE,
    PATIENT_HEADERS
)
from core.database import (
    read_csv,
    write_csv,
    append_csv,
    generate_id
)
from core.utils import validate_phone, validate_age

class Patients:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(
            parent,
            bg="#F4F7FB"
        )
        self.selected_id = None
        self.create_ui()
        self.load_patients()

    def create_ui(self):
        tk.Label(
            self.frame,
            text="Patient Management",
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
            text="Add, update, delete and search patient records",
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
        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.disease_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.add_field(
            form,
            "Name",
            self.name_var,
            0,
            0
        )
        self.add_field(
            form,
            "Age",
            self.age_var,
            0,
            2
        )
        tk.Label(
            form,
            text="Gender",
            bg="white",
            fg="#374151",
            font=("Arial", 10, "bold")
        ).grid(
            row=0,
            column=4,
            padx=10,
            pady=(15, 5),
            sticky="w"
        )
        ttk.Combobox(
            form,
            textvariable=self.gender_var,
            values=["Male", "Female", "Other"],
            state="readonly",
            width=18
        ).grid(
            row=1,
            column=4,
            padx=10,
            pady=(0, 15),
            sticky="w"
        )
        self.add_field(
            form,
            "Phone",
            self.phone_var,
            2,
            0
        )
        self.add_field(
            form,
            "Disease",
            self.disease_var,
            2,
            2
        )
        self.add_field(
            form,
            "Address",
            self.address_var,
            2,
            4
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
            "Add Patient",
            self.add_patient,
            "#2563EB"
        )
        self.make_button(
            buttons,
            "Update",
            self.update_patient,
            "#059669"
        )
        self.make_button(
            buttons,
            "Delete",
            self.delete_patient,
            "#DC2626"
        )
        self.make_button(
            buttons,
            "Clear",
            self.clear_form,
            "#6B7280"
        )
        search_frame = tk.Frame(
            self.frame,
            bg="#F4F7FB"
        )
        search_frame.pack(
            fill="x",
            padx=30,
            pady=15
        )
        tk.Label(
            search_frame,
            text="Search:",
            font=("Arial", 10, "bold"),
            bg="#F4F7FB",
            fg="#374151"
        ).pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.search_patient)
        tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Arial", 10),
            width=35
        ).pack(side="left", padx=10)
        self.make_button(
            search_frame,
            "Show All",
            self.load_patients,
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
            pady=(0, 20)
        )
        columns = PATIENT_HEADERS
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )
        widths = {
            "Patient ID": 90,
            "Name": 150,
            "Age": 70,
            "Gender": 100,
            "Phone": 120,
            "Disease": 150,
            "Address": 220
        }
        for column in columns:
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
            self.select_patient
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
            width=22,
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

    def add_patient(self):
        name = self.name_var.get().strip()
        age = self.age_var.get().strip()
        gender = self.gender_var.get().strip()
        phone = self.phone_var.get().strip()
        disease = self.disease_var.get().strip()
        address = self.address_var.get().strip()
        if not name or not age or not gender or not phone:
            messagebox.showwarning(
                "Validation",
                "Please fill Name, Age, Gender and Phone."
            )
            return
        if not validate_age(age):
            messagebox.showwarning(
                "Validation",
                "Age must be a positive number."
            )
            return
        if not validate_phone(phone):
            messagebox.showwarning(
                "Validation",
                "Phone number must contain exactly 10 digits."
            )
            return
        patient_id = generate_id(
            "P",
            PATIENT_FILE,
            "Patient ID"
        )
        row = {
            "Patient ID": patient_id,
            "Name": name,
            "Age": age,
            "Gender": gender,
            "Phone": phone,
            "Disease": disease,
            "Address": address
        }
        append_csv(
            PATIENT_FILE,
            PATIENT_HEADERS,
            row
        )
        messagebox.showinfo(
            "Success",
            f"Patient added successfully.\nPatient ID: {patient_id}"
        )
        self.clear_form()
        self.load_patients()

    def update_patient(self):
        if not self.selected_id:
            messagebox.showwarning(
                "Selection",
                "Please select a patient to update."
            )
            return
        records = read_csv(PATIENT_FILE)
        for record in records:
            if record["Patient ID"] == self.selected_id:
                record["Name"] = self.name_var.get().strip()
                record["Age"] = self.age_var.get().strip()
                record["Gender"] = self.gender_var.get().strip()
                record["Phone"] = self.phone_var.get().strip()
                record["Disease"] = self.disease_var.get().strip()
                record["Address"] = self.address_var.get().strip()
                break
        write_csv(
            PATIENT_FILE,
            PATIENT_HEADERS,
            records
        )
        messagebox.showinfo(
            "Success",
            "Patient updated successfully."
        )
        self.clear_form()
        self.load_patients()

    def delete_patient(self):
        if not self.selected_id:
            messagebox.showwarning(
                "Selection",
                "Please select a patient to delete."
            )
            return
        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this patient?"
        )
        if not confirm:
            return
        records = read_csv(PATIENT_FILE)
        records = [
            record
            for record in records
            if record["Patient ID"] != self.selected_id
        ]
        write_csv(
            PATIENT_FILE,
            PATIENT_HEADERS,
            records
        )
        messagebox.showinfo(
            "Success",
            "Patient deleted successfully."
        )
        self.clear_form()
        self.load_patients()

    def clear_form(self):
        self.selected_id = None
        self.name_var.set("")
        self.age_var.set("")
        self.gender_var.set("")
        self.phone_var.set("")
        self.disease_var.set("")
        self.address_var.set("")
        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def load_patients(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        records = read_csv(PATIENT_FILE)
        for record in records:
            self.tree.insert(
                "",
                "end",
                values=[
                    record.get(column, "")
                    for column in PATIENT_HEADERS
                ]
            )

    def search_patient(self, *args):
        search = self.search_var.get().strip().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)
        records = read_csv(PATIENT_FILE)
        if not search:
            for record in records:
                self.tree.insert(
                    "",
                    "end",
                    values=[
                        record.get(column, "")
                        for column in PATIENT_HEADERS
                    ]
                )
            return
        for record in records:
            patient_id = record.get("Patient ID", "").lower()
            name = record.get("Name", "").lower()
            disease = record.get("Disease", "").lower()
            if (
                search in patient_id
                or search in name
                or search in disease
            ):
                self.tree.insert(
                    "",
                    "end",
                    values=[
                        record.get(column, "")
                        for column in PATIENT_HEADERS
                    ]
                )

    def select_patient(self, event):
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
        self.name_var.set(values[1])
        self.age_var.set(values[2])
        self.gender_var.set(values[3])
        self.phone_var.set(values[4])
        self.disease_var.set(values[5])
        self.address_var.set(values[6])