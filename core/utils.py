from datetime import datetime

def validate_phone(phone):
    return phone.isdigit() and len(phone) == 10
def validate_age(age):
    return age.isdigit() and int(age) > 0
def validate_date(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False