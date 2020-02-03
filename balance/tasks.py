from celery import shared_task

from django.core.mail import send_mail
from django.db.models import Sum

from balance.models import Transaction
from members.models import User


@shared_task
def mail_payment_info(user_id, amount):
    """
        Task to send an e-mail notification when an order is successfully created
        """
    user = User.objects.get(id=user_id)
    total_balance = Transaction.objects.filter(user=user, status=True).aggregate(Sum('amount')).get("amount__sum")
    subject = 'Transaction Report on ITEA'
    message = """Dear {0},\n\nYour  payment (BDT - {1}) has been successfully added to your account.
                Now your total  balance is {2} Tk""".format(user.name, amount, total_balance)

    mail_sent = send_mail(subject, message,
                          'iiteabd@gmail.com',
                          [user.email])
    return mail_sent
