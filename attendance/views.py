from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.core.mail import EmailMessage
from django.utils.formats import date_format
from io import BytesIO
import qrcode
from .models import Employee, Attendance

# Home view for employee login
def home(request):
    return render(request, 'attendance/home.html')


# Generate QR code for employee attendance
def generate_qr_code(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    qr_code_url = f"http://192.168.0.22:8000/submit_attendance/emp-{employee_id}/"
    qr = qrcode.make(qr_code_url)

    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    buffer.seek(0)

    response = HttpResponse(buffer, content_type="image/png")
    response['Content-Disposition'] = f'attachment; filename="qr_code_emp_{employee_id}.png"'
    return response


# Display employee details and QR code
def employee_detail(request):
    employee_id = request.GET.get('employee_id')
    
    if employee_id:
        try:
            employee = get_object_or_404(Employee, employee_id=employee_id)
            return render(request, 'attendance/employee_detail.html', {'employee': employee})
        except ValueError:
            return HttpResponse("Invalid employee ID provided.", status=400)
    return HttpResponse("Employee ID not provided.", status=400)


# Submit attendance (check-in and check-out) based on QR code
def submit_attendance(request, qr_code):
    employee_id = qr_code.split('-')[-1]  
    employee = get_object_or_404(Employee, id=employee_id)
    today = timezone.now().date()
    attendance = Attendance.objects.filter(employee=employee, check_in_time__date=today).first()

    if attendance and not attendance.check_out_time:
        # Check-out process
        attendance.check_out_time = timezone.now()
        attendance.save()
        local_check_out_time = timezone.localtime(attendance.check_out_time)
        check_out_time_formatted = f"{date_format(local_check_out_time, 'DATE_FORMAT')}, {date_format(local_check_out_time, 'TIME_FORMAT')}"

        return render(request, 'attendance/attendance_confirmation.html', {
            'message': f"Check-out successful for {employee.name}.",
            'check_out_time': check_out_time_formatted,
            'quote': "Success is not the key to happiness. Happiness is the key to success."
        })

    elif not attendance:
        # Check-in process
        attendance = Attendance.objects.create(employee=employee, check_in_time=timezone.now())
        local_check_in_time = timezone.localtime(attendance.check_in_time)
        check_in_time_formatted = f"{date_format(local_check_in_time, 'DATE_FORMAT')}, {date_format(local_check_in_time, 'TIME_FORMAT')}"

        return render(request, 'attendance/attendance_confirmation.html', {
            'message': f"Attendance submitted for {employee.name}.",
            'check_in_time': check_in_time_formatted,
            'quote': "The journey of a thousand miles begins with one step."
        })
    
    return HttpResponse(f"Attendance already recorded for {employee.name}.")


# Attendance list for HR dashboard
def attendance_list(request):
    attendances = Attendance.objects.all().order_by('-check_in_time')  # Order by check-in time
    return render(request, 'attendance/attendance_list.html', {'attendances': attendances})


# Generate and send daily report via email
def generate_and_send_report():
    today = timezone.now().date()
    attendance_records = Attendance.objects.filter(check_in_time__date=today)

    if attendance_records.exists():
        report = "Today's Attendance Report:\n"
        for record in attendance_records:
            report += f"{record.employee.name}: Check-in: {record.check_in_time}, Check-out: {record.check_out_time}\n"

        email = EmailMessage(
            'Daily Attendance Report',
            report,
            'your-email@example.com',  # Replace with your sender email
            ['hr@example.com'],  # Replace with the HR email
        )
        email.send()


# View for generating the report (for HR)
def generate_report(request):
    generate_and_send_report()  # Call the function to generate and send the report
    return HttpResponse("Attendance report has been sent to HR.")


# Index view (if needed)
def index(request):
    return render(request, 'attendance/index.html')
