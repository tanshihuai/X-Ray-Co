# X Ray Co

X-Ray Co is a comprehensive in-house app that integrates a machine trained model during a diagnostic to help distinguish between COVID-positive patients and non COVID-positive patients more accurately.

pic1

## Summary
Our model will assign a percentage of COVID-19, Peunomia, or Normal given an X-Ray image. This helps doctors get a better picture and can improve on their decision making process on whether a patient has contracted COVID-19 or not.

doc1

## Features
n1
Nurses view the patient's visit history can add patients to the doctor's queue

d1
Doctors can see how likely a patient has COVID-19 from their symptoms. They can also register a patient for an X-Ray, see how likely they are to be COVID-positive from the X-Ray, diagnose the patient and prescribe them medicine.

x1
X-Ray staffs can take X-Rays and upload the images for the AI to generate the results.

Patients
The patients will receive a customised SMS and Email notifying them of their diagnosis results and medication prescribed.

## Application code
***Full-stack***
<br>
Web Framework: [Django](https://www.djangoproject.com/)
<br>


***APIS***
<br>
Image and model hosting: [AWS S3](https://aws.amazon.com/s3/)
<br>
Automated Emails: [Postmark](https://postmarkapp.com/)
<br>
Automated SMSes: [Twilio](https://www.twilio.com/)
<br>

***Deployment***
<br>
Cloud Application Platform: [Heroku](https://heroku.com/)
<br>

***Dataset***
<br>
[COVID-19 Radiography Dataset](https://www.kaggle.com/datasets/tawsifurrahman/covid19-radiography-database)
<br>
[COVID-19 Symptoms Dataset]: to be added







