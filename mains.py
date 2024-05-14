import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QDialog, QMessageBox, QListWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from homepage import HomePage
import mysql.connector

class UserListWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window title
        self.setWindowTitle('User List')
        # Set window size
        self.resize(400, 300)

        # Create a vertical layout
        layout = QVBoxLayout()

        # Create a label for the list
        label = QLabel('User List')
        label.setFont(QFont('Arial', 16))
        layout.addWidget(label)

        # Create a list widget to display users
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        # Set the layout for the window
        self.setLayout(layout)

    def loadUsers(self):
        try:
            # Connect to the database
            conn = mysql.connector.connect(
                host="localhost",
                user="gallery_user",
                password="varun2711",
                database="art_gallery"
            )

            cursor = conn.cursor()

            # Execute a SELECT query to retrieve user data
            cursor.execute("SELECT * FROM users")

            # Fetch all rows
            rows = cursor.fetchall()

            # Clear existing items in the list widget
            self.list_widget.clear()

            # Add user data to the list widget
            for row in rows:
                user_info = f"{row[0]} - {row[1]} {row[2]} ({row[3]})"
                self.list_widget.addItem(user_info)

            conn.close()
        except mysql.connector.Error as e:
            print(f'Failed to retrieve users: {e}')


class ArtGalleryManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window title
        self.setWindowTitle('CANVAS')
        # Set window size
        self.resize(600, 400)

        # Set background color
        self.setStyleSheet('background-color: #222;')

        # Create a vertical layout
        layout = QVBoxLayout()

        # Create a label for the app name
        label = QLabel('CANVAS')
        # Set label text color and font
        label.setStyleSheet('color: #4CAF50; font-size: 34px; font-weight: bold;')
        # Align the label to center
        label.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(250, 20, 250, 300)

        # Create login button
        self.login_button = QPushButton('Login')
        # Set button color
        self.login_button.setStyleSheet('background-color: #008CBA; color: white;')
        # Set button font
        self.login_button.setFont(QFont('Arial', 14))
        # Connect login button to login function
        self.login_button.clicked.connect(self.showLogin)

        # Create registration button
        registration_button = QPushButton('Register')
        # Set button color
        registration_button.setStyleSheet('background-color: #f44336; color: white;')
        # Set button font
        registration_button.setFont(QFont('Arial', 14))
        # Connect registration button to register function
        registration_button.clicked.connect(self.showRegistration)

        # Add widgets to the layout
        layout.addWidget(label)
        layout.addWidget(self.login_button)
        layout.addWidget(registration_button)

        # Set the layout for the window
        self.setLayout(layout)

    def showLogin(self):
        # Function to show the login form
        login_form = LoginForm(self)
        if login_form.exec_() == QDialog.Accepted:
            # If login is successful, show the home page
            username = login_form.username_edit.text()
            self.showHomePage(username)

    def showRegistration(self):
        # Function to show the registration form
        registration_form = RegistrationForm(self)
        registration_form.exec_()

    def showHomePage(self):
        # Function to show the home page
        self.home_page = HomePage()
        self.home_page.show()
        # Disable login button after successful login
        self.login_button.setEnabled(False)


class RegistrationForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Registration Form')

        # Create form fields
        self.first_name_edit = QLineEdit()
        self.last_name_edit = QLineEdit()
        self.username_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.confirm_password_edit = QLineEdit()

        # Set text color to white for form fields
        self.first_name_edit.setStyleSheet('color: white;')
        self.last_name_edit.setStyleSheet('color: white;')
        self.username_edit.setStyleSheet('color: white;')
        self.email_edit.setStyleSheet('color: white;')
        self.password_edit.setStyleSheet('color: white;')
        self.confirm_password_edit.setStyleSheet('color: white;')

        # Set password mode for password fields
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.confirm_password_edit.setEchoMode(QLineEdit.Password)

        # Create labels for form fields
        layout = QVBoxLayout()

        # Add labels and input fields to the layout
        self.addFormField(layout, 'First Name:', self.first_name_edit)
        self.addFormField(layout, 'Last Name:', self.last_name_edit)
        self.addFormField(layout, 'Username:', self.username_edit)
        self.addFormField(layout, 'Email:', self.email_edit)
        self.addFormField(layout, 'Password:', self.password_edit)
        self.addFormField(layout, 'Confirm Password:', self.confirm_password_edit)

        # Add form fields to the dialog
        self.setLayout(layout)

        # Add standard buttons to the dialog
        self.ok_button = QPushButton('OK')
        self.cancel_button = QPushButton('Cancel')

        # Set text color to white for buttons
        self.ok_button.setStyleSheet('color: white;')
        self.cancel_button.setStyleSheet('color: white;')

        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

        # Connect standard buttons to functions
        self.ok_button.clicked.connect(self.register)
        self.cancel_button.clicked.connect(self.reject)

    def addFormField(self, layout, label_text, edit_widget):
        label = QLabel(label_text)
        label.setStyleSheet('color: white;')
        layout.addWidget(label)
        layout.addWidget(edit_widget)

    # The register method and other methods remain unchanged


    def register(self):
        # Function to validate and register user
        first_name = self.first_name_edit.text()
        last_name = self.last_name_edit.text()
        username = self.username_edit.text()
        email = self.email_edit.text()
        password = self.password_edit.text()
        confirm_password = self.confirm_password_edit.text()

        if not (first_name and last_name and username and email and password and confirm_password):
            QMessageBox.critical(self, 'Error', 'All fields are required!')
            return

        if password != confirm_password:
            QMessageBox.critical(self, 'Error', 'Passwords do not match!')
            return

        # If validation passes, insert user data into the database
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="gallery_user",
                password="varun2711",
                database="art_gallery"
            )

            cursor = conn.cursor()

            # Insert user data into the users table
            cursor.execute("INSERT INTO users (first_name, last_name, username, email, password) VALUES (%s, %s, %s, %s, %s)",
                           (first_name, last_name, username, email, password))
            conn.commit()
            conn.close()

            QMessageBox.information(self, 'Success', 'Registration Successful!')
            self.accept()  # Close the registration form
        except mysql.connector.Error as e:
            QMessageBox.critical(self, 'Error', f'Failed to register user: {e}')

class LoginForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Login')

        # Create form fields
        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()

        # Set text color to white for form fields
        self.username_edit.setStyleSheet('color: white;')
        self.password_edit.setStyleSheet('color: white;')

        # Set password mode for password field
        self.password_edit.setEchoMode(QLineEdit.Password)

        # Create labels for form fields
        layout = QVBoxLayout()

        # Add labels and input fields to the layout
        self.addFormField(layout, 'Username:', self.username_edit)
        self.addFormField(layout, 'Password:', self.password_edit)

        # Add form fields to the dialog
        self.setLayout(layout)

        # Add standard buttons to the dialog
        self.ok_button = QPushButton('Login')
        self.cancel_button = QPushButton('Cancel')

        # Set text color to white for buttons
        self.ok_button.setStyleSheet('color: white;')
        self.cancel_button.setStyleSheet('color: white;')

        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

        # Connect standard buttons to functions
        self.ok_button.clicked.connect(self.login)
        self.cancel_button.clicked.connect(self.reject)

    def addFormField(self, layout, label_text, edit_widget):
        label = QLabel(label_text)
        label.setStyleSheet('color: white;')
        layout.addWidget(label)
        layout.addWidget(edit_widget)

    def login(self):
        # Function to authenticate user
        username = self.username_edit.text()
        password = self.password_edit.text()

        if not (username and password):
            QMessageBox.critical(self, 'Error', 'Username and password are required!')
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="gallery_user",
                password="varun2711",
                database="art_gallery"
            )

            cursor = conn.cursor()

            # Execute a SELECT query to check if the user exists and password matches
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))

            # Fetch the first row
            row = cursor.fetchone()

            if row:
                QMessageBox.information(self, 'Success', 'Login Successful!')
                self.accept()  # Close the login form
            else:
                QMessageBox.critical(self, 'Error', 'Invalid username or password!')

            conn.close()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, 'Error', f'Failed to authenticate user: {e}')


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Home Page')
        self.resize(400, 300)
        layout = QVBoxLayout()
        label = QLabel('Welcome to the Home Page!')
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)


class ArtGalleryManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window title
        self.setWindowTitle('Art Gallery Management')
        # Set window size
        self.resize(600, 400)

        # Set background color
        self.setStyleSheet('background-color: #40618E;')

        # Create a vertical layout
        layout = QVBoxLayout()

        # Create a label for the app name
        label = QLabel('ART GALLERY MANAGEMENT')
        # Set label text color and font
        label.setStyleSheet('color: #4CAF50; font-size: 34px; font-weight: bold;')
        # Align the label to center
        label.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(250, 20, 250, 300)

        # Create login button
        login_button = QPushButton('Login')
        # Set button color
        login_button.setStyleSheet('background-color: #008CBA; color: white;')
        # Set button font
        login_button.setFont(QFont('Arial', 14))
        # Connect login button to login function
        login_button.clicked.connect(self.showLogin)

        # Create registration button
        registration_button = QPushButton('Register')
        # Set button color
        registration_button.setStyleSheet('background-color: #171065; color: white;')
        # Set button font
        registration_button.setFont(QFont('Arial', 14))
        # Connect registration button to register function
        registration_button.clicked.connect(self.showRegistration)

        # Add widgets to the layout
        layout.addWidget(label)
        layout.addWidget(login_button)
        layout.addWidget(registration_button)

        # Set the layout for the window
        self.setLayout(layout)

    def showLogin(self):
    # Function to show the login form
        login_form = LoginForm(self)
        if login_form.exec_() == QDialog.Accepted:
            # If login is successful, retrieve the username
            username = login_form.username_edit.text()
            # Pass the username to the showHomePage method
            self.showHomePage()
            self.home_page.show()


    def showRegistration(self):
        # Function to show the registration form
        registration_form = RegistrationForm(self)
        registration_form.exec_()

    def showHomePage(self):
    # Function to show the home page
        self.home_page = HomePage()
        self.home_page.show()


if __name__ == '__main__':
    # Create the application instance
    app = QApplication(sys.argv)

    # Create the GUI window
    window = ArtGalleryManagement()

    # Show the window
    window.show()

    # Execute the application's event loop
    sys.exit(app.exec_())
