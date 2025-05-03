# Stock Management API - Postman Guide

## JWT Authentication

### 1. Register a User
- **Method**: POST
- **URL**: `http://localhost:5000/api/users/register/`
- **Body** (raw JSON):
```json
{
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "StrongPassword123!",
    "confirm_password": "StrongPassword123!",
    "first_name": "Test",
    "last_name": "User",
    "phone": "1234567890",
    "department": "Testing"
}
```

### 2. Obtain JWT Token
- **Method**: POST
- **URL**: `http://localhost:5000/api/token/`
- **Body** (raw JSON):
```json
{
    "username": "testuser",
    "password": "StrongPassword123!"
}
```
- **Response**: Will include `access` and `refresh` tokens

### 3. Using the Token
- For all subsequent API requests, add an Authorization header:
- **Header**: `Authorization: Bearer <your_access_token>`

### 4. Refresh Token
- **Method**: POST
- **URL**: `http://localhost:5000/api/token/refresh/`
- **Body** (raw JSON):
```json
{
    "refresh": "<your_refresh_token>"
}
```

## API Endpoints

### Categories

#### List All Categories
- **Method**: GET
- **URL**: `http://localhost:5000/api/inventory/categories/`
- **Auth**: Bearer Token

#### Create a Category
- **Method**: POST
- **URL**: `http://localhost:5000/api/inventory/categories/`
- **Auth**: Bearer Token
- **Body** (raw JSON):
```json
{
    "name": "New Category",
    "description": "Description of the category"
}
```

#### Retrieve a Category
- **Method**: GET
- **URL**: `http://localhost:5000/api/inventory/categories/{id}/`
- **Auth**: Bearer Token

#### Update a Category (Full)
- **Method**: PUT
- **URL**: `http://localhost:5000/api/inventory/categories/{id}/`
- **Auth**: Bearer Token
- **Body** (raw JSON):
```json
{
    "name": "Updated Category Name",
    "description": "Updated description"
}
```

#### Update a Category (Partial)
- **Method**: PATCH
- **URL**: `http://localhost:5000/api/inventory/categories/{id}/`
- **Auth**: Bearer Token
- **Body** (raw JSON):
```json
{
    "description": "Updated description only"
}
```

#### Delete a Category
- **Method**: DELETE
- **URL**: `http://localhost:5000/api/inventory/categories/{id}/`
- **Auth**: Bearer Token

### Products

#### List All Products
- **Method**: GET
- **URL**: `http://localhost:5000/api/inventory/products/`
- **Auth**: Bearer Token

#### Create a Product
- **Method**: POST
- **URL**: `http://localhost:5000/api/inventory/products/`
- **Auth**: Bearer Token
- **Body** (raw JSON):
```json
{
    "name": "New Product",
    "description": "Description of the product",
    "category": 1,
    "unit": "pcs",
    "price": 19.99,
    "reorder_level": 10
}
```

#### Retrieve a Product
- **Method**: GET
- **URL**: `http://localhost:5000/api/inventory/products/{id}/`
- **Auth**: Bearer Token

#### Update a Product (Full)
- **Method**: PUT
- **URL**: `http://localhost:5000/api/inventory/products/{id}/`
- **Auth**: Bearer Token
- **Body** (raw JSON):
```json
{
    "name": "Updated Product Name",
    "description": "Updated description",
    "category": 1,
    "unit": "pcs",
    "price": 24.99,
    "reorder_level": 15
}
```

#### Update a Product (Partial)
- **Method**: PATCH
- **URL**: `http://localhost:5000/api/inventory/products/{id}/`
- **Auth**: Bearer Token
- **Body** (raw JSON):
```json
{
    "price": 29.99
}
```

#### Delete a Product
- **Method**: DELETE
- **URL**: `http://localhost:5000/api/inventory/products/{id}/`
- **Auth**: Bearer Token

#### Get Product Stock Level
- **Method**: GET
- **URL**: `http://localhost:5000/api/inventory/products/{id}/stock_level/`
- **Auth**: Bearer Token

#### Get Product Transactions
- **Method**: GET
- **URL**: `http://localhost:5000/api/inventory/products/{id}/transactions/`
- **Auth**: Bearer Token

