from django.contrib import admin
from .models import Worker, Wallet

class WorkerAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'recent_activity'
    )

class WalletAdmin(admin.ModelAdmin):
    list_display = (
        'hidden_address',
        'balance',
        'net_earnings',
        'earning_rate'
    )

admin.site.register(Worker, WorkerAdmin)
admin.site.register(Wallet, WalletAdmin)