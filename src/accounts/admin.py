from django.contrib import admin
from accounts.models import *
# Register your models here.


admin.site.register(User)

admin.site.register(UserProfile)
@admin.register(OtpCode)
class OTPAdmin(admin.ModelAdmin):
    model=OtpCode
    list_display =['phone_number','code','expire_at']