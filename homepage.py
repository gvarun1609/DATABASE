from PyQt5.QtCore import Qt
import mysql.connector
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QWidget

class HomePage(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle('Home Page')
        self.resize(800, 600)
        self.username = username

        # Create header layout
        self.header_layout = QVBoxLayout()

        # Add label for username in the top left corner
        self.username_label = QLabel(f"Logged in as: {self.username}")
        self.header_layout.addWidget(self.username_label)

        # Add button for adding album
        self.add_album_button = QPushButton('Add Album')
        self.add_album_button.clicked.connect(self.addAlbum)
        self.header_layout.addWidget(self.add_album_button)

        # Add layout for albums
        self.albums_layout = QVBoxLayout()
        self.header_layout.addLayout(self.albums_layout)

        # Load albums from database
        self.loadAlbums()

        # Set main layout
        self.setLayout(self.header_layout)

    def loadAlbums(self):
        # Function to load albums from the database and display them on the UI
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="gallery_user",
                password="varun2711",
                database="art_gallery"
            )
            cursor = conn.cursor()

            # Query albums from the database
            cursor.execute("SELECT * FROM photo_album")
            albums = cursor.fetchall()

            # Clear existing albums from the layout
            for i in reversed(range(self.albums_layout.count())):
                widget = self.albums_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()

            # Populate albums_layout with album widgets
            for album in albums:
                album_widget = self.createAlbumWidget(album)
                self.albums_layout.addWidget(album_widget)

            conn.close()
        except mysql.connector.Error as e:
            print(f'Failed to load albums: {e}')

    def createAlbumWidget(self, album):
        # Function to create a widget for displaying an album
        album_widget = QWidget()
        layout = QVBoxLayout()

        # Add album information to the layout
        album_name_label = QLabel(f"Album Name: {album[1]}")
        description_label = QLabel(f"Description: {album[2]}")
        artist_label = QLabel(f"Artist: {album[3]}")

        layout.addWidget(album_name_label)
        layout.addWidget(description_label)
        layout.addWidget(artist_label)

        # Add buttons for editing and deleting the album
        edit_button = QPushButton('Edit')
        edit_button.clicked.connect(lambda: self.editAlbum(album[0]))

        delete_button = QPushButton('Delete')
        delete_button.clicked.connect(lambda: self.deleteAlbum(album[0]))

        button_layout = QHBoxLayout()
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)

        album_widget.setLayout(layout)
        return album_widget

    def addAlbum(self):
        # Function to add a new album
        dialog = AddAlbumDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            album_data = dialog.getAlbumData()
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="gallery_user",
                    password="varun2711",
                    database="art_gallery"
                )
                cursor = conn.cursor()

                # Insert album into the database
                cursor.execute("INSERT INTO photo_album (album_name, description, artist_name, photo_path) VALUES (%s, %s, %s, %s)",
                               album_data)
                conn.commit()
                conn.close()

                # Reload albums from the database and update UI
                self.loadAlbums()
            except mysql.connector.Error as e:
                print(f'Failed to add album: {e}')

    def editAlbum(self, album_id):
        # Function to edit an existing album
        dialog = EditAlbumDialog(self, album_id)
        if dialog.exec_() == QDialog.Accepted:
            updated_album_data = dialog.getAlbumData()
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="gallery_user",
                    password="varun2711",
                    database="art_gallery"
                )
                cursor = conn.cursor()

                # Update album in the database
                cursor.execute("UPDATE photo_album SET album_name = %s, description = %s, artist_name = %s, photo_path = %s WHERE album_id = %s",
                               (*updated_album_data, album_id))
                conn.commit()
                conn.close()

                # Reload albums from the database and update UI
                self.loadAlbums()
            except mysql.connector.Error as e:
                print(f'Failed to edit album: {e}')

    def deleteAlbum(self, album_id):
        # Function to delete an existing album
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="gallery_user",
                password="varun2711",
                database="art_gallery"
            )
            cursor = conn.cursor()

            # Delete album from the database
            cursor.execute("DELETE FROM photo_album WHERE album_id = %s", (album_id,))
            conn.commit()
            conn.close()

            # Reload albums from the database and update UI
            self.loadAlbums()
        except mysql.connector.Error as e:
            print(f'Failed to delete album: {e}')

class AddAlbumDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Add Album')

        self.album_name_edit = QLineEdit()
        self.description_edit = QLineEdit()
        self.artist_name_edit = QLineEdit()
        self.photo_path = None

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Album Name:'))
        layout.addWidget(self.album_name_edit)
        layout.addWidget(QLabel('Description:'))
        layout.addWidget(self.description_edit)
        layout.addWidget(QLabel('Artist Name:'))
        layout.addWidget(self.artist_name_edit)

        photo_button = QPushButton('Select Photo')
        photo_button.clicked.connect(self.selectPhoto)
        layout.addWidget(photo_button)

        ok_button = QPushButton('OK')
        ok_button.clicked.connect(self.accept)

        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def selectPhoto(self):
        # Function to select a photo for the album
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.photo_path, _ = QFileDialog.getOpenFileName(self, "Select Photo", "", "Image Files (*.png *.jpg *.jpeg)", options=options)

    def getAlbumData(self):
        # Function to retrieve album data entered by the user
        album_name = self.album_name_edit.text()
        description = self.description_edit.text()
        artist_name = self.artist_name_edit.text()
        return album_name, description, artist_name, self.photo_path

class EditAlbumDialog(AddAlbumDialog):
    def __init__(self, parent=None, album_id=None):
        super().__init__(parent)
        self.setWindowTitle('Edit Album')
        self.album_id = album_id

        # Load existing album data for editing
        self.loadAlbumData()

    def loadAlbumData(self):
        # Function to load existing album data for editing
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="gallery_user",
                password="varun2711",
                database="art_gallery"
            )
            cursor = conn.cursor()

            # Query album data from the database
            cursor.execute("SELECT * FROM albums WHERE album_id = %s", (self.album_id,))
            album_data = cursor.fetchone()

            # Populate fields with existing album data
            self.album_name_edit.setText(album_data[1])
            self.description_edit.setText(album_data[2])
            self.artist_name_edit.setText(album_data[3])

            conn.close()
        except mysql.connector.Error as e:
            print(f'Failed to load album data: {e}')

    def getAlbumData(self):
        # Function to retrieve updated album data entered by the user
        album_name = self.album_name_edit.text()
        description = self.description_edit.text()
        artist_name = self.artist_name_edit.text()
        return album_name, description, artist_name, self.photo_path, self.album_id
