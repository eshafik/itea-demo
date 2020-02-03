from django.contrib import admin

from balance.models import Transaction, IncomeTransaction, ExpenseTransaction


admin.site.register(Transaction)
admin.site.register(IncomeTransaction)
admin.site.register(ExpenseTransaction)
