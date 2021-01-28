from django.contrib import admin
from oauth.models import User, FundCompany, FundManager, Fund


admin.site.register(User)
admin.site.register(FundCompany)
admin.site.register(FundManager)
admin.site.register(Fund)
