# X Ray Co


X-Ray Co is a comprehensive in-house app that integrates a machine trained model during a diagnostic to help distinguish between COVID-positive patients and non COVID-positive patients more accurately.
<br>
<br>
<p>
<p align="center">
<img src="https://github.com/tanshihuai/X-Ray-Co/blob/master/uploads/images/pic1.jpg" width="600">
<br>
</p>


## Summary
Our model will predict the probability of someone being at risk of having COVID-19, Pneunomia or is healthy given an X-Ray image. This prediction helps doctors get a better picture and improve on their decision making process on whether a patient has contracted COVID-19 or not.

<p>
<p align="center">
<img src="https://github.com/tanshihuai/X-Ray-Co/blob/master/uploads/images/doc1.JPG" width="600">
</p>

## Features

***Nurses***
<br>
Nurses are able to view a patient's visit history and add patients to the doctor's queue. They can also enroll new patients into the hospital's database.
<p>
<p align="center">
<img src="https://github.com/tanshihuai/X-Ray-Co/blob/master/uploads/images/nurse1.JPG" width="600">
</p>

<br>
<br>

***X-Ray staff***
<br>
X-Ray staff can take X-Rays and upload the images for the AI to generate the results.
<p>
<p align="center">
<img src="https://github.com/tanshihuai/X-Ray-Co/blob/master/uploads/images/xray1.JPG" width="600">
</p>

<br>
<br>

***Doctors***
<br>
Doctors are able to see how likely a patient has COVID-19 from their symptoms. They can also register a patient for an X-Ray, see how likely they are to be COVID-positive from the X-Ray, diagnose the patient and prescribe them medicine.
<p>
<p align="center">
<img src="https://github.com/tanshihuai/X-Ray-Co/blob/master/uploads/images/doc1.JPG" width="600">
</p>

<br>
<br>


***Patients***
<br>
The patients will receive a customised SMS and Email notifying them of their diagnosis results and prescribed medication.
<p>
<p align="center">
<img src="https://github.com/tanshihuai/X-Ray-Co/blob/master/uploads/images/patient1.JPG" width="950">
</p>

<br>
<br>

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

***Datasets*** 
<br>
[COVID-19 Radiography Dataset 1](https://www.kaggle.com/datasets/tawsifurrahman/covid19-radiography-database)
<br>
[COVID-19 Radiography Dataset 2](https://www.kaggle.com/datasets/khoongweihao/covid19-xray-dataset-train-test-sets)
<br>
[COVID-19 Radiography Dataset 3](https://www.kaggle.com/datasets/fusicfenta/chest-xray-for-covid19-detection)
<br>
[COVID-19 Symptoms Dataset](https://www.kaggle.com/code/midouazerty/symptoms-covid-19-using-7-machine-learning-98/data)



## To use:
Log in credentials available upon request. Please email xraycofyp@gmail.com.

#Developement to local 

For Mac user
run
  python3 manage.py runserver
  
For windows user
run
  python manage.py runserver


