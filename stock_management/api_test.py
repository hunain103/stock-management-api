import requests
import json
import argparse
import sys
from datetime import datetime
from pprint import pprint

# The base URL of your running API
BASE_URL = 'http://localhost:5000/api'

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Test data
TEST_USER = {
    'username': f'testuser_{datetime.now().strftime("%Y%m%d%H%M%S")}',
    'email': f'testuser_{datetime.now().strftime("%Y%m%d%H%M%S")}@example.com',
    'password': 'Test@1234',
    'confirm_password': 'Test@1234',
    'first_name': 'Test',
    'last_name': 'User',
    'phone': '1234567890',
    'department': 'Testing'
}

TEST_CATEGORY = {
    'name': f'Test Category {datetime.now().strftime("%Y%m%d%H%M%S")}',
    'description': 'This is a test category'
}

TEST_SUPPLIER = {
    'name': f'Test Supplier {datetime.now().strftime("%Y%m%d%H%M%S")}',
    'contact_person': 'John Doe',
    'address': '123 Test Street',
    'phone': '1234567890',
    'email': 'supplier@example.com'
}

TEST_PRODUCT = {
    'name': f'Test Product {datetime.now().strftime("%Y%m%d%H%M%S")}',
    'description': 'This is a test product',
    'unit': 'pieces',
    'price': '19.99',
    'reorder_level': 10
}

def print_response(response, operation):
    """Print the response in a nice format"""
    print(f"\n{Colors.BOLD}{operation}{Colors.ENDC}")
    print(f"Status Code: {response.status_code}")
    print("Headers:")
    print(json.dumps(dict(response.headers), indent=4))
    print("Response:")
    try:
        pprint(response.json())
    except Exception:
        print(response.text)
    
    if 200 <= response.status_code < 300:
        print(f"\n{Colors.OKGREEN}✓ Success!{Colors.ENDC}")
    else:
        print(f"\n{Colors.FAIL}✗ Failed!{Colors.ENDC}")

def test_auth(headers=None):
    """Test authentication API endpoints"""
    session = requests.Session()
    if headers:
        session.headers.update(headers)
    
    print(f"\n{Colors.HEADER}Testing Authentication Endpoints{Colors.ENDC}")
    
    # Register a new user
    response = session.post(f"{BASE_URL}/users/register/", json=TEST_USER)
    print_response(response, "Register User")
    
    # Login
    login_data = {
        'username': TEST_USER['username'],
        'password': TEST_USER['password']
    }
    response = session.post(f"{BASE_URL}/token/", json=login_data)
    print_response(response, "Login User (Get JWT Token)")
    
    # Extract tokens if login was successful
    if response.status_code == 200:
        tokens = response.json()
        session.headers.update({
            'Authorization': f"Bearer {tokens['access']}"
        })
        print(f"\n{Colors.OKGREEN}Authentication successful! Access token obtained.{Colors.ENDC}")
        
        # Verify token
        response = session.post(f"{BASE_URL}/token/verify/", json={'token': tokens['access']})
        print_response(response, "Verify Token")
        
        # Refresh token
        response = session.post(f"{BASE_URL}/token/refresh/", json={'refresh': tokens['refresh']})
        print_response(response, "Refresh Token")
        
        return session, tokens
    else:
        print(f"\n{Colors.FAIL}Failed to authenticate!{Colors.ENDC}")
        return session, None

def test_category_crud(session):
    """Test CRUD operations for categories"""
    print(f"\n{Colors.HEADER}Testing Category CRUD Operations{Colors.ENDC}")
    
    # Create
    response = session.post(f"{BASE_URL}/inventory/categories/", json=TEST_CATEGORY)
    print_response(response, "Create Category")
    
    if response.status_code == 201:
        category_id = response.json()["id"]
        
        # Retrieve
        response = session.get(f"{BASE_URL}/inventory/categories/{category_id}/")
        print_response(response, "Retrieve Category")
        
        # Update (PUT)
        update_data = TEST_CATEGORY.copy()
        update_data['description'] = 'Updated description (PUT)'
        response = session.put(f"{BASE_URL}/inventory/categories/{category_id}/", json=update_data)
        print_response(response, "Update Category (PUT)")
        
        # Update (PATCH)
        patch_data = {'description': 'Updated description (PATCH)'}
        response = session.patch(f"{BASE_URL}/inventory/categories/{category_id}/", json=patch_data)
        print_response(response, "Update Category (PATCH)")
        
        # List
        response = session.get(f"{BASE_URL}/inventory/categories/")
        print_response(response, "List Categories")
        
        # Delete
        response = session.delete(f"{BASE_URL}/inventory/categories/{category_id}/")
        print_response(response, "Delete Category")
        
        return category_id
    else:
        print(f"\n{Colors.FAIL}Failed to create category!{Colors.ENDC}")
        return None

