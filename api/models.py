from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from simple_history.models import HistoricalRecords

# Create your models here.

class User(AbstractUser):
    code = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    dui = models.CharField(max_length=20, unique=True)
    short_name = models.CharField(max_length=50)
    position = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    password = models.TextField()
    phone = models.TextField(max_length=150, null=True, blank=True, default=None)
    extra_emails = models.TextField(max_length=200, null=True, blank=True, default=None)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

class Entity(models.Model):
    CAMPANIA = 1
    PROYECTO = 2

    TYPE_CHOICES = [
        (CAMPANIA, "Campaña"),
        (PROYECTO, "Proyecto"),
    ]

    name = models.CharField(max_length=250)
    extra_information = models.TextField(null=True, blank=True)
    type = models.IntegerField(choices=TYPE_CHOICES, default=CAMPANIA)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["type"]),
            models.Index(fields=["parent"]),
        ]

    def clean(self):
        if self.type == self.CAMPANIA and self.parent_id is not None:
            raise ValidationError("Una campaña no puede tener parent")

        if self.type == self.PROYECTO:
            if not self.parent_id:
                raise ValidationError("Un proyecto debe depender de una campaña")

            if not Entity.objects.filter(id=self.parent_id, type=self.CAMPANIA).exists():
                raise ValidationError("El parent debe ser una campaña")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Activity(models.Model):
    name = models.CharField(max_length=150)

    # null = global | no null = específica de proyecto
    project = models.ForeignKey(
        Entity,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        limit_choices_to={"type": Entity.PROYECTO},
        related_name="activities"
    )

    class Meta:
        unique_together = ("name", "project")

    def __str__(self):
        return self.name


# class Registro(models.Model):
#     # ENUM EQUIPOS
#     EQ_A = 1
#     EQ_B = 2
#     EQ_C = 3

#     EQ_CHOICES = [
#         (EQ_A, "Molino SAG"),
#         (EQ_B, "Molino de Bolas N°1"),
#         (EQ_C, "Molino de Bolas N°2"),
#     ]

#     proyecto = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="registros")
#     equipo = models.IntegerField(choices=EQ_CHOICES)
#     actividad = models.ForeignKey(Activity, on_delete=models.CASCADE)
#     fecha = models.DateField(auto_now_add=True)

#     class Meta:
#         unique_together = ("proyecto", "equipo", "actividad", "fecha")

#     def clean(self):
#         if self.proyecto.type != Entity.PROYECTO:
#             raise ValidationError("El proyecto debe ser tipo PROYECTO")

#         # actividad global o del mismo proyecto
#         if self.actividad.project and self.actividad.project_id != self.proyecto_id:
#             raise ValidationError("La actividad no pertenece a este proyecto")

#     def save(self, *args, **kwargs):
#         self.full_clean()
#         super().save(*args, **kwargs)

class Equipment(models.Model):
    name = models.CharField(max_length=150)
    extra_info = models.CharField(max_length=255, null=True, blank=True)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Ubication(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    
class EquipmentFiles(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='images')
    file = models.FileField(upload_to='equipment_images/')
    type = models.ForeignKey(Ubication, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class RegisterHead(models.Model):

    proyecto = models.ForeignKey(Entity, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipment, on_delete=models.CASCADE)

    name = models.CharField(max_length=500, null=True, blank=True)
    initial_date = models.DateTimeField()
    final_date = models.DateTimeField(null=True, blank=True)
    extra_information = models.TextField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




class Job(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class RegisterFiles(models.Model):
    register = models.ForeignKey(RegisterHead, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='register_files/')
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)


    


class RegisterDetail(models.Model):
    register_head = models.ForeignKey(RegisterHead, null=True, blank=True, on_delete=models.CASCADE, related_name="details")
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    ubication = models.ForeignKey(Ubication, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    shape_information = models.TextField(null=True)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

class PistolaTorque(models.Model):
    equipo = models.ForeignKey(Entity, on_delete=models.CASCADE)
    ubicacion = models.ForeignKey(Ubication, on_delete=models.CASCADE)
    company_in_charge = models.CharField(max_length=250)
    manufacturer = models.CharField(max_length=250)
    model = models.CharField(max_length=100)
    calibration_cert = models.CharField(max_length=100)
    calibration_number = models.CharField(max_length=100)
    tension_by_manufacturer = models.CharField(max_length=100)
    torque_by_manufacturer = models.CharField(max_length=100)
    giro_number = models.CharField(max_length=50)
    torque_in_field = models.CharField(max_length=150)
    tension_by_test_bench = models.CharField(max_length=150)
    calibration_date = models.DateField()
    calibration_time = models.TimeField()
    serial_number = models.CharField(max_length=50)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    
    
class PernosVerif(models.Model):
    equipo = models.ForeignKey(Entity, on_delete=models.CASCADE)
    ubicacion = models.ForeignKey(Ubication, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    color = models.CharField(max_length=150)
    total_campo = models.IntegerField()
    no_cumple_dimens = models.IntegerField()
    presenta_oxido = models.IntegerField()
    hilo_daniado = models.IntegerField()
    tuerca_daniada = models.IntegerField()
    pernos_operativ_total = models.IntegerField()
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()