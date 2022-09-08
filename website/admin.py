from django.contrib import admin
from .models import Patient, Role, Employee, Diagnosis, CaseReport

# Register your models here.


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'E_Name', 'E_Phone', 'E_Email', 'E_RoleName')

class PatientAdmin(admin.ModelAdmin):
    list_display = ('P_Name', 'P_NRIC', 'P_Phone', 'P_Email')

class CaseReportAdmin(admin.ModelAdmin):
    list_display = ('CR_PatientID', 'CR_Fever', 'CR_DryCough', 'CR_SoreThroat', 'CR_BreathingDifficulty', 'CR_OverseasTravel', 'CR_CloseContact', 'CR_DateTime')

class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('D_PatientID', 'D_EmployeeID', 'D_SymptomRisk', 'D_XRayRisk', 'D_CovidDiagnosis', 'D_Medication', 'D_DateTime')


admin.site.register(Role)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(CaseReport, CaseReportAdmin)
admin.site.register(Diagnosis, DiagnosisAdmin)