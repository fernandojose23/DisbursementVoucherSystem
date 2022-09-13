from rest_framework import serializers
from disbursement_voucher.models import Department, DisbursmentVocuher, Receipt, SubDepartment
from rest_framework.exceptions import AuthenticationFailed

from django.core.mail import EmailMessage
from django.conf import settings
from django.template import Context
from django.template.loader import render_to_string, get_template

from rest_framework import generics, status, views, permissions
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


class DepartmentSerializer(serializers.ModelSerializer):
    # dept_name =  serializers.ReadOnlyField(source='departments.dept_name')
    class Meta:
        model = Department

        fields = '__all__'

class SubDepartmentSerializer(serializers.ModelSerializer):
    # dept_name =  serializers.ReadOnlyField(source='departments.dept_name')
    class Meta:
        model = SubDepartment

        fields = '__all__'

class DisbursmentVocuherSerializer(serializers.ModelSerializer):
    dept_name =  serializers.ReadOnlyField(source='department.dept_name')
    class Meta:
        model = DisbursmentVocuher
        fields = '__all__'


class ReceiptSerializer(serializers.ModelSerializer):

    class Meta:
        model = Receipt

        fields = '__all__'

# class DepartmentSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = Department
#     fields = '__all__'
