from django.contrib import admin
from .models import TimeOffType, TimeOffRequest, TimeOffBalance


@admin.register(TimeOffType)
class TimeOffTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']


@admin.register(TimeOffRequest)
class TimeOffRequestAdmin(admin.ModelAdmin):
    list_display = ['employee', 'time_off_type', 'start_date', 'end_date', 'allocation', 'status', 'created_at']
    list_filter = ['status', 'time_off_type', 'created_at']
    search_fields = ['employee__login_id', 'reason']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Request Information', {
            'fields': ('employee', 'time_off_type', 'start_date', 'end_date', 'allocation')
        }),
        ('Validity Period', {
            'fields': ('validity_period_start', 'validity_period_end')
        }),
        ('Details', {
            'fields': ('reason', 'attachment')
        }),
        ('Status', {
            'fields': ('status', 'reviewed_by', 'reviewed_at', 'review_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TimeOffBalance)
class TimeOffBalanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'time_off_type', 'total_days', 'used_days', 'available_days', 'year']
    list_filter = ['time_off_type', 'year']
    search_fields = ['employee__login_id']