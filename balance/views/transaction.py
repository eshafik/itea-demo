import csv
from wsgiref.util import FileWrapper

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
# specific to this view
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from balance.forms import DateForm, TransactionForm
from members.models import User
from balance.models.transaction import Transaction
from applibs.permission import FinancePermissionMixin
from balance.tasks import mail_payment_info


class TransactionListView(LoginRequiredMixin, ListView):
    """
    Show all Transaction list
    """
    model = Transaction
    template_name = 'balance/list_transaction.html'
    context_object_name = 'transactions'

    def get_queryset(self, *args, **kwargs):
        query_dict = {
            "me_current": Transaction.objects.get_my_current_transaction(user=self.request.user),
            "me_all": Transaction.objects.get_my_all_transaction(user=self.request.user),
            "all_current": Transaction.objects.get_current_month_transaction(),
        }
        object_list = Transaction.objects.filter(status=True)
        if self.request.GET.get('p'):
            object_list = query_dict.get(self.request.GET.get('p'))

        paginator = Paginator(object_list, 50)  # maping total object with this paginator
        page = self.request.GET.get('page')  # getting current page number
        try:
            transactions = paginator.page(page)
        except PageNotAnInteger:
            # if page is not an interger deliver first page
            transactions = paginator.page(1)
        except EmptyPage:
            # if page is out of range deliver last page
            transactions = paginator.page(paginator.num_pages)
        return transactions


class TransactionCreate(FinancePermissionMixin, CreateView):
    """
        Create Transaction
    """
    template_name = 'balance/create_transaction.html'
    model = Transaction
    # fields = ("user", "amount", "transaction_date", "transaction_type", "transaction_details")
    form_class = TransactionForm

    def get_success_url(self):
        return reverse_lazy('balance:transaction-details', kwargs={'pk': self.object.id})


class TransactionUpdateView(FinancePermissionMixin, UpdateView):
    """
    Update Transaction
    """
    model = Transaction
    template_name = 'balance/update.html'
    context_object_name = 'transaction'
    fields = ('amount', 'transaction_date', 'transaction_type', 'transaction_details')

    def get_success_url(self):
        return reverse_lazy('balance:transaction-details', kwargs={'pk': self.object.id})


class TransactionDetailView(LoginRequiredMixin, DetailView):
    """
    Transaction Details
    """
    model = Transaction
    template_name = 'balance/details_transaction.html'
    context_object_name = 'transaction'


class TransactionDeleteView(FinancePermissionMixin, DeleteView):
    """
    Delete transaction
    """
    model = Transaction
    template_name = 'balance/delete_transaction.html'
    context_object_name = 'transaction'
    success_url = reverse_lazy('balance:transaction-list')

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.status = False
        self.object.save()
        return HttpResponseRedirect(success_url)


class TransactionQuery(LoginRequiredMixin, View):
    """
        Transaction query by datepicker
    """

    def get(self, request, *args, **kwargs):
        return render(request, 'datepicker/datepicker.html', {"form": DateForm(), "name": "Transaction"})

    def post(self, request, *args, **kwargs):
        data = self.request.POST.dict()
        start_date = timezone.datetime.strptime(data.get("start_date"), "%m/%d/%Y %H:%M %p").date()
        end_date = timezone.datetime.strptime(data.get("end_date"), "%m/%d/%Y %H:%M %p").date()
        user_id = data.get('user')
        user = None
        if user_id:
            user = get_object_or_404(User, id=int(user_id))
        queryset = Transaction.objects.get_date_query_transaction(start_date=start_date, end_date=end_date, user=user)
        total = queryset.aggregate(Sum('amount')).get('amount__sum')

        # for csv file generate
        if "Finance" in request.user.groups.values_list('name', flat=True):
            with open('media/file/names.csv', 'w', newline='') as csvfile:
                fieldnames = ['user__name', 'amount', 'transaction_guid', 'transaction_date', 'transaction_type',
                              'transaction_details', 'created_at']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                dict_list = queryset.values('user__name', 'amount', 'transaction_guid', 'transaction_date',
                                            'transaction_type', 'transaction_details', 'created_at')
                for row in dict_list:
                    writer.writerow(row)
                writer.writerow({"user__name": "Total", "amount": total})

        return render(request, 'balance/list_transaction.html',
                      {"transactions": queryset, "download": True, 'total': total})


class DueMonthQuery(LoginRequiredMixin, View):
    """
        Query due months by date picker
    """

    def get(self, request, *args, **kwargs):
        return render(request, 'datepicker/datepicker.html', {"form": DateForm(), "name": "Due Month Query"})

    def post(self, request, *args, **kwargs):
        data = self.request.POST.dict()
        start_date = timezone.datetime.strptime(data.get("start_date"), "%m/%d/%Y %H:%M %p").date()
        end_date = timezone.datetime.strptime(data.get("end_date"), "%m/%d/%Y %H:%M %p").date()
        user_id = data.get('user')
        user = None
        transactions = []
        if user_id:
            user = get_object_or_404(User, id=int(user_id))
            due_months = Transaction.objects.get_due_transaction_by_date(start_date, end_date, user)
            due_months = 0 if due_months < 0 else due_months
            transactions.append({"member": user.name, "due_months": due_months})
            return render(request, 'balance/due_transaction.html', {"transactions": transactions})
        for member in User.objects.get_all_members():
            due_months = Transaction.objects.get_due_transaction_by_date(start_date, end_date, user=member)
            due_months = 0 if due_months < 0 else due_months
            transactions.append({"member": member.name, "due_months": due_months})

        return render(request, 'balance/due_transaction.html', {"transactions": transactions})


class MyDueMonths(LoginRequiredMixin, TemplateView):
    """
        For individual due months query
    """
    template_name = "balance/due_transaction.html"

    def get_context_data(self, **kwargs):
        context = super(MyDueMonths, self).get_context_data(**kwargs)
        due_months = Transaction.objects.get_my_due_transaction(user=self.request.user)
        context['transactions'] = [{"member": self.request.user.name,
                                    "due_months": due_months}, ]
        return context


class DownloadCSV(FinancePermissionMixin, View):
    """
        Download CSV file after querying by date of transaction
    """

    def get(self, request, *args, **kwargs):
        file_name = settings.MEDIA_ROOT + '/file/' + 'names.csv'
        download_name = "transaction-{}.csv".format(timezone.now().date())
        wrapper = FileWrapper(open(file_name))
        file = FileWrapper
        response = HttpResponse(wrapper, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}'.format(download_name)
        return response


# @receiver(post_save, sender=Transaction)
# def send_email_after_adding_payment(sender, instance, created, **kwargs):
#     mail_payment_info.delay(user_id=instance.user.id, amount=instance.amount)
