import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models
from django.utils import timezone

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)  # Field for telephone
    employee_id = models.CharField(max_length=20, unique=True, null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Generate new employee_id if creating a new Employee
        if self.pk is None:
            existing_ids = Employee.objects.values_list('employee_id', flat=True)
            existing_ids = [int(emp_id) for emp_id in existing_ids if emp_id.isdigit()]  # Convert to int if it's a digit
            new_id = str(max(existing_ids) + 1) if existing_ids else '1001'  # Start from '1001' if no existing IDs
            self.employee_id = new_id  # Assign new employee_id

        super().save(*args, **kwargs)  # Save first to generate an ID if necessary

        # Generate and save QR code after saving the Employee
        qr_data = f"emp-{self.employee_id}"  # Use employee ID for QR code
        qr_img = qrcode.make(qr_data)

        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        file_name = f"qr_code_emp_{self.employee_id}.png"

        # Save the QR code image to the model's field
        self.qr_code.save(file_name, File(buffer), save=False)
        super().save(*args, **kwargs)  # Final save to ensure the image is saved

    def __str__(self):
        return self.name


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(default=timezone.now)
    check_out_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee.name} - {self.check_in_time} - {self.check_out_time or 'Not checked out yet'}"
