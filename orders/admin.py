from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price', 'subtotal']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'full_name', 'total', 'status', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method', 'payment_status']
    list_editable = ['status']
    search_fields = ['order_number', 'full_name', 'email', 'phone']
    readonly_fields = ['order_number', 'subtotal', 'total', 'created_at']
    inlines = [OrderItemInline]
