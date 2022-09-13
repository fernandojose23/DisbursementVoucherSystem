from django.db import models
from account.models import Account
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _

# Create your models here.
 

class Department(models.Model):
    dept_id = models.CharField(unique=True, max_length=100, primary_key=True)
    dept_name = models.CharField(
        max_length=50, null=False, blank=False, unique=True)
    department_email = models.EmailField(
        _('department email'), null=True, blank=True)
    is_archive_department = models.BooleanField(default=False)
    is_archive_department_date = models.CharField(
        max_length=40, null=True, blank=True)

    def __str__(self):
        return '%s' % self.dept_name

class SubDepartment(models.Model):
    sub_dept_id = models.AutoField(primary_key=True)
    sub_dept_name = models.CharField(
        max_length=50, null=False, blank=False)
    department = models.ForeignKey(
        Department, related_name='department_id', on_delete=models.SET_NULL, null=True)
    is_archive_sub_department = models.BooleanField(default=False)
    is_archive_sub_department_date = models.CharField(
        max_length=40, null=True, blank=True)

    def __str__(self):
        return '%s' % self.sub_dept_name

class DisbursmentVocuher(models.Model):

    FUND_TYPE = [
        ("1000", "General Fund"),
        ("2000", "Special Educational Fund"),
        ("3000", "Trust Fund"),

    ]
    EXPENDETURE = [
        ("M.O.O.E", "M.O.O.E"),
        ("P.S","P.S"),
        ("C.O","C.O"),

    ]
    
    MODE_OF_PAYMENT = [
        ("Check", 'Check'),
        ("Cash", 'Cash'),
        ("Others", 'Others'),

    ]
    voucher_number = models.CharField(
        primary_key=True, unique=True, max_length=50)
    department = models.ForeignKey(
        Department, related_name='departmentId', on_delete=models.SET_NULL, null=True)
    insert_by = models.ForeignKey(
        Account, related_name='accountId', on_delete=models.SET_NULL, null=True)
    payee = models.CharField(max_length=300, null=False, blank=False)
    particulars = models.CharField(max_length=300, null=False, blank=False)
    check_number = models.CharField(max_length=100, null=True, blank=True)
    mode_of_payment = models.CharField(
        max_length=100, null=False, blank=False, choices=MODE_OF_PAYMENT)
    obligation_number = models.CharField(
        max_length=100, null=False, blank=False)
    vat = models.FloatField(null=False, blank=False)
    fund_type = models.CharField( 
        max_length=100, null=True, blank=False, choices=FUND_TYPE)
    createdAT = models.DateTimeField(auto_now_add=True)
    date_issued = models.DateField(default=None, null=True, blank=True)
    ammount = models.FloatField(null=False, blank=False)
    address = models.CharField(max_length=300, null=False, blank=False)
    subdept_name = models.CharField(
        max_length=50, null=True, blank=True)
    expendeture = models.CharField(
        max_length=50, null=True, blank=True, choices=EXPENDETURE)
    isPaid = models.BooleanField(default=False)
    is_archive_voucher = models.BooleanField(default=False)
    is_archive_voucher_Date = models.CharField(
        max_length=40, null=True, blank=True)

    def __str__(self):
        return '%s' % self.department.dept_name
 

class Receipt(models.Model):
    BUDGET_TYPE = [
        ("P.S", 'P.S'),
        ("M.O.O.E", 'M.O.O.E'),
        ("C.O", 'C.O'),
    ]
    receipt_id = models.AutoField(primary_key=True)
    voucher_number = models.ForeignKey(
        DisbursmentVocuher, related_name='voucher_id', on_delete=models.CASCADE, null=True)
    income_target = models.CharField(max_length=100, null=False, blank=False)
    budget_type = models.CharField(
        max_length=100, null=True, blank=False, choices=BUDGET_TYPE)
    total = models.FloatField(null=False, blank=False)
    total_income = models.FloatField(null=False, blank=False)
    picture = models.ImageField(
        upload_to='receipt/', null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    is_archive_reciept = models.BooleanField(default=False)
    is_archive_reciept_date = models.CharField(
        max_length=40, null=True, blank=True)

    def __str__(self):
        return '%s' % self.receipt_id
