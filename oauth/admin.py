from django.contrib import admin

from oauth.models import Fund, FundAccount, FundCompany, FundManager, User

admin.site.register(User)
admin.site.register(FundCompany)
admin.site.register(FundManager)
admin.site.register(Fund)
admin.site.register(FundAccount)
