from django.db import models

from members.models import User


class Notice(models.Model):
    """
        Storing Notice Objects
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notice')
    notice_title = models.CharField(max_length=255)
    notice_body = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_date']
