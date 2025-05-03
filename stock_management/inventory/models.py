from django.db import models
from users.models import CustomUser

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    unit = models.CharField(max_length=50, help_text="Unit of measurement (e.g., kg, liters, pieces)")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    reorder_level = models.PositiveIntegerField(default=0, help_text="Level at which to reorder the product")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        unique_together = ['name', 'category']

    def __str__(self):
        return self.name
    
    @property
    def current_stock(self):
        try:
            return self.stock.quantity
        except Stock.DoesNotExist:
            return 0


class Stock(models.Model):
    product = models.OneToOneField(Product, related_name='stock', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Stock'

    def __str__(self):
        return f"{self.product.name} - {self.quantity} {self.product.unit}"


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
    )
    
    product = models.ForeignKey(Product, related_name='transactions', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    quantity = models.PositiveIntegerField()
    supplier = models.ForeignKey(Supplier, related_name='transactions', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(CustomUser, related_name='transactions', on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-transaction_date']

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.product.name} ({self.quantity})"

    def save(self, *args, **kwargs):
        # Create stock if it doesn't exist
        stock, created = Stock.objects.get_or_create(product=self.product)
        
        # Update stock quantity
        if self.transaction_type == 'IN':
            stock.quantity += self.quantity
        elif self.transaction_type == 'OUT':
            stock.quantity -= self.quantity
        
        stock.save()
        super().save(*args, **kwargs)


class StockAdjustment(models.Model):
    ADJUSTMENT_TYPES = (
        ('ADD', 'Add to Stock'),
        ('SUB', 'Subtract from Stock'),
    )
    
    product = models.ForeignKey(Product, related_name='adjustments', on_delete=models.CASCADE)
    adjustment_type = models.CharField(max_length=3, choices=ADJUSTMENT_TYPES)
    quantity = models.PositiveIntegerField()
    reason = models.TextField()
    user = models.ForeignKey(CustomUser, related_name='adjustments', on_delete=models.CASCADE)
    adjustment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-adjustment_date']

    def __str__(self):
        return f"{self.get_adjustment_type_display()} - {self.product.name} ({self.quantity})"

    def save(self, *args, **kwargs):
        # Create stock if it doesn't exist
        stock, created = Stock.objects.get_or_create(product=self.product)
        
        # Update stock quantity
        if self.adjustment_type == 'ADD':
            stock.quantity += self.quantity
        elif self.adjustment_type == 'SUB':
            stock.quantity -= self.quantity
        
        stock.save()
        super().save(*args, **kwargs)
