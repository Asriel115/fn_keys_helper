#!/usr/bin/env python3
import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QShortcut,
    QPushButton,
    QDialog,
    QLineEdit,
    QFormLayout,
    QDialogButtonBox,
)
from PyQt5.QtGui import QKeySequence, QFont, QIcon
from PyQt5.QtCore import Qt, QStandardPaths


class SettingsDialog(QDialog):
    def __init__(self, fn_keys, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit F-Key Functions")
        self.setFixedSize(500, 600)

        self.fn_keys = fn_keys.copy()
        self.edits = {}

        layout = QFormLayout()

        for key, desc in self.fn_keys.items():
            edit = QLineEdit(desc)
            self.edits[key] = edit
            layout.addRow(f"{key}:", edit)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(buttons)
        self.setLayout(main_layout)

    def get_updated_keys(self):
        return {key: edit.text() for key, edit in self.edits.items()}


class FnKeyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        
        self.setWindowTitle("Fn Key Functions")
        self.setFixedSize(400, 700)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

       
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

       
        title_layout = QVBoxLayout()

        header_layout = QVBoxLayout()
        title = QLabel("Function Key Reference")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(14)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)

        
        settings_btn = QPushButton()
        settings_btn.setIcon(QIcon.fromTheme("configure"))
        settings_btn.setFixedSize(32, 32)
        settings_btn.setFlat(True)
        settings_btn.clicked.connect(self.show_settings)
        settings_btn.setToolTip("Edit F-key functions")

        
        btn_container = QWidget()
        btn_layout = QVBoxLayout()
        btn_layout.addWidget(settings_btn, 0, Qt.AlignRight)
        btn_layout.setContentsMargins(0, 0, 5, 0)
        btn_container.setLayout(btn_layout)
        header_layout.addWidget(btn_container)

        title_layout.addLayout(header_layout)
        layout.addLayout(title_layout)

        
        self.fn_keys = self.load_fn_keys()

        
        self.key_labels = {}
        for key, desc in self.fn_keys.items():
            label = QLabel(
                f"<b>{key}:</b> {desc}" if desc else f"<b>{key}:</b> (No function)"
            )
            label.setMargin(5)
            self.key_labels[key] = label
            layout.addWidget(label)

        # Close button
        close_label = QLabel("Press Esc or click to close")
        close_label.setAlignment(Qt.AlignCenter)
        close_label.setStyleSheet("color: gray;")
        layout.addWidget(close_label)

        # Close shortcuts
        QShortcut(QKeySequence(Qt.Key_Escape), self, self.close)

        # Set style
        self.setStyleSheet("""
            QMainWindow {
                background: #000000 ;
                border: 1px solid #aaa;
                border-radius: 5px;
            }
            QLabel {
                padding: 5px;
            }
            QPushButton:hover {
                background: #e0e0e0;
                border-radius: 3px;
            }
        """)

    def get_config_path(self):
        """Get path to config file"""
        config_dir = QStandardPaths.writableLocation(QStandardPaths.ConfigLocation)
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, "fn_key_helper.json")

    def load_fn_keys(self):
        """Load F-key functions from config file or use defaults"""
        config_file = self.get_config_path()
        default_keys = {
            "F1": "Dim Screen",
            "F2": "Brighten Screen",
            "F3": "??",
            "F4": "?",
            "F5": "Dim keyboard LED",
            "F6": "Brighten keyboard LED",
            "F7": "Rewind",
            "F8": "Play/Pause",
            "F9": "Fastforward",
            "F10": "Mute",
            "F11": "Lower Volume",
            "F12": "Increase Volume",
        }

        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    return json.load(f)
            except:
                return default_keys
        return default_keys

    def save_fn_keys(self, fn_keys):
        """Save F-key functions to config file"""
        config_file = self.get_config_path()
        with open(config_file, "w") as f:
            json.dump(fn_keys, f, indent=2)

    def show_settings(self):
        """Show settings dialog to edit F-key functions"""
        dialog = SettingsDialog(self.fn_keys, self)
        if dialog.exec_() == QDialog.Accepted:
            self.fn_keys = dialog.get_updated_keys()
            self.save_fn_keys(self.fn_keys)
            self.update_key_labels()

    def update_key_labels(self):
        """Update the displayed key descriptions"""
        for key, label in self.key_labels.items():
            desc = self.fn_keys.get(key, "")
            label.setText(
                f"<b>{key}:</b> {desc}" if desc else f"<b>{key}:</b> (No function)"
            )

    def mousePressEvent(self, event):
        # Close window when clicked
        self.close()


def main():
    app = QApplication(sys.argv)
    window = FnKeyWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
