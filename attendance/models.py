from django.db import models
from django.conf import settings
from datetime import datetime, timedelta

class Attendance(models.Model):
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    
    date = models.DateField()
    
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)

    class Meta:
        unique_together = ('employee', 'date')
        verbose_name_plural = "Attendance"

    def __str__(self):
        return f"{self.employee} - {self.date}"

    @property
    def work_hours(self):
        if self.check_in and self.check_out:
            start = datetime.combine(self.date, self.check_in)
            end = datetime.combine(self.date, self.check_out)
            return end - start
        return timedelta(0)

    @property
    def extra_hours(self):
        standard_shift = timedelta(hours=8)
        total = self.work_hours
        if total > standard_shift:
            return total - standard_shift
        return timedelta(0)