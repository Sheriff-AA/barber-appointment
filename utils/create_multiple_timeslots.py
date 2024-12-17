from datetime import timedelta, datetime, time
from django.utils.timezone import now, make_aware

from appointments.models import TimeSlot


def create_timeslots(start_date, days_to_create, duration, opening_hour, closing_hour, barber_user):
    """
    Creates multiple timeslots from the start_date
    """

    # Define slot time range using datetime objects
    time_start = datetime.combine(start_date, datetime.min.time()).replace(hour=opening_hour.hour, minute=opening_hour.minute)  # 9:00 AM
    time_end = datetime.combine(start_date, datetime.min.time()).replace(hour=closing_hour.hour, minute=closing_hour.minute)   # 4:00 PM
    slot_duration = timedelta(minutes=duration)  # Duration of each slot (60 minutes)

    for day in range(days_to_create):
        current_date = start_date + timedelta(days=day)  # Get the current day
        current_time = time_start.replace(year=current_date.year, month=current_date.month, day=current_date.day)

        current_time = make_aware(current_time)
        time_end_day = make_aware(time_end.replace(year=current_date.year, month=current_date.month, day=current_date.day))

        # Generate time slots from 9:00 AM to 4:00 PM for each day
        while current_time < time_end_day.replace(year=current_date.year, month=current_date.month, day=current_date.day):
            end_time = current_time + slot_duration  # Calculate end time by adding slot duration
            
            if end_time <= time_end_day.replace(year=current_date.year, month=current_date.month, day=current_date.day):
                TimeSlot.objects.get_or_create(
                    date=current_date,
                    start_time=current_time,  # Store full datetime for start
                    end_time=end_time,  # Store full datetime for end
                    is_reserved = False,
                    barber = barber_user
                )

            # Increment current time by slot duration (60 minutes)
            current_time += slot_duration