from .logic import generarreportes_logic as gl
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Pago, Cronograma, Curso, Institucion
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors


# Create your views here.

@csrf_exempt
def formulario_view(request):
    #if request.method == 'GET':
    #    id = request.GET.get("id", None)
    #    variables_dto = gl.getCursos()
    #    variables = serializers.serialize('json', variables_dto)
    #    return HttpResponse(variables, 'application/json')
    return render(request, 'consulta.html')


@csrf_exempt
def generarreportes_view(request):
    
    if request.method == 'POST':
        data = request.POST
        cursoid =  Curso.objects.get(id=data['curso_id'])

        pagados = gl.getPagados(cursoid.nombre)
        pendientes = gl.getPendientes(cursoid)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="estado_de_cuenta.pdf"'

        pdf = canvas.Canvas(response, pagesize=A4)
        pdf.setTitle("Reporte de Estado de Cuenta")
        pdf.setFont("Times-Bold", 16)
        pdf.drawString(100, 800, "Reporte de Estado de Cuenta")

        pdf.setFont("Times-Bold", 14)
        pdf.drawString(100, 780, "Pagos Pendientes:")
        pdf.setFont("Times-Roman", 12)

        y = 760 
        totalpendiente = 0 
        for pago in pendientes:
            nombre = pago.nombre
            fecha = pago.fecha
            valor = pago.valor
            tipo = pago.tipo
            estudiante = pago.estudiante.nombre

            pdf.drawString(100, y, f"Nombre: {nombre} Fecha: {fecha} Valor: {valor} Concepto: {tipo}  Estudiante: {estudiante}")
            y -= 20  

            if y < 100:  
                pdf.showPage()
                pdf.setFont("Times_Roman", 12)
                y = 800
            
            totalpendiente += valor
        pdf.setFont("Times-Bold", 12)
        pdf.drawString(100, y, "Total Pendiente: " + str(totalpendiente))
        y -= 20
        pdf.setFont("Times-Bold", 14)
        pdf.drawString(100, y, "Pagos Realizados:")
        y -= 20
        totalpagado = 0
        for pago in pagados:
            nombre = pago.nombre
            fecha = pago.fecha
            valor = pago.valor
            tipo = pago.tipo
            estudiante = pago.estudiante.nombre
            
            pdf.drawString(100, y, f"Nombre: {nombre} Fecha: {fecha} Valor: {valor} Concepto: {tipo} Estudiante: {estudiante}")
            y -= 20  

            if y < 100:  
                pdf.showPage()
                pdf.setFont("Times_Roman", 12)
                y = 800

            totalpagado += valor

        pdf.setFont("Times-Bold", 12)
        pdf.drawString(100, y, "Total Pagado: " + str(totalpagado))
        y -= 20
        pdf.showPage()
        pdf.save()

        return response
