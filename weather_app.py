from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import sys, requests, json

class WeatherApp(QWidget):
    baseURL = "https://api.openweathermap.org/data/2.5/weather?q="
    apiKey = "&appid=e209f337bb6a6327a09ffada0f56152c"

    def __init__(self):
        super().__init__()
        with open("Weather/defaultData.json", "r") as defaults:
            jsonDataRead = defaults.read()
            dataFromJSON = json.loads(jsonDataRead)

        self.degree = dataFromJSON["degree"]
        self.defaultCity = dataFromJSON["city"]
        self.firstBoot = True

        self.vbox = QVBoxLayout()

        #setting window configuration
        self.setWindowTitle("Weather App")
        self.setWindowIcon(QIcon("Weather/cloudy.png"))
        self.setMaximumSize(QtCore.QSize(300, 200))
        self.setMinimumSize(QtCore.QSize(300, 200))

        self.menuBar()
        self.appGUI()
        self.setLayout(self.vbox)
        self.onStart()
        self.show()

    def appGUI(self):
        #Search bar & search button layout
        self.searchBox = QHBoxLayout()

        #Search bar widget
        self.searchBar = QLineEdit()
        self.searchBar.setStyleSheet("font-size:16px;")
        self.searchBar.returnPressed.connect(self.getData)
        self.searchBox.addWidget(self.searchBar)

        #Search button widget
        self.searchBtn = QPushButton("Get")
        self.searchBtn.clicked.connect(self.getData)
        self.searchBtn.setStyleSheet("font-size:16px")
        self.searchBox.addWidget(self.searchBtn)

        #City's name shows here
        self.cityName = QLabel("----")
        self.cityName.setStyleSheet("font-size: 20px;")

        #Temperature shows here
        self.result = QLabel("--")
        self.result.setStyleSheet("font-size: 18px; font-weight:bold;")

        #Decription shows here
        self.description = QLabel("--")
        self.description.setStyleSheet("font-size: 14px;")

        #Pressure shows here
        self.pressureCount = QLabel("-- : --")
        self.pressureCount.setStyleSheet("font-size: 15px;")

        #Humidity shows here
        self.humidityCount = QLabel("-- : --")
        self.humidityCount.setStyleSheet("font-size: 15px;")

        #adding all widgets to main layout
        self.vbox.addLayout(self.searchBox)
        self.vbox.addWidget(self.cityName)
        self.vbox.addWidget(self.result)
        self.vbox.addWidget(self.description)
        self.vbox.addWidget(self.pressureCount)
        self.vbox.addWidget(self.humidityCount)
    
    def menuBar(self):
        self.menu = QMenuBar(self)
        self.menu.setFixedHeight(20)

        #First menu name Option
        self.optionMenu = self.menu.addMenu("Options")
        #Options inside Option Menu
        self.unitMenu = self.optionMenu.addMenu("Temperature Units")

        #Options inside Units Menu | Options to change unit of temperature
        self.celsiusOp = self.unitMenu.addAction("Celsius", self.changeDegree)
        self.fahrenheitOp = self.unitMenu.addAction("Fahrenheit", self.changeDegree)
        self.kelvinOp = self.unitMenu.addAction("Kelvin", self.changeDegree)
        
        self.menu.show()
        self.vbox.addWidget(self.menu)

    def changeDegree(self):
        #get signal send from Unit menu of Options
        getDegree = self.sender()
        #check which is option is selected and change unit of temperature
        if getDegree.text()=="Celsius":
            self.degree = "C"
        elif getDegree.text()=="Kelvin":
            self.degree = "K"
        else:
            self.degree = "F"
        #call getData() to rewrite data on screen
        if self.firstBoot:
            self.onStart()
        else:
            self.getData()
        
    def getData(self):
        req = requests.get(self.baseURL + self.searchBar.text() + self.apiKey)
    
        if req.status_code == 200:
            data = req.json()
            temperature = data["main"]["temp"]
            #showing all data on window
            if self.degree == "K":
                self.result.setText(str(temperature) + "°K")
            elif self.degree == "C":
                self.result.setText(str(round(temperature-273.15, 2)) + "°C")
            else:
                self.result.setText(str(round((temperature-273.15)*(9/5)+32, 2)) + "°F")
            self.description.setText(data["weather"][0]["description"])
            self.cityName.setText((data["name"] + ", " + data["sys"]["country"]).upper())
            self.pressureCount.setText("Pressure: " + str(data["main"]["pressure"]) + "hPa")
            self.humidityCount.setText("Humidity: " + str(data["main"]["humidity"]) + "%")
        else:
            #if something went bad this will show error on window screen
            self.result.setText("Error")
        self.firstBoot = False
    
    def onStart(self):
        req = requests.get(self.baseURL + self.defaultCity + self.apiKey)
    
        if req.status_code == 200:
            data = req.json()
            temperature = data["main"]["temp"]
            #showing all data on window
            if self.degree == "K":
                self.result.setText(str(temperature) + "°K")
            elif self.degree == "C":
                self.result.setText(str(round(temperature-273.15, 2)) + "°C")
            else:
                self.result.setText(str(round((temperature-273.15)*(9/5)+32, 2)) + "°F")
            self.description.setText(data["weather"][0]["description"])
            self.cityName.setText((data["name"] + ", " + data["sys"]["country"]).upper())
            self.pressureCount.setText("Pressure: " + str(data["main"]["pressure"]) + "hPa")
            self.humidityCount.setText("Humidity: " + str(data["main"]["humidity"]) + "%")
        else:
            #if something went bad this will show error on window screen
            self.result.setText("Error")



if __name__=="__main__":
    app = QApplication(sys.argv)
    win = WeatherApp()
    sys.exit(app.exec_())