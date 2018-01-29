from django.contrib import admin

from .models import (
    AlgorithmLog,
    AlgorithmUtilisation,
    WorkerActivityLog,
    AlgorithmBalanceLog,
    PaymentLog,
    BalanceLog
)

class AlgorithmLogAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
    )

class AlgorithmUtilisationAdmin(admin.ModelAdmin):
    list_display = (
        'algorithm_id',
        'algorithm_name',
        'count',
    )

class WorkerActivityLogAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
    )

class AlgorithmBalanceLogAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
    )

class PaymentLogAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
    )

class BalanceLogAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
    )

admin.site.register(AlgorithmLog, AlgorithmLogAdmin)
admin.site.register(AlgorithmUtilisation, AlgorithmUtilisationAdmin)
admin.site.register(WorkerActivityLog, WorkerActivityLogAdmin)
admin.site.register(AlgorithmBalanceLog, AlgorithmBalanceLogAdmin)
admin.site.register(PaymentLog, PaymentLogAdmin)
admin.site.register(BalanceLog, BalanceLogAdmin)
