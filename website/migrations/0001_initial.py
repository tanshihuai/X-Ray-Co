# Generated by Django 4.0.4 on 2022-08-18 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NRIC', models.CharField(max_length=9)),
                ('Name', models.CharField(max_length=100)),
                ('Phone', models.IntegerField(unique=True)),
            ],
        ),
    ]
