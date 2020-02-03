from django.core.exceptions import PermissionDenied


class ViewPermissionsMixin(object):
    """Base class for all custom permission mixins to inherit from"""
    def has_permissions(self):
        return True

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise PermissionDenied
        return super(ViewPermissionsMixin, self).dispatch(
            request, *args, **kwargs)


class FinancePermissionMixin(ViewPermissionsMixin):
    """
        Check permission for Finance
    """

    def has_permissions(self):
        return self.request.user.groups.filter(name="Finance").exists()


class ExecutivePermissionMixin(ViewPermissionsMixin):
    """
        Check permission for executive member
    """

    def has_permissions(self):
        return self.request.user.groups.filter(name="Executive").exists()


class OwnProfilePermissionMixin(ViewPermissionsMixin):
    """
        Check permission for own profile
    """

    def has_permissions(self):
        return self.request.user.id == self.get_object().user.id


class OwnUserPermissionMixin(ViewPermissionsMixin):
    """
        Check permission for own User object
    """
    def has_permissions(self):
        return self.request.user.id == self.get_object().id


class OwnNoticePermissionMixin(ViewPermissionsMixin):
    """
        Check permission own notice
    """

    def has_permissions(self):
        return self.request.user.id == self.get_object().author.id
