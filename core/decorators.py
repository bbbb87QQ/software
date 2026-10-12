from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def admin_required(view_func):
    """
    【管理員門禁卡】：
    1. 沒登入 -> 踢去登入頁面
    2. 已登入但不是管理員 -> 提示權限不足，擋下來
    3. 是管理員 -> 放行
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # 1. 檢查是否登入
        if not request.user.is_authenticated:
            messages.warning(request, "請先登入管理員帳號！")
            return redirect('login')
        
        # 2. 檢查身分牌是否為管理員
        profile = getattr(request.user, 'profile', None)
        if profile and profile.is_admin():
            return view_func(request, *args, **kwargs)
        
        # 3. 身分不符，跳出提示並導回首頁/登入頁
        messages.error(request, "權限不足：此功能僅限系統管理員操作！")
        return redirect('login')
    return _wrapped_view


def borrower_required(view_func):
    """
    【借用人門禁卡】：
    滿足你剛才提的「平常查教室不用登入，要借用時才強制要求登入」！
    組員 4 做預約借用功能時，直接把這個掛在借用按鈕/函式上面即可。
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "請先登入帳號以進行教室借用！")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view