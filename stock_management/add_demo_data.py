#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_management.settings')
django.setup()

# Import models after Django setup
from inventory.models import Category, Product, Supplier, Stock, Transaction
from users.models import CustomUser
from django.db import transaction
from django.contrib.auth import get_user_model

User = get_user_model()

# Get or create demo user
user = User.objects.get(username='admin')

@transaction.atomic
def load_demo_data():
    print("Adding demo data for stock management system...")
    
    # Create categories
    categories = [
        {'name': 'Electronics', 'description': 'Electronic devices and components'},
        {'name': 'Office Supplies', 'description': 'Office stationery and supplies'},
        {'name': 'Furniture', 'description': 'Office and home furniture'},
        {'name': 'Kitchen Supplies', 'description': 'Kitchen items and appliances'},
        {'name': 'Tools', 'description': 'Hand and power tools'}
    ]
    
    for cat_data in categories:
        Category.objects.get_or_create(name=cat_data['name'], defaults={
            'description': cat_data['description']
        })
    
    # Create suppliers
    suppliers = [
        {'name': 'Tech Solutions Inc.', 'contact_person': 'John Smith', 'phone': '555-1234', 'email': 'john@techsolutions.com'},
        {'name': 'Office Depot', 'contact_person': 'Jane Doe', 'phone': '555-5678', 'email': 'jane@officedepot.com'},
        {'name': 'Furniture World', 'contact_person': 'Bob Johnson', 'phone': '555-9012', 'email': 'bob@furnitureworld.com'}
    ]
    
    for sup_data in suppliers:
        Supplier.objects.get_or_create(name=sup_data['name'], defaults={
            'contact_person': sup_data['contact_person'],
            'phone': sup_data['phone'],
            'email': sup_data['email']
        })
    
    # Create products with initial stock
    products = [
        {'name': 'Laptop', 'description': 'Business laptop computer', 'category': 'Electronics', 'unit': 'piece', 'price': 999.99, 'reorder_level': 5},
        {'name': 'Desktop Computer', 'description': 'Office desktop computer', 'category': 'Electronics', 'unit': 'piece', 'price': 799.99, 'reorder_level': 3},
        {'name': 'Printer', 'description': 'Laser printer', 'category': 'Electronics', 'unit': 'piece', 'price': 299.99, 'reorder_level': 2},
        {'name': 'Paper', 'description': 'A4 printer paper', 'category': 'Office Supplies', 'unit': 'ream', 'price': 4.99, 'reorder_level': 20},
        {'name': 'Pens', 'description': 'Blue ballpoint pens', 'category': 'Office Supplies', 'unit': 'box', 'price': 5.99, 'reorder_level': 10},
        {'name': 'Office Chair', 'description': 'Ergonomic office chair', 'category': 'Furniture', 'unit': 'piece', 'price': 149.99, 'reorder_level': 5},
        {'name': 'Desk', 'description': 'Office desk', 'category': 'Furniture', 'unit': 'piece', 'price': 249.99, 'reorder_level': 2},
        {'name': 'Coffee Maker', 'description': 'Office coffee machine', 'category': 'Kitchen Supplies', 'unit': 'piece', 'price': 79.99, 'reorder_level': 1},
        {'name': 'Screwdriver Set', 'description': 'Set of various screwdrivers', 'category': 'Tools', 'unit': 'set', 'price': 19.99, 'reorder_level': 3}
    ]
    
    # Get supplier for initial stock
    supplier = Supplier.objects.first()
    
    for prod_data in products:
        # Get category
        category = Category.objects.get(name=prod_data['category'])
        
        # Create product if it doesn't exist
        product, created = Product.objects.get_or_create(
            name=prod_data['name'],
            category=category,
            defaults={
                'description': prod_data['description'],
                'unit': prod_data['unit'],
                'price': prod_data['price'],
                'reorder_level': prod_data['reorder_level']
            }
        )
        
        # Add initial stock if product was just created
        if created:
            # Create initial stock entry with random quantity between reorder_level and reorder_level*3
            import random
            quantity = random.randint(prod_data['reorder_level'], prod_data['reorder_level'] * 3)
            
            # Create stock record
            stock, _ = Stock.objects.get_or_create(product=product, defaults={'quantity': 0})
            
            # Create transaction record for initial stock
            Transaction.objects.create(
                product=product,
                transaction_type='IN',
                quantity=quantity,
                supplier=supplier,
                user=user,
                notes='Initial stock'
            )
            
            print(f"Added {product.name} with initial stock of {quantity}")
        else:
            print(f"Product {product.name} already exists, skipping")
    
    print("Demo data loaded successfully!")


if __name__ == '__main__':
    load_demo_data()
