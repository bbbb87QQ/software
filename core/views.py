from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse
from .decorators import admin_required, borrower_required

# 引入你在 classrooms 建立的模型
from classrooms.models import Classroom, Booking


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


# 3. 門禁套用示範：管理員專區
@admin_required
def admin_only_view(request):
    return HttpResponse("<h1>🎉 恭喜！你成功通過門禁，進入了【管理員專區】！</h1><a href='/'>回首頁</a>")


# 4. 首頁：動態讀取真實資料庫與時段借用狀態
def home_view(request):
    classrooms = Classroom.objects.all()

    # 日期預設為 2026-10-08，也可以由前端傳入
    date = request.GET.get('date', '2026-10-08').replace('/', '-')
    
    # 預設教室為 A101
    classroom_name = request.GET.get('classroom', 'A101')

    # 定義時段對照表
    raw_slots = [
        {"id": "1", "label": "09:00–10:00", "time_slot": "09:00-10:00"},
        {"id": "2", "label": "10:00–11:00", "time_slot": "10:00-11:00"},
        {"id": "3", "label": "11:00–12:00", "time_slot": "11:00-12:00"},
    ]

    # 從真實資料庫找出該教室在該日期已被預約的時段
    booked_slots = Booking.objects.filter(
        classroom__name=classroom_name,
        date=date
    ).values_list('time_slot', flat=True)

    # 去除字串空格後比對狀態
    cleaned_booked_slots = [s.replace(' ', '') for s in booked_slots]

    time_slots = []
    for slot in raw_slots:
        is_booked = slot['time_slot'].replace(' ', '') in cleaned_booked_slots
        time_slots.append({
            "id": slot["id"],
            "label": slot["label"],
            "available": not is_booked  # 如果已被借用，available 就是 False
        })

    return render(request, "home.html", {
        "classrooms": classrooms,
        "time_slots": time_slots,
        "date": date,
        "classroom_name": classroom_name,
    })


# 5. 預約功能：真正寫入 Booking 資料庫
@borrower_required
def reservation_view(request):
    time_slots = {
        "1": "09:00-10:00",
        "2": "10:00-11:00",
        "3": "11:00-12:00",
    }

    classroom_name = request.GET.get("classroom", "") or request.POST.get("classroom", "")
    date = request.GET.get("date", "") or request.POST.get("date", "")
    slot_id = request.GET.get("slot", "") or request.POST.get("slot", "")
    slot_label = time_slots.get(str(slot_id))

    if not classroom_name or not slot_label or not date:
        messages.error(request, "請從首頁選擇教室與時段。")
        return redirect("home")

    if request.method == "POST":
        purpose = request.POST.get("purpose", "").strip()

        if purpose:
            # 取得對應教室實體
            classroom_obj = Classroom.objects.filter(name=classroom_name).first()
            if not classroom_obj:
                classroom_obj = Classroom.objects.create(name=classroom_name, capacity=40, equipment="投影機")

            # 真實寫入資料庫！
            Booking.objects.create(
                classroom=classroom_obj,
                date=date,
                time_slot=slot_label,
                status="Booked"
            )

            messages.success(
                request,
                f"預約成功：{classroom_name}，{date}，{slot_label}"
            )
            return redirect("home")

        messages.error(request, "請填寫借用用途。")

    return render(request, "reservation.html", {
        "classroom": classroom_name,
        "date": date,
        "slot_label": slot_label,
    })