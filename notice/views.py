from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
# specific to this view
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from notice.models import Notice
from applibs.permission import ExecutivePermissionMixin, OwnNoticePermissionMixin


class NoticeCreate(ExecutivePermissionMixin, CreateView):
    """
        Create Notice
    """
    template_name = 'notice/notice_create.html'
    model = Notice
    fields = ("notice_title", "notice_body")

    def get_success_url(self):
        return reverse_lazy('notice:notice-details', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        f = form.save(commit=False)
        f.author = self.request.user
        f.save()
        return super().form_valid(form)


class NoticeListView(LoginRequiredMixin, ListView):
    """
    Show all notice list
    """
    model = Notice
    template_name = 'notice/notice_list.html'
    context_object_name = 'notices'

    def get_queryset(self, *args, **kwargs):
        object_list = Notice.objects.filter(status=True)
        paginator = Paginator(object_list, 20)  # maping total object with this paginator
        page = self.request.GET.get('page')  # getting current page number
        try:
            notices = paginator.page(page)
        except PageNotAnInteger:
            # if page is not an interger deliver first page
            notices = paginator.page(1)
        except EmptyPage:
            # if page is out of range deliver last page
            notices = paginator.page(paginator.num_pages)
        return notices


class NoticeDetailView(LoginRequiredMixin, DetailView):
    """
    Details of Notice
    """
    model = Notice
    template_name = 'notice/notice_details.html'
    context_object_name = 'notice'


class NoticeUpdateView(OwnNoticePermissionMixin, UpdateView):
    """
    Update Notice
    """

    model = Notice
    template_name = 'notice/notice_update.html'
    context_object_name = 'user'
    fields = ('notice_title', 'notice_body',)

    def get_success_url(self):
        return reverse_lazy('notice:notice-details', kwargs={'pk': self.object.id})


class NoticeDeleteView(OwnNoticePermissionMixin, DeleteView):
    """
    Delete transaction
    """
    model = Notice
    template_name = 'notice/notice_delete.html'
    context_object_name = 'notice'
    success_url = reverse_lazy('notice:notice-list')

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


class NoticeBoard(LoginRequiredMixin, View):

    def get(self, request):
        try:
            notice = Notice.objects.filter(status=True).latest('id')
        except:
            notice = None
        return render(request, 'notice/notice_board.html', {'notice': notice})

