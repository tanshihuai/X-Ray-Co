from django.db import models

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
    P_NRIC = models.CharField(max_length=9, unique=True)
    P_Name = models.CharField(max_length=100)
    P_Phone = models.IntegerField(unique=True)
    P_Email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.P_Name}"


class CaseReport(models.Model):
    CR_PatientID = models.ForeignKey(Patient, on_delete=models.CASCADE)
    CR_DateTime = models.DateTimeField()
    CR_Fever = models.BooleanField()
    CR_DryCough = models.BooleanField()
    CR_SoreThroat = models.BooleanField()
    CR_BreathingDifficulty = models.BooleanField()
    CR_OverseasTravel = models.BooleanField()
    CR_CloseContact = models.BooleanField()

    def __str__(self):
        return f'{self.CR_PatientID.P_Name}({self.CR_DateTime})'


class DoctorQueue(models.Model):
    DQ_EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    #inherits Patients's ID from class CaseReport which inherits from class Patient, 
    # not sure if errors will occur, if they occur just inherit from patient directly
    DQ_PatientID = models.OneToOneField(CaseReport, on_delete=models.CASCADE)
    DQ_DateTime = models.DateTimeField()
    DQ_SymptomRisk = models.CharField(max_length=30)


    def __str__(self):
        return f'Patient ({self.DQ_PatientID.CR_PatientID.P_Name}) attended to by Dr.({self.DQ_EmployeeID.E_Name})'


class XRayQueue(models.Model):
    XR_EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    XR_PatientID = models.OneToOneField(DoctorQueue, on_delete=models.CASCADE)
    XR_DateTime = models.DateTimeField()
    #TODO: XR_XRayPicture 
    XR_XRayRisk = models.CharField(max_length=30)

    def __str__(self):
        return f"Patient ({self.XR_PatientID.DQ_PatientID.CR_PatientID.P_Name})'s X-ray by Staff ({self.XR_EmployeeID.E_Name})"


class Diagnosis(models.Model):
    D_PatientID = models.ForeignKey(Patient, on_delete=models.CASCADE)
    D_DateTime = models.DateTimeField()
    D_EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    D_Room = models.CharField(max_length=9)
    D_SymptomRisk = models.OneToOneField(DoctorQueue, on_delete=models.CASCADE)
    D_XRayRisk = models.OneToOneField(XRayQueue, on_delete=models.CASCADE)
    #D_XRayPicture
    D_CovidDiagnosis = models.CharField(max_length=50)
    D_Medication = models.TextField()

    def __str__(self):
        return f'{self.D_PatientID.P_Name}, visit on ({self.D_DateTime})'