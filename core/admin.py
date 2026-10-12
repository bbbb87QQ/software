from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # 設定在後台清單頁面要顯示的欄位
    list_display = ('user', 'role') 
    
    # 在右側加上一個側邊欄，讓您可以快速篩選「系統管理員」或「借用人」
    list_filter = ('role',) 
    
    # 增加一個搜尋框，允許您透過使用者的帳號名稱來搜尋
    search_fields = ('user__username',)