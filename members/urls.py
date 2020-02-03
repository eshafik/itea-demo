from django.urls import path
from django.contrib.auth import views as auth_views

from members.views import SignUp, UserListView, UserDetailView, UserBasicUpdateView, UserProfileUpdateView, \
    ActivateMemberRequest

app_name = "member"

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('list/', UserListView.as_view(), name='member-list'),
    path('details/<int:pk>/', UserDetailView.as_view(), name='member-details'),
    path('basic/<int:pk>/update', UserBasicUpdateView.as_view(), name='basic-update'),
    path('profile/<int:pk>/update', UserProfileUpdateView.as_view(), name='profile-update'),
    path('activate/', ActivateMemberRequest.as_view(), name='activate'),
]
