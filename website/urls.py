from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index),

    path('Homepage/', views.Homepage),
    path('ForgetPassword/', views.ForgetPassword),
    path('ChangePassword/', views.ChangePassword),
    path('AdminHomepage/', views.AdminHomepage),

    path('NurseHomepage/', views.NurseHomepage),
    path('NurseViewPatientProfile/<slug:P_slug>', views.NurseViewPatientProfile),
    path('NurseViewPatientDiagnosis/<slug:diagnosis_id>', views.NurseViewPatientDiagnosis),
    path('NurseCaseReport/', views.NurseCaseReport),

    path('DoctorHomepage/', views.DoctorHomepage),
    path('DoctorSeePatient/', views.DoctorSeePatient),
    path('DoctorViewPatientQuestionnaire/', views.DoctorViewPatientQuestionnaire),

    path('XRayStaffHomepage/', views.XRayStaffHomepage),
    path('XRayStaffXrayPage/', views.XRayStaffXrayPage),

    ############################################################################################

    path('delete_dq_entry/<id>', views.delete_dq_entry)
]
