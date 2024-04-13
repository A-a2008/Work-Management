from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Litigation(models.Model):
    choices = [
        ('OS', 'OS'),
        ('MC', 'MC'),
        ('CRL.MISC', 'CRL.MISC'),
        ('CC', 'Consumer Complaint'),
        ('CN', 'Crime No.'),
        ('WP', 'WP'),
        ('RFA', 'RFA'),
        ('WA', 'WA'),
        ('MFA', 'MFA'),
        ('LRF', 'LRF'),
        ('RA', 'RA'),
        ('MA', 'MA'),
        ('MISC', 'MISC'),
        ('HRA', 'HRA'),
        ('CRL.APPEAL', 'CRL.APPEAL'),
        ('CRP', 'CRP'), 
    ]

    name = models.CharField(max_length=1000)
    case_type = models.CharField(max_length=100, choices=choices)
    case_number = models.CharField(max_length=12)
    representing_for = models.CharField(max_length=1000)
    document_link = models.URLField()
    rough_work_pic = models.ImageField(upload_to="litigation/")

class WorkLigitation(models.Model):
    litigation = models.ForeignKey(Litigation, on_delete=models.CASCADE)
    work = models.CharField(max_length=1000)
    details = models.TextField()
    to_name = models.CharField(max_length=255, blank=True, null=True)
    to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'groups__name': 'Employees'})
    completion_date = models.DateField()

    def save(self, *args, **kwargs):
        if self.to:
            self.to_name = self.to.username
        super().save(*args, **kwargs)
