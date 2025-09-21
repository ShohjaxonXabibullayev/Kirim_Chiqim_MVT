from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from .forms import CustomUserCreationForm, CustomAuthenticationForm
import random

User = get_user_model()


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Ro‘yxatdan o‘tish muvaffaqiyatli!")
            login(request, user)
            return redirect('accounts:profile')
        else:
            messages.error(request, "Formani to‘g‘ri to‘ldiring!")
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Tizimga muvaffaqiyatli kirdingiz!")
                return redirect('accounts:profile')
            else:
                messages.error(request, "Login yoki parol noto‘g‘ri")
        else:
            messages.error(request, "Forma noto‘g‘ri to‘ldirilgan")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'account/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Tizimdan chiqdingiz")
    return redirect('accounts:login')


@login_required
def profile_view(request):
    return render(request, 'account/profile.html', {'user': request.user})


@login_required
def profile_update_view(request):
    if request.method == "POST":
        user = request.user
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.phone = request.POST.get("phone")
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.save()
        return redirect("accounts:profile")

    return render(request, "account/profile_update.html")


@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Parol muvaffaqiyatli o‘zgartirildi!")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Parolni o‘zgartirishda xato")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'account/password_change.html', {'form': form})


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:

            code = str(random.randint(1000, 9999))


            request.session['reset_user_id'] = user.id
            request.session['reset_code'] = code


            print(f"Parolni tiklash kodi: {code}")

            messages.success(request, "Tasdiqlash kodi terminalga yuborildi. Uni kiriting.")
            return redirect('accounts:verify_reset_code')
        else:
            messages.error(request, "Bunday email topilmadi")
    return render(request, 'account/forgot_password.html')


def verify_reset_code_view(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        saved_code = request.session.get('reset_code')
        if code == saved_code:
            messages.success(request, "Kod to‘g‘ri! Endi yangi parol qo‘ying.")
            return redirect('accounts:reset_password')
        else:
            messages.error(request, "Kod noto‘g‘ri!")
    return render(request, 'account/verify_reset_code.html')


def reset_password_view(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Parollar bir xil bo‘lishi kerak!")
            return redirect('accounts:reset_password')

        user_id = request.session.get('reset_user_id')
        if not user_id:
            messages.error(request, "Sessiya muddati tugagan. Qayta urinib ko‘ring.")
            return redirect('accounts:forgot_password')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, "Foydalanuvchi topilmadi.")
            return redirect('accounts:forgot_password')

        user.set_password(password)
        user.save()

        request.session.pop('reset_user_id', None)
        request.session.pop('reset_code', None)

        messages.success(request, "Parol muvaffaqiyatli yangilandi! Endi login qiling.")
        return redirect('accounts:login')

    return render(request, 'account/reset_password.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Parolingiz muvaffaqiyatli o‘zgartirildi!")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Xatolik bor, qaytadan urinib ko‘ring.")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'account/change_password.html', {'form': form})
