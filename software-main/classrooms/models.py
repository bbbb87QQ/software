from django.db import models

class Classroom(models.Model):
    name = models.CharField(max_length=50, verbose_name="教室名稱")
    capacity = models.IntegerField(verbose_name="容納人數")
    equipment = models.CharField(max_length=255, blank=True, verbose_name="設備")

    def __str__(self):
        return self.name

class Booking(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, verbose_name="教室")
    date = models.DateField(verbose_name="借用日期")
    time_slot = models.CharField(max_length=50, verbose_name="借用時段 (例: 09:00-10:00)")
    status = models.CharField(max_length=20, default='Booked', verbose_name="狀態")

    def __str__(self):
        return f"{self.classroom.name} - {self.date} ({self.time_slot})"