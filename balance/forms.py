from django import forms

from members.models import User
from balance.models.transaction import Transaction
from .widgets import BootstrapDateTimePickerInput


class DateForm(forms.Form):
    start_date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=BootstrapDateTimePickerInput()
    )
    end_date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=BootstrapDateTimePickerInput()
    )
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True, is_superuser=False), required=False,
                                  empty_label="All Members")


class TransactionForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True, is_superuser=False),
                                  empty_label='Select Member')

    class Meta:
        model = Transaction
        fields = ("user", "amount", "transaction_date", "transaction_type", "transaction_details")
