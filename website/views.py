from django.shortcuts import render, redirect
from .models import Diagnosis, Employee, Patient, CaseReport, Diagnosis
from .forms import PatientForm, CaseReportForm

# Create your views here.

def index(request):
    return render(request, 'website/index.html')


########################################################################################################


def Homepage(request):
    return render(request, 'website/Homepage.html')

def ForgetPassword(request):
    return render(request, 'website/ForgetPassword.html')

def ChangePassword(request):
    return render(request, 'website/ChangePassword.html')

def AdminHomepage(request):
    return render(request, 'website/AdminHomepage.html')


########################################################################################################


def NurseHomepage(request):
    if request.method =="GET":
        patientform = PatientForm()
    else:
        patientform = PatientForm(request.POST)
        if patientform.is_valid():

            # for case report auto redirect
            request.session['nric'] = patientform.cleaned_data['P_NRIC']

            # for patient table
            patient = patientform.save()

            
            return redirect(f'/NurseCaseReport/')

    all_patients = Patient.objects.all()
    context = {'all_patients': all_patients, 'patientform': patientform}
    return render(request, 'website/NurseHomepage.html', context)


def NurseViewPatientProfile(request, P_slug):
    patient_history = Diagnosis.objects.filter(D_PatientID__CR_PatientID__P_slug=P_slug)
    context = {'patient_history': patient_history}
    return render(request, 'website/NurseViewPatientProfile.html', context)


def NurseViewPatientDiagnosis(request, diagnosis_id):
    diag = Diagnosis.objects.get(id=diagnosis_id)
    context = {'diag': diag}
    return render(request, 'website/NurseViewPatientDiagnosis.html', context)


def NurseCaseReport(request):
    nric = request.session['nric']
    patient = Patient.objects.get(P_NRIC=nric)

    if request.method == "GET":
        questionnaire = CaseReportForm()
        context = {'questionnaire': questionnaire}
        return render(request, 'website/NurseCaseReport.html', context)
    else:
        # u need the slug in action=/nursecasereport/HERE to come to here via post, now check why the other one dont need
        patient_fk = CaseReport(CR_PatientID=patient)
        questionnaire = CaseReportForm(request.POST, instance= patient_fk)
        casereport = questionnaire.save()

        # for doctor's queue
        d = Diagnosis()
        d.D_PatientID = casereport
        d.D_EmployeeID = Employee.objects.get(id=5) #hardcoded, change this later
        d.D_SymptomRisk = "to be done"
        d.D_XRayRisk = "to be done"
        d.save()

        return redirect(f'/NurseHomepage/')

def DoctorHomepage(request):
    all_patients = Diagnosis.objects.all()
    context = {'all_patients': all_patients}
    return render(request, 'website/DoctorHomepage.html', context)

def DoctorSeePatient(request, p_id):
    d_obj = Diagnosis.objects.get(D_PatientID__CR_PatientID__id= p_id)
    context = {'d_obj': d_obj}
    return render(request, 'website/DoctorSeePatient.html', context)

def DoctorViewPatientQuestionnaire(request):
    return render(request, 'website/DoctorViewPatientQuestionnaire.html')


########################################################################################################


def XRayStaffHomepage(request):
    return render(request, 'website/XRayStaffHomepage.html')

def XRayStaffXrayPage(request):
    return render(request, 'website/XRayStaffXrayPage.html')


########################################################################################################


def delete_dq_entry(request, p_id):
    d_obj = Diagnosis.objects.get(D_PatientID__CR_PatientID__id=p_id)
    print(d_obj)
    d_obj.delete()
    return redirect('/DoctorHomepage/')