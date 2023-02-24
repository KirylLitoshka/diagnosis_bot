from datetime import date, timedelta


def get_date_range(days_number=14):
    current_date = date.today()
    date_range = []
    for day_number in range(days_number):
        delta_date = current_date + timedelta(days=day_number)
        date_range.append(delta_date.strftime("%d.%m"))
    return date_range


def get_time_range(start=8, end=22):
    time_range = []
    for num in range(start, end):
        time_range.append(f"{num:02d}:00 - {num+1:02d}:00")
    return time_range
