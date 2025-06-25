import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QMessageBox, QInputDialog, QFormLayout, QDialog, QCheckBox, QListWidgetItem
)
from PyQt5.QtCore import Qt

CONTACTS_FILE = "contacts.json"

class ContactDialog(QDialog):
    def __init__(self, parent=None, contact=None):
        super().__init__(parent)
        self.setWindowTitle("Contact Details")
        self.contact = contact or {"name": "", "phone": "", "email": "", "address": "", "favorite": False, "emergency": False}
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)

        self.name_edit = QLineEdit(self.contact["name"])
        self.name_edit.setStyleSheet("background-color: #34495E; color: white; border: none; padding: 6px;")
        self.phone_edit = QLineEdit(self.contact["phone"])
        self.phone_edit.setStyleSheet("background-color: #34495E; color: white; border: none; padding: 6px;")
        self.email_edit = QLineEdit(self.contact["email"])
        self.email_edit.setStyleSheet("background-color: #34495E; color: white; border: none; padding: 6px;")
        self.address_edit = QLineEdit(self.contact["address"])
        self.address_edit.setStyleSheet("background-color: #34495E; color: white; border: none; padding: 6px;")

        layout.addRow("Name:", self.name_edit)
        layout.addRow("Phone:", self.phone_edit)
        layout.addRow("Email:", self.email_edit)
        layout.addRow("Address:", self.address_edit)

        self.favorite_checkbox = QCheckBox("Favorite")
        self.favorite_checkbox.setChecked(self.contact.get("favorite", False))
        self.favorite_checkbox.setStyleSheet("color: white;")
        layout.addRow(self.favorite_checkbox)

        self.emergency_checkbox = QCheckBox("Emergency")
        self.emergency_checkbox.setChecked(self.contact.get("emergency", False))
        self.emergency_checkbox.setStyleSheet("color: white;")
        layout.addRow(self.emergency_checkbox)

        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)

        layout.addRow(buttons_layout)

    def get_contact_data(self):
        return {
            "name": self.name_edit.text().strip(),
            "phone": self.phone_edit.text().strip(),
            "email": self.email_edit.text().strip(),
            "address": self.address_edit.text().strip(),
            "favorite": self.favorite_checkbox.isChecked(),
            "emergency": self.emergency_checkbox.isChecked()
        }

class ContactManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contact Manager")
        self.contacts = []
        self.load_contacts()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #2C3E50; color: white;")  # Modern professional dark theme for main window

        main_layout = QVBoxLayout(self)

        # Buttons for Call, Video Call, Message
        buttons_layout = QHBoxLayout()
        self.call_button = QPushButton("Call")
        self.call_button.setStyleSheet("background-color: #16A085; color: white; padding: 8px 12px; border-radius: 4px;")
        self.call_button.clicked.connect(self.call_contact)
        buttons_layout.addWidget(self.call_button)

        self.video_call_button = QPushButton("Video Call")
        self.video_call_button.setStyleSheet("background-color: #9B59B6; color: white; padding: 8px 12px; border-radius: 4px;")
        self.video_call_button.clicked.connect(self.video_call_contact)
        buttons_layout.addWidget(self.video_call_button)

        self.message_button = QPushButton("Message")
        self.message_button.setStyleSheet("background-color: #F39C12; color: white; padding: 8px 12px; border-radius: 4px;")
        self.message_button.clicked.connect(self.message_contact)
        buttons_layout.addWidget(self.message_button)

        main_layout.addLayout(buttons_layout)

        # Search bar
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_edit = QLineEdit()
        self.search_edit.setStyleSheet("background-color: #34495E; color: white; border: none; padding: 6px;")  # Dark theme input
        self.search_edit.textChanged.connect(self.update_contact_list)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_edit)
        main_layout.addLayout(search_layout)

        # Contact list
        self.contact_list = QListWidget()
        self.contact_list.setStyleSheet("background-color: #34495E; color: white; border: none;")  # Dark theme list
        self.contact_list.itemSelectionChanged.connect(self.on_contact_selected)
        main_layout.addWidget(self.contact_list)

        # Buttons for Add, Update, Delete, Merge
        buttons_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Contact")
        self.add_button.setStyleSheet("background-color: #27AE60; color: white; padding: 8px 12px; border-radius: 4px;")  # Consistent modern theme buttons
        self.add_button.clicked.connect(self.add_contact)
        self.update_button = QPushButton("Update Contact")
        self.update_button.setStyleSheet("background-color: #2980B9; color: white; padding: 8px 12px; border-radius: 4px;")
        self.update_button.clicked.connect(self.update_contact)
        self.delete_button = QPushButton("Delete Contact")
        self.delete_button.setStyleSheet("background-color: #C0392B; color: white; padding: 8px 12px; border-radius: 4px;")
        self.delete_button.clicked.connect(self.delete_contact)
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.update_button)
        buttons_layout.addWidget(self.delete_button)

        self.merge_button = QPushButton("Merge")
        self.merge_button.setStyleSheet("background-color: #8E44AD; color: white; padding: 8px 12px; border-radius: 4px;")
        self.merge_button.clicked.connect(self.merge_contacts)
        buttons_layout.addWidget(self.merge_button)

        main_layout.addLayout(buttons_layout)

        self.selected_index = None
        self.update_contact_list()

    def load_contacts(self):
        if os.path.exists(CONTACTS_FILE):
            with open(CONTACTS_FILE, "r") as f:
                self.contacts = json.load(f)
        else:
            self.contacts = []

    def save_contacts(self):
        with open(CONTACTS_FILE, "w") as f:
            json.dump(self.contacts, f, indent=4)

    def update_contact_list(self):
        search_term = self.search_edit.text().lower()
        self.contact_list.clear()
        for i, contact in enumerate(self.contacts):
            if search_term in contact["name"].lower() or search_term in contact["phone"]:
                label = f"{'★ ' if contact.get('favorite') else ''}{'⚠ ' if contact.get('emergency') else ''}{contact['name']} - {contact['phone']}"
                item = QListWidgetItem(label)
                font = item.font()
                font.setPointSize(24)  # Increased font size for saved contacts
                item.setFont(font)
                if contact.get("emergency"):
                    item.setForeground(Qt.red)
                self.contact_list.addItem(item)

    def on_contact_selected(self):
        selected_items = self.contact_list.selectedItems()
        if selected_items:
            self.selected_index = self.contact_list.currentRow()
        else:
            self.selected_index = None

    def add_contact(self):
        dialog = ContactDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            new_contact = dialog.get_contact_data()
            if not new_contact["name"] or not new_contact["phone"]:
                QMessageBox.warning(self, "Input Error", "Name and Phone are required.")
                return
            self.contacts.append(new_contact)
            self.save_contacts()
            self.update_contact_list()

    def update_contact(self):
        if self.selected_index is None:
            QMessageBox.warning(self, "Selection Error", "No contact selected.")
            return
        dialog = ContactDialog(self, self.contacts[self.selected_index])
        if dialog.exec_() == QDialog.Accepted:
            updated_contact = dialog.get_contact_data()
            if not updated_contact["name"] or not updated_contact["phone"]:
                QMessageBox.warning(self, "Input Error", "Name and Phone are required.")
                return
            self.contacts[self.selected_index] = updated_contact
            self.save_contacts()
            self.update_contact_list()

    def delete_contact(self):
        if self.selected_index is None:
            QMessageBox.warning(self, "Selection Error", "No contact selected.")
            return
        reply = QMessageBox.question(
            self, "Confirm Delete", "Are you sure you want to delete this contact?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            del self.contacts[self.selected_index]
            self.save_contacts()
            self.update_contact_list()
            self.selected_index = None

    def merge_contacts(self):
        if len(self.contact_list.selectedItems()) != 2:
            QMessageBox.warning(self, "Selection Error", "Select exactly 2 contacts to merge.")
            return
        idx1, idx2 = self.contact_list.selectedIndexes()[0].row(), self.contact_list.selectedIndexes()[1].row()
        c1, c2 = self.contacts[idx1], self.contacts[idx2]
        merged = {
            "name": c1["name"] or c2["name"],
            "phone": c1["phone"] or c2["phone"],
            "email": c1["email"] or c2["email"],
            "address": c1["address"] or c2["address"],
            "favorite": c1.get("favorite", False) or c2.get("favorite", False),
            "emergency": c1.get("emergency", False) or c2.get("emergency", False),
        }
        del self.contacts[max(idx1, idx2)]
        del self.contacts[min(idx1, idx2)]
        self.contacts.append(merged)
        self.save_contacts()
        self.update_contact_list()

    def call_contact(self):
        if self.selected_index is None:
            QMessageBox.warning(self, "Selection Error", "No contact selected.")
            return
        name = self.contacts[self.selected_index]["name"]
        QMessageBox.information(self, "Calling", f"Calling {name}...")

    def video_call_contact(self):
        if self.selected_index is None:
            QMessageBox.warning(self, "Selection Error", "No contact selected.")
            return
        name = self.contacts[self.selected_index]["name"]
        QMessageBox.information(self, "Video Call", f"Starting video call with {name}...")

    def message_contact(self):
        if self.selected_index is None:
            QMessageBox.warning(self, "Selection Error", "No contact selected.")
            return
        name = self.contacts[self.selected_index]["name"]
        QMessageBox.information(self, "Message", f"Sending message to {name}...")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContactManager()
    window.resize(400, 500)
    window.show()
    sys.exit(app.exec_())