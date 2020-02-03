from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
# specific to this view
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from applibs.permission import FinancePermissionMixin
from balance.forms import DateForm
from balance.models.income_transaction import IncomeTransaction
from members.models import User


class IncmTransactionListView(LoginRequiredMixin, ListView):
    """
    Show all income Transaction list
    """
    model = IncomeTransaction
    template_name = 'balance/list_incm_transaction.html'
    context_object_name = 'transactions'

    def get_queryset(self, *args, **kwargs):
        query_dict = {
            "current": IncomeTransaction.objects.get_current_month_incm_transaction(),
        }
        object_list = IncomeTransaction.objects.filter(status=True)
        if self.request.GET.get('p'):
            object_list = query_dict.get(self.request.GET.get('p'))

        paginator = Paginator(object_list, 20)  # maping total object with this paginator
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


class IncmTransactionCreate(FinancePermissionMixin, CreateView):
    """
        Create Income Transaction
    """
    template_name = 'balance/create_incm_transaction.html'
    model = IncomeTransaction
    fields = ("received_by", "amount", "received_date", "received_details")

    def get_success_url(self):
        return reverse_lazy('balance:incm-transaction-details', kwargs={'pk': self.object.id})


class IncmTransactionUpdateView(FinancePermissionMixin, UpdateView):
    """
    Update Income Transaction
    """
    model = IncomeTransaction
    template_name = 'balance/update.html'
    context_object_name = 'transaction'
    fields = ("received_by", "amount", "received_date", "received_details")

    def get_success_url(self):
        return reverse_lazy('balance:incm-transaction-details', kwargs={'pk': self.object.id})


class IncmTransactionDetailView(LoginRequiredMixin, DetailView):
    """
    Transaction Details
    """
    model = IncomeTransaction
    template_name = 'balance/details_incm_transaction.html'
    context_object_name = 'transaction'


class IncmTransactionDeleteView(FinancePermissionMixin, DeleteView):
    """
    Delete transaction
    """
    model = IncomeTransaction
    template_name = 'balance/delete_incm_transaction.html'
    context_object_name = 'transaction'
    success_url = reverse_lazy('balance:incm-transaction-list')

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


class IncmTransactionQuery(LoginRequiredMixin, View):
    """
        Query income transaction by datepicker
    """

    def get(self, request, *args, **kwargs):
        return render(request, 'datepicker/datepicker.html', {"form": DateForm(), "name": "Income"})

    def post(self, request, *args, **kwargs):
        data = self.request.POST.dict()
        start_date = timezone.datetime.strptime(data.get("start_date"), "%m/%d/%Y %H:%M %p").date()
        end_date = timezone.datetime.strptime(data.get("end_date"), "%m/%d/%Y %H:%M %p").date()
        user_id = data.get('user')
        user = None
        if user_id:
            user = get_object_or_404(User, id=int(user_id))
        queryset = IncomeTransaction.objects.get_date_query_incm_transaction(start_date=start_date, end_date=end_date,
                                                                             user=user)
        total = queryset.aggregate(Sum('amount')).get('amount__sum')

        return render(request, 'balance/list_incm_transaction.html', {"transactions": queryset, "total": total})
