from django.contrib import admin
from .models import Category, Product, Stock, Supplier, Transaction, StockAdjustment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'unit', 'price', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'updated_at')
    list_filter = ('product__category', 'updated_at')
    search_fields = ('product__name',)
    date_hierarchy = 'updated_at'

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'email')
    search_fields = ('name', 'contact_person', 'phone', 'email')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('product', 'transaction_type', 'quantity', 'user', 'transaction_date')
    list_filter = ('transaction_type', 'transaction_date', 'product__category')
    search_fields = ('product__name', 'user__username')
    date_hierarchy = 'transaction_date'

@admin.register(StockAdjustment)
class StockAdjustmentAdmin(admin.ModelAdmin):
    list_display = ('product', 'adjustment_type', 'quantity', 'reason', 'user', 'adjustment_date')
    list_filter = ('adjustment_type', 'adjustment_date', 'product__category')
    search_fields = ('product__name', 'reason', 'user__username')
    date_hierarchy = 'adjustment_date'
