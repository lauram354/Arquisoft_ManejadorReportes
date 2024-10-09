from ..models import Curso, Estudiante, Cronograma, Pago, Reporte


def getPagados(cursoId):
    
    pagados = Pago.objects.filter(cronograma__curso__nombre = cursoId,  pagado = True ).all()
    return pagados

def getPendientes(cursoId):

    pendientes = Pago.objects.filter(cronograma__curso__nombre = cursoId, pagado = False ).all()
    return pendientes

def getCursos():
    return Curso.objects.all()

def crearReporte(nombre, tipo, fechaCreacion, ruta, pagos):
    reporte = Reporte(nombre, tipo, fechaCreacion, ruta)
    reporte.pago.add(pagos)
    return reporte.save()
    