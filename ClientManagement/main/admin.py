from django.contrib import admin
from .models import Litigation, NonLitigation, WorkLigitation, WorkNonLitigation, PaymentsLitigation, PaymentsNonLitigation, PaymentsLitigationDate, PaymentsNonLitigationDate, NoticeSent, NoticeSentRejoinder, NoticeSentReply, NoticeReceived, NoticeReceivedRejoinder


# Register your models here.

admin.site.register(Litigation)
admin.site.register(WorkLigitation)
admin.site.register(PaymentsLitigation)
admin.site.register(PaymentsLitigationDate)
admin.site.register(NonLitigation)
admin.site.register(WorkNonLitigation)
admin.site.register(PaymentsNonLitigation)
admin.site.register(PaymentsNonLitigationDate)
admin.site.register(NoticeSent)
admin.site.register(NoticeSentRejoinder)
admin.site.register(NoticeSentReply)
admin.site.register(NoticeReceived)
admin.site.register(NoticeReceivedRejoinder)

