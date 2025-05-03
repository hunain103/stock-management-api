#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_management.settings')
django.setup()

# Import models after Django setup
from inventory.models import Product, Stock, Transaction, Supplier
from users.models import CustomUser
from django.db import transaction

def add_stock():
    print("Adding stock for existing products...")
    
    # Get admin user
    try:
        user = CustomUser.objects.get(username='admin')
    except CustomUser.DoesNotExist:
        print("Admin user not found. Please create an admin user first.")
        return
    
    # Get a supplier
    try:
        supplier = Supplier.objects.first()
        if not supplier:
            supplier = Supplier.objects.create(
                name='Default Supplier',
                contact_person='Contact Person',
                email='contact@supplier.com'
            )
    except Exception as e:
        print(f"Error getting supplier: {e}")
        return
    
    # Add stock for each product
    for product in Product.objects.all():
        with transaction.atomic():
            # Create or get stock entry
            stock, created = Stock.objects.get_or_create(
                product=product,
                defaults={'quantity': 0}
            )
            
            if stock.quantity == 0:
                # Add initial stock
                quantity = product.reorder_level * 2
                
                # Update stock quantity
                stock.quantity = quantity
                stock.save()
                
                # Create transaction record
                Transaction.objects.create(
                    product=product,
                    transaction_type='IN',
                    quantity=quantity,
                    supplier=supplier,
                    user=user,
                    notes='Initial stock'
                )
                
                print(f"Added {quantity} {product.unit}s of {product.name} to stock")
            else:
                print(f"Stock already exists for {product.name} with quantity {stock.quantity}")

if __name__ == '__main__':
    add_stock()
