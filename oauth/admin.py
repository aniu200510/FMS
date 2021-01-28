from django.contrib import admin

from oauth.models import Fund, FundCompany, FundManager, User

admin.site.register(User)
admin.site.register(FundCompany)
admin.site.register(FundManager)
admin.site.register(Fund)
