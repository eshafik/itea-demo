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

from balance.forms import DateForm
from balance.models.expense_transaction import ExpenseTransaction
from applibs.permission import FinancePermissionMixin
from members.models import User


class ExpTransactionListView(LoginRequiredMixin, ListView):
    """
    Show all Expense Transaction list
    """
    model = ExpenseTransaction
    template_name = 'balance/list_exp_transaction.html'
    context_object_name = 'transactions'

    def get_queryset(self, *args, **kwargs):
        query_dict = {
            "current": ExpenseTransaction.objects.get_current_month_exp_transaction(),
        }
        object_list = ExpenseTransaction.objects.filter(status=True)

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


class ExpTransactionCreate(FinancePermissionMixin, CreateView):
    """
        Create Transaction
    """
    template_name = 'balance/create_exp_transaction.html'
    model = ExpenseTransaction
    fields = ("expense_by", "amount", "expense_date", "expense_type", "expense_details")

    def get_success_url(self):
        return reverse_lazy('balance:exp-transaction-details', kwargs={'pk': self.object.id})


class ExpTransactionUpdateView(FinancePermissionMixin, UpdateView):
    """
    Update Transaction
    """
    model = ExpenseTransaction
    template_name = 'balance/update.html'
    context_object_name = 'transaction'
    fields = ("expense_by", "amount", "expense_date", "expense_type", "expense_details")

    def get_success_url(self):
        return reverse_lazy('balance:exp-transaction-details', kwargs={'pk': self.object.id})


class ExpTransactionDetailView(LoginRequiredMixin, DetailView):
    """
    Transaction Details
    """
    model = ExpenseTransaction
    template_name = 'balance/details_exp_transaction.html'
    context_object_name = 'transaction'


class ExpTransactionDeleteView(FinancePermissionMixin, DeleteView):
    """
    Delete transaction
    """
    model = ExpenseTransaction
    template_name = 'balance/delete_exp_transaction.html'
    context_object_name = 'transaction'
    success_url = reverse_lazy('balance:exp-transaction-list')

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


class ExpTransactionQuery(LoginRequiredMixin, View):
    """
        Query expense transaction by datepicker
    """

    def get(self, request, *args, **kwargs):
        return render(request, 'datepicker/datepicker.html', {"form": DateForm(), "name": "Expense"})

    def post(self, request, *args, **kwargs):
        data = self.request.POST.dict()
        start_date = timezone.datetime.strptime(data.get("start_date"), "%m/%d/%Y %H:%M %p").date()
        end_date = timezone.datetime.strptime(data.get("end_date"), "%m/%d/%Y %H:%M %p").date()
        user_id = data.get('user')
        user = None
        if user_id:
            user = get_object_or_404(User, id=int(user_id))
        queryset = ExpenseTransaction.objects.get_date_query_exp_transaction(start_date=start_date, end_date=end_date,
                                                                             user=user)
        total = queryset.aggregate(Sum('amount')).get('amount__sum')

        return render(request, 'balance/list_exp_transaction.html', {"transactions": queryset, "total": total})
