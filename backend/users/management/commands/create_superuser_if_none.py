from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'Crea un superusuario si no existe ninguno (requiere variables de entorno)'

    def handle(self, *args, **options):
        # Obtener credenciales SOLO de variables de entorno
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        
        if not email or not password:
            self.stdout.write(self.style.WARNING(
                'No se creó superusuario: falta DJANGO_SUPERUSER_EMAIL o DJANGO_SUPERUSER_PASSWORD'
            ))
            return
        
        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f'El usuario {email} ya existe'))
            return
        
        user = User.objects.create_superuser(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        
        self.stdout.write(self.style.SUCCESS(f'Superusuario creado: {email}'))
