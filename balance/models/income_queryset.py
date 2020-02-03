from django.db import models
from django.utils import timezone


class IncmTransactionQuerySet(models.QuerySet):
    """
        QuerySet of Income Transaction Model
    """

    def get_all_incm_transaction(self):
        """
            get all active income transaction
        """
        return self.filter(status=True)

    def get_current_month_incm_transaction(self):
        """
            get all current months transaction
        """
        return self.filter(status=True, received_date__year=timezone.now().year,
                           received_date__month=timezone.now().month)

    def get_date_query_incm_transaction(self, start_date, end_date, user=None):
        """
            Query by date picker
        """
        if user:
            return self.filter(status=True, user=user, received_date__range=[start_date, end_date])
        return self.filter(status=True, received_date__range=[start_date, end_date])
