import uuid

from django.db import models

from members.models import User
from balance.models.income_queryset import IncmTransactionQuerySet


class IncmTransactionManager(models.Manager):
    """
        Transaction manager for filtering data
    """

    def get_queryset(self):
        """
            Using for TransactionQuerySet methods
        """
        return IncmTransactionQuerySet(self.model, using=self._db)

    def get_all_incm_transaction(self):
        """
            Return all transaction of all users
        """
        return self.get_queryset().get_all_incm_transaction()

    def get_current_month_incm_transaction(self):
        """
            Return all current month transaction of all users
        """
        return self.get_queryset().get_current_month_incm_transaction()

    def get_date_query_incm_transaction(self, start_date, end_date, user=None):
        """
            Return queryset
        """
        return self.get_queryset().get_date_query_incm_transaction(start_date=start_date, end_date=end_date, user=user)


class IncomeTransaction(models.Model):
    """
        Organization's Income Transaction Model
    """
    income_guid = models.CharField(max_length=45, default=uuid.uuid4, editable=False)
    received_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')
    amount = models.DecimalField(default=0, max_digits=12, decimal_places=4)
    received_date = models.DateField(blank=True, null=True, db_index=True, help_text='YYYY-MM-DD')
    received_details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    objects = IncmTransactionManager()

    def __str__(self):
        return str(self.amount)

    class Meta:
        ordering = ('-received_date', )
