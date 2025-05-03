#!/bin/bash

# Set variables
API_URL="http://localhost:5000/api"
USERNAME="admin"
PASSWORD="adminpassword"

# Function to get JWT token
get_token() {
    response=$(curl -s -X POST -H "Content-Type: application/json" -d '{"username":"'$USERNAME'", "password":"'$PASSWORD'"}' $API_URL/token/)
    access_token=$(echo $response | grep -o '"access":"[^"]*"' | cut -d '"' -f 4)
    echo $access_token
}

# Get token
echo "Getting JWT token..."
ACCESS_TOKEN=$(get_token)

if [ -z "$ACCESS_TOKEN" ]; then
    echo "Failed to get access token. Check your credentials."
    exit 1
fi

echo "Token obtained successfully."
echo ""

# Test API root endpoint
echo "Testing API root endpoint..."
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" $API_URL/ | python -m json.tool
echo ""

# Test categories endpoint
echo "Testing categories endpoint..."
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" $API_URL/inventory/categories/ | python -m json.tool
echo ""

# Test products endpoint
echo "Testing products endpoint..."
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" $API_URL/inventory/products/ | python -m json.tool
echo ""

# Test stock endpoint
echo "Testing stock endpoint..."
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" $API_URL/inventory/stock/ | python -m json.tool
echo ""

# Test suppliers endpoint
echo "Testing suppliers endpoint..."
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" $API_URL/inventory/suppliers/ | python -m json.tool
echo ""

# Test transactions endpoint
echo "Testing transactions endpoint..."
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" $API_URL/inventory/transactions/ | python -m json.tool
echo ""

# Test low stock report
echo "Testing low stock report..."
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" $API_URL/inventory/stock/low_stock/ | python -m json.tool
echo ""

# Create a new category (staff only)
echo "Creating a new category..."
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" -H "Content-Type: application/json" -d '{"name":"Test Category", "description":"Test Description"}' $API_URL/inventory/categories/ | python -m json.tool
echo ""

# Test user profile endpoint
echo "Testing user profile endpoint..."
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" $API_URL/users/profile/ | python -m json.tool
echo ""

echo "API tests completed."
