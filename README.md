

# CatVault - Password Manager & Generator Web App

CatVault is a secure, cat-themed (for fun!) and user-friendly password manager and generator web application built with **Flask**(Python). This application allows users to store, manage, and generate strong passwords in a safe and encrypted manner. It is designed with security in mind, making use of encryption and hashing techniques to ensure that sensitive user data remains protected. CatVault is perfect for individuals and small teams who need a convenient, easy-to-use password management solution.
Check it out here: [CatVault](https://catvault-d0092287f236.herokuapp.com/)


---

## Features

### 1. **Password Management**
- **Store & Manage Passwords:**  
  Securely store, edit, and delete passwords for various online accounts.
- **Encryption & Hashing:**  
  Passwords are encrypted using the **Cryptography** library and hashed with **bcrypt** before being stored, ensuring no sensitive information is stored in plain text.

### 2. **Password Generation**
- **Built-in Password Generator:**  
  Generate secure, random passwords based on user-defined length and complexity preferences.
- **Secure Storage:**  
  Generated passwords are securely hashed before being stored.

### 3. **User Authentication**
- **Standard Authentication:**  
  Users can register, log in, and manage their profiles with secure, hashed passwords using **Flask-Bcrypt**.
  
### 4. **Password Reset (Forgot Password)**
- **Forgot Password Flow:**  
  Users can request a password reset via email. A secure, time-limited token is generated and emailed to the user.
- **Reset Password:**  
  Using the link from the email, users can set a new password after token verification.

### 5. **Session Management**
- **Secure Sessions:**  
  User sessions are managed via **Flask-Session** (filesystem-based for development) to ensure session persistence and security.

### 6. **Responsive & Cat-Themed UI**
- **Modern Design with Bootstrap:**  
  A responsive interface that looks great on all devices, enhanced with modern Bootstrap styling and playful cat-themed accents.
- **Dark/Light Mode Toggle:**  
  Enjoy a customized experience with a JavaScript-powered dark/light mode switch.

### 7. **Database Integration**
- **MySQL for Local Development:**  
  For development purposes, CatVault uses **MySQL** as its database backend.
- **PostgreSQL for Production:**  
  When deployed (for example on Heroku), the app uses **PostgreSQL** to manage user data.

### 8. **Security Best Practices**
- **Encryption and Hashing:**  
  All sensitive data is encrypted or hashed using industry-standard algorithms.
- **Secure Token Generation:**  
  Forgot password tokens are generated with **itsdangerous**, ensuring tamper-proof and time-limited access.

---

## Installation

### Prerequisites
Ensure you have the following installed on your system:
- Python 3.9+
- pip (Python package installer)

### Steps to Install

1. **Clone the Repository**
   ```bash
   git clone https://github.com/baibhab-adhikari/CatVault.git
   cd CatVault
   ```

2. **Create a Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create the Database**
   - For development, configure your MySQL database and update your configuration accordingly.
   - Run the `db_init.py` file at least once to create the database schema.

5. **Run the Application**
   ```bash
   python main.py
   ```
   The app will be available at `http://127.0.0.1:5000/` in your preferred browser.

---

## Dependencies

Key dependencies include:
- **Flask** – Web framework.
- **Flask-Bcrypt** – For password hashing.
- **Flask-Session** – For session management.
- **Flask-SQLAlchemy** – ORM for database operations.
- **Flask-Mail** - For sending mails
- **Cryptography** – For data encryption/decryption.
- **itsdangerous** – For generating secure tokens.
- **Gunicorn** – Production WSGI server.
- **python-dotenv** – For environment variable management (local development).

Refer to `requirements.txt` for a complete list.

---

## Changelog

### **Version 2.0 - Latest Updates**
- **Forgot Password & Reset Password:**
  - Implemented secure token generation and verification using **itsdangerous**.
  - Added email-based password reset flow with time-limited tokens.
- **Database Updates:**
  - Changed development database from SQLite3 to **MySQL**.
  - Production now uses **PostgreSQL** (suitable for Heroku deployments).
- **UI Enhancements:**
  - Updated templates with modern, cat-themed Bootstrap styling.
  - Improved responsive design and added a dark/light mode toggle.
- **Bug Fixes & Security Improvements:**
  - Fixed several issues related to password hashing and token expiration.
  - Enhanced security best practices across the app.

### **Version 1.0**
- Initial release with core features: password management, password generation, and basic user authentication using Flask.
- Implemented encryption and hashing for secure data storage.
- Basic UI built with Bootstrap and a playful cat theme.



## Screenshots


1. **Homepage**  
   ![Homepage](/screenshots/home.png)
2. **Account Dashboard**  
   ![Account](/screenshots/account.png)
3. **Dashboard with Password Management**  
   ![Dashboard](/screenshots/manager.png)
4. **Password Generator Interface**  
   ![Password Generator](/screenshots/generator.png)


---

## Conclusion

CatVault is a powerful, user-friendly password manager that emphasizes strong security and modern design. With features like secure password storage, dynamic password generation, email-based password reset, and robust encryption practices, CatVault offers a comprehensive solution for managing sensitive data. The app is continuously evolving with improvements in usability, security, and scalability—making it a robust tool for individuals and small teams alike.
