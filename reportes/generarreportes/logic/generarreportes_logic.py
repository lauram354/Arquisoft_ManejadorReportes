from ..models import Curso, Estudiante, Cronograma, Pago


def getPagados(cursoId):
    
    pagados = Pago.objects.filter(cronograma__curso__nombre = cursoId,  pagado = True ).all()
    return pagados

def getPendientes(cursoId):

    pendientes = Pago.objects.filter(cronograma__curso__nombre = cursoId, pagado = False ).all()
    return pendientes

def getCursos():
    return Curso.objects.all()