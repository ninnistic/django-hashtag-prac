from django.db import models

# Create your models here.


class Doctor(models.Model):
    name = models.TextField()

    def __str__(self):
        return f'{self.name} 전문의'


class Patient(models.Model):
    # Reservation이라는 테이블을 통해 ManyToManyField를 맺음
    doctors = models.ManyToManyField(Doctor, through='Reservation')
    name = models.TextField()

    def __str__(self):
        return f"{self.pk}번 환자 {self.name}"


# 중개테이블 생성 (ManyToMany로 해결되지 않는 더 많은 필드가 필요한 경우)
class Reservation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    sympptom = models.TextField()
    reserved_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.doctor_id}번 의사의 {self.patient_id}번 환자"
