from django import forms
from .models import Patient, CaseReport, Diagnosis


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('P_NRIC', 'P_Name', 'P_Phone', 'P_Email')
        labels = {
            "P_NRIC": "NRIC",
            "P_Name": "Name",
            "P_Phone": "Phone",
            "P_Email": "Email",
        }


class CaseReportForm(forms.ModelForm):
    class Meta:
        model = CaseReport
        fields = ('CR_Fever', 'CR_DryCough', 'CR_SoreThroat', 'CR_BreathingDifficulty', 'CR_OverseasTravel', 'CR_CloseContact')
        labels = {
            "CR_Fever": "Fever",
            "CR_DryCough": "Dry cough",
            "CR_SoreThroat": "Sore throat",
            "CR_BreathingDifficulty": "Breathing difficulty",
            "CR_OverseasTravel": "Overseas travel",
            "CR_CloseContact": "Close contact",
        }


class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = ('D_CovidDiagnosis', 'D_Medication')
        labels = {
            "D_CovidDiagnosis": "Diagnosis",
            "D_Medication": "Prescribed medication",
        }


