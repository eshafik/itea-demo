import uuid

from django.db import models

from balance.models.transaction_queryset import TransactionQuerySet
from members.models import User


class TransactionManager(models.Manager):
    """
        Transaction manager for filtering data
    """

    def get_queryset(self):
        """
            Using for TransactionQuerySet methods
        """
        return TransactionQuerySet(self.model, using=self._db)

    def get_all_transaction(self):
        """
            Return all transaction of all users
        """
        return self.get_queryset().get_all_transaction()

    def get_current_month_transaction(self):
        """
            Return all current month transaction of all users
        """
        return self.get_queryset().get_current_month_transaction()

    def get_my_all_transaction(self, user):
        """
            Return all my transaction
        """
        return self.get_queryset().get_my_all_transaction(user=user)

    def get_my_current_transaction(self, user):
        """
            Return my current month transaction
        """
        return self.get_queryset().get_my_current_transaction(user=user)

    def get_date_query_transaction(self, start_date, end_date, user=None):
        """
            Return queryset
        """
        return self.get_queryset().get_date_query_transaction(start_date=start_date, end_date=end_date, user=user)

    def get_my_due_transaction(self, user):
        """
        Return my due transaction
        """
        return self.get_queryset().get_my_due_transaction(user)

    def get_due_transaction_by_date(self, start_date, end_date, user):
        return self.get_queryset().get_due_transaction_by_date(start_date, end_date, user)


class Transaction(models.Model):
    """
        User Transaction for submitting money to the organization
    """
    TRANSACTION_TYPE = (
        ('monthly', 'Monthly'),
        ('additional', 'Additional'),
        ('others', 'Others'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_guid = models.CharField(max_length=45, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(default=0, max_digits=12, decimal_places=4)
    transaction_date = models.DateField(blank=True, null=True, db_index=True, help_text='YYYY-MM-DD')
    transaction_type = models.CharField(max_length=45, choices=TRANSACTION_TYPE)
    transaction_details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    objects = TransactionManager()

    def __str__(self):
        return self.user.name

    class Meta:
        ordering = ('-transaction_date', )
