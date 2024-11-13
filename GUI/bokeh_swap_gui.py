from PyQt6 import QtWidgets, uic
import sys
sys.path.append(".")


class BokehSwapUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("GUI/bokeh_swap_ui.ui", self)
        self.setWindowTitle("Bokeh Swap")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = BokehSwapUI()
    window.show()
    sys.exit(app.exec())