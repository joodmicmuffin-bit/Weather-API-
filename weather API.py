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

        self.city_label = QLabel("City Name", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather API")
        self.setGeometry(300, 300, 350, 500)

        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)


        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: Calibri;
            }

            QLabel#city_label {
                font-size: 25px;
            }

            QLineEdit#city_input {
                font-size: 20px;
                padding: 5px;
            }

            QPushButton#get_weather_button {
                font-size: 25px;
                font-weight: bold;
                padding: 5px;
            }

            QLabel#temperature_label {
                font-size: 60px;
            }

            QLabel#emoji_label {
                font-size: 100px;
                font-family: "Segoe UI Emoji";
                min-height: 120px;
            }

            QLabel#description_label {
                font-size: 30px;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "12b8ff5bceca5500020d451d952cd62d"
        city = self.city_input.text().strip()

        if not city:
            self.display_error("Please enter a city name")
            return

        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={api_key}&units=metric"
        )

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized\nInvalid API key")
                case 403:
                    self.display_error("Forbidden\nAccess is denied")
                case 404:
                    self.display_error("City not found")
                case 500:
                    self.display_error("Internal server error\nPlease try again later")
                case 502:
                    self.display_error("Bad gateway\nInvalid server response")
                case 503:
                    self.display_error("Service unavailable")
                case 504:
                    self.display_error("Gateway timeout")
                case _:
                    self.display_error(f"Unexpected error\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection error\nCheck your internet")
        except requests.exceptions.Timeout:
            self.display_error("Request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request error\n{req_error}")

    def display_error(self, message):
        self.temperature_label.setText("")
        self.emoji_label.setText("❌")
        self.description_label.setStyleSheet("font-size: 15px;")
        self.description_label.setText(message)

    def display_weather(self, data):
        self.description_label.setStyleSheet("font-size: 30px;")

        temperature_c = data["main"]["temp"]
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        self.temperature_label.setText(f"{temperature_c:.0f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description.title())

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return "❓"


if __name__ == "__main__":

    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())

