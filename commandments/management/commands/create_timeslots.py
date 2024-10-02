from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import timedelta, datetime, time
from appointments.models import TimeSlot


class Command(BaseCommand):
    help = 'Create time slots for a range of days'

    def handle(self, *args, **kwargs):
        start_date = now().date()
        days_to_create = 7  # You can adjust this range as necessary
        time_start = time(9, 0)  # Start time of the slots (9:00 AM)
        time_end = time(16, 0)  # End time of the slots (4:00 PM)
        slot_duration = timedelta(minutes=60)  # 60-minute slots

        for day in range(days_to_create):
            current_date = start_date + timedelta(days=day)
            current_time = datetime.combine(current_date, time_start)

            while current_time.time() < time_end:
                end_time = (current_time + slot_duration).time()
                if end_time <= time_end:
                    TimeSlot.objects.get_or_create(
                        date=current_date,
                        start_time=current_time.time(),
                        end_time=end_time
                    )
                current_time += slot_duration

        self.stdout.write(self.style.SUCCESS('Successfully created time slots!'))
