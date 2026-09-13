import tkinter as tk
from tkinter import messagebox
from core.config import PATIENT_FILE
from core.database import read_csv

class Statistics:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(
            parent,
            bg="#F4F7FB"
        )
        self.create_ui()

    def create_ui(self):
        tk.Label(
            self.frame,
            text="Statistics",
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
            text="View patient statistics",
            font=("Arial", 11),
            bg="#F4F7FB",
            fg="#6B7280"
        ).pack(
            anchor="w",
            padx=30,
            pady=(0, 30)
        )
        card = tk.Frame(
            self.frame,
            bg="white",
            highlightbackground="#E5E7EB",
            highlightthickness=1
        )
        card.pack(
            padx=30,
            fill="x"
        )
        tk.Label(
            card,
            text="Patient Gender Statistics",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#1F2937"
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 10)
        )
        tk.Label(
            card,
            text=(
                "View a graphical representation of "
                "patients by gender."
            ),
            font=("Arial", 10),
            bg="white",
            fg="#6B7280"
        ).pack(anchor="w", padx=25)
        tk.Button(
            card,
            text="Show Gender Statistics",
            command=self.show_gender_statistics,
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2"
        ).pack(
            anchor="w",
            padx=25,
            pady=25
        )

    def show_gender_statistics(self):
        records = read_csv(PATIENT_FILE)
        if not records:
            messagebox.showinfo(
                "Statistics",
                "No patient data available."
            )
            return
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            messagebox.showerror(
                "Matplotlib Not Available",
                "Matplotlib is not installed.\n\n"
                "Please run:\n"
                "pip install matplotlib"
            )
            return
        gender_count = {}
        for record in records:
            gender = record.get(
                "Gender",
                "Unknown"
            )
            if not gender:
                gender = "Unknown"
            gender_count[gender] = (gender_count.get(gender, 0) + 1)
        genders = list(gender_count.keys())
        counts = list(gender_count.values())
        plt.figure(figsize=(8, 5))
        plt.bar(genders, counts)
        plt.title("Patients by Gender")
        plt.xlabel("Gender")
        plt.ylabel("Number of Patients")
        plt.tight_layout()
        plt.show()