from django.db import models
from accounts.models import User
import os

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

class NoticeSent(models.Model):
    acknowledgement_choices = [
        ("Received", "Received"),
        ("Refused", "Refused"),
        ("Address not Found", "Address not Found"),
        ("Addressee Left", "Addressee Left"),
        ("Door Locked", "Door Locked"),
        ("Informed to sender", "Informed to sender"),
        ("Not claimed", "Not claimed"),
        ("Addressee cannot be located", "Addressee cannot be located"),
        ("Lost in transit", "Lost in transit"),
        ("Insufficient Address", "Insufficient Address"),
        ("No such person", "No such person"),
        ("Deceased", "Deceased"),
    ]
    name = models.CharField(max_length=1000)
    completion_date = models.DateField()
    acknowledgement = models.CharField(max_length=100, choices=acknowledgement_choices, null=True)
    acknowledgement_received_date = models.DateField(null=True)
    tracking_number = models.CharField(max_length=500, null=True)
    notice_document = models.FileField(upload_to=f"notice_sent/", null=True)
    sent_date = models.DateField(null=True)
    reply_notice_given = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def notice_type(self) -> str:
        return "Sent"
    
    def notice_file_name(self):
        return os.path.basename(self.notice_document.name)
    
    def __str__(self):
        return self.name

class NoticeSentRejoinder(models.Model):
    notice_sent = models.ForeignKey(NoticeSent, on_delete=models.CASCADE)
    acknowledgement_choices = [
        ("Received", "Received"),
        ("Refused", "Refused"),
        ("Address not Found", "Address not Found"),
        ("Addressee Left", "Addressee Left"),
        ("Door Locked", "Door Locked"),
        ("Informed to sender", "Informed to sender"),
        ("Not claimed", "Not claimed"),
        ("Addressee cannot be located", "Addressee cannot be located"),
        ("Lost in transit", "Lost in transit"),
        ("Insufficient Address", "Insufficient Address"),
        ("No such person", "No such person"),
        ("Deceased", "Deceased"),
    ]
    acknowledgement = models.CharField(max_length=100, choices=acknowledgement_choices, null=True)
    acknowledgement_received_date = models.DateField(null=True)
    notice_document = models.FileField(upload_to=f"notice_sent/", null=True)
    sent_date = models.DateField()
    reply_notice_given = models.BooleanField(default=False)

class NoticeSentReply(models.Model):
    notice_sent = models.ForeignKey(NoticeSent, on_delete=models.CASCADE)
    reply_notice_document = models.FileField(upload_to=f"notice_sent/", null=True)
    sent_date = models.DateField()

class NoticeReceived(models.Model):
    type_choices = [
        ("MC", "MC"),
        ("OS", "OS"),
        ("NI", "NI"),
        ("Consumer", "Consumer"),
    ]
    name = models.CharField(max_length=1000)
    type = models.CharField(max_length=50, choices=type_choices)
    received_date_client = models.DateField()
    received_date_office = models.DateField()
    received_employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'groups__name': 'Employees'})
    received_employee_name = models.CharField(max_length=255, blank=True, null=True)
    completion_date = models.DateField()
    reply_notice_sent = models.BooleanField(default=False)
    reply_notice_sent_date = models.DateField(null=True)
    reply_notice_document = models.FileField(upload_to=f"notice_received/", null=True)
    ni_deadline = models.DateField(null=True) # TODO: Add way to send reminder for this.
    completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
    
    def reply_notice_file_name(self):
        return os.path.basename(self.reply_notice_document.name)
    
    def notice_type(self) -> str:
        return "Recieved"
    
    def save(self, *args, **kwargs):
        if self.received_employee:
            self.received_employee_name = f"{self.received_employee.first_name} {self.received_employee.last_name}"
        super().save(*args, **kwargs)
    
class NoticeReceivedRejoinder(models.Model):
    notice_received = models.ForeignKey(NoticeReceived, on_delete=models.CASCADE)
    acknowledgement_choices = [
        ("Received", "Received"),
        ("Refused", "Refused"),
        ("Address not Found", "Address not Found"),
        ("Addressee Left", "Addressee Left"),
        ("Door Locked", "Door Locked"),
        ("Informed to sender", "Informed to sender"),
        ("Not claimed", "Not claimed"),
        ("Addressee cannot be located", "Addressee cannot be located"),
        ("Lost in transit", "Lost in transit"),
        ("Insufficient Address", "Insufficient Address"),
        ("No such person", "No such person"),
        ("Deceased", "Deceased"),
    ]
    acknowledgement = models.CharField(max_length=100, choices=acknowledgement_choices, null=True)
    acknowledgement_received_date = models.DateField(null=True)
    notice_document = models.FileField(upload_to=f"notice_received/", null=True)
    sent_date = models.DateField()
    reply_notice_given = models.BooleanField(default=False)

