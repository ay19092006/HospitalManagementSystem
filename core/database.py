import csv
import os
from tkinter import messagebox

def create_data_folder():
    try:
        os.makedirs(
            os.path.dirname(
                os.path.abspath(__file__)
            ).replace(
                os.path.join("core", ""),
                ""
            ),
            exist_ok=True
        )
    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Unable to create data folder:\n{e}"
        )

def initialize_file(filename, headers):
    try:
        folder = os.path.dirname(filename)
        if folder:
            os.makedirs(folder, exist_ok=True)
        if not os.path.exists(filename):
            with open(
                filename,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:
                writer = csv.writer(file)
                writer.writerow(headers)
    except Exception as e:
        messagebox.showerror(
            "File Error",
            str(e)
        )

def read_csv(filename):
    try:
        with open(
            filename,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []
    except Exception as e:
        messagebox.showerror(
            "File Error",
            str(e)
        )
        return []

def write_csv(filename, fieldnames, data):
    try:
        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        messagebox.showerror(
            "File Error",
            str(e)
        )

def append_csv(filename, fieldnames, row):
    try:
        file_exists = os.path.exists(filename)
        with open(
            filename,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )
            if (
                not file_exists
                or os.path.getsize(filename) == 0
            ):
                writer.writeheader()

            writer.writerow(row)
    except Exception as e:
        messagebox.showerror(
            "File Error",
            str(e)
        )

def generate_id(prefix, filename, id_field):
    records = read_csv(filename)
    numbers = []
    for record in records:
        value = record.get(id_field, "")
        try:
            if value.startswith(prefix):
                numbers.append(
                    int(value[len(prefix):])
                )
        except ValueError:
            pass
    next_number = max(numbers, default=0) + 1
    return f"{prefix}{next_number:03d}"