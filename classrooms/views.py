from django.shortcuts import render
from django.http import JsonResponse
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