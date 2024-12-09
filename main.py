import sys
import time
import mediapipe as mp
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
import os
import cv2
from bokeh_and_overlay import bokeh_bg
from img_segmentation import icon_segmentation
from img_segmentation import person_segmentation
from img_overlay import img_overlayv2
from bokeh_effect import bokeh
from extra_features import resize

class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        
        self.setPixmap(QPixmap('Input/Other/bokehswap_splash.png').scaled(800, 600, Qt.AspectRatioMode.KeepAspectRatio))
        self.show()
class AlternativeGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BokehSwap")
        self.setWindowIcon(QtGui.QIcon('Input/Icon/app_logo.png'))
        self.setFixedSize(1200, 900)

        self.theme_colors()
        self.default_stuff()
        self.col1()
        self.col2()
        self.col3()
        self.col4()
        self.col5()

        self.clear_paths()
        self.clear_labels()
        self.signals()

    def default_stuff(self):
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

    def theme_colors(self):
        self.theme1 = '#F6C6AD'
        self.theme2 = '#F2AA84'
        self.theme3 = '#C04F15'
        self.theme4 = '#80350E'
        self.theme5 = '#000000'

    def custom_block(self, color, width, height, x=0, y=0):
        block = QLabel(self)
        block.setStyleSheet('background:'+color)
        block.setGeometry(x, y, width, height)
        return block
    
    def col1(self):
        self.face_block = self.custom_block(self.theme1, 300, 675)
        
        self.input_label = QLabel("Input Image Here", parent=self)
        self.stylize_label(self.input_label)
        
        self.upload_input_btn = QPushButton("Upload Input Image", parent=self)
        self.stylize_button(self.upload_input_btn)

        self.place_center(self.input_label, self.face_block)
        self.place_down(self.upload_input_btn, self.input_label)
        self.center_horizontally(self.upload_input_btn, self.input_label)

    def col2(self):
        self.icon_block = self.custom_block(self.theme2, 300, 675)
        
        self.icon_label = QLabel("Icon Image Here", parent=self)
        self.stylize_label(self.icon_label)
        
        self.upload_icon_btn = QPushButton("Upload Icon Image", parent=self)
        self.stylize_button(self.upload_icon_btn)

        self.place_right(self.icon_block, self.face_block)
        self.place_center(self.icon_label, self.icon_block)
        self.place_down(self.upload_icon_btn, self.icon_label)
        self.center_horizontally(self.upload_icon_btn, self.icon_label)

    def col3(self):
        self.bg_block = self.custom_block(self.theme3, 300, 675)
        
        self.background_label = QLabel("Background Image Here", parent=self)
        self.stylize_label(self.background_label)
        
        self.upload_background_btn = QPushButton("Upload Background Image", parent=self)
        self.stylize_button(self.upload_background_btn)

        self.place_right(self.bg_block, self.icon_block)
        self.place_center(self.background_label, self.bg_block)
        self.place_down(self.upload_background_btn, self.background_label)
        self.center_horizontally(self.upload_background_btn, self.background_label)

    def col4(self):
        self.output_block = self.custom_block(self.theme4, 300, 675)
        
        self.output_label = QLabel("Processed Image Here", parent=self)
        self.stylize_label(self.output_label)
        
        self.process_btn = QPushButton("Processed Image", parent=self)
        self.process_btn.setCheckable(True)
        self.button_group.addButton(self.process_btn)
        self.stylize_button(self.process_btn)

        self.place_right(self.output_block, self.bg_block)
        self.place_center(self.output_label, self.output_block)
        self.place_down(self.process_btn, self.output_label)
        self.center_horizontally(self.process_btn, self.output_label)

    def col5(self):
        self.other_block = self.custom_block(self.theme5, 1200, 225)
        self.enhance_btn = QPushButton("Enhance Image?", parent=self)
        self.enhance_btn.setCheckable(True)
        self.stylize_button(self.enhance_btn, w=500, h=100)

        self.reset_btn = QPushButton("Reset", parent=self)
        self.reset_btn.setCheckable(True)
        self.button_group.addButton(self.reset_btn)
        self.stylize_button(self.enhance_btn, w=200, h=50)

        self.place_down(self.other_block, self.face_block, spacing=0)
        self.place_center(self.enhance_btn, self.other_block)
        self.place_down(self.reset_btn, self.enhance_btn, 25)
        self.center_horizontally(self.reset_btn, self.enhance_btn)

    def error_notif(self):
        self.notification = QMessageBox(self)
        self.notification.setWindowTitle("Error")
        self.notification.setWindowIcon(QtGui.QIcon('Input/Icon/stop.png'))
        self.notification.setText("Please reset first")
        self.notification.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.notification.setIcon(QMessageBox.Icon.Warning)

        self.notification.exec()
        
    def signals(self):
        self.upload_input_btn.clicked.connect(self.upload_input_image)
        self.upload_icon_btn.clicked.connect(self.upload_icon_image)
        self.upload_background_btn.clicked.connect(self.upload_background_image)
        self.process_btn.toggled.connect(self.process_images)
        self.enhance_btn.toggled.connect(self.enhance_image)
        self.reset_btn.toggled.connect(self.reset_gui)
    
    def clear_paths(self):
        self.input_image_path = None
        self.icon_image_path = None
        self.background_image_path = None
        self.output_path = None

    def clear_labels(self):
        self.input_label.clear()
        self.icon_label.clear()
        self.background_label.clear()
        self.output_label.clear()

        self.input_label.setText("Input Image Here")
        self.icon_label.setText("Icon Image Here")
        self.background_label.setText("Background Image Here")
        self.output_label.setText("Procesed Image Here")

    def clear_buttons(self):
        for button in self.button_group.buttons():
            button.setChecked(False)

    def stylize_label(self, label, w=250, h=250):
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFixedSize(w, h)
        label.setStyleSheet("border: 1px solid black;"
                            "background: white")

    def stylize_button(self, button, w=275, h=50):
        button.setFixedSize(w, h)

    def place_right(self, target, dest, spacing=0):
        target.move(int(dest.width()+dest.x()+spacing),
                    dest.y())
    
    def place_down(self, target, dest, spacing=25):
        target.move(dest.x(), 
                    int(dest.height()+dest.y()+spacing))
    
    def place_center(self, target, dest):
        target.move(int((dest.width()-target.width())/2+dest.x()), 
                    int((dest.height()-target.height())/2)+dest.y())

    def center_horizontally(self, target, dest):
        target.move(int((dest.width()-target.width())/2+dest.x()), 
                    target.y())
        
    def upload_input_image(self):
        if self.output_path != None:
            self.error_notif()
            return
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Input Image", "Input/Face", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.input_image_path = file_path
            self.input_label.setPixmap(QPixmap(file_path).scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))

    def upload_icon_image(self):
        if self.output_path != None:
            self.error_notif()
            return
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Icon Image", "Input/Icon", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.icon_image_path = file_path
            self.icon_label.setPixmap(QPixmap(file_path).scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))

    def upload_background_image(self):
        if self.output_path != None:
            self.error_notif()
            return
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Background Image", "Input/Background", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.background_image_path = file_path
            self.background_label.setPixmap(QPixmap(file_path).scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))

    def process_images(self, checked):
        if not all([self.input_image_path, self.icon_image_path, self.background_image_path]):
            self.output_label.setText("Please upload all images.\n Press Reset to try again.")
            self.clear_buttons()
            return
        if checked:
            self.output_path = os.path.relpath("Output/Overlay/processed_image.jpeg")
            icon_mask = icon_segmentation.segment_iconv2(self.icon_image_path)
            bokeh_background = bokeh_bg(self.input_image_path, self.icon_image_path, self.background_image_path, bokeh_selector=0)
            result = img_overlayv2.img_overlay(bokeh_background, self.icon_image_path, output_path="processed_image")
            try:
                self.output_label.setPixmap(QPixmap(self.output_path).scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))
            except:
                pass

    def enhance_image(self, checked):
        try:
            if not self.output_path:
                return
            original_path = os.path.relpath("Output/Overlay/processed_image.jpeg")
            enhanced_path = os.path.relpath("Output/randomly_enhanced_img.jpeg")
            if checked:
                self.output_label.setPixmap(QPixmap(enhanced_path).scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))
            else:
                self.output_label.setPixmap(QPixmap(original_path).scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))
        except:
            pass
    
    def reset_gui(self, checked):
        try:
            if checked:
                self.clear_paths()
                self.clear_labels()
                self.clear_buttons()
        except:
            pass
        
class BokehGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BokehSwap")
        self.setWindowIcon(QtGui.QIcon('Input/Icon/app_logo.png'))
        self.resize(1200, 900)
        self.setStyleSheet(
            """
            #MainWindow {
                background-image: url('Input/Background/page_bg.png');
                background-repeat: no-repeat;
                background-position: center;
            }
            """
        )
        main_layout = QVBoxLayout()
        image_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        self.input_label = QLabel("Input Image Here")
        self.icon_label = QLabel("Icon Image Here")
        self.background_label = QLabel("Background Image Here")
        self.output_label = QLabel("Processed Image Here")

        for label in [self.input_label, self.icon_label, self.background_label, self.output_label]:
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setFixedSize(250, 250)
            label.setStyleSheet("border: 1px solid black;")

        image_layout.addWidget(self.input_label)
        image_layout.addWidget(self.icon_label)
        image_layout.addWidget(self.background_label)
        image_layout.addWidget(self.output_label)

        self.upload_input_btn = QPushButton("Upload Input Image")
        self.upload_icon_btn = QPushButton("Upload Icon Image")
        self.upload_background_btn = QPushButton("Upload Background Image")
        self.process_btn = QPushButton("Process Images")

        button_layout.addWidget(self.upload_input_btn)
        button_layout.addWidget(self.upload_icon_btn)
        button_layout.addWidget(self.upload_background_btn)
        button_layout.addWidget(self.process_btn)

        self.upload_input_btn.clicked.connect(self.upload_input_image)
        self.upload_icon_btn.clicked.connect(self.upload_icon_image)
        self.upload_background_btn.clicked.connect(self.upload_background_image)
        self.process_btn.clicked.connect(self.process_images)

        main_layout.addLayout(image_layout)
        main_layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # image paths
        self.input_image_path = None
        self.icon_image_path = None
        self.background_image_path = None

    def upload_input_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Input Image", "Input/Face", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.input_image_path = file_path
            self.input_label.setPixmap(QPixmap(file_path).scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))

    def upload_icon_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Icon Image", "Input/Icon", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.icon_image_path = file_path
            self.icon_label.setPixmap(QPixmap(file_path).scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))

    def upload_background_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Background Image", "Input/Background", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.background_image_path = file_path
            self.background_label.setPixmap(QPixmap(file_path).scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))

    def process_images(self):
        if not all([self.input_image_path, self.icon_image_path, self.background_image_path]):
            self.output_label.setText("Please upload all images.")
            return
        self.output_path = os.path.relpath("Output/Overlay/processed_image.jpeg")
        icon_mask = icon_segmentation.segment_iconv2(self.icon_image_path)
        bokeh_background = bokeh_bg(self.input_image_path, self.icon_image_path, self.background_image_path, bokeh_selector=0)
        result = img_overlayv2.img_overlay(bokeh_background, self.icon_image_path, output_path="processed_image")
        try:
            self.output_label.setPixmap(QPixmap(self.output_path).scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))
        except:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)

    splash = SplashScreen()
    
    for i in range(1, 101):
        time.sleep(0.02)  
        splash.showMessage(f"Loading... {i}%", Qt.AlignBottom | Qt.AlignCenter, Qt.black)
        QApplication.processEvents()

    # window = BokehGUI()
    window = AlternativeGui()
    window.show()
    splash.finish(window)

    sys.exit(app.exec())

