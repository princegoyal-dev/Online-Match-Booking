from django.db import models
import datetime
# Create your models here.
class order_details(models.Model):
    name = models.CharField(max_length=50)
    in_game_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)
    date = models.DateField(("Date"), default=datetime.date.today)
    order_id = models.CharField(max_length=20, default='None')
    status = models.BooleanField(default=False)

class contact_us(models.Model):
    from_email = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=500)
    status = models.BooleanField(default=False)
