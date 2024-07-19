# api/management/commands/seed.py

from django.core.management.base import BaseCommand
from api.models import User, Asset, Request
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # Create users
        superadmin = User.objects.create_superuser(
            email='superadmin@example.com',
            first_name='Super',
            last_name='Admin',
            phone_number='1234567890',
            department='Management',
            role='superadmin',
            password='password123'
        )

        admin1 = User.objects.create_user(
            email='admin1@example.com',
            first_name='Admin',
            last_name='One',
            phone_number='1234567891',
            department='IT',
            role='admin',
            password='password123'
        )

        admin2 = User.objects.create_user(
            email='admin2@example.com',
            first_name='Admin',
            last_name='Two',
            phone_number='1234567892',
            department='HR',
            role='admin',
            password='password123'
        )

        employee1 = User.objects.create_user(
            email='employee1@example.com',
            first_name='Employee',
            last_name='One',
            phone_number='1234567893',
            department='Finance',
            role='employee',
            password='password123'
        )

        employee2 = User.objects.create_user(
            email='employee2@example.com',
            first_name='Employee',
            last_name='Two',
            phone_number='1234567894',
            department='Sales',
            role='employee',
            password='password123'
        )

        employee3 = User.objects.create_user(
            email='employee3@example.com',
            first_name='Employee',
            last_name='Three',
            phone_number='1234567895',
            department='Support',
            role='employee',
            password='password123'
        )

        employee4 = User.objects.create_user(
            email='employee4@example.com',
            first_name='Employee',
            last_name='Four',
            phone_number='1234567896',
            department='Development',
            role='employee',
            password='password123'
        )

        # Create assets
        asset1 = Asset.objects.create(
            name='Laptop',
            description='A powerful laptop',
            category='Electronics',
            serial_number='SN123456',
            tag='IT',
            status=True,
            asset_type='Device'
        )

        asset2 = Asset.objects.create(
            name='Projector',
            description='A high-resolution projector',
            category='Electronics',
            serial_number='SN123457',
            tag='AV',
            status=True,
            asset_type='Device'
        )

        asset3 = Asset.objects.create(
            name='Desk Chair',
            description='An ergonomic desk chair',
            category='Furniture',
            serial_number='SN123458',
            tag='Office',
            status=True,
            asset_type='Furniture'
        )

        # Create requests
        Request.objects.create(
            asset=asset1,
            employee=employee1,
            status='pending'
        )

        Request.objects.create(
            asset=asset2,
            employee=employee2,
            status='pending'
        )

        Request.objects.create(
            asset=asset3,
            employee=employee3,
            status='pending'
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database'))
