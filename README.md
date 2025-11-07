# Great Kart - E-Commerce Platform

A full-featured Django-based e-commerce platform with Razorpay payment integration, user authentication, cart management, and order processing.

## 🚀 Features

### Implemented Features

- ✅ **User Authentication & Authorization**
  - User registration with email verification
  - Login/Logout functionality
  - Password reset via email
  - Profile management

- ✅ **Product Management**
  - Product catalog with categories
  - Product variations (size, color)
  - Product search functionality
  - Product detail pages with reviews

- ✅ **Shopping Cart**
  - Add/Remove products
  - Update quantities
  - Cart persistence for authenticated users
  - Variation-based cart items

- ✅ **Order Management**
  - Checkout process
  - Order placement
  - Order tracking
  - Order history in dashboard

- ✅ **Payment Integration**
  - Razorpay payment gateway integration
  - Multiple payment methods (Card, UPI, Netbanking, Wallets)
  - Payment verification
  - Order completion with invoice

- ✅ **Admin Panel**
  - Django admin interface
  - Product management
  - Order management
  - User management

- ✅ **Security**
  - Environment variables for sensitive data
  - CSRF protection
  - Secure password handling
  - Email verification

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd GREAT_KART
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv env
env\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root directory:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Email Configuration
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Razorpay Configuration (Test Mode)
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxxx
```

**Important:** 
- Never commit the `.env` file to version control
- Use test keys for development
- Switch to live keys for production

### 5. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Collect Static Files

```bash
python manage.py collectstatic
```

### 8. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## 📁 Project Structure

```
GREAT_KART/
├── accounts/          # User authentication and profile management
├── carts/             # Shopping cart functionality
├── category/          # Category management
├── orders/            # Order and payment processing
├── store/             # Product management
├── greatkart/         # Main project settings
├── templates/         # HTML templates
├── static/            # Static files (CSS, JS, images)
├── media/             # User uploaded files
├── .env               # Environment variables (not in git)
└── requirements.txt   # Python dependencies
```

## 🔑 Razorpay Setup

### Test Mode

1. Sign up at [Razorpay Dashboard](https://dashboard.razorpay.com)
2. Go to **Settings → API Keys → Generate Test Key**
3. Copy Key ID and Key Secret
4. Add them to your `.env` file

### Test Payment Methods

- **Card:** 4111 1111 1111 1111
- **UPI:** success@razorpay
- **Netbanking:** Use any test bank (username: success, password: success, OTP: 123456)
- **Wallets:** Mobile: 9999999999, OTP: 123456

### Live Mode

1. Complete KYC verification in Razorpay Dashboard
2. Generate Live API Keys
3. Update `.env` with live keys
4. Set `DEBUG=False` in settings
5. Configure proper `ALLOWED_HOSTS`

## 🎯 Next Steps (To Be Implemented)

### 108. Change Password
- Implement password change functionality
- Add password change form
- Validate old password before allowing change

### 109. Order Detail Dashboard
- Create detailed order view page
- Show order items, shipping address, payment details
- Add order status tracking

### 110. Fix Profile Picture in Dashboard
- Ensure profile pictures display correctly
- Add default avatar if no picture uploaded
- Optimize image display and sizing

### 111. Product Gallery Model with Image Preview in Admin
- Create ProductGallery model
- Add multiple images per product
- Implement image preview in Django admin

### 112. Product Gallery Implementation with jQuery
- Add image gallery on product detail page
- Implement image carousel/slider
- Add zoom functionality for product images

### 113. Store Sensitive Info Securely
- Move all sensitive data to environment variables
- Implement proper secret key management
- Add .env.example file for reference

### 114. Secure Admin Panel & Record Login Attempts
- Implement admin login attempt tracking
- Add rate limiting for admin login
- Log failed login attempts
- Add IP-based blocking for suspicious activity

### 115. Automatically Logout After Inactivity
- Implement session timeout
- Add automatic logout after inactivity
- Show warning before session expires

### 116. Show Rating On Homepage
- Display product ratings on homepage
- Show average ratings for each product
- Add star rating display component

## 🛠️ Technology Stack

- **Backend:** Django 5.2.7
- **Database:** SQLite (Development)
- **Payment Gateway:** Razorpay
- **Frontend:** Bootstrap, jQuery
- **Image Processing:** Pillow
- **Email:** Django Email Backend (SMTP)

## 📝 API Endpoints

### Authentication
- `/accounts/register/` - User registration
- `/accounts/login/` - User login
- `/accounts/logout/` - User logout
- `/accounts/dashboard/` - User dashboard
- `/accounts/edit_profile/` - Edit user profile

### Store
- `/store/` - Product listing
- `/store/category/<slug>/` - Category products
- `/store/<category_slug>/<product_slug>/` - Product detail

### Cart
- `/cart/` - View cart
- `/cart/add_cart/<product_id>/` - Add to cart
- `/cart/checkout/` - Checkout page

### Orders
- `/orders/place_order/` - Place order
- `/orders/payments/` - Payment page
- `/orders/verify_payment/` - Verify payment
- `/orders/order-complete/` - Order complete page

## 🔒 Security Notes

- Always use environment variables for sensitive data
- Never commit `.env` file to version control
- Use HTTPS in production
- Keep Django and dependencies updated
- Use strong secret keys in production
- Enable Django's security middleware in production

## 📧 Email Configuration

For email functionality to work:

1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password from Google Account settings
3. Use the App Password in `EMAIL_HOST_PASSWORD` in `.env`

## 🐛 Troubleshooting

### Payment Gateway Not Working
- Ensure Razorpay keys are set in `.env`
- Restart the development server after updating `.env`
- Check that keys are for the correct mode (test/live)

### Static Files Not Loading
- Run `python manage.py collectstatic`
- Check `STATIC_URL` and `STATIC_ROOT` in settings
- Ensure `DEBUG=True` for development

### Database Issues
- Run migrations: `python manage.py migrate`
- Check database file permissions
- For production, use PostgreSQL or MySQL

## 📄 License

This project is for educational purposes.

## 👨‍💻 Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
```

### Applying Migrations
```bash
python manage.py migrate
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📞 Support

For issues and questions, please open an issue on the repository.

---

**Note:** This is a development project. For production deployment, ensure:
- `DEBUG=False`
- Proper database configuration (PostgreSQL/MySQL)
- HTTPS enabled
- Secure secret keys
- Production-ready email configuration
- Proper static file serving
- Security headers configured

