from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


User = settings.AUTH_USER_MODEL

class Currency(models.TextChoices):
    UZS = "UZS", _("UZS")
    USD = "USD", _("USD")

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    name = models.CharField(max_length=100)
    initial_balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.UZS)

    def __str__(self):
        return f"{self.name} ({self.currency})"

class Category(models.Model):
    INCOME = "income"
    EXPENSE = "expense"
    TYPE_CHOICES = [(INCOME, "Income"), (EXPENSE, "Expense")]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    icon = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.type})"

class Transaction(models.Model):
    INCOME = "income"
    EXPENSE = "expense"

    TRANSACTION_TYPE = [(INCOME, "Income"), (EXPENSE, "Expense")]
    PAYMENT_METHODS = [("cash", "Cash"), ("card", "Card"), ("bank", "Bank")]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions")
    t_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.UZS)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default="cash")
    date = models.DateField()
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.get_t_type_display()} {self.amount} {self.currency}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
