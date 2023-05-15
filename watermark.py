import os
import math
import random
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget
from utils import extract_watermark,apply_watermark,watermark_images






class WatermarkApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Watermark App")
        self.setGeometry(100, 100, 400, 200)

        self.input_folder = ""
        self.output_folder = ""

        self.create_widgets()

    def create_widgets(self):
        widget = QWidget(self)
        layout = QVBoxLayout(widget)

        self.input_label = QLabel("Input Directory:")
        layout.addWidget(self.input_label)

        self.input_path_label = QLabel("")
        layout.addWidget(self.input_path_label)

        self.input_button = QPushButton("Select Input Directory")
        self.input_button.clicked.connect(self.select_input_directory)
        layout.addWidget(self.input_button)

        self.output_label = QLabel("Output Directory:")
        layout.addWidget(self.output_label)

        self.output_path_label = QLabel("")
        layout.addWidget(self.output_path_label)

        self.output_button = QPushButton("Select Output Directory")
        self.output_button.clicked.connect(self.select_output_directory)
        layout.addWidget(self.output_button)

        self.text_label = QLabel("Watermark Text:")
        layout.addWidget(self.text_label)



        self.text_input = QLineEdit()
        layout.addWidget(self.text_input)

        self.font_size_label = QLabel("Font Size:")
        layout.addWidget(self.font_size_label)

        self.font_size_input = QLineEdit()
        layout.addWidget(self.font_size_input)

        self.watermark_button = QPushButton("Apply Watermark")
        self.watermark_button.clicked.connect(self.apply_watermark)
        layout.addWidget(self.watermark_button)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        self.setCentralWidget(widget)

    def select_input_directory(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Input Directory")
        self.input_folder = folder
        self.input_path_label.setText(folder)

    def select_output_directory(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        self.output_folder = folder
        self.output_path_label.setText(folder)

    def apply_watermark(self):
        if not self.input_folder or not self.output_folder:
            self.status_label.setText("Please select input and output directories.")
            return

        text = self.text_input.text()
        font_size = int(self.font_size_input.text())

        watermark_images(self.input_folder, self.output_folder, text, font_size)

        self.status_label.setText("Watermark applied to images.")

        self.input_folder = ""
        self.output_folder = ""
        self.input_path_label.setText("")
        self.output_path_label.setText("")
        self.text_input.setText("")
        self.font_size_input.setText("")

        self.status_label.setText("Watermark applied to images.")

if __name__ == '__main__':
    app = QApplication([])
    window = WatermarkApp()
    window.show()
    app.exec_()