def test_supplier_crud(session):
    """Test CRUD operations for suppliers"""
    print(f"\n{Colors.HEADER}Testing Supplier CRUD Operations{Colors.ENDC}")
    
    # Create
    response = session.post(f"{BASE_URL}/inventory/suppliers/", json=TEST_SUPPLIER)
    print_response(response, "Create Supplier")
    
    if response.status_code == 201:
        supplier_id = response.json()["id"]
        
        # Retrieve
        response = session.get(f"{BASE_URL}/inventory/suppliers/{supplier_id}/")
        print_response(response, "Retrieve Supplier")
        
        # Update (PUT)
        update_data = TEST_SUPPLIER.copy()
        update_data['contact_person'] = 'Jane Smith (PUT)'
        response = session.put(f"{BASE_URL}/inventory/suppliers/{supplier_id}/", json=update_data)
        print_response(response, "Update Supplier (PUT)")
        
        # Update (PATCH)
        patch_data = {'contact_person': 'Jane Smith (PATCH)'}
        response = session.patch(f"{BASE_URL}/inventory/suppliers/{supplier_id}/", json=patch_data)
        print_response(response, "Update Supplier (PATCH)")
        
        # List
        response = session.get(f"{BASE_URL}/inventory/suppliers/")
        print_response(response, "List Suppliers")
        
        # Delete
        response = session.delete(f"{BASE_URL}/inventory/suppliers/{supplier_id}/")
        print_response(response, "Delete Supplier")
        
        return supplier_id
    else:
        print(f"\n{Colors.FAIL}Failed to create supplier!{Colors.ENDC}")
        return None

def test_product_crud(session, category_id):
    """Test CRUD operations for products"""
    print(f"\n{Colors.HEADER}Testing Product CRUD Operations{Colors.ENDC}")
    
    # Create a new category first if needed
    if not category_id:
        response = session.post(f"{BASE_URL}/inventory/categories/", json=TEST_CATEGORY)
        if response.status_code == 201:
            category_id = response.json()["id"]
        else:
            print(f"\n{Colors.FAIL}Failed to create category for product test!{Colors.ENDC}")
            return None
    
    # Create Product
    product_data = TEST_PRODUCT.copy()
    product_data['category'] = category_id
    response = session.post(f"{BASE_URL}/inventory/products/", json=product_data)
    print_response(response, "Create Product")
    
    if response.status_code == 201:
        product_id = response.json()["id"]
        
        # Retrieve
        response = session.get(f"{BASE_URL}/inventory/products/{product_id}/")
        print_response(response, "Retrieve Product")
        
        # Update (PUT)
        update_data = product_data.copy()
        update_data['description'] = 'Updated product description (PUT)'
        response = session.put(f"{BASE_URL}/inventory/products/{product_id}/", json=update_data)
        print_response(response, "Update Product (PUT)")
        
        # Update (PATCH)
        patch_data = {'description': 'Updated product description (PATCH)'}
        response = session.patch(f"{BASE_URL}/inventory/products/{product_id}/", json=patch_data)
        print_response(response, "Update Product (PATCH)")
        
        # List
        response = session.get(f"{BASE_URL}/inventory/products/")
        print_response(response, "List Products")
        
        # Stock Level
        response = session.get(f"{BASE_URL}/inventory/products/{product_id}/stock_level/")
        print_response(response, "Get Product Stock Level")
        
        # Transactions
        response = session.get(f"{BASE_URL}/inventory/products/{product_id}/transactions/")
        print_response(response, "Get Product Transactions")
        
        # Don't delete the product yet - we'll need it for stock operations
        return product_id
    else:
        print(f"\n{Colors.FAIL}Failed to create product!{Colors.ENDC}")
        return None

