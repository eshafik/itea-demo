from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render
from django.views import View

from balance.models.transaction import Transaction
from balance.models.expense_transaction import ExpenseTransaction
from balance.models.income_transaction import IncomeTransaction


class OrganizationalView(LoginRequiredMixin, View):
    """
        For individual due months query
    """

    def get(self, request):
        monthly_amount_by_members = Transaction.objects.filter(status=True,
                                                               transaction_type='monthly'
                                                               ).aggregate(Sum('amount')
                                                                           ).get('amount__sum')
        additional_amount_by_members = Transaction.objects.filter(status=True,
                                                                  transaction_type='additional'
                                                                  ).aggregate(Sum('amount')
                                                                              ).get('amount__sum')
        others_amount_by_members = Transaction.objects.filter(status=True,
                                                              transaction_type='others'
                                                              ).aggregate(Sum('amount')
                                                                          ).get('amount__sum')
        total_expense = ExpenseTransaction.objects.filter(status=True
                                                          ).aggregate(Sum('amount')
                                                                      ).get('amount__sum')
        total_income = IncomeTransaction.objects.filter(status=True
                                                        ).aggregate(Sum('amount')
                                                                    ).get('amount__sum')

        context = {
            "monthy": monthly_amount_by_members,
            "additional": additional_amount_by_members,
            "others": others_amount_by_members,
            "total_expense": total_expense,
            "total_income": total_income
        }
        return render(request, 'balance/organization.html', context)
