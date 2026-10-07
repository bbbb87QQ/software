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

#測試資料(先給ui用的)
def home_view(request):
    classrooms = [
        {
            "id": 1,
            "name": "A101",
            "capacity": 40,
            "equipment": ["投影機", "白板"],
        },
        {
            "id": 2,
            "name": "A102",
            "capacity": 60,
            "equipment": ["投影機", "麥克風"],
        },
    ]

    reservations = [
        {
            "classroom_id": 1,
            "date": "2026-10-08",
            "start_time": "09:00",
            "end_time": "10:00",
        }
    ]

    time_slots = [
        {"id": 1, "label": "09:00–10:00", "available": False},
        {"id": 2, "label": "10:00–11:00", "available": True},
        {"id": 3, "label": "11:00–12:00", "available": True},
    ]

    return render(request, "home.html", {
    "classrooms": classrooms,
    "time_slots": time_slots,
})

@borrower_required
def reservation_view(request):
    time_slots = {
        "1": "09:00-10:00",
        "2": "10:00-11:00",
        "3": "11:00-12:00",
    }

    classroom = request.GET.get("classroom", "")
    date = request.GET.get("date", "")
    slot_id = request.GET.get("slot", "")
    slot_label = time_slots.get(slot_id)

    if classroom not in ["A101", "A102"] or not slot_label:
        messages.error(request, "請從首頁選擇教室與時段。")
        return redirect("home")

    if request.method == "POST":
        purpose = request.POST.get("purpose", "").strip()

        if purpose:
            messages.success(
                request,
                f"模擬預約成功：{classroom}，{date}，{slot_label}"
            )
            return redirect("home")

        messages.error(request, "請填寫借用用途。")

    return render(request, "reservation.html", {
        "classroom": classroom,
        "date": date,
        "slot_label": slot_label,
    })