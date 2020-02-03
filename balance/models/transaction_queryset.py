from django.db import models
from django.utils import timezone


class TransactionQuerySet(models.QuerySet):
    """
        QuerySet of User Model
    """

    def get_all_transaction(self):
        """
            get all active transaction
        """
        return self.filter(status=True)

    def get_current_month_transaction(self):
        """
            get all current months transaction
        """
        return self.filter(status=True, transaction_date__year=timezone.now().year,
                           transaction_date__month=timezone.now().month)

    def get_my_all_transaction(self, user):
        """
            get all my transactions
        """
        return self.filter(user=user, status=True)

    def get_my_current_transaction(self, user):
        """
            get my current month transaction
        """
        return self.filter(user=user, status=True, transaction_date__year=timezone.now().year,
                           transaction_date__month=timezone.now().month)

    def get_date_query_transaction(self, start_date, end_date, user=None):
        """
            Query by date picker
        """
        if user:
            return self.filter(status=True, user=user, transaction_date__range=[start_date, end_date])
        return self.filter(status=True, transaction_date__range=[start_date, end_date])

    def get_my_due_transaction(self, user):
        """
            Get Due month transaction
        """
        start_date = timezone.datetime(2015, 1, 1).date()
        current_date = timezone.now().date()
        paid_month_number = self.filter(status=True, user=user,
                                        transaction_date__range=[start_date, current_date],
                                        transaction_type="monthly").count()
        total_months = abs(start_date.month - current_date.month + 12*(start_date.year - current_date.year)) + 1

        return total_months - paid_month_number

    def get_due_transaction_by_date(self, start_date, end_date, user):
        paid_month_number = self.filter(status=True, user=user,
                                        transaction_date__range=[start_date, end_date],
                                        transaction_type="monthly").count()

        total_months = abs(start_date.month - end_date.month + 12 * (start_date.year - end_date.year)) + 1
        return total_months - paid_month_number
