import tkinter as tk
from core.config import (
    PATIENT_FILE,
    DOCTOR_FILE,
    APPOINTMENT_FILE,
    BILL_FILE
)
from core.database import read_csv

class Dashboard:
    def __init__(self, parent, show_page):
        self.parent = parent
        self.show_page = show_page
        self.frame = tk.Frame(
            parent,
            bg="#F4F7FB"
        )
        self.create_ui()

    def create_ui(self):
        title = tk.Label(
            self.frame,
            text="Dashboard",
            font=("Arial", 24, "bold"),
            bg="#F4F7FB",
            fg="#1F2937"
        )
        title.pack(
            anchor="w",
            padx=30,
            pady=(25, 5)
        )
        subtitle = tk.Label(
            self.frame,
            text="Overview of hospital administration",
            font=("Arial", 11),
            bg="#F4F7FB",
            fg="#6B7280"
        )
        subtitle.pack(
            anchor="w",
            padx=30,
            pady=(0, 20)
        )
        cards_frame = tk.Frame(
            self.frame,
            bg="#F4F7FB"
        )
        cards_frame.pack(
            fill="x",
            padx=30
        )
        self.patient_card = self.create_card(
            cards_frame,
            "Total Patients",
            "#2563EB"
        )
        self.doctor_card = self.create_card(
            cards_frame,
            "Total Doctors",
            "#059669"
        )
        self.appointment_card = self.create_card(
            cards_frame,
            "Appointments",
            "#D97706"
        )
        self.bill_card = self.create_card(
            cards_frame,
            "Total Bills",
            "#7C3AED"
        )
        self.update_cards()
        quick_frame = tk.Frame(
            self.frame,
            bg="#F4F7FB"
        )
        quick_frame.pack(
            fill="x",
            padx=30,
            pady=35
        )
        tk.Label(
            quick_frame,
            text="Quick Actions",
            font=("Arial", 16, "bold"),
            bg="#F4F7FB",
            fg="#1F2937"
        ).pack(anchor="w", pady=(0, 15))
        buttons_frame = tk.Frame(
            quick_frame,
            bg="#F4F7FB"
        )
        buttons_frame.pack(anchor="w")
        tk.Button(
            buttons_frame,
            text="Add Patient",
            command=lambda: self.show_page("Patients"),
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2"
        ).pack(side="left", padx=(0, 10))
        tk.Button(
            buttons_frame,
            text="Add Doctor",
            command=lambda: self.show_page("Doctors"),
            bg="#059669",
            fg="white",
            activebackground="#047857",
            activeforeground="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2"
        ).pack(side="left", padx=10)
        tk.Button(
            buttons_frame,
            text="Appointment",
            command=lambda: self.show_page("Appointments"),
            bg="#D97706",
            fg="white",
            activebackground="#B45309",
            activeforeground="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2"
        ).pack(side="left", padx=10)
        tk.Button(
            buttons_frame,
            text="Billing",
            command=lambda: self.show_page("Billing"),
            bg="#7C3AED",
            fg="white",
            activebackground="#6D28D9",
            activeforeground="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2"
        ).pack(side="left", padx=10)

    def create_card(self, parent, title, color):
        card = tk.Frame(
            parent,
            bg="white",
            highlightbackground="#E5E7EB",
            highlightthickness=1
        )
        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=8
        )
        tk.Frame(
            card,
            bg=color,
            width=6
        ).pack(side="left", fill="y")
        content = tk.Frame(
            card,
            bg="white"
        )
        content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=18
        )
        tk.Label(
            content,
            text=title,
            font=("Arial", 11),
            bg="white",
            fg="#6B7280"
        ).pack(anchor="w")
        value_label = tk.Label(
            content,
            text="0",
            font=("Arial", 26, "bold"),
            bg="white",
            fg="#111827"
        )
        value_label.pack(
            anchor="w",
            pady=(5, 0)
        )
        return value_label

    def update_cards(self):
        patients = read_csv(PATIENT_FILE)
        doctors = read_csv(DOCTOR_FILE)
        appointments = read_csv(APPOINTMENT_FILE)
        bills = read_csv(BILL_FILE)
        self.patient_card.config(text=str(len(patients)))
        self.doctor_card.config(text=str(len(doctors)))
        self.appointment_card.config(text=str(len(appointments)))
        self.bill_card.config(text=str(len(bills)))