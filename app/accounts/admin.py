from django.contrib import admin
from app.accounts import models


class LoanAccountAdmin(admin.ModelAdmin):
    fields = ['user', 'balance', 'principal', 'status', 'due_date']
    list_display = fields


class BankTypeAdmin(admin.ModelAdmin):
    fields = ['type']
    list_display = fields


class BankNameAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = fields


class BankAdmin(admin.ModelAdmin):
    fields = ['user', 'bank_name', 'bank_type', 'account_number']
    list_display = fields


admin.site.register(models.LoanAccount, LoanAccountAdmin)
admin.site.register(models.BankName, BankNameAdmin)
admin.site.register(models.BankType, BankTypeAdmin)
admin.site.register(models.Bank, BankAdmin)
