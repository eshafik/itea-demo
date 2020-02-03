from django.urls import path
from django.views.generic import TemplateView

from balance.views.transaction import TransactionListView, TransactionCreate, TransactionDetailView, \
    TransactionUpdateView, TransactionDeleteView, TransactionQuery, DueMonthQuery, MyDueMonths, DownloadCSV
from balance.views.exp_transaction import ExpTransactionListView, ExpTransactionCreate, ExpTransactionDetailView, \
    ExpTransactionUpdateView, ExpTransactionDeleteView, ExpTransactionQuery
from balance.views.incm_transaction import IncmTransactionListView, IncmTransactionCreate, IncmTransactionDetailView, \
    IncmTransactionUpdateView, IncmTransactionDeleteView, IncmTransactionQuery
from balance.views.org_views import OrganizationalView

app_name = "balance"

urlpatterns = [
    path('dashboard/', TemplateView.as_view(template_name="balance/balance_dashboard.html"), name='balance-dashboard'),
    path('transaction/list/', TransactionListView.as_view(), name='transaction-list'),
    path('transaction/create/', TransactionCreate.as_view(), name='transaction-create'),
    path('transaction/<int:pk>/', TransactionDetailView.as_view(), name='transaction-details'),
    path('transaction/<int:pk>/update/', TransactionUpdateView.as_view(), name='transaction-edit'),
    path('transaction/<int:pk>/delete/', TransactionDeleteView.as_view(), name='transaction-delete'),
    path('transaction/query/', TransactionQuery.as_view(), name='transaction-query'),
    path('transaction/query-due/', DueMonthQuery.as_view(), name='transaction-query-due'),
    path('transaction/my-due/', MyDueMonths.as_view(), name='transaction-my-due'),
    path('transaction/download/', DownloadCSV.as_view(), name='transaction-download'),
]
EXPENSE_URL = [
    path('exp-transaction/list/', ExpTransactionListView.as_view(), name='exp-transaction-list'),
    path('exp-transaction/create/', ExpTransactionCreate.as_view(), name='exp-transaction-create'),
    path('exp-transaction/<int:pk>/', ExpTransactionDetailView.as_view(), name='exp-transaction-details'),
    path('exp-transaction/<int:pk>/update/', ExpTransactionUpdateView.as_view(), name='exp-transaction-edit'),
    path('exp-transaction/<int:pk>/delete/', ExpTransactionDeleteView.as_view(), name='exp-transaction-delete'),
    path('exp-transaction/query/', ExpTransactionQuery.as_view(), name='exp-transaction-query'),
]

INCOME_URL = [
    path('incm-transaction/list/', IncmTransactionListView.as_view(), name='incm-transaction-list'),
    path('incm-transaction/create/', IncmTransactionCreate.as_view(), name='incm-transaction-create'),
    path('incm-transaction/<int:pk>/', IncmTransactionDetailView.as_view(), name='incm-transaction-details'),
    path('incm-transaction/<int:pk>/update/', IncmTransactionUpdateView.as_view(), name='incm-transaction-edit'),
    path('incm-transaction/<int:pk>/delete/', IncmTransactionDeleteView.as_view(), name='incm-transaction-delete'),
    path('incm-transaction/query/', IncmTransactionQuery.as_view(), name='incm-transaction-query'),
]
OTHERS_URL = [
    path('organization/', OrganizationalView.as_view(), name='organization'),
]

urlpatterns += EXPENSE_URL + INCOME_URL + OTHERS_URL
