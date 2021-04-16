from django.db import models
from django.contrib.auth import get_user_model

CITIES = [
            ('Alexandria', 'Alexandria'),
            ('Aswan', 'Aswan'),
            ('Asyut', 'Asyut'),
            ('Beheira', 'Beheira'),
            ('Beni Suef', 'Beni Suef'),
            ('Cairo', 'Cairo'),
            ('Dakahlia', 'Dakahlia'),
            ('Damietta', 'Damietta'),
            ('Faiyum', 'Faiyum'),
            ('Gharbia', 'Gharbia'),
            ('Giza', 'Giza'),
            ('Ismailia', 'Ismailia'),
            ('Kafr El Sheikh', 'Kafr El Sheikh'),
            ('Luxor', 'Luxor'),
            ('Matruh', 'Matruh'),
            ('Minya', 'Minya'),
            ('Monufia', 'Monufia'),
            ('New Valley', 'New Valley'),
            ('North Sinai', 'North Sinai'),
            ('Port Said', 'Port Said'),
            ('Qalyubia', 'Qalyubia'),
            ('Qena', 'Qena'),
            ('Red Sea', 'Red Sea'),
            ('Sharqia', 'Sharqia'),
            ('Sohag', 'Sohag'),
            ('South Sinai', 'South Sinai'),
            ('Suez', 'Suez')
        ]

class Clinic(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    city = models.CharField(choices=CITIES,max_length=14)    
    address = models.CharField(max_length=250)    
    description = models.TextField()
    working_from = models.TimeField(auto_now=False, auto_now_add=False)
    working_till = models.TimeField(auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s clinic"

RATING = [
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')
    ]
class ClinicReview(models.Model):
    patient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    comment_review = models.TextField()
    rating = models.CharField(choices=RATING, max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.patient}'s review on {self.clinic}"


STATUS = [
        ('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')
    ]
class Appointment(models.Model):
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    status = models.CharField(null=True, choices=STATUS, max_length=10, default='Pending')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    patient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    paied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    def __str__(self):
        return f"{self.patient.username}'s Appointment with {self.clinic.user.username}'s clinic"

class Prescription(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    patient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    symptoms = models.TextField()
    prescription = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f"{self.clinic.user.username}' prescription to {self.patient.username}"

PAYMENT_TYPES = [
    ('I','Individual'),
    ('C','Consulting')
]

class Payment(models.Model):
    patient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    paid = models.FloatField(null=True)
    outstanding = models.FloatField(null=True)
    total = models.FloatField(null=True)
    payment_type = models.CharField(choices=PAYMENT_TYPES, max_length=1, default="I")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return "Payment Patient-{} Amount-{}".format(self.patient, self.total)