from django.contrib import admin

from oauth.models import (Fund, FundAccount, FundCompany, FundManager, FundNet, User)

admin.site.register(User)
admin.site.register(FundCompany)
admin.site.register(FundManager)
admin.site.register(Fund)
admin.site.register(FundAccount)
admin.site.register(FundNet)
