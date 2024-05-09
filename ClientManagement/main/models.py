from django.db import models
from accounts.models import User

# Create your models here.

class Litigation(models.Model):
    choices = [
        ('OS', 'OS'),
        ('MC', 'MC'),
        ('CRL.MISC', 'CRL.MISC'),
        ('CCo', 'Consumer Complaint'),
        ('CN', 'Crime No.'),
        ('CC', 'CC'),
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

    def __str__(self) -> str:
        return self.name

class WorkLigitation(models.Model):
    priorities = [
        ("High", "High"),
        ("Normal", "Normal"),
        ("Low", "Low")
    ]
    litigation = models.ForeignKey(Litigation, on_delete=models.CASCADE)
    work = models.CharField(max_length=1000)
    details = models.TextField(null=True)
    to_name = models.CharField(max_length=255, blank=True, null=True)
    to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'groups__name': 'Employees'})
    completion_date = models.DateField()
    reminder_start_date = models.DateField()
    priority_level = models.CharField(max_length=10, choices=priorities)
    finished = models.BooleanField(default=False)
    finished_time = models.DateTimeField(null=True)
    finished_in_time = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.to:
            self.to_name = f"{self.to.first_name} {self.to.last_name}"
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.work

class NonLitigation(models.Model):
    types = [
        ("Site", "Site"),
        ("Villa", "Villa"),
        ("Gated Community", "Gated Community"),
        ("Apartment", "Apartment"),
        ("Row Houses", "Row Houses"),
    ]
    name = models.CharField(max_length=1000)
    project_name = models.CharField(max_length=1000)
    situation = models.TextField()
    property_type = models.CharField(max_length=100, choices=types)
    site_no = models.CharField(max_length=1000)
    present_owner = models.CharField(max_length=1000)
    document_link = models.URLField()
    rough_work_pic = models.ImageField(upload_to="nonlitigation/")
    case_stage = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name

class WorkNonLitigation(models.Model):
    non_litigation = models.ForeignKey(NonLitigation, on_delete=models.CASCADE)
    work = models.CharField(max_length=1000)
    details = models.TextField(null=True)
    to_name = models.CharField(max_length=255, blank=True, null=True)
    # add to_telegram_user_id if possible
    to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'groups__name': 'Employees'})
    completion_date = models.DateField()
    reminder_start_date = models.DateField()
    finished = models.BooleanField(default=False)
    finished_time = models.DateTimeField(null=True)
    finished_in_time = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.to:
            self.to_name = f"{self.to.first_name} {self.to.last_name}"
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.work

class PaymentsLitigation(models.Model):
    litigation = models.ForeignKey(Litigation, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    amount = models.IntegerField()
    amount_paid = models.IntegerField(default=0)
    amount_pending = models.IntegerField()
    total_paid = models.IntegerField(default=0)

    def save(self, *args, **kwards):
        if not self.pk:
            self.amount_pending = self.amount
        self.amount_pending = self.amount_pending - self.amount_paid
        self.total_paid += self.amount_paid
        super().save(*args, **kwards)

    def __str__(self) -> str:
        return f"{self.name} - {self.litigation.name}"
    
class PaymentsLitigationDate(models.Model):
    payment = models.ForeignKey(PaymentsLitigation, on_delete=models.CASCADE)
    date_paid = models.DateField()
    amount = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.payment.name} - {self.amount} - {self.date_paid}"
    
class PaymentsNonLitigation(models.Model):
    non_litigation = models.ForeignKey(NonLitigation, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    amount = models.IntegerField()
    amount_paid = models.IntegerField(default=0)
    amount_pending = models.IntegerField()
    total_paid = models.IntegerField(default=0)

    def save(self, *args, **kwards):
        if not self.pk:
            self.amount_pending = self.amount
        self.amount_pending = self.amount_pending - self.amount_paid
        self.total_paid += self.amount_paid
        super().save(*args, **kwards)

    def __str__(self) -> str:
        return f"{self.name} - {self.non_litigation.name}"

class PaymentsNonLitigationDate(models.Model):
    payment = models.ForeignKey(PaymentsNonLitigation, on_delete=models.CASCADE)
    date_paid = models.DateField()
    amount = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.payment.name} - {self.amount} - {self.date_paid}"