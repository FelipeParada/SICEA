from django.db import models


class Meter(models.Model):
    TYPE_CHOICES = (
        ('ELECTRICITY', 'Electricity'),
        ('WATER', 'Water'),
    )
    meter_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    name = models.CharField(max_length=100, blank=True, default='')
    client_number = models.CharField(max_length=50)
    macrozona = models.CharField(max_length=200, blank=True, default='')
    instalacion = models.CharField(max_length=200, blank=True, default='')
    direccion = models.CharField(max_length=250, blank=True, default='')
    
    # Campo deprecado pero mantenido para compatibilidad
    coverage = models.CharField(max_length=250, blank=True, default='')

    def __str__(self):
        return f"{self.name or self.instalacion or 'Sin nombre'} ({self.client_number})"


class Bill(models.Model):
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE, related_name='bills')
    month = models.IntegerField()
    year = models.IntegerField()
    total_to_pay = models.DecimalField(max_digits=10, decimal_places=2)
    pdf_filename = models.CharField(max_length=255, null=True, blank=True, default=None)
    tarifa = models.CharField(max_length=100, blank=True, default='')  # Para facturas de electricidad
    invoice_number = models.CharField(max_length=50, blank=True, default='')  # Número de factura del PDF

    class Meta:
        unique_together = (('meter', 'month', 'year'),)

    def __str__(self):
        return f"Bill {self.month}/{self.year} - Meter {self.meter.name}"


class Charge(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='charges')
    name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    value_type = models.CharField(max_length=50)
    charge = models.IntegerField()

    def __str__(self):
        return f"{self.name} - Bill {self.bill.id}"