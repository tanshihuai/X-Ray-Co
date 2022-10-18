from django.shortcuts import render, redirect
from django.contrib.auth import login as library_login, authenticate
from .models import Diagnosis, Employee, Patient, CaseReport, Diagnosis
from .forms import PatientForm, CaseReportForm, DiagnosisForm, PictureForm, UserForm
from .filters import PatientFilter, DiagnosisFilter


# Create your views here.


def default(request):
    return render(request, 'website/default.html')

def index(request):
    return render(request, 'website/index.html')

def login(request):

    if request.method =="POST":
        loginform = UserForm(request.POST)
        username = loginform['username'].value()
        password = loginform['password'].value()
        user = authenticate(username=username,password=password)
        library_login(request, user)
        print(f"User {user} successfully logged in.")
        is_doctor = request.session['is_doctor'] = request.user.groups.filter(name="Doctor").exists()
        is_nurse = request.session['is_nurse'] = request.user.groups.filter(name="Nurse").exists()
        is_xraystaff = request.session['is_xraystaff'] = request.user.groups.filter(name="XRayStaff").exists()


        print(f'Doctor: {is_doctor}, Nurse: {is_nurse}, XRayStaff: {is_xraystaff}')

        if is_doctor:
            return redirect('/DoctorHomepage/')
        elif is_nurse:
            return redirect('/NurseHomepage/')
        elif is_xraystaff:
            return redirect('/XRayStaffHomepage/')
        else:
            print("An error has occured - user is neither doctor nor nurse nor xray staff.")

    else:
        request.session['is_doctor'] = request.session['is_nurse'] = request.session['is_xraystaff'] = False
        loginform = UserForm()

    context = {'loginform': loginform}
    return render(request, 'website/login.html', context)


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

    all_patients = Patient.objects.all()

    if request.method =="GET":
        patientform = PatientForm()
        if 'search' in request.GET:
            nricfilter =  PatientFilter(request.GET, queryset=all_patients)
            all_patients = nricfilter.qs
        else:
            nricfilter =  PatientFilter()
        

    else:
        patientform = PatientForm(request.POST)
        if patientform.is_valid():

            # for case report auto redirect
            request.session['nric'] = patientform.cleaned_data['P_NRIC']

            # for patient table
            try:
                registered = Patient.objects.get(P_NRIC= request.session['nric'])
            except:
                patient = patientform.save()
                
            return redirect(f'/NurseCaseReport/')

    
    context = {'all_patients': all_patients, 'patientform': patientform, 'nricfilter': nricfilter, 'is_nurse': request.session['is_nurse']}
    return render(request, 'website/NurseHomepage.html', context)


def NurseViewPatientProfile(request, P_slug):
    patient_history = Diagnosis.objects.filter(D_PatientID__CR_PatientID__P_slug=P_slug)
    context = {'patient_history': patient_history, 'is_nurse': request.session['is_nurse']}
    return render(request, 'website/NurseViewPatientProfile.html', context)


def NurseViewPatientDiagnosis(request, diagnosis_id):
    diag = Diagnosis.objects.get(id=diagnosis_id)
    context = {'diag': diag, 'is_nurse': request.session['is_nurse']}
    return render(request, 'website/NurseViewPatientDiagnosis.html', context)


def NurseCaseReport(request):
    nric = request.session['nric']
    patient = Patient.objects.get(P_NRIC=nric)

    if request.method == "GET":
        questionnaire = CaseReportForm()
        context = {'questionnaire': questionnaire, 'is_nurse': request.session['is_nurse']}
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


########################################################################################################


def DoctorHomepage(request):

    all_patients = Diagnosis.objects.all()
    
    if 'search' in request.GET:
        nricfilter = DiagnosisFilter(request.GET, queryset=all_patients)
        all_patients = nricfilter.qs
    else:
        nricfilter =  DiagnosisFilter()

    context = {'all_patients': all_patients, 'nricfilter': nricfilter, 'is_doctor': request.session['is_doctor']}
    return render(request, 'website/DoctorHomepage.html', context)


def DoctorSeePatient(request, p_id):

    d_obj = Diagnosis.objects.filter(D_PatientID__CR_PatientID__id= p_id)
            
    if request.method == "GET":
        diagnosisform = DiagnosisForm()
        for i in d_obj:
            if i.D_dr_queue:
                context = {'currentdiagnosis': i, 'diagnosisform': diagnosisform, 'is_doctor': request.session['is_doctor']}
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
    #TODO
    context = {'is_doctor': request.session['is_doctor']}
    return render(request, 'website/DoctorViewPatientQuestionnaire.html', context)


########################################################################################################


def XRayStaffHomepage(request):

    all_diagnosis = Diagnosis.objects.all()
    
    if 'search' in request.GET:
        nricfilter = DiagnosisFilter(request.GET, queryset=all_diagnosis)
        all_diagnosis = nricfilter.qs
    else:
        nricfilter =  DiagnosisFilter()

    context = {'all_diagnosis': all_diagnosis, 'nricfilter': nricfilter, 'is_xraystaff': request.session['is_xraystaff']}
    return render(request, 'website/XRayStaffHomepage.html', context)


def XRayStaffXrayPage(request, p_id):

    all_diagnosis = Diagnosis.objects.filter(D_PatientID__CR_PatientID__id=p_id)
    message_flag = False

    if request.method == "GET":
        pictureform = PictureForm()
    else:
        pictureform = PictureForm(request.POST, request.FILES)
        if pictureform.is_valid():
            for i in all_diagnosis:
                print(i)
                i.D_XRayPicture = pictureform.cleaned_data['D_XRayPicture']
                i.save()
                message_flag = True



    context = {'all_diagnosis': all_diagnosis, 'pictureform': pictureform, 'message_flag': message_flag, 'is_xraystaff': request.session['is_xraystaff']}
    return render(request, 'website/XRayStaffXrayPage.html', context)


########################################################################################################


def remove_from_dr_queue(request, p_id):
    d_obj = Diagnosis.objects.filter(D_PatientID__CR_PatientID__id=p_id)
    for i in d_obj:
        if i.D_dr_queue:
            i.D_dr_queue = False
            i.D_xr_queue = False
            i.save()
            return redirect('/DoctorHomepage/')


def add_to_xr_queue(request, p_id):
    d_obj = Diagnosis.objects.filter(D_PatientID__CR_PatientID__id=p_id)
    for i in d_obj:
        if i.D_dr_queue:
            i.D_dr_queue = False
            i.D_xr_queue = True
            i.save()
            return redirect('/DoctorHomepage/')


def completeXray(request, p_id):
    d_obj = Diagnosis.objects.filter(D_PatientID__CR_PatientID__id=p_id)
    for i in d_obj:
        if i.D_xr_queue:
            i.D_dr_queue = True
            i.D_xr_queue = False
            i.save()

    return redirect('/XRayStaffHomepage/')



#TODO: LOGOUT NEEDS TO SET SESSION'S IS_DOCTOR IS_NURSE IS_XRAYSTAFF TO FALSE