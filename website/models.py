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


class CaseReport(models.Model):
    CR_PatientID = models.ForeignKey(Patient, on_delete=models.CASCADE)
    CR_DateTime = models.DateTimeField(auto_now=True)
    CR_Fever = models.BooleanField()
    CR_DryCough = models.BooleanField()
    CR_SoreThroat = models.BooleanField()
    CR_BreathingDifficulty = models.BooleanField()
    CR_OverseasTravel = models.BooleanField()
    CR_CloseContact = models.BooleanField()

    def __str__(self):
        return f'{self.CR_PatientID.P_Name}, CR'

'''
class DoctorQueue(models.Model):
    DQ_EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    DQ_PatientID = models.OneToOneField(CaseReport, on_delete=models.CASCADE)
    DQ_DateTime = models.DateTimeField(auto_now=True)
    DQ_SymptomRisk = models.CharField(max_length=30)


    def __str__(self):
        return f'{self.DQ_SymptomRisk}'


class XRayQueue(models.Model):
    XR_EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    XR_PatientID = models.OneToOneField(DoctorQueue, on_delete=models.CASCADE)
    XR_DateTime = models.DateTimeField(auto_now=True)
    #TODO: XR_XRayPicture 
    XR_XRayRisk = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.XR_XRayRisk}"
'''

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
    #D_XRayPicture
    D_CovidDiagnosis = models.CharField(max_length=50, choices=COVID_CHOICES, default='positive')
    D_Medication = models.TextField(blank=True, null=True)
    D_dr_queue = models.BooleanField(default=True)
    D_xr_queue = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.D_PatientID.CR_PatientID.P_Name}, visit on ({self.D_DateTime})'




