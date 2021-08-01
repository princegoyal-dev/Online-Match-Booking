from django.contrib import admin

# Register your models here.
from user.models import order_details,contact_us

class register_model(admin.ModelAdmin):
    list_display = ['name','in_game_name','phone_number','date','order_id','status']

class register_contactform(admin.ModelAdmin):
    list_display = ['from_email', 'subject', 'message','status']

admin.site.register(order_details,register_model)
admin.site.register(contact_us, register_contactform)
