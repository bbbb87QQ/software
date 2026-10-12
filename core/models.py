from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# 使用者擴充資料：區分「系統管理員」與「借用人」
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', '系統管理員'),
        ('borrower', '借用人'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='borrower', verbose_name="身分角色")

    def is_admin(self):
        return self.role == 'admin'

    def is_borrower(self):
        return self.role == 'borrower'

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

# 當系統每建立一個帳號，就自動幫他綁定一個 UserProfile（預設為借用人）
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()