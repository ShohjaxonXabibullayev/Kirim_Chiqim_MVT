from django.contrib import admin
from .models import Account, Category, Transaction

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "currency", "initial_balance")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "type")

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("t_type", "amount", "currency", "user", "date", "category", "payment_method")
    list_filter = ("t_type", "currency", "payment_method", "date")

