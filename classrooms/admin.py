from django.contrib import admin
from .models import Classroom, Booking

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'equipment')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    # 列表顯示欄位：教室、借用人、日期、時段、狀態
    list_display = ('classroom', 'user', 'date', 'time_slot', 'status')
    # 提供快速篩選
    list_filter = ('date', 'status', 'classroom')
    # 搜尋欄位
    search_fields = ('user__username', 'classroom__name', 'purpose')