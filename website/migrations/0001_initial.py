# Generated by Django 4.1.3 on 2022-11-08 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CaseReport",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("CR_DateTime", models.DateTimeField(auto_now=True)),
                ("CR_BreathingDifficulty", models.BooleanField()),
                (
                    "CR_FeverTemp",
                    models.CharField(
                        choices=[
                            ("<37.6°C", "<37.6°C"),
                            ("37.6°C - 38.3°C", "37.6°C - 38.3°C"),
                            ("38.4°C - 39.0°C", "38.4°C - 39.0°C"),
                            ("39.1°C - 39.9°C", "39.1°C - 39.9°C"),
                            (">40.0°C", ">40.0°C"),
                        ],
                        default="<37.6°C",
                        max_length=50,
                    ),
                ),
                ("CR_DryCough", models.BooleanField()),
                ("CR_SoreThroat", models.BooleanField()),
                ("CR_OverseasTravel", models.BooleanField()),
                ("CR_CloseContact", models.BooleanField()),
                ("CR_LargeGathering", models.BooleanField()),
                ("CR_PublicExposedPlaces", models.BooleanField()),
                ("CR_FamilyWorksPublicExposedPlaces", models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name="Patient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("P_NRIC", models.CharField(max_length=9)),
                ("P_Name", models.CharField(max_length=100)),
                ("P_Phone", models.IntegerField()),
                ("P_Email", models.EmailField(max_length=254)),
                ("P_slug", models.SlugField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Role",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("R_RoleName", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Employee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("E_Password", models.CharField(max_length=255)),
                ("E_Name", models.CharField(max_length=255)),
                ("E_Phone", models.CharField(max_length=255)),
                ("E_Email", models.CharField(max_length=255)),
                (
                    "E_RoleName",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="website.role"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Diagnosis",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("D_DateTime", models.DateTimeField(auto_now=True)),
                ("D_SymptomRisk", models.CharField(max_length=100)),
                ("D_XRayRisk", models.CharField(max_length=100)),
                ("D_AtRiskOf", models.CharField(max_length=100)),
                (
                    "D_XRayPicture",
                    models.ImageField(max_length=110, upload_to="images"),
                ),
                (
                    "D_CovidDiagnosis",
                    models.CharField(
                        choices=[
                            ("covid positive", "Positive"),
                            ("covid negative", "Negative"),
                            ("n/a", "n/a"),
                        ],
                        default="positive",
                        max_length=100,
                    ),
                ),
                ("D_Medication", models.TextField(blank=True, null=True)),
                ("D_dr_queue", models.BooleanField(default=True)),
                ("D_xr_queue", models.BooleanField(default=False)),
                (
                    "D_EmployeeID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="website.employee",
                    ),
                ),
                (
                    "D_PatientID",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="website.casereport",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="casereport",
            name="CR_PatientID",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="website.patient"
            ),
        ),
    ]
