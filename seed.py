import os
import django

# 1. 初始化 Django 設定環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'classroom_system.settings')
django.setup()

from django.contrib.auth.models import User
# 這裡請替換成 classrooms.models 裡面實際定義的 Model 名稱
# 例如：from classrooms.models import Classroom

def run_seed():
    print("🌱 開始建立種子資料...")

    # --- 建立使用者帳號 ---
    admin_user, created = User.objects.get_or_create(username='admin')
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        admin_user.profile.role = 'admin'
        admin_user.profile.save()
        print("✔ 管理員帳號建立完成: admin / admin123")

    borrower_user, created = User.objects.get_or_create(username='student01')
    if created:
        borrower_user.set_password('student123')
        borrower_user.save()
        borrower_user.profile.role = 'borrower'
        borrower_user.profile.save()
        print("✔ 借用人帳號建立完成: student01 / student123")

    # --- 建立教室資料（請依照組員寫的 classrooms/models.py 欄位微調）---
    # sample_classrooms = [
    #     {'name': 'INS-101', 'capacity': 60, 'equipment': '投影機、麥克風'},
    #     {'name': 'INS-201', 'capacity': 40, 'equipment': '投影機、電腦設備'},
    #     {'name': '大講堂', 'capacity': 150, 'equipment': '雙投影機、無線麥克風'},
    # ]
    # for c in sample_classrooms:
    #     Classroom.objects.get_or_create(name=c['name'], defaults=c)
    # print("✔ 教室資料建立完成！")

    print("🎉 種子資料建立完畢！")

if __name__ == '__main__':
    run_seed()