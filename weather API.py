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
        self.temperature_label = QLabel("30°C", self)
        self.emoji_label = QLabel("🌞", self)
        self.description_label = QLabel("Description", self)

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

        # set objects ---->

        self.city_label.setObjectName('city_label')
        self.city_input.setObjectName('city_input')
        self.temperature_label.setObjectName('temperature_label')
        self.emoji_label.setObjectName('emoji_label')
        self.description_label.setObjectName('description_label')
        self.get_weather_button.setObjectName('get_weather_button')


        #CSS code part

        self.setStyleSheet("""
            QLabel,QPushButton {
                font-family: calibri;
            }

            QLabel#city_label {
                font-size: 25px;
            }
            
            QLineEdit#city_input {
                font-size: 20px;
            }
            
            QPushButton#get_weather_button {
                font-size: 25px;
                font-weight: bold;
            }
            
            QLabel#temperature_label {
                font-size: 60px;
            }
            
            QLabel#emoji_label {
                font-size: 70px;
            }
            
            QLabel#description_label {
                font-size: 40px; 
            }
            
            
        """)
        self.get_weather_button.clicked.connect(self.get_weather)


    def get_weather(self):
        api_key = "12b8ff5bceca5500020d451d952cd62d"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    print("Bad request\nplease check your input")
                case 401:
                    print("Unauthorized\nInvalid API Key")
                case 403:
                    print("Forbidden\nAccess is denied")
                case 404:
                    print("not found\nCity not found")
                case 500:
                    print("Internal Server Error\nPlease try again later.")
                case 502:
                    print("Bad Gateway\nServer received an invalid response.")
                case 503:
                    print("Service Unavailable\nThe server is temporarily unavailable.")
                case 504:
                    print("Gateway Timeout\nThe server took too long to respond.")
                case _:
                    print(F"Unexpected error occurred\n{http_error}.")

        except requests.exceptions.ConnectionError:
            print("Connection Error:\nCheck your internet connection.")
        except requests.exceptions.Timeout:
            print("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            print("Too many redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            print(f"Request Error:\n{req_error}")



    def display_error(self, message):
        pass






if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())