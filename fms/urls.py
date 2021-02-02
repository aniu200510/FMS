"""fms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from oauth import views as ovs

router = DefaultRouter()
router.register(r'^oauth/fund-companies', ovs.FundCompanyViewSet)
router.register(r'^oauth/fund-mangers', ovs.FundManagerViewSet)
router.register(r'^oauth/funds', ovs.FundViewSet)
router.register(r'^oauth/fund-account', ovs.FundAccountViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api-token-auth/', obtain_auth_token),
]
