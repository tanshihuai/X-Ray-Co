from django.contrib import admin
from .models import Patient, Role, Employee, Diagnosis, CaseReport, DoctorQueue, XRayQueue

# Register your models here.


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'E_Name', 'E_Phone', 'E_Email', 'E_RoleName')

class PatientAdmin(admin.ModelAdmin):
    list_display = ('P_Name', 'P_NRIC', 'P_Phone', 'P_Email')

class CaseReportAdmin(admin.ModelAdmin):
    list_display = ('CR_PatientID', 'CR_Fever', 'CR_DryCough', 'CR_SoreThroat', 'CR_BreathingDifficulty', 'CR_OverseasTravel', 'CR_CloseContact', 'CR_DateTime')

class DoctorQueueAdmin(admin.ModelAdmin):
    list_display = ('DQ_EmployeeID', 'get_DQ_PatientID', 'DQ_SymptomRisk', 'DQ_DateTime')

    def get_DQ_PatientID(self, obj):
        return obj.DQ_PatientID.CR_PatientID.P_Name

class XRayQueueAdmin(admin.ModelAdmin):
    list_display = ('XR_EmployeeID', 'get_XR_PatientID', 'XR_XRayRisk', 'XR_DateTime')

    def get_XR_PatientID(self, obj):
        return obj.XR_PatientID.DQ_PatientID.CR_PatientID.P_Name


class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('D_PatientID', 'D_EmployeeID', 'D_Room', 'get_D_SymptomRisk', 'get_D_XRayRisk', 'D_CovidDiagnosis', 'D_Medication', 'D_DateTime')

    def get_D_SymptomRisk(self, obj):
            return obj.D_SymptomRisk.DQ_SymptomRisk

    def get_D_XRayRisk(self, obj):
            return obj.D_XRayRisk.XR_XRayRisk


admin.site.register(Role)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(CaseReport, CaseReportAdmin)
admin.site.register(DoctorQueue, DoctorQueueAdmin)
admin.site.register(XRayQueue, XRayQueueAdmin)
admin.site.register(Diagnosis, DiagnosisAdmin)