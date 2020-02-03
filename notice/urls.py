from django.urls import path

from notice.views import NoticeCreate, NoticeListView, NoticeDetailView, \
    NoticeUpdateView, NoticeDeleteView, NoticeBoard

app_name = "notice"

urlpatterns = [
    path('list/', NoticeListView.as_view(), name='notice-list'),
    path('create/', NoticeCreate.as_view(), name='notice-create'),
    path('<int:pk>/', NoticeDetailView.as_view(), name='notice-details'),
    path('<int:pk>/update/', NoticeUpdateView.as_view(), name='notice-edit'),
    path('<int:pk>/delete/', NoticeDeleteView.as_view(), name='notice-delete'),
    path('board/', NoticeBoard.as_view(), name='notice-board'),
]
