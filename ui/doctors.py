import tkinter as tk
from tkinter import ttk, messagebox
from core.config import (
    DOCTOR_FILE,
    DOCTOR_HEADERS
)
from core.database import (
    read_csv,
    write_csv,
    append_csv,
    generate_id
)
from core.utils import validate_phone

class Doctors:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(
            parent,
            bg="#F4F7FB"
        )
        self.selected_id = None
        self.create_ui()
        self.load_doctors()

    def create_ui(self):
        tk.Label(
            self.frame,
            text="Doctor Management",
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
            text="Manage doctor information and records",
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
        self.specialization_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.experience_var = tk.StringVar()
        self.add_field(
            form,
            "Name",
            self.name_var,
            0,
            0
        )
        self.add_field(
            form,
            "Specialization",
            self.specialization_var,
            0,
            2
        )
        self.add_field(
            form,
            "Phone",
            self.phone_var,
            0,
            4
        )
        self.add_field(
            form,
            "Experience",
            self.experience_var,
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
            "Add Doctor",
            self.add_doctor,
            "#2563EB"
        )
        self.make_button(
            buttons,
            "Update",
            self.update_doctor,
            "#059669"
        )
        self.make_button(
            buttons,
            "Delete",
            self.delete_doctor,
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
            columns=DOCTOR_HEADERS,
            show="headings"
        )
        widths = {
            "Doctor ID": 100,
            "Name": 180,
            "Specialization": 200,
            "Phone": 150,
            "Experience": 130
        }
        for column in DOCTOR_HEADERS:
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
            self.select_doctor
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

    def add_doctor(self):
        name = self.name_var.get().strip()
        specialization = self.specialization_var.get().strip()
        phone = self.phone_var.get().strip()
        experience = self.experience_var.get().strip()
        if not name or not specialization or not phone:
            messagebox.showwarning(
                "Validation",
                "Please fill Name, Specialization and Phone."
            )
            return
        if not validate_phone(phone):
            messagebox.showwarning(
                "Validation",
                "Phone number must contain exactly 10 digits."
            )
            return
        doctor_id = generate_id(
            "D",
            DOCTOR_FILE,
            "Doctor ID"
        )
        row = {
            "Doctor ID": doctor_id,
            "Name": name,
            "Specialization": specialization,
            "Phone": phone,
            "Experience": experience
        }
        append_csv(
            DOCTOR_FILE,
            DOCTOR_HEADERS,
            row
        )
        messagebox.showinfo(
            "Success",
            f"Doctor added successfully.\nDoctor ID: {doctor_id}"
        )
        self.clear_form()
        self.load_doctors()

    def update_doctor(self):
        if not self.selected_id:
            messagebox.showwarning(
                "Selection",
                "Please select a doctor to update."
            )
            return
        records = read_csv(DOCTOR_FILE)
        for record in records:
            if record["Doctor ID"] == self.selected_id:
                record["Name"] = self.name_var.get().strip()
                record["Specialization"] = self.specialization_var.get().strip()
                record["Phone"] = self.phone_var.get().strip()
                record["Experience"] = self.experience_var.get().strip()
                break
        write_csv(
            DOCTOR_FILE,
            DOCTOR_HEADERS,
            records
        )
        messagebox.showinfo(
            "Success",
            "Doctor updated successfully."
        )
        self.clear_form()
        self.load_doctors()

    def delete_doctor(self):
        if not self.selected_id:
            messagebox.showwarning(
                "Selection",
                "Please select a doctor to delete."
            )
            return
        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this doctor?"
        )
        if not confirm:
            return
        records = read_csv(DOCTOR_FILE)
        records = [
            record
            for record in records
            if record["Doctor ID"] != self.selected_id
        ]
        write_csv(
            DOCTOR_FILE,
            DOCTOR_HEADERS,
            records
        )
        messagebox.showinfo(
            "Success",
            "Doctor deleted successfully."
        )
        self.clear_form()
        self.load_doctors()

    def clear_form(self):
        self.selected_id = None
        self.name_var.set("")
        self.specialization_var.set("")
        self.phone_var.set("")
        self.experience_var.set("")
        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def load_doctors(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        records = read_csv(DOCTOR_FILE)
        for record in records:
            self.tree.insert(
                "",
                "end",
                values=[
                    record.get(column, "")
                    for column in DOCTOR_HEADERS
                ]
            )

    def select_doctor(self, event):
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
        self.specialization_var.set(values[2])
        self.phone_var.set(values[3])
        self.experience_var.set(values[4])