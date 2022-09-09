from django.urls import path
from . import views

urlpatterns = [
    path('', views.default),
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
    path('DoctorSeePatient/<p_id>', views.DoctorSeePatient),
    path('DoctorViewPatientQuestionnaire/', views.DoctorViewPatientQuestionnaire),

    path('XRayStaffHomepage/', views.XRayStaffHomepage),
    path('XRayStaffXrayPage/<p_id>', views.XRayStaffXrayPage),

    ############################################################################################

    path('remove_from_dr_queue/<p_id>', views.remove_from_dr_queue),
    path('add_to_xr_queue/<p_id>', views.add_to_xr_queue),
    path('completeXray/<p_id>', views.completeXray)
]
