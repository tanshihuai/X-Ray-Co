from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as library_login, logout as library_logout, authenticate
from .models import Diagnosis, Employee, Patient, CaseReport, Diagnosis
from .forms import PatientForm, CaseReportForm, DiagnosisForm, PictureForm, UserForm
from .filters import PatientFilter, DiagnosisFilter
import os
import boto3

# Twilio and Postmark
from twilio.rest import Client
from postmarker.core import PostmarkClient

# ML libraries
from tensorflow import keras
from skimage.transform import resize
import numpy as np
import matplotlib.pyplot as plt
import pickle




def default(request):
    return render(request, 'website/default.html')


def login(request):

    if request.method =="POST":
        loginform = UserForm(request.POST)
        username = loginform['username'].value()
        password = loginform['password'].value()
        user = authenticate(username=username, password=password)
        if user is not None:
            library_login(request, user)
            
            is_doctor = request.user.groups.filter(name="Doctor").exists()
            is_nurse = request.user.groups.filter(name="Nurse").exists()
            is_xraystaff = request.user.groups.filter(name="XRayStaff").exists()

            if is_doctor:
                return redirect('/DoctorHomepage/')
            elif is_nurse:
                return redirect('/NurseHomepage/')
            elif is_xraystaff:
                return redirect('/XRayStaffHomepage/')
            elif user.is_superuser:
                return redirect('/admin/')
            else:
                print("An error has occurred - user is neither doctor nor nurse nor xray staff.")
        else:
            messages.error(request,'Login failed. Username or password is incorrect.')
            return redirect('/')

    else:
        loginform = UserForm()

    context = {'loginform': loginform}
    return render(request, 'website/login.html', context)


def logoutpage(request):
    return render(request, 'website/logoutpage.html')


########################################################################################################


def NurseHomepage(request):

    all_patients = Patient.objects.all()

    if request.method =="GET":
        patientform = PatientForm()
        if 'search' in request.GET:
            nricfilter = PatientFilter(request.GET, queryset=all_patients)
            all_patients = nricfilter.qs
        else:
            nricfilter = PatientFilter()
        

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

    
    context = {'all_patients': all_patients, 'patientform': patientform, 'nricfilter': nricfilter}
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
        casereport_with_ID = CaseReport(CR_PatientID=patient)       # create a case report with the "patientID field filled in"
        questionnaire_with_ID = CaseReportForm(request.POST, instance= casereport_with_ID)      # put the case report u created into the form
        casereport = questionnaire_with_ID.save()
        if casereport.CR_FeverTemp != "no fever":
            fever = True
        else:
            fever = False
        questionnaire = [casereport.CR_BreathingDifficulty, fever, casereport.CR_DryCough,
                         casereport.CR_SoreThroat, casereport.CR_OverseasTravel, casereport.CR_CloseContact,
                         casereport.CR_LargeGathering, casereport.CR_PublicExposedPlaces, casereport.CR_FamilyWorksPublicExposedPlaces
                         ]
        results = predictsymptom(questionnaire)

        # for doctor's queue
        d = Diagnosis()
        d.D_PatientID = casereport
        d.D_EmployeeID = Employee.objects.get(id=5) #hardcoded, change this later
        d.D_SymptomRisk = results
        d.D_XRayRisk = "X-Ray not yet taken"
        d.D_AtRiskOf = "X-Ray not yet taken"
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

    context = {'all_patients': all_patients, 'nricfilter': nricfilter}
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

                    message = f"Dear {i.D_PatientID.CR_PatientID.P_Name},\n\nYour diagnosis is complete. "
                    if i.D_CovidDiagnosis == "covid positive":
                        message += f"You have tested POSITIVE for COVID-19. Your medications are: {i.D_Medication}. "
                    else:
                        message += f"You have tested NEGATIVE for COVID-19."

                    message += "\n\nPlease continue following the latest safety measures set by MOH. Have a nice day."

                    # Email
                    email = i.D_PatientID.CR_PatientID.P_Email

                    postmark_api_key = os.getenv("postmark_api_key")
                    postmark = PostmarkClient(server_token=postmark_api_key)
                    postmark.emails.send(
                        From='shtan092@mymail.sim.edu.sg',
                        To=email,
                        Subject='X-Ray Diagnosis',
                        HtmlBody=f"<p>{message}<p>"
                    )

                    # SMS
                    phone_prefix = "+65"
                    phone_number = phone_prefix + str(i.D_PatientID.CR_PatientID.P_Phone)

                    account_sid = "ACb9304b77776dfa3a1ad5770c80021aae"
                    auth_token = os.getenv("twilio_api_key")
                    client = Client(account_sid, auth_token)
                    message = client.messages.create(
                        to=phone_number,
                        from_="X Ray Co",
                        body=message)
                    print(message.body)

                    return redirect('/DoctorHomepage/')


