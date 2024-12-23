import datetime

def formatted_date(date):
    if isinstance(date, datetime.date):
        return date.strftime('%B') + " " + ordinal(date.day) + ", " + date.strftime('%Y')
    return date

def ordinal(day):
    if 11 <= day <= 13:  # Special case for teens
        return f"{day}th"
    suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    return f"{day}{suffix}"