### Stock

#### List All Stock
- **Method**: GET
- **URL**: `http://localhost:5000/api/inventory/stock/`
- **Auth**: Bearer Token

#### Get Low Stock Items
- **Method**: GET
- **URL**: `http://localhost:5000/api/inventory/stock/low_stock/`
- **Auth**: Bearer Token

### Transactions

#### List All Transactions
- **Method**: GET
- **URL**: `http://localhost:5000/api/inventory/transactions/`
- **Auth**: Bearer Token

#### Create a Transaction (Stock In)
- **Method**: POST
- **URL**: `http://localhost:5000/api/inventory/transactions/`
- **Auth**: Bearer Token
- **Body** (raw JSON):
```json
{
    "product": 1,
    "transaction_type": "IN",
    "quantity": 50,
    "supplier": 1,
    "notes": "Initial stock"
}
```

#### Create a Transaction (Stock Out)
- **Method**: POST
- **URL**: `http://localhost:5000/api/inventory/transactions/`
- **Auth**: Bearer Token
- **Body** (raw JSON):
```json
{
    "product": 1,
    "transaction_type": "OUT",
    "quantity": 10,
    "notes": "Stock out for customer"
}
```

### Stock Adjustments

#### List All Stock Adjustments
- **Method**: GET
- **URL**: `http://localhost:5000/api/inventory/stock-adjustments/`
- **Auth**: Bearer Token

#### Create a Stock Adjustment
- **Method**: POST
- **URL**: `http://localhost:5000/api/inventory/stock-adjustments/`
- **Auth**: Bearer Token
- **Body** (raw JSON):
```json
{
    "product": 1,
    "adjustment_type": "ADD",
    "quantity": 5,
    "reason": "Found extra items in storage"
}
```

### Suppliers

#### List All Suppliers
- **Method**: GET
- **URL**: `http://localhost:5000/api/inventory/suppliers/`
- **Auth**: Bearer Token

#### Create a Supplier
- **Method**: POST
- **URL**: `http://localhost:5000/api/inventory/suppliers/`
- **Auth**: Bearer Token
- **Body** (raw JSON):
```json
{
    "name": "New Supplier",
    "contact_person": "John Doe",
    "address": "123 Supplier St",
    "phone": "1234567890",
    "email": "supplier@example.com"
}
```

#### Retrieve a Supplier
- **Method**: GET
- **URL**: `http://localhost:5000/api/inventory/suppliers/{id}/`
- **Auth**: Bearer Token

#### Update a Supplier (Full)
- **Method**: PUT
- **URL**: `http://localhost:5000/api/inventory/suppliers/{id}/`
- **Auth**: Bearer Token
- **Body** (raw JSON):
```json
{
    "name": "Updated Supplier",
    "contact_person": "Jane Smith",
    "address": "456 New St",
    "phone": "0987654321",
    "email": "updated@example.com"
}
```

#### Update a Supplier (Partial)
- **Method**: PATCH
- **URL**: `http://localhost:5000/api/inventory/suppliers/{id}/`
- **Auth**: Bearer Token
- **Body** (raw JSON):
```json
{
    "contact_person": "New Contact Person"
}
```

#### Delete a Supplier
- **Method**: DELETE
- **URL**: `http://localhost:5000/api/inventory/suppliers/{id}/`
- **Auth**: Bearer Token

#### Get Supplier Transactions
- **Method**: GET
- **URL**: `http://localhost:5000/api/inventory/suppliers/{id}/transactions/`
- **Auth**: Bearer Token

## Troubleshooting

### Authentication Issues

1. **401 Unauthorized**
   - Check that you're including the correct Authorization header
   - Ensure your token hasn't expired
   - Try refreshing the token using the token/refresh endpoint

2. **403 Forbidden**
   - Your user might not have the necessary permissions
   - Some endpoints require staff or admin privileges

### Content Type Issues

- Always set Content-Type header to `application/json` for request bodies
- Ensure your JSON is valid (no trailing commas, proper quotes, etc.)

### Request Format Issues

- Double check field names match exactly what the API expects
- Ensure all required fields are included in your request
- For PUT requests, include all fields, not just the ones you're changing