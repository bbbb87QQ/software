from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),                     # 首頁（公開）
    path('login/', views.login_view, name='login'),             # 登入頁
    path('logout/', views.logout_view, name='logout'),          # 登出功能
    path('admin-only/', views.admin_only_view, name='admin_only'), # 管理員門禁測試頁
]