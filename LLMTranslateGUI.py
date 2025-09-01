import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QStackedWidget, QListWidget, QLabel, QLineEdit, QTextEdit,
                               QPushButton, QFileDialog, QComboBox, QProgressBar, QMessageBox,
                               QGroupBox, QFormLayout)
from PySide6.QtCore import Qt

class ConfigurationPage(QWidget):
    """Configuration screen for API keys and prompt settings"""
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # API Keys section
        api_group = QGroupBox("API Configuration")
        api_layout = QFormLayout()

        self.openai_key_edit = QLineEdit()
        self.openai_key_edit.setEchoMode(QLineEdit.Password)
        api_layout.addRow("OpenAI-compatible API Key:", self.openai_key_edit)

        self.mistral_key_edit = QLineEdit()
        self.mistral_key_edit.setEchoMode(QLineEdit.Password)
        api_layout.addRow("Mistral API Key:", self.mistral_key_edit)

        api_group.setLayout(api_layout)
        layout.addWidget(api_group)

        # System Prompt section
        prompt_group = QGroupBox("Translation Prompt")
        prompt_layout = QVBoxLayout()

        self.prompt_edit = QTextEdit()
        self.prompt_edit.setPlaceholderText("Enter your system prompt for translation...")
        self.prompt_edit.setMinimumHeight(300)
        prompt_layout.addWidget(self.prompt_edit)

        # Add default prompt button
        default_btn = QPushButton("Load Default Prompt")
        default_btn.clicked.connect(self.load_default_prompt)
        prompt_layout.addWidget(default_btn)

        prompt_group.setLayout(prompt_layout)
        layout.addWidget(prompt_group)

        # Save button
        save_btn = QPushButton("Save Configuration")
        save_btn.clicked.connect(self.save_config)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    def load_default_prompt(self):
        """Placeholder: Load the default system prompt"""
        # TODO: Implement loading of default system prompt
        self.prompt_edit.setPlainText("Default prompt will appear here")
        print("Load default prompt button clicked")

    def save_config(self):
        """Placeholder: Save configuration to file"""
        # TODO: Implement configuration saving
        print("Save configuration button clicked")
        QMessageBox.information(self, "Success", "Configuration saved successfully!")


class TranslationPage(QWidget):
    """Translation screen for file selection and progress monitoring"""
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # File selection
        file_group = QGroupBox("File Selection")
        file_layout = QHBoxLayout()

        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText("Select a file to translate...")
        file_layout.addWidget(self.file_path_edit)

        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_btn)

        file_group.setLayout(file_layout)
        layout.addWidget(file_group)

        # Model selection
        model_group = QGroupBox("Translation Settings")
        model_layout = QFormLayout()

        self.model_combo = QComboBox()
        self.model_combo.addItems(['openai-compatible', 'mistral'])
        model_layout.addRow("Model:", self.model_combo)

        model_group.setLayout(model_layout)
        layout.addWidget(model_group)

        # Progress section
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout()

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.progress_bar.setVisible(False)
        progress_layout.addWidget(self.progress_bar)

        self.status_label = QLabel("Ready")
        progress_layout.addWidget(self.status_label)

        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)

        # Action buttons
        button_layout = QHBoxLayout()

        self.start_btn = QPushButton("Start Translation")
        self.start_btn.clicked.connect(self.start_translation)
        button_layout.addWidget(self.start_btn)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.cancel_translation)
        self.cancel_btn.setEnabled(False)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def browse_file(self):
        """Placeholder: Open file dialog to select a file"""
        # TODO: Implement file browsing
        print("Browse file button clicked")
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select File", "", "PDF Files (*.pdf);;All Files (*)"
        )
        if file_path:
            self.file_path_edit.setText(file_path)

    def start_translation(self):
        """Placeholder: Start the translation process"""
        # TODO: Implement translation process
        print("Start translation button clicked")
        file_path = self.file_path_edit.text()
        if not file_path:
            QMessageBox.warning(self, "Warning", "Please select a file first.")
            return

        # Update UI to show progress
        self.start_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.status_label.setText("Translation in progress...")

        # TODO: Implement actual translation logic here
        # This is just a simulation
        # In real implementation, this would run in a separate thread

    def cancel_translation(self):
        """Placeholder: Cancel the ongoing translation"""
        # TODO: Implement translation cancellation
        print("Cancel translation button clicked")
        self.status_label.setText("Translation cancelled.")
        self.reset_ui()

    def reset_ui(self):
        """Reset UI to initial state"""
        self.start_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.progress_bar.setVisible(False)


class MainWindow(QMainWindow):
    """Main application window with sidebar navigation"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LLM Translation Tool")
        self.setGeometry(100, 100, 900, 600)

        self.initUI()

    def initUI(self):
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        # Create sidebar
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(150)
        self.sidebar.addItems(["Configuration", "Translation"])
        self.sidebar.currentRowChanged.connect(self.change_page)

        # Create stacked widget for pages
        self.stacked_widget = QStackedWidget()
        self.config_page = ConfigurationPage()
        self.translation_page = TranslationPage()

        self.stacked_widget.addWidget(self.config_page)
        self.stacked_widget.addWidget(self.translation_page)

        # Add widgets to main layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stacked_widget)

        # Select first page by default
        self.sidebar.setCurrentRow(0)

    def change_page(self, index):
        """Change the current page based on sidebar selection"""
        self.stacked_widget.setCurrentIndex(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
