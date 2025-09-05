import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QStackedWidget, QListWidget, QLabel, QLineEdit, QTextEdit,
                               QPushButton, QFileDialog, QComboBox, QProgressBar, QMessageBox,
                               QGroupBox, QFormLayout)
from PySide6.QtCore import Qt, QThread, Signal

import configparser
from pathlib import Path

import MistralOCR
from mistralai import Mistral
from LLMTranslate import apiCall
from utility import filenameFromPath
from openai import OpenAI
from openai.types.chat.chat_completion import Choice
import os

class AppConfig:
    """Central configuration object for the application"""
    def __init__(self):
        self.openai_url = ""
        self.openai_key = ""
        self.mistral_key = ""
        self.system_prompt = ""

    def load_from_file(self, config_file = Path("LLM-translate-config.ini")):
        """Load configuration from file"""
        try:
            config = configparser.ConfigParser()
            config.read(config_file)

            if 'DEFAULT' in config:
                self.openai_url = config['DEFAULT'].get('openai_url', '')
                self.openai_key = config['DEFAULT'].get('openai', '')
                self.mistral_key = config['DEFAULT'].get('mistral', '')

            if 'PROMPT' in config and 'system_prompt' in config['PROMPT']:
                self.system_prompt = config['PROMPT']['system_prompt']

            return True
        except Exception as e:
            print(f"Error loading config: {e}")
            return False

    def save_to_file(self, config_file="LLM-translate-config.ini"):
        """Save configuration to file"""
        try:
            config = configparser.ConfigParser()
            config['DEFAULT'] = {
                'openai_url': self.openai_url,
                'openai': self.openai_key,
                'mistral': self.mistral_key
            }

            config['PROMPT'] = {
                'system_prompt': self.system_prompt
            }

            with open(config_file, 'w') as f:
                config.write(f)

            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False



class ConfigurationPage(QWidget):
    """Configuration screen for API keys and prompt settings"""
    def __init__(self, app_config):
        super().__init__()
        self.app_config = app_config
        self.initUI()
        self.load_config()

    def initUI(self):
        layout = QVBoxLayout()

        # API Keys section
        api_group = QGroupBox("API Configuration")
        api_layout = QFormLayout()


        self.openai_url_edit = QLineEdit()
        api_layout.addRow("OpenAI-compatible API URL:", self.openai_url_edit)

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


        prompt_group.setLayout(prompt_layout)
        layout.addWidget(prompt_group)

        # Save button
        save_btn = QPushButton("Save Configuration")
        save_btn.clicked.connect(self.save_config)
        layout.addWidget(save_btn)

        self.setLayout(layout)


    def load_config(self):
        """loads the config"""
        self.openai_url_edit.setText(self.app_config.openai_url)
        self.openai_key_edit.setText(self.app_config.openai_key)
        self.mistral_key_edit.setText(self.app_config.mistral_key)
        self.prompt_edit.setPlainText(self.app_config.system_prompt)

    def save_config(self):
        """Save configuration to file"""
        # Update the shared config object
        self.app_config.openai_url = self.openai_url_edit.text()
        self.app_config.openai_key = self.openai_key_edit.text()
        self.app_config.mistral_key = self.mistral_key_edit.text()
        self.app_config.system_prompt = self.prompt_edit.toPlainText()

        # Save to file
        if self.app_config.save_to_file():
            QMessageBox.information(self, "Success", "Configuration saved successfully!")
        else:
            QMessageBox.critical(self, "Error", "Failed to save configuration!")

class TranslationPage(QWidget):
    """Translation screen for file selection and progress monitoring"""
    def __init__(self, app_config):
        super().__init__()
        self.app_config = app_config  # Reference to shared config
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
        """Start the OCR and translation process"""
        print("Start translation button clicked")
        file_path = self.file_path_edit.text()
        if not file_path:
            QMessageBox.warning(self, "Warning", "Please select a file first.")
            return
        if not os.path.exists(file_path):
            QMessageBox.warning(self, "Warning", "The selected file does not exist.")
            return



        # Update UI to show progress
        self.start_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.status_label.setText("Translation in progress...")

        # implement the translation thread
        self.worker = TranslationWorker(file_path, self.model_combo.currentText(), self.app_config)

        # Connect signals
        self.worker.progress_update.connect(self.update_progress)
        self.worker.status_update.connect(self.status_label.setText)
        self.worker.finished.connect(self.translation_finished)

        # Start the thread
        self.worker.start()

    def cancel_translation(self):
        """Placeholder: Cancel the ongoing translation"""
        if hasattr(self, 'worker') and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()
        print("Cancel translation button clicked")
        self.status_label.setText("Translation cancelled.")
        self.reset_ui()

    def reset_ui(self):
        """Reset UI to initial state"""
        self.start_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.progress_bar.setVisible(False)

    def update_progress(self, page_num):
        self.status_label.setText(f"Processing page {page_num}")

    def translation_finished(self, success, message):
        self.reset_ui()
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.critical(self, "Error", message)


class TranslationWorker(QThread):
    """OCR and translation main thread"""
    progress_update = Signal(int)  # current, total
    status_update = Signal(str)
    finished = Signal(bool, str)  # success, message


    def __init__(self, file_path, model, app_config):
        super().__init__()
        self.file_path = file_path
        self.model = model
        self.app_config = app_config
        self._is_running = True

        # Initialize llm clients
        self.mistral_client = Mistral(api_key=self.app_config.mistral_key)
        self.openai_client = OpenAI(
            base_url=self.app_config.openai_url,
            api_key=self.app_config.openai_key,
        )

    def run(self):
        try:
            # OCR for PDF files
            if self.file_path.lower().endswith('.pdf'):
                self.status_update.emit("Performing OCR...")


                # Perform OCR
                MistralOCR.ocrCall(self.file_path, self.mistral_client)

                # Use OCR output as input for translation
                input_file = filenameFromPath(self.file_path) + " ocred.md"
                self.status_update.emit("OCR completed. Starting translation...")

            else:
                input_file = self.file_path

            # enumerate chunks for translation
            parsedListFromFile = []
            with open(input_file, 'r', encoding='utf-8') as f:
                pageNum = 0
                for line in f:

                    if not self._is_running:
                        break

                    if line.strip() != "---":
                        parsedListFromFile.append(line)
                    else:
                        content = ""
                        for index, item in enumerate(parsedListFromFile):
                            content = content + item + '\n'
                        parsedListFromFile = []
                        # Call translation API TODO: add custom llmName support
                        apiCall(
                            content,
                            self.file_path,
                            self.model,
                            self.mistral_client,
                            self.openai_client,
                            self.app_config.system_prompt,
                            "deepseek/deepseek-r1:free"
                        )
                        # Update progress
                        pageNum = pageNum + 1
                        self.progress_update.emit(pageNum)


            if self._is_running:
                self.finished.emit(True, "Translation completed successfully!")
            else:
                self.finished.emit(False, "Translation cancelled.")

        except Exception as e:
            self.finished.emit(False, f"Error: {str(e)}")

    def stop(self):
        self._is_running = False


class MainWindow(QMainWindow):
    """Main application window with sidebar navigation"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LLM Translation Tool")
        self.setGeometry(100, 100, 900, 600)

        # Create central configuration object
        self.app_config = AppConfig()
        self.app_config.load_from_file()

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
        self.config_page = ConfigurationPage(self.app_config)
        self.translation_page = TranslationPage(self.app_config)

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
