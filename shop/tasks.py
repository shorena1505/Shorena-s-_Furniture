from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Order
import time

@shared_task
def send_order_confirmation_email(order_id):
    order = Order.objects.get(id=order_id)
    subject = f"Order #{order.order_number} confirmed"
    message = f"Dear {order.user.get_full_name()},\n\nYour order has been received.\nTotal: {order.total_amount} GEL."
    email = order.user.email

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
    return "Email sent"


@shared_task
def update_order_status(order_id):
    time.sleep(10)  # wait 10 seconds (demo)
    order = Order.objects.get(id=order_id)
    if order.status == False:   # Pending
        order.status = True     # Processing
        order.save()
    return "Order status updated"
