from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index),
    
    path('Homepage/', views.Homepage),
    path('PatientCreateAccountPage/', views.PatientCreateAccountPage),
    path('ForgetPassword/', views.ForgetPassword),
    path('ChangePassword/', views.ChangePassword),
    path('AdminHomepage/', views.AdminHomepage),

    path('NurseHomepage/', views.NurseHomepage),
    path('NurseViewPatientProfile/', views.NurseViewPatientProfile),
    path('NurseCaseReport/', views.NurseCaseReport),

    path('DoctorHomepage/', views.DoctorHomepage),
    path('DoctorSeePatient/', views.DoctorSeePatient),
    path('DoctorViewPatientQuestionnaire/', views.DoctorViewPatientQuestionnaire),

    path('XRayStaffHomepage/', views.XRayStaffHomepage),
    path('XRayStaffXrayPage/', views.XRayStaffXrayPage),

    path('PatientHomePage/', views.PatientHomePage),
    path('PatientViewVisit/', views.PatientViewVisit),
    path('PatientViewDiagnosis/', views.PatientViewDiagnosis),
    path('PatientAccountPage/', views.PatientAccountPage),
]

