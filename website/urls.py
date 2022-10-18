from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.login),

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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
