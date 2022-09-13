from rest_framework import viewsets, permissions
from .serializers import DepartmentSerializer, DisbursmentVocuherSerializer, ReceiptSerializer,SubDepartmentSerializer
from .models import Department, DisbursmentVocuher, Receipt,SubDepartment
from rest_framework.response import Response
from django.core import serializers
import os.path
import json
from rest_framework import status

from django.utils import timezone as time_zone

from django.http import QueryDict
import calendar

from datetime import datetime, date, timezone

from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.conf import settings
from django.template import Context
from django.db.models import Q


class DisbursmentVocuherViewSet(viewsets.ModelViewSet):

    queryset = DisbursmentVocuher.objects.all().order_by("-createdAT")
    serializer_class = DisbursmentVocuherSerializer

    permission_classes_by_action = {'create': [permissions.AllowAny],
                                    'list': [permissions.AllowAny],
                                    'update': [permissions.AllowAny],
                                    'retrieve': [permissions.AllowAny],
                                    'destroy': [permissions.AllowAny],
                                    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def list(self, request, *args, **kwargs):

        page_size = 5
        if self.request.query_params.get('page_size'):
            page_size = int(self.request.query_params.get('page_size'))
        if self.request.query_params.get('getAllDisbursementVoucherRecord') is not None:
            data = self.get_queryset().filter(is_archive_voucher=False)
        elif self.request.query_params.get('getDepartmentDisbursementVoucherRecord') is not None:
            data = self.get_queryset().filter(department=self.request.query_params.get('getDepartmentDisbursementVoucherRecord'),is_archive_voucher=False)
        elif self.request.query_params.get('getDepartmentDisbursementVoucherSummary') is not None:
            dept_id=self.request.query_params.get('getDepartmentDisbursementVoucherSummary')
            
            disbursement_voucher_count = self.get_queryset().filter(department=dept_id,is_archive_voucher=False).count()
            disbursed_voucher_count=Receipt.objects.filter(voucher_number__department=dept_id,is_archive_reciept=False).count()
            payable_count=disbursement_voucher_count-disbursed_voucher_count
            
            return Response({ "disbursement_voucher_count": disbursement_voucher_count,"disbursed_voucher_count":disbursed_voucher_count, "payable_count": payable_count})
        elif self.request.query_params.get('getTotalDisbursementVoucherForAYear') is not None:
            year=self.request.query_params.get('getTotalDisbursementVoucherForAYear')
            data=[]
            try:
                for x in range(12):
                    month_range=calendar.monthrange(int(year), int(x+1))
                    data.append(self.get_queryset().filter( 
                              date_issued__year__gte=year,
                              date_issued__month__gte=int(x+1),
                              date_issued__day__gte=1,
                              date_issued__year__lte=year,
                              date_issued__month__lte=int(x+1),
                              date_issued__day__lte=month_range[1],
                              is_archive_voucher=False).count())
              
                return Response(data)
            except:
                 return Response([0,0,0,0,0,0,0,0,0,0,0,0,0])
        elif self.request.query_params.get('getTotalPayableForAYear') is not None:
            year=self.request.query_params.get('getTotalPayableForAYear')
            data=[]
            try:
                for x in range(12):
                    month_range=calendar.monthrange(int(year), int(x+1))
                    disbursement_voucher_count=self.get_queryset().filter( 
                              date_issued__year__gte=year,
                              date_issued__month__gte=int(x+1),
                              date_issued__day__gte=1,
                              date_issued__year__lte=year,
                              date_issued__month__lte=int(x+1),
                              date_issued__day__lte=month_range[1],
                              is_archive_voucher=False).count()
                    disbursed_voucher_count=Receipt.objects.filter( 
                            created_at__year__gte=year,
                            created_at__month__gte=int(x+1),
                            created_at__day__gte=1,
                            created_at__year__lte=year,
                            created_at__month__lte=int(x+1),
                            created_at__day__lte=month_range[1],
                            is_archive_reciept=False).count()
                    data.append(disbursement_voucher_count-disbursed_voucher_count)
                   
                return Response(data)
            except:
                 return Response([0,0,0,0,0,0,0,0,0,0,0,0,0])
        
        elif self.request.query_params.get('getTotalDisbursedForAYear') is not None:
            year=self.request.query_params.get('getTotalDisbursedForAYear')
            data=[]
            try:
                for x in range(12):
                    month_range=calendar.monthrange(int(year), int(x+1))
                    data.append(Receipt.objects.filter( 
                            created_at__year__gte=year,
                            created_at__month__gte=int(x+1),
                            created_at__day__gte=1,
                            created_at__year__lte=year,
                            created_at__month__lte=int(x+1),
                            created_at__day__lte=month_range[1],
                            is_archive_reciept=False).count())
                print(data)    
                return Response(data)
            except:
                 return Response([0,0,0,0,0,0,0,0,0,0,0,0,0])
        elif self.request.query_params.get('getDisburementSummaryForMonth') is not None:
            month=self.request.query_params.get('getDisburementSummaryForMonth')
            year=self.request.query_params.get('year')
             
            try:
               
                    month_range=calendar.monthrange(int(year), int(month))

                    disbursement_voucher_count=self.get_queryset().filter( 
                             createdAT__year__gte=year,
                             createdAT__month__gte=int(month),
                              createdAT__day__gte=1,
                              createdAT__year__lte=year,
                              createdAT__month__lte=int(month),
                              createdAT__day__lte=month_range[1],
                              is_archive_voucher=False).count()

                    disbursed_voucher_count=Receipt.objects.filter( 
                            created_at__year__gte=year,
                            created_at__month__gte=int(month),
                            created_at__day__gte=1,
                            created_at__year__lte=year,
                            created_at__month__lte=int(month),
                            created_at__day__lte=month_range[1],
                            is_archive_reciept=False).count()

                    payable=disbursement_voucher_count-disbursed_voucher_count
                  
                    return Response({"disbursement_voucher_count": disbursement_voucher_count,"disbursed_voucher_count":disbursed_voucher_count,"payable":payable})
                
            except:
                 return Response([0,0,0])
        if self.request.query_params.get('fund_type') is not None and self.request.query_params.get('fund_type')!="all" : 
                    data=data.filter(fund_type=self.request.query_params.get('fund_type'),)
        if self.request.query_params.get('mode_of_payment') is not None and self.request.query_params.get('mode_of_payment')!="all" : 
                    data=data.filter(mode_of_payment=self.request.query_params.get('mode_of_payment'),)
        if self.request.query_params.get('dept_id') is not None and self.request.query_params.get('dept_id')!="all" : 
                    data=data.filter(department=self.request.query_params.get('dept_id'),)
        if self.request.query_params.get('sub dept name') is not None and self.request.query_params.get('sub dept name')!="all" : 
                    data=data.filter(subdept_name=self.request.query_params.get('sub dept name'))
        if self.request.query_params.get('date_from') is not None and self.request.query_params.get('date_from')!="all" and  self.request.query_params.get('date_to') is not None and self.request.query_params.get('date_to')!="all" and self.request.query_params.get('date_from')!=""and self.request.query_params.get('date_to')!="" :
                    date_from=self.request.query_params.get('date_from')
                    date_to=self.request.query_params.get('date_to')
                    
                    date1 =date_from.split("-")
                    date2 =date_to.split("-")
                  
                    todays_date = datetime.now()
                    
                    modified_date = todays_date.replace(year=int(date1[0]),month=int(date1[1]),day=int(date1[2]) ,hour=0 ,minute=0, second=0,tzinfo=timezone.utc)

                    modified_date2 = todays_date.replace(year=int(date2[0]),month=int(date2[1]),day=int(date2[2]) ,hour=23,minute=59,second=59,tzinfo=timezone.utc)

                    data=data.filter(
                      createdAT__gte=modified_date ,
                        createdAT__lte=modified_date2
                         )
                 ############## Search ##########
        if self.request.query_params.get('search') is not None and self.request.query_params.get('search')!="" : 
                    search=self.request.query_params.get('search')
                    data=data.filter((Q(payee__icontains=search))|(Q(subdept_name__icontains=search))|(Q(voucher_number__icontains=search))|(Q(voucher_number__icontains=search)) |(Q(department__dept_id__icontains=search)) |(Q(department__dept_name__icontains=search)) |(Q(check_number__icontains=search)) |(Q(obligation_number__icontains=search)) )

        page = self.paginate_queryset(data)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            reponse = self.get_paginated_response(serializer.data)
            totalpage = 0
            if reponse.data['count'] > page_size:
                totalpage += int(reponse.data['count']/page_size)
                if reponse.data['count'] % page_size != 0:
                    totalpage = totalpage+1

            if reponse.data['count'] <= page_size:
                totalpage = 1

            if reponse.data['count'] == 0:
                totalpage = 0

            reponse.data['total_pages'] = totalpage
            return reponse

    def create(self, request, *args, **kwargs):
        print("hello")

        today = datetime.today()
        year = str(today.year)
        l = len(year)
        month = int(today.month)
        if month < 10:
            month = "0"+str(month)
        # day = today.day
        
        count = self.get_queryset().filter(is_archive_voucher=False).count()
        voucher_number = request.data["fund_type"] + \
            "-"+str(year[l-2:])+str(month)+"-"+str(count)
        request.data["voucher_number"] = voucher_number
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):

        instance = self.get_object()
        partial = kwargs.pop('partial', True)
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_archive_voucher = True
        instance. is_archive_voucher_Date = time_zone.now()
        instance.save()

        try: 
            reciept= Receipt.objects.get(voucher_number=instance.voucher_number)
            reciept.is_archive_reciept = True
            reciept.is_archive_voucher_Date = time_zone.now()
            reciept.save()
        except:
            print("No Voucher Record")
        
        return Response("archive successfully")

 
