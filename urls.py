from rest_framework import routers
from .api import DepartmentViewSet, DisbursmentVocuherViewSet, ReceiptViewSet, SubDepartmentViewSet

router = routers.DefaultRouter()

router.register('api/department', DepartmentViewSet, 'department')
router.register('api/disbursement_voucher',
                DisbursmentVocuherViewSet, 'disbursement_voucher')
router.register('api/receipt', ReceiptViewSet, 'reciept')
router.register('api/sub_dept', SubDepartmentViewSet, 'sub_dept')

urlpatterns = router.urls
