from django.core.management.base import BaseCommand
from django.utils.timezone import now, make_aware
from datetime import timedelta, datetime, time
from appointments.models import TimeSlot


# class Command(BaseCommand):
#     help = 'Create time slots for a range of days'

#     def handle(self, *args, **kwargs):
#         start_date = now().date()
#         days_to_create = 7  # You can adjust this range as necessary
#         time_start = datetime(9, 0)  # Start time of the slots (9:00 AM)
#         time_end = time(16, 0)  # End time of the slots (4:00 PM)
#         slot_duration = timedelta(minutes=60)  # 60-minute slots

#         for day in range(days_to_create):
#             current_date = start_date + timedelta(days=day)
#             current_time = datetime.combine(current_date, time_start)

#             while current_time.time() < time_end:
#                 end_time = (current_time + slot_duration).time()
#                 if end_time <= time_end:
#                     TimeSlot.objects.get_or_create(
#                         date=current_date,
#                         start_time=current_time.time(),
#                         end_time=end_time
#                     )
#                 current_time += slot_duration

#         self.stdout.write(self.style.SUCCESS('Successfully created time slots!'))

class Command(BaseCommand):
    help = 'Create time slots for a range of days'

    def handle(self, *args, **kwargs):
        start_date = now().date()  # Get today's date
        days_to_create = 7  # Number of days to create slots for

        # Define slot time range using datetime objects
        time_start = datetime.combine(start_date, datetime.min.time()).replace(hour=9, minute=0)  # 9:00 AM
        time_end = datetime.combine(start_date, datetime.min.time()).replace(hour=16, minute=0)   # 4:00 PM
        slot_duration = timedelta(minutes=60)  # Duration of each slot (60 minutes)

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
                        end_time=end_time  # Store full datetime for end
                    )

                # Increment current time by slot duration (60 minutes)
                current_time += slot_duration

        self.stdout.write(self.style.SUCCESS('Successfully created time slots!'))