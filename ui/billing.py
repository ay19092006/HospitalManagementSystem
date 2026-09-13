import tkinter as tk
from tkinter import ttk, messagebox
from core.config import (
    BILL_FILE,
    BILL_HEADERS,
    PATIENT_FILE
)
from core.database import (
    read_csv,
    write_csv,
    append_csv,
    generate_id
)


class Billing:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(
            parent,
            bg="#F4F7FB"
        )
        self.selected_id = None
        self.create_ui()
        self.load_bills()

    def create_ui(self):
        tk.Label(
            self.frame,
            text="Billing Management",
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
            text="Generate and manage patient bills",
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
        self.consultation_var = tk.StringVar()
        self.medicine_var = tk.StringVar()
        self.room_var = tk.StringVar()
        self.add_field(
            form,
            "Patient ID",
            self.patient_var,
            0,
            0
        )
        self.add_field(
            form,
            "Consultation",
            self.consultation_var,
            0,
            2
        )
        self.add_field(
            form,
            "Medicine",
            self.medicine_var,
            0,
            4
        )
        self.add_field(
            form,
            "Room",
            self.room_var,
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
            "Generate Bill",
            self.generate_bill,
            "#2563EB"
        )
        self.make_button(
            buttons,
            "Delete Bill",
            self.delete_bill,
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
            columns=BILL_HEADERS,
            show="headings"
        )
        widths = {
            "Bill ID": 90,
            "Patient ID": 100,
            "Patient Name": 160,
            "Consultation": 120,
            "Medicine": 120,
            "Room": 120,
            "Total": 120
        }
        for column in BILL_HEADERS:
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
            self.select_bill
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

    def generate_bill(self):
        patient_id = self.patient_var.get().strip()
        consultation_text = (self.consultation_var.get().strip())
        medicine_text = (self.medicine_var.get().strip())
        room_text = (self.room_var.get().strip())
        patients = read_csv(PATIENT_FILE)
        patient = None
        for record in patients:
            if record["Patient ID"] == patient_id:
                patient = record
                break
        if patient is None:
            messagebox.showwarning(
                "Validation",
                "Patient ID does not exist."
            )
            return
        try:
            consultation = float(
                consultation_text or 0
            )
            medicine = float(
                medicine_text or 0
            )
            room = float(
                room_text or 0
            )
        except ValueError:
            messagebox.showwarning(
                "Validation",
                "Charges must be valid numbers."
            )
            return
        total = consultation + medicine + room
        bill_id = generate_id(
            "B",
            BILL_FILE,
            "Bill ID"
        )
        row = {
            "Bill ID": bill_id,
            "Patient ID": patient_id,
            "Patient Name": patient["Name"],
            "Consultation": f"{consultation:.2f}",
            "Medicine": f"{medicine:.2f}",
            "Room": f"{room:.2f}",
            "Total": f"{total:.2f}"
        }
        append_csv(
            BILL_FILE,
            BILL_HEADERS,
            row
        )
        messagebox.showinfo(
            "Success",
            f"Bill generated successfully.\n"
            f"Bill ID: {bill_id}\n"
            f"Total Amount: ₹{total:.2f}"
        )
        self.clear_form()
        self.load_bills()

    def delete_bill(self):
        if not self.selected_id:
            messagebox.showwarning(
                "Selection",
                "Please select a bill to delete."
            )
            return
        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this bill?"
        )
        if not confirm:
            return
        records = read_csv(BILL_FILE)
        records = [
            record
            for record in records
            if record["Bill ID"] != self.selected_id
        ]
        write_csv(
            BILL_FILE,
            BILL_HEADERS,
            records
        )
        messagebox.showinfo(
            "Success",
            "Bill deleted successfully."
        )
        self.clear_form()
        self.load_bills()

    def clear_form(self):
        self.selected_id = None
        self.patient_var.set("")
        self.consultation_var.set("")
        self.medicine_var.set("")
        self.room_var.set("")
        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def load_bills(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        records = read_csv(BILL_FILE)
        for record in records:
            self.tree.insert(
                "",
                "end",
                values=[
                    record.get(column, "")
                    for column in BILL_HEADERS
                ]
            )

    def select_bill(self, event):
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
        self.consultation_var.set(values[3])
        self.medicine_var.set(values[4])
        self.room_var.set(values[5])