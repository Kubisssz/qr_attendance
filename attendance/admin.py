from django.contrib import admin
from .models import Employee, Attendance
from django.utils.html import format_html

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'qr_code_img')  # Include the QR code image in the display

    def qr_code_img(self, obj):
        if obj.qr_code:  # Check if there is a QR code
            return format_html('<img src="{}" width="100" height="100" />', obj.qr_code.url)  # Use format_html for safe HTML rendering
        return "No QR Code"

    qr_code_img.short_description = 'QR Code'  # Add a column header for clarity

admin.site.register(Employee, EmployeeAdmin)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'check_in_time', 'check_out_time')  # Display check-out time
    list_filter = ('check_in_time',)
    ordering = ('-check_in_time',)

# Register the models with their respective admin classes
admin.site.register(Attendance, AttendanceAdmin)
