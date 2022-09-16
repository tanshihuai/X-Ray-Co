import django_filters
from django import forms
from django_filters import CharFilter

from .models import *

class PatientFilter(django_filters.FilterSet):
    nric = CharFilter(field_name='P_NRIC', lookup_expr='icontains', label = 'Search by NRIC:')
    class Meta:
        model = Patient
        fields = ('nric',)


class DiagnosisFilter(django_filters.FilterSet):
    nric = CharFilter(field_name='D_PatientID__CR_PatientID__P_NRIC', lookup_expr='icontains', label = 'Search by NRIC:')
    class Meta:
        model = Diagnosis
        fields = ('nric',)