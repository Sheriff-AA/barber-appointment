from profiles.models import ProfileType

barber_profiletype = ProfileType.objects.get(name="Barber Profile Type")

customer_profiletype = ProfileType.objects.get(name="Customer Profile Type")