def DoctorViewPatientQuestionnaire(request, p_id):

    casereport = Diagnosis.objects.filter(D_PatientID__CR_PatientID__id=p_id)
    if request.method == "GET":

        for i in casereport:
            if i.D_dr_queue:
                questionnaire = CaseReportForm(instance=i.D_PatientID)
                context = {"questionnaire": questionnaire, "i": i}
                return render(request, 'website/DoctorViewPatientQuestionnaire.html', context)

    else:
        print("I am here")
        questionnaire = CaseReportForm(request.POST)
        if questionnaire.is_valid():
            for i in casereport:
                if i.D_dr_queue:

                    patient = Patient.objects.get(id=p_id)
                    casereport_with_ID = CaseReport(CR_PatientID=patient)  # create a case report with the "patientID field filled in"
                    questionnaire_with_ID = CaseReportForm(request.POST, instance=casereport_with_ID)  # put the case report u created into the form
                    i.D_PatientID = questionnaire_with_ID.save()

                    questionnaire = [i.D_PatientID.CR_BreathingDifficulty, i.D_PatientID.CR_Fever, i.D_PatientID.CR_DryCough,
                                     i.D_PatientID.CR_SoreThroat, i.D_PatientID.CR_OverseasTravel, i.D_PatientID.CR_CloseContact,
                                     i.D_PatientID.CR_LargeGathering, i.D_PatientID.CR_PublicExposedPlaces,
                                     i.D_PatientID.CR_FamilyWorksPublicExposedPlaces
                                     ]
                    results = predictsymptom(questionnaire)
                    i.D_SymptomRisk = results
                    i.save()

                    return redirect(f'/DoctorSeePatient/{p_id}')



########################################################################################################


def XRayStaffHomepage(request):

    all_diagnosis = Diagnosis.objects.all()
    
    if 'search' in request.GET:
        nricfilter = DiagnosisFilter(request.GET, queryset=all_diagnosis)
        all_diagnosis = nricfilter.qs
    else:
        nricfilter = DiagnosisFilter()

    context = {'all_diagnosis': all_diagnosis, 'nricfilter': nricfilter}
    return render(request, 'website/XRayStaffHomepage.html', context)


def XRayStaffXrayPage(request, p_id):
    aws_api_key = os.getenv("aws_api_key")
    s3_client = boto3.client('s3', aws_access_key_id='AKIARMZGHF3PA6DUO75U', aws_secret_access_key=aws_api_key)
    result = s3_client.download_file('covidh5model', 'static/website/model.h5', 'tmp')
    model = keras.models.load_model('tmp')
    all_diagnosis = Diagnosis.objects.filter(D_PatientID__CR_PatientID__id=p_id)
    message_flag = False

    if request.method == "GET":
        pictureform = PictureForm()
    else:
        pictureform = PictureForm(request.POST, request.FILES)
        if pictureform.is_valid():
            for i in all_diagnosis:
                if i.D_xr_queue:
                    i.D_XRayPicture = pictureform.cleaned_data['D_XRayPicture']

                    results = predictxray(i.D_XRayPicture)
                    string_rephrase = ""
                    for x, y in results.items():
                        string_rephrase += f"{x}: {y}%, "
                    i.D_XRayRisk = string_rephrase.rstrip(", ")
                    first_pair = next(iter((results.items())))
                    most_at_risk = f"{first_pair[0]}: {first_pair[1]}%"
                    i.D_AtRiskOf = most_at_risk
                    i.save()
                    message_flag = True

    context = {'all_diagnosis': all_diagnosis, 'pictureform': pictureform, 'message_flag': message_flag}
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


def logout(request):
    library_logout(request)
    return redirect('/logoutpage/')


def predictxray(image):
    new_image = plt.imread(image)
    resized_image = resize(new_image, (224, 224, 3))
    predictions = model.predict(np.array([resized_image]))
    list_index = [0, 1, 2]
    x = predictions

    for i in range(3):
        for j in range(3):
            if x[0][list_index[i]] > x[0][list_index[j]]:
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp

    classification = ['COVID-19', 'Normal', 'Pneumonia']
    results = {}
    for i in range(3):
        results[classification[list_index[i]]] = round(predictions[0][list_index[i]] * 100, 2)
    print(results)
    return results


def predictsymptom(symptoms):
    # takes in a list of 9 elements, each referring to a question in the case report
    loaded_model = pickle.load(open('website/symptom_model.sav', 'rb'))
    symptoms = np.reshape(symptoms, -1).reshape(1, -1)
    y_pred = round(loaded_model.predict(symptoms)[0], 2)
    print(f"{y_pred*100}%")
    return f"{y_pred*100}%"

