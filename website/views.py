from django.shortcuts import render, redirect
from .models import Diagnosis, Employee, Patient, CaseReport, Diagnosis
from .forms import PatientForm, CaseReportForm, DiagnosisForm

# Create your views here.

def default(request):
    return render(request, 'website/default.html')

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
        patient_fk = CaseReport(CR_PatientID=patient)       # create a case report with the "patientID field filled in"
        questionnaire = CaseReportForm(request.POST, instance= patient_fk)      # put the case report u created into the form
        casereport = questionnaire.save()

        # for doctor's queue
        d = Diagnosis()
        d.D_PatientID = casereport
        d.D_EmployeeID = Employee.objects.get(id=5) #hardcoded, change this later
        d.D_SymptomRisk = "to be generated"
        d.D_XRayRisk = "to be generated"
        d.save()
        return redirect(f'/NurseHomepage/')


def DoctorHomepage(request):
    all_patients = Diagnosis.objects.all()
    context = {'all_patients': all_patients}
    return render(request, 'website/DoctorHomepage.html', context)


def DoctorSeePatient(request, p_id):

    d_obj = Diagnosis.objects.filter(D_PatientID__CR_PatientID__id= p_id)
            
    if request.method == "GET":
        diagnosisform = DiagnosisForm()
        for i in d_obj:
            if i.D_dr_queue:
                context = {'currentdiagnosis': i, 'diagnosisform': diagnosisform}
                return render(request, 'website/DoctorSeePatient.html', context)

    else:
        diag_part2 = DiagnosisForm(request.POST)
        if diag_part2.is_valid():
            for i in d_obj:
                if i.D_dr_queue:
                    i.D_CovidDiagnosis = diag_part2.cleaned_data['D_CovidDiagnosis']
                    i.D_Medication = diag_part2.cleaned_data['D_Medication']
                    i.D_dr_queue = False
                    i.D_xr_queue = False
                    i.save()

                    return redirect('/DoctorHomepage/')







def DoctorViewPatientQuestionnaire(request):
    return render(request, 'website/DoctorViewPatientQuestionnaire.html')


########################################################################################################


def XRayStaffHomepage(request):
    all_diagnosis = Diagnosis.objects.all()
    context = {'all_diagnosis': all_diagnosis}
    return render(request, 'website/XRayStaffHomepage.html', context)


def XRayStaffXrayPage(request, p_id):
    all_diagnosis = Diagnosis.objects.filter(D_PatientID__CR_PatientID__id=p_id)
    context = {'all_diagnosis': all_diagnosis}
    return render(request, 'website/XRayStaffXrayPage.html', context)


########################################################################################################


def remove_from_dr_queue(request, p_id):
    d_obj = Diagnosis.objects.get(D_PatientID__CR_PatientID__id=p_id)
    print(d_obj)
    d_obj.D_dr_queue = False
    d_obj.D_xr_queue = False
    d_obj.save()
    return redirect('/DoctorHomepage/')


def add_to_xr_queue(request, p_id):
    d_obj = Diagnosis.objects.get(D_PatientID__CR_PatientID__id=p_id)
    print(d_obj)
    d_obj.D_dr_queue = True
    d_obj.D_xr_queue = True
    d_obj.save()
    return redirect('/DoctorHomepage/')


def completeXray(request, p_id):
    d_obj = Diagnosis.objects.filter(D_PatientID__CR_PatientID__id=p_id)
    for i in d_obj:
        print(i)
        print(i.D_xr_queue)
        if i.D_xr_queue:
            i.D_xr_queue = False
            i.save()

    return redirect('/XRayStaffHomepage/')