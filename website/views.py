from django.shortcuts import render
from .models import Patient

# Create your views here.

def index(request):
    return render(request, 'website/index.html')


########################################################################################################


def Homepage(request):
    return render(request, 'website/Homepage.html')

def PatientCreateAccountPage(request):
    return render(request, 'website/PatientCreateAccountPage.html')

def ForgetPassword(request):
    return render(request, 'website/ForgetPassword.html')

def ChangePassword(request):
    return render(request, 'website/ChangePassword.html')

def AdminHomepage(request):
    return render(request, 'website/AdminHomepage.html')


########################################################################################################


def NurseHomepage(request):
    all_patients = Patient.objects.all()
    context = {'all_patients': all_patients}
    return render(request, 'website/NurseHomepage.html', context)

def NurseViewPatientProfile(request):
    return render(request, 'website/NurseViewPatientProfile.html')

def NurseCaseReport(request):
    return render(request, 'website/NurseCaseReport.html')

def DoctorHomepage(request):
    return render(request, 'website/DoctorHomepage.html')

def DoctorSeePatient(request):
    return render(request, 'website/DoctorSeePatient.html')

def DoctorViewPatientQuestionnaire(request):
    return render(request, 'website/DoctorViewPatientQuestionnaire.html')


########################################################################################################


def XRayStaffHomepage(request):
    return render(request, 'website/XRayStaffHomepage.html')

def XRayStaffXrayPage(request):
    return render(request, 'website/XRayStaffXrayPage.html')


########################################################################################################


def PatientHomePage(request):
    return render(request, 'website/PatientHomePage.html')

def PatientViewVisit(request):
    return render(request, 'website/PatientViewVisit.html')

def PatientViewDiagnosis(request):
    return render(request, 'website/PatientViewDiagnosis.html')

def PatientAccountPage(request):
    return render(request, 'website/PatientAccountPage.html')
    