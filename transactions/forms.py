from django import forms
from .models import Transaction, Account, Category

class TransactionForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={"type":"date"}))
    class Meta:
        model = Transaction
        fields = ["t_type", "amount", "currency", "payment_method", "date", "account", "category", "note"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["account"].queryset = Account.objects.filter(user=user)
            self.fields["category"].queryset = Category.objects.filter(user=user)
