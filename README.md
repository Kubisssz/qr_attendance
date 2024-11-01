# QR Attendance System

## Overview
This project is a simple QR Attendance System developed using Django. It allows employees to mark their attendance by scanning a QR code. The system displays a unique QR code for each employee, which they can scan to submit their attendance. This project aims to streamline the attendance tracking process and is suitable for small to medium-sized organizations.

## Features
- **QR Code Attendance**: Employees can mark their attendance by scanning a QR code.
- **Automatic QR Code Generation**: QR codes are generated automatically for each employee.
- **User-Friendly Interface**: Simple and intuitive design for ease of use.
- **Confirmation Messages**: Users receive confirmation messages upon successful attendance submission.

## Requirements
- **Python**: Version 3.x
- **Django**: A web framework for building the application.
- **SQLite** (or any other preferred database management system).
- **(Optional)**: Virtual environment for managing dependencies.

## Getting Started

### Installation

1. **Clone the Repository**
   Clone this repository to your local machine using the following command:
   ```bash
   git clone https://github.com/Kubisssz/qr_attendance.git
   
2. **Navigate to the Project Directory**
    Navigate to the Project Directory Change your directory to the project folder:
   ```bash
   cd qr_attendance

3. **Install Requirements**
     It is recommended to create a virtual environment and activate it. Then, install the required packages:
    ```bash
    pip install -r requirements.txt

4.**Run Migrations**
     Run Migrations Apply database migrations to set up the initial database schema:
   ```bash
   python manage.py migrate