class DepartmentViewSet(viewsets.ModelViewSet):

    queryset = Department.objects.all().order_by("-dept_id")
    serializer_class = DepartmentSerializer

    permission_classes_by_action = {'create': [permissions.AllowAny],
                                    'list': [permissions.AllowAny],
                                    'update': [permissions.AllowAny],
                                    'retrieve': [permissions.AllowAny],
                                    'destroy': [permissions.AllowAny],
                                    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def list(self, request, *args, **kwargs):

        page_size = 5
        if self.request.query_params.get('page_size'):
            page_size = int(self.request.query_params.get('page_size'))
        if self.request.query_params.get('getAllDepartment') is not None:
            data = self.get_queryset().filter(is_archive_department=False).order_by("-dept_id")
        ######## Filter Department ##############
        if self.request.query_params.get('dept_id') is not None and self.request.query_params.get('dept_id')!="all" : 
                    data=data.filter(department=self.request.query_params.get('dept_id'),)
        if self.request.query_params.get('date_from') is not None and self.request.query_params.get('date_from')!="all" and  self.request.query_params.get('date_to') is not None and self.request.query_params.get('date_to')!="all" and self.request.query_params.get('date_from')!=""and self.request.query_params.get('date_to')!="" :
                    date_from=self.request.query_params.get('date_from')
                    date_to=self.request.query_params.get('date_to')
                    
                    date1 =date_from.split("-")
                    date2 =date_to.split("-")
                  
                    todays_date = datetime.now()
                    
                    modified_date = todays_date.replace(year=int(date1[0]),month=int(date1[1]),day=int(date1[2]) ,hour=0 ,minute=0, second=0,tzinfo=timezone.utc)

                    modified_date2 = todays_date.replace(year=int(date2[0]),month=int(date2[1]),day=int(date2[2]) ,hour=23,minute=59,second=59,tzinfo=timezone.utc)

                    data=data.filter(
                      createdAT__gte=modified_date ,
                        createdAT__lte=modified_date2
                         )
                 ############## Search Department ##########
        if self.request.query_params.get('search') is not None and self.request.query_params.get('search')!="" : 
                    search=self.request.query_params.get('search')
                    data=data.filter((Q(dept_id__icontains=search))|(Q(dept_name__icontains=search)) |(Q(department_email__icontains=search)) )
                ############################    
        page = self.paginate_queryset(data)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            reponse = self.get_paginated_response(serializer.data)
            totalpage = 0
            if reponse.data['count'] > page_size:
                totalpage += int(reponse.data['count']/page_size)
                if reponse.data['count'] % page_size != 0:
                    totalpage = totalpage+1

            if reponse.data['count'] <= page_size:
                totalpage = 1

            if reponse.data['count'] == 0:
                totalpage = 0

            reponse.data['total_pages'] = totalpage
            return reponse

    def destroy(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            instance = self.get_object()
            instance.is_archive_department = True
            instance.is_archive_department_date = datetime.now().strftime('%Y-%m-%d %H:%M')

            instance.save()

            return Response("archive successfully")
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
                instance = self.get_object()
                partial = kwargs.pop('partial', True)
                serializer = self.get_serializer(instance, data=request.data, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(serializer.data)
         
class SubDepartmentViewSet(viewsets.ModelViewSet):

    queryset = SubDepartment.objects.all().order_by("-sub_dept_id")
    serializer_class = SubDepartmentSerializer

    permission_classes_by_action = {'create': [permissions.AllowAny],
                                    'list': [permissions.AllowAny],
                                    'update': [permissions.AllowAny],
                                    'retrieve': [permissions.AllowAny],
                                    'destroy': [permissions.AllowAny],
                                    }
    def list(self, request, *args, **kwargs):

        if self.request.query_params.get('getSubDepartment') is not None:
            data = self.get_queryset().filter(is_archive_sub_department=False,department= self.request.query_params.get('getSubDepartment')).order_by("-sub_dept_id")
            print("hello")
            serializer = self.get_serializer(data, many=True)
            return Response( serializer.data)
        if self.request.query_params.get('getSubDepartment_disbursement_id') is not None:
            disbursement=DisbursmentVocuher.objects.get( voucher_number=self.request.query_params.get('getSubDepartment_disbursement_id'))
            data = self.get_queryset().filter(is_archive_sub_department=False,department= disbursement.department).order_by("-sub_dept_id")
            print("hello")
            serializer = self.get_serializer(data, many=True)
            return Response( serializer.data)
         
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
# ewan ko kung ano to basta inadd ko lang dito sa subdept
    def update(self, request, *args, **kwargs):
                instance = self.get_object()
                partial = kwargs.pop('partial', True)
                serializer = self.get_serializer(instance, data=request.data, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(serializer.data)
     
         
class ReceiptViewSet(viewsets.ModelViewSet):

    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer

    permission_classes_by_action = {'create': [permissions.AllowAny],
                                    'list': [permissions.AllowAny],
                                    'update': [permissions.AllowAny],
                                    'retrieve': [permissions.AllowAny],
                                    'destroy': [permissions.AllowAny],
                                    }

    def list(self, request, *args, **kwargs):

        page_size = 5
        if self.request.query_params.get('page_size'):
            page_size = int(self.request.query_params.get('page_size'))

        if self.request.query_params.get('getReceiptRecord') is not None:
            data = self.get_queryset().filter(voucher_number=self.request.query_params.get('getReceiptRecord'),is_archive_reciept=False) 
            serializer = self.get_serializer(data, many=True)
            print("data")
            print(serializer.data)
            if serializer.data:
                return Response(serializer.data[0])
            return Response({})
            
        page = self.paginate_queryset(data)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            reponse = self.get_paginated_response(serializer.data)
            totalpage = 0
            if reponse.data['count'] > page_size:
                totalpage += int(reponse.data['count']/page_size)
                if reponse.data['count'] % page_size != 0:
                    totalpage = totalpage+1

            if reponse.data['count'] <= page_size:
                totalpage = 1

            if reponse.data['count'] == 0:
                totalpage = 0

            reponse.data['total_pages'] = totalpage
            return reponse
