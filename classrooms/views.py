from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from django.contrib import messages 
from core.decorators import borrower_required
from .models import Classroom, Booking

def classroom_query_view(request):
    date = request.GET.get('date')
    time_slot = request.GET.get('time_slot')

    print("--- 收到前端傳來的參數 ---")
    print(f"date: {repr(date)}")
    print(f"time_slot: {repr(time_slot)}")
    
    if date:
        date = date.replace('/', '-')
    
    classrooms = Classroom.objects.all()
    result = []
    
    booked_room_ids = []
    if date and time_slot:
        booked_room_ids = Booking.objects.filter(
            date=date, 
            time_slot=time_slot
        ).values_list('classroom_id', flat=True)

    for room in classrooms:
        is_booked = room.id in booked_room_ids
        result.append({
            'id': room.id,
            'name': room.name,
            'capacity': room.capacity,
            'equipment': room.equipment,
            'status': '已借用' if is_booked else '可借用'
        })
        
    # 如果是前端透過 API 請求，回傳 JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'data': result})
        
    return render(request, 'classrooms/query.html', {'classrooms': result})

@borrower_required
def reserve_classroom(request):
    if request.method == 'POST':
        room_name = request.POST.get('classroom')
        date_str = request.POST.get('date')
        slot = request.POST.get('slot')
        purpose = request.POST.get('purpose','').strip()

        classroom = get_object_or_404(Classroom, name=room_name)


        is_conflict=Booking.objects.filter(
            classroom=classroom,
            date=date_str,
            time_slot=slot,
            status='Booked'
        ).exists()
        # 檢查該時段是否已被預約（防撞時段）
        if is_conflict:
            messages.error(request, f"預約失敗: {classroom.name} 於 ({date_str} {slot}) 已被預約!")
            return render(
                request,'reservation.html',
                {'classroom':room_name,
                'date':date_str,
                'slot_label':slot,
                'purpose':purpose,}
            )
        Booking.objects.create(
            user=request.user,
            classroom=classroom,
            date=date_str,
            time_slot=slot,
            purpose=purpose,
            status='Booked'
        )
        messages.success(request, f"成功預約 {classroom.name} 於（{date_str} {slot})!")
        return redirect('home')

    context = {
        'classroom':request.GET.get('classroom', ''),
        'date':request.GET.get('date', ''),
        'slot_label': request.GET.get('slot', ''),
    }
    return render(request, 'reservation.html', context)
