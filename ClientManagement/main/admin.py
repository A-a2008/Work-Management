from django.contrib import admin
from .models import Litigation, NonLitigation, WorkLigitation, WorkNonLitigation

# Register your models here.

admin.site.register(Litigation)
admin.site.register(WorkLigitation)
admin.site.register(NonLitigation)
admin.site.register(WorkNonLitigation)
