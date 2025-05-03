# Stock Management System API

A comprehensive Django REST API for stock management with JWT authentication, providing robust inventory tracking, transaction management, and supplier integration.

## Features

- **Django REST Framework Backend**: Complete API with interactive documentation
- **JWT Authentication**: Secure token-based authentication system
- **Inventory Management**: Track products, categories, and stock levels
- **Transaction Tracking**: Record all stock movements with detailed reporting
- **Supplier Integration**: Manage supplier relationships and track supplier-specific transactions
- **Low Stock Alerts**: Monitor inventory levels and receive alerts when stock is low
- **Dashboard Customization**: Personalized widget-based dashboard for users

## API Capabilities

- **Complete CRUD Operations**: All entities support Create, Read, Update, Delete operations
- **Advanced Filtering**: Filter products by category, price range, stock level, etc.
- **Search Functionality**: Search across products, transactions, and suppliers
- **Sorting and Pagination**: Sort results and navigate through paginated responses

## Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. Register a user account
2. Obtain access and refresh tokens
3. Include the access token in the Authorization header for protected endpoints
4. Refresh tokens as needed

## Development

### Prerequisites

- Python 3.8+
- PostgreSQL
- Django 4.0+

### Setting Up for Development

1. Clone the repository
   ```bash
   git clone https://github.com/[your-username]/stock-management-api.git
   cd stock-management-api
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your database in settings.py or through environment variables

5. Run migrations
   ```bash
   cd stock_management
   python manage.py migrate
   ```

6. Create a superuser
   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server
   ```bash
   python manage.py runserver
   ```

8. Load demo data (optional)
   ```bash
   python add_demo_data.py
   ```

### API Testing

See the included [Postman guide](stock_management/postman_guide.md) for detailed examples of how to test all API endpoints.

## Dashboard Customization

The system includes a personalized dashboard feature that allows users to:

- Add, remove, and rearrange widgets on their dashboard
- Enable/disable specific widgets
- Configure widget settings
- Leverage various widget types (statistics, charts, alerts, etc.)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

Based on the original stock management system by [DonGuillotine](https://github.com/DonGuillotine/stock-management-system), with significant enhancements to the API functionality and dashboard customization features.