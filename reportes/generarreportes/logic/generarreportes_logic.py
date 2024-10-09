from ..models import Curso, Estudiante, Cronograma, Pago, Reporte


def getPagados(cursoId):
    
    pagados = Pago.objects.filter(cronograma__curso__nombre = cursoId,  pagado = True ).all()
    return pagados

def getPendientes(cursoId):

    pendientes = Pago.objects.filter(cronograma__curso__nombre = cursoId, pagado = False ).all()
    return pendientes

def getCursos():
    return Curso.objects.all()

def crearReporte(nombre, tipo, pagos):
    ruta = '/Downloads'
    reporte = Reporte(nombre, tipo, ruta, pagos)
    return reporte.save()
    