from rest_framework import serializers
from inventory.models import Category, Product, Stock, Supplier, Transaction, StockAdjustment


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    """
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    """
    category_name = serializers.ReadOnlyField(source='category.name')
    current_stock = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'category_name', 
                 'unit', 'price', 'reorder_level', 'current_stock', 
                 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'current_stock']
    
    def get_current_stock(self, obj):
        try:
            return obj.stock.quantity
        except Stock.DoesNotExist:
            return 0


class StockSerializer(serializers.ModelSerializer):
    """
    Serializer for the Stock model.
    """
    product_name = serializers.ReadOnlyField(source='product.name')
    unit = serializers.ReadOnlyField(source='product.unit')
    
    class Meta:
        model = Stock
        fields = ['id', 'product', 'product_name', 'quantity', 'unit', 'updated_at']
        read_only_fields = ['updated_at']


class SupplierSerializer(serializers.ModelSerializer):
    """
    Serializer for the Supplier model.
    """
    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Transaction model.
    """
    product_name = serializers.ReadOnlyField(source='product.name')
    supplier_name = serializers.ReadOnlyField(source='supplier.name', default=None)
    username = serializers.ReadOnlyField(source='user.username')
    transaction_type_display = serializers.CharField(source='get_transaction_type_display', read_only=True)
    
    class Meta:
        model = Transaction
        fields = ['id', 'product', 'product_name', 'transaction_type', 
                 'transaction_type_display', 'quantity', 'supplier', 
                 'supplier_name', 'user', 'username', 'transaction_date', 'notes']
        read_only_fields = ['user', 'transaction_date']
    
    def create(self, validated_data):
        """
        Create a new transaction and update stock accordingly.
        """
        return Transaction.objects.create(**validated_data)


class StockAdjustmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the StockAdjustment model.
    """
    product_name = serializers.ReadOnlyField(source='product.name')
    username = serializers.ReadOnlyField(source='user.username')
    adjustment_type_display = serializers.CharField(source='get_adjustment_type_display', read_only=True)
    
    class Meta:
        model = StockAdjustment
        fields = ['id', 'product', 'product_name', 'adjustment_type', 
                 'adjustment_type_display', 'quantity', 'reason', 
                 'user', 'username', 'adjustment_date']
        read_only_fields = ['user', 'adjustment_date']
    
    def create(self, validated_data):
        """
        Create a new stock adjustment and update stock accordingly.
        """
        return StockAdjustment.objects.create(**validated_data)
