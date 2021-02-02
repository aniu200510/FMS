from rest_framework import viewsets

from oauth.models import Fund, FundAccount, FundCompany, FundManager
from oauth.serializers import (FundAccountSerializer, FundCompanySerializer,
                               FundManagerSerializer, FundSerializer)


class FundCompanyViewSet(viewsets.ModelViewSet):
    serializer_class = FundCompanySerializer
    queryset = FundCompany.objects.all()


class FundManagerViewSet(viewsets.ModelViewSet):
    serializer_class = FundManagerSerializer
    queryset = FundManager.objects.all()


class FundViewSet(viewsets.ModelViewSet):
    serializer_class = FundSerializer
    queryset = Fund.objects.all()


class FundAccountViewSet(viewsets.ModelViewSet):
    serializer_class = FundAccountSerializer
    queryset = FundAccount.objects.all()
    filter_fields = ('date', 'fund')
    search_fields = ('date', 'fund__name')
