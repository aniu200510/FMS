# -*- coding:utf-8 -*-
from rest_framework import serializers

from oauth.models import Fund, FundAccount, FundCompany, FundManager, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'email'
        )


class FundCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = FundCompany
        fields = (
            'id',
            'name'
        )


class FundManagerSerializer(serializers.ModelSerializer):

    class Meta:
        model = FundManager
        fields = (
            'id',
            'name',
            'working_seniority',
            'fund_company'
        )


class FundSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fund
        fields = (
            'id',
            'name',
            'code',
            'type',
            'scale',
            'found_date',
            'managers',
            'custodian'
        )


class FundAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = FundAccount
        fields = (
            'id',
            'date',
            'principal',
            'amount',
            'fund_net',
            'share',
            'fund',
        )
