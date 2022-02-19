from django.contrib import admin
from app.accounts import models

# Register your models here.


class LoanAccountAdmin(admin.ModelAdmin):
    fields = ['user', 'balance', 'status', 'due_date']


admin.site.register(models.LoanAccount, LoanAccountAdmin)
