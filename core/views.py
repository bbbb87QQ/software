from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse
from .decorators import admin_required, borrower_required

# 1. 登入功能
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                role = getattr(user, 'profile', None)
                role_name = role.get_role_display() if role else "使用者"
                messages.success(request, f"登入成功！身分：{role_name}")
                
                # 如果使用者原本是要去某個受保護頁面被踢過來的，登入後自動帶他回去
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('home')
        else:
            messages.error(request, "帳號或密碼錯誤，請重新輸入。")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


# 2. 登出功能
def logout_view(request):
    logout(request)
    messages.info(request, "您已成功登出。")
    return redirect('home')


# 3. 公開首頁（不掛門禁，任何人沒登入都能看）
def home_view(request):
    return render(request, 'home.html')


# 4. 門禁套用示範：管理員專區（掛上 @admin_required，只有管理員能進）
@admin_required
def admin_only_view(request):
    return HttpResponse("<h1>🎉 恭喜！你成功通過門禁，進入了【管理員專區】！</h1><a href='/'>回首頁</a>")