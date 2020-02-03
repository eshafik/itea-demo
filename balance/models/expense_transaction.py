import uuid

from django.db import models

from members.models import User
from balance.models.expense_queryset import ExpTransactionQuerySet


class ExpTransactionManager(models.Manager):
    """
        Transaction manager for filtering data
    """

    def get_queryset(self):
        """
            Using for TransactionQuerySet methods
        """
        return ExpTransactionQuerySet(self.model, using=self._db)

    def get_all_exp_transaction(self):
        """
            Return all transaction of all users
        """
        return self.get_queryset().get_all_exp_transaction()

    def get_current_month_exp_transaction(self):
        """
            Return all current month transaction of all users
        """
        return self.get_queryset().get_current_month_exp_transaction()

    def get_date_query_exp_transaction(self, start_date, end_date, user=None):
        """
            Return queryset
        """
        return self.get_queryset().get_date_query_exp_transaction(start_date=start_date, end_date=end_date, user=user)


class ExpenseTransaction(models.Model):
    """
        Organization's Expense Transaction Model
    """
    EXPENSE_TYPE = (
        ('invest', 'Invest'),
        ('non_invest', 'Non_Invest'),
    )
    expense_guid = models.CharField(max_length=45, default=uuid.uuid4, editable=False)
    expense_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(default=0, max_digits=12, decimal_places=4)
    expense_date = models.DateField(blank=True, null=True, db_index=True, help_text='YYYY-MM-DD')
    expense_type = models.CharField(max_length=45, choices=EXPENSE_TYPE)
    expense_details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    objects = ExpTransactionManager()

    def __str__(self):
        return str(self.amount)

    class Meta:
        ordering = ('-expense_date',)
