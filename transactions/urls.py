from django.urls import path
from .views import *

app_name = "transactions"
urlpatterns = [
    path("", home, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("transactions/", transaction_list, name="transaction_list"),
    path("transactions/create/", transaction_create, name="transaction_create"),
    path("transactions/<int:pk>/edit/", transaction_update, name="transaction_update"),
    path("<int:pk>/delete/", transaction_delete, name="transaction_delete"),
    path("reports/", report_view, name="reports"),
    path("accounts/", accounts, name="accounts"),
    path("accounts/create/", account_create, name="account_create"),
    path("accounts/<int:pk>/edit/", account_edit, name="account_edit"),
    path("categories/", categories, name="categories"),
    path("categories/create/", category_create, name="category_create")
]
