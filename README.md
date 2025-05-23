# 🏥 Medical Appointment System

A comprehensive web-based medical appointment system built with Django that connects patients with doctors, enabling easy appointment scheduling, patient history tracking, and doctor reviews.

## ✨ Features

### 👥 User Management
- **🔐 Role-based Authentication**
  - Doctor registration and verification
  - Patient registration
  - Admin dashboard
  - Secure JWT authentication
  - Password reset functionality

- **👤 Profile Management**
  - Personal information management
  - Profile picture upload
  - Contact information
  - Location settings
  - Specialization details (for doctors)

### 👨‍⚕️ Doctor Features
- **📋 Profile Management**
  - Specialization selection
  - Consultation price setting
  - Professional certificate upload
  - Location management with GPS coordinates
  - Professional bio
  - Consultation hours

- **📅 Appointment Management**
  - Availability calendar
  - Appointment scheduling
  - Patient history tracking
  - Consultation notes
  - Payment tracking

### 👨‍💼 Patient Features
- **🔍 Search and Discovery**
  - Doctor search by specialization
  - Location-based search
  - Price filtering
  - Rating-based sorting
  - Availability checking

- **📱 Appointment Management**
  - Online booking
  - Appointment history
  - Medical records
  - Payment processing
  - Appointment reminders

- **⭐ Review System**
  - Doctor rating
  - Written reviews
  - Rating history
  - Review management

### 👨‍💻 Admin Features
- **👥 User Management**
  - User verification
  - Account management
  - Role assignment
  - Content moderation

- **⚙️ System Management**
  - Specialization management
  - System configuration
  - Analytics dashboard
  - Report generation

## 🛠️ Technical Stack

### 🔧 Backend
- **Framework**: Django 5.1.6
- **API**: Django REST Framework
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Task Queue**: Celery (for background tasks)

### 🎨 Frontend
- **Admin Interface**: Django Material Admin
- **API Documentation**: Swagger/ReDoc
- **File Storage**: Local storage (Development) / Cloud storage (Production)

### 🔌 Additional Features
- CORS support for cross-origin requests
- API documentation with drf-yasg
- Material Design admin interface
- File upload handling
- Email notifications
- SMS notifications (optional)
- Payment gateway integration

## 📋 Prerequisites

### 💻 System Requirements
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- Git
- PostgreSQL (for production)

### 🛠️ Development Tools
- Code editor (VS Code, PyCharm, etc.)
- Postman or similar API testing tool
- Git client

## 🚀 Installation

1. **📥 Clone the repository**:
```bash
git clone [repository-url]
cd [project-directory]
```

2. **🔧 Create and activate virtual environment**:
```bash
# Create virtual environment
python -m venv .venv

# Activate on Windows
.venv\Scripts\activate

# Activate on Unix or MacOS
source .venv/bin/activate
```

3. **📦 Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **⚙️ Environment Setup**:
Create a `.env` file in the project root with the following variables:
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

5. **🗄️ Database Setup**:
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

6. **📁 Static Files**:
```bash
python manage.py collectstatic
```

7. **▶️ Run Development Server**:
```bash
python manage.py runserver
```

## 📁 Project Structure

```
├── appointments/         # Appointment management app
│   ├── models.py        # Appointment models
│   ├── views.py         # Appointment views
│   ├── urls.py          # Appointment URLs
│   └── serializers.py   # Appointment serializers
├── config/              # Project configuration
│   ├── settings.py      # Project settings
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py          # WSGI configuration
├── media/              # User uploaded files
├── model_ai/           # AI model integration
├── rating/             # Doctor rating system
├── register_user/      # User registration and management
├── static/             # Static files
└── manage.py           # Django management script
```

## 📚 API Documentation

The API documentation is available at:
- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

### 🔌 Available Endpoints

