from io import BytesIO
from django.http import HttpResponse
from openpyxl import Workbook
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from reader.models import Meter, Bill


class ExportExcelView(APIView):
    """
    Exporta datos de facturas y cargos en un Excel con:
      - una hoja 'Resumen' con todos los medidores
      - una hoja por cada medidor
    """

    def get(self, request):
        meter_type = request.query_params.get('meter_type')  # 'WATER' o 'ELECTRICITY'
        start_date = request.query_params.get('start_date')  # formato: YYYY-MM
        end_date = request.query_params.get('end_date')      # formato: YYYY-MM

        if not meter_type or not start_date or not end_date:
            return Response(
                {"detail": "Debe indicar 'meter_type', 'start_date' y 'end_date'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar tipo de medidor
        if meter_type not in dict(Meter.TYPE_CHOICES):
            return Response(
                {"detail": "Tipo de medidor inválido. Use 'WATER' o 'ELECTRICITY'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Parseo de fechas: se trabaja con año y mes
        try:
            start_year, start_month = map(int, start_date.split('-'))
            end_year, end_month = map(int, end_date.split('-'))
        except ValueError:
            return Response(
                {"detail": "Formato inválido de fechas. Use YYYY-MM."},
                status=status.HTTP_400_BAD_REQUEST
            )

        start_period = start_year * 12 + start_month
        end_period = end_year * 12 + end_month

        # Filtrar medidores y facturas
        meters = Meter.objects.filter(meter_type=meter_type)
        bills = Bill.objects.filter(meter__in=meters)

        # Filtrar por rango de fechas
        bills = [b for b in bills if start_period <= (b.year * 12 + b.month) <= end_period]

        # Crear workbook
        output = BytesIO()
        workbook = Workbook()

        # ---------------------------
        #  HOJA 1: RESUMEN GENERAL
        # ---------------------------
        summary_sheet = workbook.active
        summary_sheet.title = "Resumen"

        headers = [
            "Nombre del Medidor",  # Meter Name
            "Número de Cliente",  # Client Number
            "Tipo de Medidor",  # Meter Type
            "Área de Cobertura",  # Coverage
            "Mes de Factura",  # Bill Month
            "Año de Factura",  # Bill Year
            "Total a Pagar",  # Total to Pay
            "Nombre del Cargo",  # Charge Name
            "Valor del Cargo",  # Charge Value
            "Tipo de Valor",  # Value Type
            "Costo del Cargo"  # Charge Number
        ]
        summary_sheet.append(headers)

        for bill in bills:
            for charge in bill.charges.all():
                summary_sheet.append([
                    bill.meter.name,
                    bill.meter.client_number,
                    bill.meter.get_meter_type_display(),
                    bill.meter.coverage,
                    bill.month,
                    bill.year,
                    bill.total_to_pay,
                    charge.name,
                    charge.value,
                    charge.value_type,
                    charge.charge
                ])

        # --------------------------------
        #  HOJAS INDIVIDUALES POR MEDIDOR
        # --------------------------------
        for meter in meters:
            meter_bills = [b for b in bills if b.meter_id == meter.id]
            if not meter_bills:
                continue

            sheet_name = meter.name[:25]  # limitar nombre de hoja (Excel máx. 31 chars)
            sheet = workbook.create_sheet(title=sheet_name)

            sheet.append(headers)

            for bill in meter_bills:
                for charge in bill.charges.all():
                    sheet.append([
                        meter.name,
                        meter.client_number,
                        meter.get_meter_type_display(),
                        meter.coverage,
                        bill.month,
                        bill.year,
                        bill.total_to_pay,
                        bill.pdf_filename or '',
                        charge.name,
                        charge.value,
                        charge.value_type,
                        charge.charge
                    ])

        # Guardar y enviar el archivo
        workbook.save(output)
        output.seek(0)
        if meter_type == "ELECTRICITY":
            filename = f"Facturas_Enel_{start_date}_a_{end_date}.xlsx"
        if meter_type == "WATER":
            filename = f"Facturas_AguasAndinas_{start_date}_a_{end_date}.xlsx"
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
