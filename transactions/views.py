from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Transaction, Account, Category
from .forms import TransactionForm
from .utils import compute_summary, transactions_by_period

def home(request):
    return render(request, 'base.html')

@login_required
def dashboard(request):
    user = request.user
    summary = compute_summary(user)
    recent = Transaction.objects.filter(user=user)[:6]
    return render(request, "transactions/dashboard.html", {"summary": summary, "recent": recent})

@login_required
def transaction_list(request):
    user = request.user
    qs = Transaction.objects.filter(user=user)
    t_type = request.GET.get("type")
    if t_type in ("income", "expense"):
        qs = qs.filter(t_type=t_type)
    return render(request, "transactions/transaction_list.html", {"transactions": qs})

@login_required
def transaction_create(request):
    if request.method == "POST":
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            tr = form.save(commit=False)
            tr.user = request.user
            tr.save()
            return redirect("transactions:transaction_list")
    else:
        form = TransactionForm(user=request.user)
    return render(request, "transactions/transaction_form.html", {"form": form})

@login_required
def transaction_update(request, pk):
    tr = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == "POST":
        form = TransactionForm(request.POST, instance=tr, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("transactions:transaction_list")
    else:
        form = TransactionForm(instance=tr, user=request.user)
    return render(request, "transactions/transaction_form.html", {"form": form})

@login_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    transaction.delete()
    return redirect("transactions:transaction_list")

@login_required
def report_view(request):
    start = request.GET.get("start")
    end = request.GET.get("end")
    user = request.user
    data = transactions_by_period(user, start, end)
    return render(request, "transactions/reports.html", {"data": data})

@login_required
def accounts(request):
    accs = Account.objects.filter(user=request.user)
    return render(request, "transactions/accounts.html", {"accounts": accs})

@login_required
def account_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        initial_balance = request.POST.get("initial_balance", 0)
        currency = request.POST.get("currency", "UZS")

        Account.objects.create(
            user=request.user,
            name=name,
            initial_balance=initial_balance,
            currency=currency,
        )
        return redirect("transactions:accounts")
    return render(request, "transactions/account_form.html")

@login_required
def account_edit(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)

    if request.method == "POST":
        account.name = request.POST.get("name")
        account.initial_balance = request.POST.get("initial_balance")
        account.save()
        return redirect("transactions:accounts")

    return render(request, "transactions/account_edit.html", {"account": account})

@login_required
def categories(request):
    cats = Category.objects.filter(user=request.user)
    return render(request, "transactions/categories.html", {"categories": cats})


@login_required
def category_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        type_ = request.POST.get("type")
        if name and type_:
            Category.objects.create(
                user=request.user,
                name=name,
                type=type_
            )
    return redirect("transactions:categories")





