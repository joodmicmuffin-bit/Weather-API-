
import sys
import requests

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout
)


from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label: QLabel = ("City Name ", self)
        self.input =QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.Temperature_label: QLabel("Temperature ", self)
        self.emoji_label: QLabel("Emoji ", self)
        self.description_label = QLabel("Description ", self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Weather_App = WeatherApp()
    Weather_App.show()
    sys.exit(app.exec_())












