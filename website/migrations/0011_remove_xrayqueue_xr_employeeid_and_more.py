# Generated by Django 4.0.4 on 2022-09-08 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_patient_p_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='xrayqueue',
            name='XR_EmployeeID',
        ),
        migrations.RemoveField(
            model_name='xrayqueue',
            name='XR_PatientID',
        ),
        migrations.RemoveField(
            model_name='diagnosis',
            name='D_Room',
        ),
        migrations.AlterField(
            model_name='casereport',
            name='CR_DateTime',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='D_CovidDiagnosis',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='D_DateTime',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='D_Medication',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='D_PatientID',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='website.casereport'),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='D_SymptomRisk',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='D_XRayRisk',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='patient',
            name='P_slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='DoctorQueue',
        ),
        migrations.DeleteModel(
            name='XRayQueue',
        ),
    ]