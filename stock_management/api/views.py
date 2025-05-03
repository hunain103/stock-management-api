from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.reverse import reverse


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_root(request, format=None):
    """
    API root endpoint that provides links to all other API endpoints.
    """
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'categories': reverse('category-list', request=request, format=format),
        'products': reverse('product-list', request=request, format=format),
        'stock': reverse('stock-list', request=request, format=format),
        'suppliers': reverse('supplier-list', request=request, format=format),
        'transactions': reverse('transaction-list', request=request, format=format),
    })
