from django.db import models

# Create your models here.
class Institucion(models.Model):
    nombre = models.CharField(max_length=50)
    logo = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    def __str__(self):
        return '{}'.format(self.nombre)
    
class Estudiante(models.Model):
    codigo = models.IntegerField(default=1)
    nombre = models.CharField(max_length=50)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE )

    def __str__(self):
        return '{}'.format(self.nombre)
    
class Usuario(models.Model):
    usuario = models.CharField(max_length=50)
    correo = models.CharField(max_length=255)
    nombre = models.CharField(max_length=50)
    contrasenia = models.CharField(max_length=255)
    rol = models.CharField(max_length=50)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE )

    def __str__(self):
        return '{}'.format(self.nombre)

class Curso(models.Model):
    nombre = models.CharField(max_length=50)
    estudiantes = models.ManyToManyField(Estudiante)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    

    def __str__(self):
        return '{}'.format(self.nombre)

class Responsablef(Usuario):
    estudiantes = models.ManyToManyField(Estudiante)
    def __str__(self):
        return '{}'.format(self.nombre)

class Cronograma(models.Model):
    anio = models.IntegerField(default=2024)
    nombre = models.CharField(max_length= 100)
    curso = models.OneToOneField(Curso, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.nombre)

class Descuento(models.Model):
    nombre = models.CharField(max_length= 50)
    porcentaje = models.FloatField(default=0)
    fechaInicio = models.DateField(default='2024-01-01')
    fechaFinal = models.DateField(default='2024-01-01')
    fechaCreacion = models.DateField(auto_now = True)

    def __str__(self):
        return '{}'.format(self.nombre)
         
class Pago(models.Model):
    nombre = models.CharField(max_length=50)
    fecha = models.DateField(default='2024-01-01')
    valor = models.FloatField(default=0)
    interes = models.FloatField(default=0)
    pagado = models.BooleanField(default=False)
    tipo = models.CharField(max_length=50)
    periodicidad = models.IntegerField(default=0)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    responsableF = models.ForeignKey(Responsablef, on_delete=models.CASCADE)
    cronograma = models.ForeignKey(Cronograma, on_delete=models.CASCADE)
    descuento = models.ForeignKey(Descuento, on_delete=models.SET_NULL, null = True)

    def __str__(self):
        return '{}'.format(self.nombre)

class Banco(models.Model):
    nombre = models.CharField(max_length= 100)
    formato = models.CharField(max_length= 255)
    pago = models.OneToOneField(Pago, on_delete=models.CASCADE)
    
    def __str__(self):
        return '{}'.format(self.nombre)

    
class Recibo(models.Model):
    PAGO = 1
    COBRO = 2
    TIPORECIBO = [ (PAGO, 'pago'), (COBRO, 'cobro') ]

    nombre = models.CharField(max_length= 50)
    fecha = models.DateField(default='2024-01-01')
    valor = models.FloatField(default=0)
    medioPago = models.CharField(max_length= 50)
    tipo = models.IntegerField(choices=TIPORECIBO, default=PAGO)
    pago = models.OneToOneField(Pago, on_delete=models.CASCADE)
    
    def __str__(self):
        return '{}'.format(self.nombre)

class Reporte(models.Model):
    nombre = models.CharField(max_length= 50)
    tipo = models.CharField(max_length= 50)
    fechaCreacion = models.DateField(auto_now = True)
    ruta = models.CharField(max_length= 255)
    pago = models.ManyToManyField(Pago)
    def __str__(self):
        return '{}'.format(self.nombre)
    
