import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import requests

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel('Enter City Name:', self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton('Get Weather', self)
        self.weather_result = QLabel("", self)
        self.weather_emoji = QLabel('', self)
        self.description = QLabel('', self)
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Weather API App')
        self.setWindowIcon(QIcon('weather_icon.png'))

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.weather_result)
        vbox.addWidget(self.weather_emoji)
        vbox.addWidget(self.description)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.weather_result.setAlignment(Qt.AlignCenter)
        self.weather_emoji.setAlignment(Qt.AlignCenter)
        self.description.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.weather_emoji.setObjectName("weather_emoji")
        self.description.setObjectName("description")
        self.weather_result.setObjectName("weather_result")

        self.setStyleSheet("""
            QLabel#city_label {
                font-size: 50px;
                font-family: calibri;
                font-style: italic;
        }
            QPushButton{
                font-size: 30px;
                font-family: calibri;
                font-weight: bold;                   
        }   
            QLineEdit{
                font-size: 40px;
        }   
            QLabel#weather_result {
                font-size: 50px;
                font-family: calibri;
                font-weight: bold;
        }
            QLabel#weather_emoji {
                font-size: 100px;
                font-family: segoe ui emoji;
        }
            QLabel#description {
                font-size: 30px;
                font-family: calibri;
                font-weight: bold;
        }                        
    """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "524faa4367f86b888d4c9626f1751d81"
        city_name = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.update_weather(data)
                
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request,\nplease check your input.")
                case 401:
                    self.display_error("Unauthorized,\nplease check your API key.")
                case 403:
                    self.display_error("Forbidden,\nplease check your API key.")
                case 404:
                    self.display_error("City not found,\nplease check the city name.")
                case 500:
                    self.display_error("Internal server error,\nplease try again later.")
                case 502:
                    self.display_error("Bad gateway,\nplease try again later.")
                case 503:
                    self.display_error("Service unavailable\nplease try again later.")
                case 504:
                    self.display_error("Gateway timeout,\nplease try again later.")
                case _:
                    self.display_error(f"An error occurred,\n{http_error}.")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection error,\nplease check your internet connection.")
        except requests.exceptions.Timeout:
            self.display_error("Request timed out,\nplease try again later.")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects,\nplease check the URL.")
        except requests.exceptions.RequestException as e:
            self.display_error(f"An error occurred,\n{e}.") 

    def update_weather(self, weather_data):
        self.weather_result.setStyleSheet("font-size: 50px;")
        temperature = weather_data["main"]["temp"] - 273.15
        self.weather_result.setText(f"{temperature:.2f} °C")
        description = weather_data["weather"][0]["description"]
        self.description.setText(description.capitalize())

        weather_id = weather_data["weather"][0]["id"]
        self.weather_emoji.setText(self.get_weather_id(weather_id))  

    def display_error(self, error_message):
        self.weather_result.setStyleSheet("font-size: 30px;")
        self.weather_result.setText(error_message)
        self.description.clear()
        self.weather_emoji.clear()

    def get_weather_id(self, weather_id):
        if weather_id >= 200 and weather_id < 300:
            return "⛈️"  # Thunderstorm
        elif weather_id >= 300 and weather_id < 500:
            return "🌦️"  # Drizzle
        elif weather_id >= 500 and weather_id < 600:
            return "🌧️"  # Rain
        elif weather_id >= 600 and weather_id == 622:
            return "❄️"  # Snow
        elif weather_id >= 701 and weather_id < 741:
            return "🌫️"  # Atmosphere (fog, mist, etc.
        elif weather_id >= 751 and weather_id <= 761:
            return "🌪️"  # Dust
        elif weather_id == 762:
            return "🌋"  # Volcanic Ash
        elif weather_id == 771:
            return "💨"  # Squall
        elif weather_id == 781:
            return "🌪️"  # Tornado
        elif weather_id == 800:
            return "☀️"  # Clear
        elif weather_id >= 801 and weather_id <= 804:
            return "☁️"  # Clouds
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('weather_icon.png'))
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())   