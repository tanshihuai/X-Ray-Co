from django import forms
from .models import Patient, CaseReport, Diagnosis
from django.contrib.auth.models import User


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
        fields = ('CR_FeverTemp', 'CR_BreathingDifficulty', 'CR_DryCough',
                  'CR_SoreThroat', 'CR_OverseasTravel', 'CR_CloseContact',
                  'CR_LargeGathering', 'CR_PublicExposedPlaces', 'CR_FamilyWorksPublicExposedPlaces')
        labels = {
            "CR_BreathingDifficulty": "Breathing difficulty",
            "CR_FeverTemp": "Temperature",
            "CR_DryCough": "Dry cough",
            "CR_SoreThroat": "Sore throat",
            "CR_OverseasTravel": "Overseas travel",
            "CR_CloseContact": "Close contact",
            "CR_LargeGathering": "Attended large gathering",
            "CR_PublicExposedPlaces": "Visited public exposed places",
            "CR_FamilyWorksPublicExposedPlaces": "Family works in public exposed places",
        }


class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = ('D_CovidDiagnosis', 'D_Medication')
        labels = {
            "D_CovidDiagnosis": "Diagnosis",
            "D_Medication": "Prescribed medication",
        }


class PictureForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = ('D_XRayPicture',)
        labels = {
            "D_XRayPicture": "X-Ray picture",
        }

class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'password')
