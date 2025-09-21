from django.db.models import Sum
from .models import Transaction
from datetime import datetime


def compute_summary(user, currency=None):
    """
    Umumiy kirim va chiqimni hisoblab, balans va foizlarini qaytaradi.
    """
    qs = Transaction.objects.filter(user=user)
    if currency:
        qs = qs.filter(currency=currency)

    income_total = (
        qs.filter(t_type=Transaction.INCOME)
        .aggregate(total=Sum("amount"))["total"]
        or 0
    )
    expense_total = (
        qs.filter(t_type=Transaction.EXPENSE)
        .aggregate(total=Sum("amount"))["total"]
        or 0
    )

    balance = income_total - expense_total
    total = income_total + expense_total

    income_percent = (income_total / total * 100) if total else 0
    expense_percent = (expense_total / total * 100) if total else 0

    return {
        "income_total": income_total,
        "expense_total": expense_total,
        "balance": balance,
        "income_percent": round(income_percent, 2),
        "expense_percent": round(expense_percent, 2),
    }


def transactions_by_period(user, start=None, end=None, currency=None):
    """
    Berilgan davr bo‘yicha tranzaksiyalarni qaytaradi:
    - umumiy kirim/chiqim
    - kategoriya bo‘yicha yig‘indi va foizlar
    - davr ichidagi yozuvlar
    """
    qs = Transaction.objects.filter(user=user)

    if currency:
        qs = qs.filter(currency=currency)

    if start:
        try:
            s = datetime.fromisoformat(start).date()
            qs = qs.filter(date__gte=s)
        except ValueError:
            pass
    if end:
        try:
            e = datetime.fromisoformat(end).date()
            qs = qs.filter(date__lte=e)
        except ValueError:
            pass

    income_by_cat = (
        qs.filter(t_type=Transaction.INCOME)
        .values("category__name")
        .annotate(total=Sum("amount"))
    )
    expense_by_cat = (
        qs.filter(t_type=Transaction.EXPENSE)
        .values("category__name")
        .annotate(total=Sum("amount"))
    )

    income_total_period = (
        qs.filter(t_type=Transaction.INCOME).aggregate(total=Sum("amount"))["total"]
        or 0
    )
    expense_total_period = (
        qs.filter(t_type=Transaction.EXPENSE).aggregate(total=Sum("amount"))["total"]
        or 0
    )

    def with_percent(rows, total):
        res = []
        for row in rows:
            percent = (row["total"] / total * 100) if total else 0
            res.append({
                "category__name": row["category__name"],
                "total": row["total"],
                "percent": round(percent, 2),
            })
        return res

    return {
        "transactions": qs,
        "income_by_cat": with_percent(income_by_cat, income_total_period),
        "expense_by_cat": with_percent(expense_by_cat, expense_total_period),
        "income_total_period": income_total_period,
        "expense_total_period": expense_total_period,
        "summary": compute_summary(user, currency),
    }