def test_stock_operations(session, product_id, supplier_id):
    """Test stock operations"""
    print(f"\n{Colors.HEADER}Testing Stock Operations{Colors.ENDC}")
    
    # Create supplier if needed
    if not supplier_id:
        response = session.post(f"{BASE_URL}/inventory/suppliers/", json=TEST_SUPPLIER)
        if response.status_code == 201:
            supplier_id = response.json()["id"]
        else:
            print(f"\n{Colors.FAIL}Failed to create supplier for stock operations!{Colors.ENDC}")
            supplier_id = None
    
    # Create a stock transaction (Stock In)
    transaction_data = {
        'product': product_id,
        'transaction_type': 'IN',
        'quantity': 50,
        'supplier': supplier_id,
        'notes': 'Initial stock'    
    }
    response = session.post(f"{BASE_URL}/inventory/transactions/", json=transaction_data)
    print_response(response, "Create Stock Transaction (IN)")
    
    if response.status_code == 201:
        transaction_id = response.json()["id"]
        
        # Get stock level
        response = session.get(f"{BASE_URL}/inventory/products/{product_id}/stock_level/")
        print_response(response, "Get Updated Stock Level")
        
        # Create another transaction (Stock Out)
        transaction_data = {
            'product': product_id,
            'transaction_type': 'OUT',
            'quantity': 10,
            'notes': 'Stock out for testing'
        }
        response = session.post(f"{BASE_URL}/inventory/transactions/", json=transaction_data)
        print_response(response, "Create Stock Transaction (OUT)")
        
        # Get stock level again
        response = session.get(f"{BASE_URL}/inventory/products/{product_id}/stock_level/")
        print_response(response, "Get Updated Stock Level After OUT")
        
        # List all stock
        response = session.get(f"{BASE_URL}/inventory/stock/")
        print_response(response, "List All Stock")
        
        # Check low stock
        response = session.get(f"{BASE_URL}/inventory/stock/low_stock/")
        print_response(response, "Check Low Stock Items")
        
        # Stock Adjustment
        adjustment_data = {
            'product': product_id,
            'adjustment_type': 'ADD',
            'quantity': 5,
            'reason': 'Found extra items in storage'
        }
        response = session.post(f"{BASE_URL}/inventory/stock-adjustments/", json=adjustment_data)
        print_response(response, "Create Stock Adjustment")
        
        # Get stock level after adjustment
        response = session.get(f"{BASE_URL}/inventory/products/{product_id}/stock_level/")
        print_response(response, "Get Stock Level After Adjustment")
        
        return True
    else:
        print(f"\n{Colors.FAIL}Failed to create stock transaction!{Colors.ENDC}")
        return False

def cleanup(session, product_id, category_id, supplier_id):
    """Clean up test data"""
    print(f"\n{Colors.HEADER}Cleaning Up Test Data{Colors.ENDC}")
    
    # Delete product
    if product_id:
        response = session.delete(f"{BASE_URL}/inventory/products/{product_id}/")
        print_response(response, "Delete Product")
    
    # Delete category
    if category_id:
        response = session.delete(f"{BASE_URL}/inventory/categories/{category_id}/")
        print_response(response, "Delete Category")
    
    # Delete supplier
    if supplier_id:
        response = session.delete(f"{BASE_URL}/inventory/suppliers/{supplier_id}/")
        print_response(response, "Delete Supplier")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Test API endpoints with JWT authentication')
    parser.add_argument('--url', type=str, help='Base URL for the API', default=BASE_URL)
    parser.add_argument('--skip-cleanup', action='store_true', help='Skip cleanup of test data')
    
    args = parser.parse_args()
    
    global BASE_URL
    if args.url:
        BASE_URL = args.url
    
    print(f"\n{Colors.BOLD}Testing API endpoints at {BASE_URL}{Colors.ENDC}")
    
    # Start testing
    session, tokens = test_auth()
    
    if tokens:
        category_id = test_category_crud(session)
        supplier_id = test_supplier_crud(session)
        product_id = test_product_crud(session, category_id)
        
        if product_id:
            test_stock_operations(session, product_id, supplier_id)
            
            if not args.skip_cleanup:
                cleanup(session, product_id, category_id, supplier_id)
    
    print(f"\n{Colors.BOLD}API Testing completed!{Colors.ENDC}")

if __name__ == "__main__":
    main()
