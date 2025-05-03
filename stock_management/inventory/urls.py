from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'stock', views.StockViewSet, basename='stock')
router.register(r'suppliers', views.SupplierViewSet, basename='supplier')
router.register(r'transactions', views.TransactionViewSet, basename='transaction')
router.register(r'stock-adjustments', views.StockAdjustmentViewSet, basename='stock-adjustment')

urlpatterns = router.urls
