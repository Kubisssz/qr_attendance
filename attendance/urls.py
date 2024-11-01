from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    # Employee part
    path('', views.home, name='attendance_home'),  # Home page for employees
    path('employee/', views.employee_detail, name='employee_detail'),  # Employee detail page
    path('generate_qr/<int:employee_id>/', views.generate_qr_code, name='generate_qr_code'),  # Generate QR code
    path('submit_attendance/<str:qr_code>/', views.submit_attendance, name='submit_attendance'),  # Submit attendance via QR code
    path('attendance_list/', views.attendance_list, name='attendance_list'),  # List of attendance records
    
    # HR part
    path('attendance/report/', views.generate_report, name='attendance_report'),  # Direct access for generating attendance report
]
