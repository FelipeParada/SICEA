from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'Crea un superusuario si no existe ninguno'

    def handle(self, *args, **options):
        # Obtener credenciales de variables de entorno
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@sicea.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
        
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS('Ya existe al menos un superusuario'))
            return
        
        User.objects.create_superuser(email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'Superusuario creado: {email}'))
