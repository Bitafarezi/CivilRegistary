import random
from django.core.management.base import BaseCommand
from registary.models import Citizen
from tqdm import tqdm
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Seed 100,000 sample records'

    def handle(self, *args, **kwargs):
        first_names = ['Ali', 'Reza', 'Mohammad', 'Hassan', 'Hossein', 'Fatemeh', 'Zahra', 'Maryam', 'Sara', 'Narges', 'Omid', 'Saeed', 'Babak', 'Nader']
        last_names = ['Ahmadi', 'Rezaei', 'Mohammadi', 'Hassani', 'Hosseini', 'Karimi', 'Mousavi', 'Ghasemi', 'Salehi', 'Moradi', 'Zarei', 'Rahimi']
        father_names = ['Akbar', 'Asghar', 'Mahmoud', 'Ebrahim', 'Ghasem', 'Rahim', 'Karim', 'Javad', 'Hamid', 'Majid']

        batch_size = 5000
        total_records = 100000
        
        self.stdout.write(f'Generating {total_records} records...')
        
        # Clear existing data to avoid unique constraint errors if re-run
        # Citizen.objects.all().delete()
        
        for i in tqdm(range(0, total_records, batch_size)):
            citizens = []
            for j in range(batch_size):
                idx = i + j
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                # National ID should be unique, using index to ensure uniqueness
                national_id = str(idx).zfill(10)
                # Phone number format: +989121111111
                phone_number = f"+98912{str(idx).zfill(7)}"
                father_name = random.choice(father_names)
                birth_date = date(1960, 1, 1) + timedelta(days=random.randint(0, 20000))
                address = f"Tehran, District {random.randint(1, 22)}, Street {random.randint(1, 100)}, No {random.randint(1, 200)}"
                
                citizens.append(Citizen(
                    first_name=first_name,
                    last_name=last_name,
                    national_id=national_id,
                    phone_number=phone_number,
                    father_name=father_name,
                    birth_date=birth_date,
                    address=address
                ))
            Citizen.objects.bulk_create(citizens)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {total_records} records'))
