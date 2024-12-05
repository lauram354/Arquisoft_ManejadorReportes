from .logic import generarreportes_logic as gl
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Pago, Cronograma, Curso, Institucion, Estudiante, Responsablef
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import requests
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
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
        auth_url = 'http://34.42.191.236:8080/usuarios/api/token/'
        payload = {
            'username': data['usuario'],
            'password': data['contrasenia'],
        }
        response = requests.post(auth_url, data=payload)
        if response.status_code == 200:
            response_data = response.json() 
            print(response_data)
            token_str = response_data['access']
            try:
                token = AccessToken(token_str)
                institu = token['last_name']

                institucion = Institucion.objects.get(id=data['institucionid'])
                print(institucion)
                print(institu)
                if institucion.nombre == institu:
                    cursoid =  Curso.objects.get(id=data['curso_id'])
                    nombre = "Reporte de Estado de Cuenta " + cursoid.nombre 
                    tipo = "Estado de Cuenta"
                    
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
                    pdf.setFont("Times-Roman", 10)

                    y = 760 
                    totalpendiente = 0 
                    pagos = []
                    for pago in pendientes:
                        pagos.append(pago.id)
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
                    pdf.setFont("Times-Roman", 10)
                    for pago in pagados:
                        pagos.append(pago.id)
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
                else:
                    return HttpResponse("Usuario no autorizado", status=400)
            except TokenError as e:
                print(f"Error al decodificar el token: {e}")
                return HttpResponse("Error al decodificar el token", status=400)
        else:
            return HttpResponse("Error obteniendo los datos", status=400)
    

@csrf_exempt
def generarReportePago(request):
    if request.method == 'POST':
        estudiante_id = request.POST.get('estudiante_id', None)
        responsable_id = request.POST.get('responsable_id', None)

        # Filtrar pagos según el criterio proporcionado
        if estudiante_id:
            estudiante = Estudiante.objects.get(id=estudiante_id)
            pagos = Pago.objects.filter(estudiante=estudiante)
            titulo = f"Reporte de Pagos del Estudiante {estudiante.nombre}"
        elif responsable_id:
            responsable = Responsablef.objects.get(id=responsable_id)
            pagos = Pago.objects.filter(responsableF=responsable)
            titulo = f"Reporte de Pagos del Responsable Financiero {responsable.nombre}"
        else:
            return HttpResponse("Debes proporcionar un ID de estudiante o de responsable financiero.", status=400)

        # Generar PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{titulo}.pdf"'

        pdf = canvas.Canvas(response, pagesize=A4)
        pdf.setTitle(titulo)
        pdf.setFont("Times-Bold", 16)
        pdf.drawString(100, 800, titulo)

        y = 760
        total = 0

        pdf.setFont("Times-Bold", 14)
        pdf.drawString(100, y, "Pagos Realizados:")
        y -= 20

        pdf.setFont("Times-Roman", 12)
        for pago in pagos:
            pdf.drawString(100, y, f"Nombre: {pago.nombre}, Fecha: {pago.fecha}, Valor: {pago.valor}, Concepto: {pago.tipo}")
            y -= 20
            total += pago.valor

            if y < 100:  # Saltar de página si no hay espacio
                pdf.showPage()
                pdf.setFont("Times-Roman", 12)
                y = 800

        pdf.setFont("Times-Bold", 14)
        pdf.drawString(100, y, f"Total Pagado: {total}")
        pdf.save()

        return response

    return render(request, 'generar_reporte_pago.html')