#### 🔐 Authentication Endpoints
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - User login
- `POST /api/auth/refresh/` - Refresh JWT token
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/password-reset/` - Request password reset
- `POST /api/auth/password-reset/confirm/` - Confirm password reset

#### 👥 User Endpoints
- `GET /api/users/` - List all users
- `POST /api/users/` - Create new user
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user
- `GET /api/users/me/` - Get current user profile
- `PUT /api/users/me/` - Update current user profile
- `GET /api/users/doctors/` - List all doctors
- `GET /api/users/patients/` - List all patients

#### 📅 Appointment Endpoints
- `GET /api/appointments/` - List all appointments
- `POST /api/appointments/` - Create new appointment
- `GET /api/appointments/{id}/` - Get appointment details
- `PUT /api/appointments/{id}/` - Update appointment
- `DELETE /api/appointments/{id}/` - Delete appointment
- `GET /api/appointments/doctor/{doctor_id}/` - Get doctor's appointments
- `GET /api/appointments/patient/{patient_id}/` - Get patient's appointments
- `PUT /api/appointments/{id}/status/` - Update appointment status
- `GET /api/appointments/available-slots/` - Get available time slots

#### ⭐ Rating Endpoints
- `GET /api/ratings/` - List all ratings
- `POST /api/ratings/` - Create new rating
- `GET /api/ratings/{id}/` - Get rating details
- `PUT /api/ratings/{id}/` - Update rating
- `DELETE /api/ratings/{id}/` - Delete rating
- `GET /api/ratings/doctor/{doctor_id}/` - Get doctor's ratings
- `GET /api/ratings/patient/{patient_id}/` - Get patient's ratings

#### 📋 Specialization Endpoints
- `GET /api/specializations/` - List all specializations
- `POST /api/specializations/` - Create new specialization
- `GET /api/specializations/{id}/` - Get specialization details
- `PUT /api/specializations/{id}/` - Update specialization
- `DELETE /api/specializations/{id}/` - Delete specialization

#### 📊 Doctor Availability Endpoints
- `GET /api/availability/` - List all availability slots
- `POST /api/availability/` - Create new availability slot
- `GET /api/availability/{id}/` - Get availability details
- `PUT /api/availability/{id}/` - Update availability
- `DELETE /api/availability/{id}/` - Delete availability
- `GET /api/availability/doctor/{doctor_id}/` - Get doctor's availability

#### 💳 Payment Endpoints
- `POST /api/payments/` - Create new payment
- `GET /api/payments/{id}/` - Get payment details
- `GET /api/payments/appointment/{appointment_id}/` - Get appointment payment
- `POST /api/payments/verify/` - Verify payment
- `GET /api/payments/history/` - Get payment history

## 💻 Development

### 📝 Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add comments for complex logic
- Write docstrings for functions and classes

### 🧪 Testing
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test appointments
```

### 🔄 Git Workflow
1. Create feature branch
2. Make changes
3. Write tests
4. Run tests
5. Create pull request

## 🚀 Deployment

### ✅ Production Checklist
- [ ] Set DEBUG=False
- [ ] Configure production database
- [ ] Set up static file serving
- [ ] Configure email settings
- [ ] Set up SSL certificate
- [ ] Configure backup system
- [ ] Set up monitoring

### 📋 Deployment Steps
1. Update environment variables
2. Run migrations
3. Collect static files
4. Configure web server
5. Set up SSL
6. Configure backup

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📝 Pull Request Process
1. Update documentation
2. Add tests if needed
3. Ensure all tests pass
4. Update the README.md if needed

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

For any queries or support, please contact:
- 📧 Email: [mostafa.3mad.salah@gmail.com](mailto:mostafa.3mad.salah@gmail.com)
- 💻 GitHub: [@Mostafa3mad](https://github.com/Mostafa3mad)
- 🔗 LinkedIn: [Mostafa Emad](https://www.linkedin.com/in/mostafa--emad?originalSubdomain=eg)
- 🐦 X (Twitter): [@mostafa___emad](https://x.com/mostafa___emad)

## 🙏 Acknowledgments

- Django Documentation
- Django REST Framework
- Material Design
- All contributors 