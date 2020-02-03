from django.db import models
from django.utils import timezone


class ExpTransactionQuerySet(models.QuerySet):
    """
        QuerySet of Expense Transaction Model
    """

    def get_all_exp_transaction(self):
        """
            get all active expense transaction
        """
        return self.filter(status=True)

    def get_current_month_exp_transaction(self):
        """
            get all current months transaction
        """
        return self.filter(status=True, expense_date__year=timezone.now().year,
                           expense_date__month=timezone.now().month)

    def get_date_query_exp_transaction(self, start_date, end_date, user=None):
        """
            Query by date picker
        """
        if user:
            return self.filter(status=True, user=user, expense_date__range=[start_date, end_date])
        return self.filter(status=True, expense_date__range=[start_date, end_date])
