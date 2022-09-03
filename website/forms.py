from django import forms
from .models import Patient, CaseReport

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('P_NRIC', 'P_Name', 'P_Phone', 'P_Email')

class CaseReportForm(forms.ModelForm):
    class Meta:
        model = CaseReport
        fields = ('CR_Fever', 'CR_DryCough', 'CR_SoreThroat', 'CR_BreathingDifficulty', 'CR_OverseasTravel', 'CR_CloseContact')
