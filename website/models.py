from django.db import models
from django.utils.text import slugify

# Create your models here.

class Role(models.Model):
    R_RoleName = models.CharField(max_length=20)

    def __str__(self):
        return self.R_RoleName


class Employee(models.Model):
    E_Password = models.CharField(max_length=30)
    E_Name = models.CharField(max_length=30)
    E_Phone = models.CharField(max_length=30)
    E_Email = models.CharField(max_length=30)
    E_RoleName = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.E_Name} ({self.E_RoleName})"


class Patient(models.Model):
    P_NRIC = models.CharField(max_length=9)
    P_Name = models.CharField(max_length=100)
    P_Phone = models.IntegerField()
    P_Email = models.EmailField()
    P_slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return f"{self.P_Name}"

    def save(self, *args, **kwargs):
        # obj = Article.objects.get(id=1)
        # set something
        if self.P_slug is None:
            self.P_slug = slugify(self.P_NRIC)
        super().save(*args, **kwargs)
        # obj.save()
        # do something


FEVER_RANGE = (
    ('<37.6°C', '<37.6°C'),
    ('37.6°C - 38.3°C', '37.6°C - 38.3°C'),
    ('38.4°C - 39.0°C', '38.4°C - 39.0°C'),
    ('39.1°C - 39.9°C', '39.1°C - 39.9°C'),
    ('>40.0°C', '>40.0°C')
)

class CaseReport(models.Model):
    CR_PatientID = models.ForeignKey(Patient, on_delete=models.CASCADE)
    CR_DateTime = models.DateTimeField(auto_now=True)
    CR_BreathingDifficulty = models.BooleanField()
    CR_FeverTemp = models.CharField(max_length=50, choices=FEVER_RANGE, default='<37.6°C')
    CR_DryCough = models.BooleanField()
    CR_SoreThroat = models.BooleanField()
    CR_OverseasTravel = models.BooleanField()
    CR_CloseContact = models.BooleanField()
    CR_LargeGathering = models.BooleanField()
    CR_PublicExposedPlaces = models.BooleanField()
    CR_FamilyWorksPublicExposedPlaces = models.BooleanField()

    def __str__(self):
        return f'{self.CR_DateTime}, CR'


COVID_CHOICES = (
    ('covid positive', 'Positive'),
    ('covid negative', 'Negative'),
    ('n/a', 'n/a')
)

class Diagnosis(models.Model):
    D_PatientID = models.OneToOneField(CaseReport, on_delete=models.CASCADE)
    D_DateTime = models.DateTimeField(auto_now=True)
    D_EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    D_SymptomRisk = models.CharField(max_length=30)
    D_XRayRisk = models.CharField(max_length=30)
    D_AtRiskOf = models.CharField(max_length=100)
    D_XRayPicture = models.ImageField(upload_to='images')
    D_CovidDiagnosis = models.CharField(max_length=50, choices=COVID_CHOICES, default='positive')
    D_Medication = models.TextField(blank=True, null=True)
    D_dr_queue = models.BooleanField(default=True)
    D_xr_queue = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.D_PatientID.CR_PatientID.P_Name}, visit on ({self.D_DateTime})'




