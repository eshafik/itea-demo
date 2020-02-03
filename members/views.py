from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic, View
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
# specific to this view
from django.views.generic import ListView, DetailView, UpdateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from members.models import User, Profile
from members.forms import SignUpForm, ActivateForm
from applibs.permission import OwnUserPermissionMixin, OwnProfilePermissionMixin, FinancePermissionMixin


class SignUp(generic.CreateView):
    """
        Member  Registration
    """
    form_class = SignUpForm
    success_url = reverse_lazy('member:login')
    template_name = 'signup/signup.html'
    model = get_user_model()


class UserListView(LoginRequiredMixin, ListView):
    """
    Show all member list
    """
    model = User
    template_name = 'members/list.html'
    context_object_name = 'users'

    def get_queryset(self, *args, **kwargs):
        object_list = User.objects.filter(is_active=True, is_superuser=False)
        paginator = Paginator(object_list, 20) # maping total object with this paginator
        page = self.request.GET.get('page')  # getting current page number
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            # if page is not an interger deliver first page
            users = paginator.page(1)
        except EmptyPage:
            # if page is out of range deliver last page
            users = paginator.page(paginator.num_pages)
        return users


class UserDetailView(LoginRequiredMixin, DetailView):
    """
    Details of user profile
    """
    model = User
    template_name = 'members/profile.html'
    context_object_name = 'user'


class UserBasicUpdateView(OwnUserPermissionMixin, UpdateView):
    """
    Update User Basic Info
    """

    model = User
    template_name = 'members/update.html'
    context_object_name = 'user'
    fields = ('name', 'designation',)

    def get_success_url(self):
        return reverse_lazy('member:member-details', kwargs={'pk': self.object.id})


class UserProfileUpdateView(OwnProfilePermissionMixin, UpdateView):
    """
    Update User profile info
    """

    model = Profile
    template_name = 'members/update.html'
    context_object_name = 'user'
    fields = ("photo", "phone", "email", "professional_details", "present_address", "permanent_address")

    def get_success_url(self):
        return reverse_lazy('member:member-details', kwargs={'pk': self.object.user.id})


class ActivateMemberRequest(FinancePermissionMixin, View):
    """
        Activate the user after sending membership request
    """
    def get(self, request, *args, **kwargs):
        return render(request, 'members/activate_member.html', {"form": ActivateForm()})

    def post(self, request, *args, **kwargs):
        data = self.request.POST.dict()
        user_id = data.get("member")
        User.objects.filter(id=user_id).update(is_active=True)
        return redirect(reverse('member:member-list'))


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
        Creating Profile during registering  new member
    """
    if created:
        Profile.objects.create(user=instance)
