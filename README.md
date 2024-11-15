

# CatVault - Password Manager & Generator Web App

CatVault is a secure, cat themed (for fun!) and user-friendly password manager and generator web application built with **Flask**. This application allows users to store, manage, and generate strong passwords in a safe and encrypted manner. It is designed with security in mind, making use of encryption techniques to ensure that sensitive user data remains protected. This project is perfect for individuals and small teams who need a convenient, easy-to-use password management solution.

## Features

### 1. **Password Management**
   - CatVault allows users to securely store passwords for their various online accounts. Users can add, edit, and delete their stored passwords with ease.
   - All passwords are hashed using **bcrypt** before being stored in the database, ensuring they are never saved in plain text.

### 2. **Password Generation**
   - The app includes a built-in password generator, which can generate secure, random passwords based on user-defined length and complexity preferences.
   - The generated passwords are also hashed before storage to ensure that even generated passwords are securely saved.

### 3. **Password Encryption & Decryption**
   - The app uses the **Cryptography** library to encrypt and decrypt passwords, ensuring that only authorized users can access them.
   - Password decryption is only performed when a valid user session is established, ensuring that the passwords are safe even in case of unauthorized access attempts.

### 4. **User Authentication**
   - **Flask-Bcrypt** is used to securely hash passwords during user authentication. This prevents password leakage and ensures that passwords are never stored in plaintext.
   - Users can register, log in, and manage their profiles through a secure and efficient authentication process.

### 5. **Session Management**
   - **Flask-Session** is used to manage user sessions. The sessions are stored in the filesystem, ensuring that session data is safely kept between requests without the risk of losing data on server restarts.

### 6. **Responsive Design**
   - The front-end uses **Bootstrap** to provide a responsive user interface. This ensures that the web app is usable on all screen sizes, from mobile devices to desktop computers.
   - **JavaScript** is employed for client-side interactivity, allowing for dynamic interactions without the need for page reloads. Also it has been used to copy generated passwords in the user's clipboard.
   - Additionally, JavaScript is used to toggle between **dark mode** and **light mode**, allowing users to customize their experience based on their preferences. This feature provides a visually comfortable environment for different lighting conditions.

### 7. **Database Integration**
   - The app uses **SQLite3** as its database backend, making it lightweight and easy to use for small projects. The **CS50 library** is used for simplifying database interactions, making it easier to execute SQL queries.

### 8. **Security Best Practices**
   - All user data is stored with encryption or hashing algorithms to prevent unauthorized access.
   - Passwords are hashed using **bcrypt** and sensitive data is encrypted using the **Cryptography** library, ensuring the app adheres to modern security standards.

## Installation

### Prerequisites
Before running the CatVault app, make sure you have the following installed on your system:

- Python 3.9+
- pip (Python package installer)

### Steps to Install

1. **Clone the Repository**
   First, clone the CatVault repository to your local machine:
   ```bash
   git clone https://github.com/baibhab-adhikari/CatVault.git
   cd CatVault
   ```

2. **Create a Virtual Environment**
   It is recommended to use a virtual environment to manage dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. **Install Dependencies**
   Install the required dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create the Database**
   The app uses SQLite3, and the database will be created automatically. However, ensure you run the app at least once to create the database schema.

5. **Run the Application**
   Finally, run the Flask app:
   ```bash
   python main.py
   ```
   The app will be available at `http://127.0.0.1:5000/` in your preferred browser.

## Dependencies

Here are the main dependencies used in the CatVault project:

- **Flask==3.0.3**: The web framework for building the application.
- **Flask-Bcrypt==1.0.1**: Used for hashing passwords securely.
- **Flask-Session==0.8.0**: Used for managing user sessions.
- **Flask-SQLAlchemy==3.1.1**: An extension that adds support for SQLAlchemy to Flask, making database interactions easier.
- **Flask-Bcrypt==1.0.1**: Provides password hashing capabilities.
- **Cryptography==43.0.3**: Used for encrypting and decrypting user data.
- **SQLite3**: Database engine used for storing user data.
- **Jinja2**: Template engine for rendering HTML pages.
- **CS50==9.4.0**: Simplifies interaction with SQLite3 databases.
- **Werkzeug==3.1.3**: A comprehensive WSGI utility library.
- **python-dotenv**: Loads environment variables from a `.env` file for configuration management.
- **bcrypt**: Provides robust password hashing for security.

For a complete list of all dependencies, please refer to the `requirements.txt` file in the repository.

## Future Considerations

1. **Multi-Device Synchronization**
   Currently, the app allows users to store passwords on a single device. A potential feature in the future is to enable synchronization across multiple devices by integrating cloud storage.

2. **Password Strength Analyzer**
   Another potential feature could be a password strength analyzer that evaluates the strength of passwords entered by users and suggests improvements.

3. **Two-Factor Authentication (2FA)**
   For enhanced security, integrating two-factor authentication could be a valuable feature. This would require users to verify their identity using a second factor, such as an authentication app or email verification, in addition to their password.

4. **Support for Multiple Users**
   Expanding the app to support multiple users would allow for more flexibility, particularly for teams or families. Users could share certain passwords with others, while maintaining the security of their personal data.

5. **Audit Logs**
   Implementing an audit log feature to track login attempts and actions performed on passwords could improve the app's security and allow users to monitor suspicious activity.

## Screenshots

Below are some placeholders for the screenshots of the actual web app:

1. **Homepage**
   ![Homapage](/screenshots/home.png)
2. **Login Page**
   ![Login Page](/screenshots/login.png)

3. **Dashboard with Password Management**
   ![Dashboard](/screenshots/manager.png)

4. **Password Generator Interface**
   ![Password Generator](/screenshots/generator.png)



---

## Conclusion

CatVault is a powerful, easy-to-use password manager that focuses on security and ease of use. By using modern encryption and hashing techniques, the app ensures that your data is always safe and protected. Whether you're an individual user or part of a small team, CatVault offers a reliable way to securely manage your passwords and sensitive information. With its clean interface, strong security features, and potential for future improvements, CatVault is a great choice for anyone looking to safeguard their online accounts.
