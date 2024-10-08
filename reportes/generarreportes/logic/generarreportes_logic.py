from ..models import Curso, Estudiante, Cronograma, Pago


def getPagados(cronogramaValor):
    
    pagados = Pago.objects.filter(cronograma__nombre = cronogramaValor, pagado = True ).all()
    return pagados

def getPendientes(cronogramaValor):

    pendientes = Pago.objects.filter(cronograma__nombre = cronogramaValor, pagado = False ).all()
    return pendientes

