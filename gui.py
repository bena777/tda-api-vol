from tda import auth
import pyqtgraph as pg
from pyqtgraph import PlotWidget
import datetime
import config
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1120, 900)
        MainWindow.setStyleSheet("background-color: rgb(243, 255, 233);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(420, 0, 271, 61))
        font = QtGui.QFont()
        font.setPointSize(32)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setObjectName("title")
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(460, 90, 181, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.start_button.setFont(font)
        self.start_button.setObjectName("start_button")
        self.key_input = QtWidgets.QLineEdit(self.centralwidget)
        self.key_input.setGeometry(QtCore.QRect(0, 40, 221, 20))
        self.key_input.setObjectName("key_input")
        self.key_label = QtWidgets.QLabel(self.centralwidget)
        self.key_label.setGeometry(QtCore.QRect(50, 0, 101, 31))
        self.vol_plot=PlotWidget(self.centralwidget)
        self.vol_plot.setGeometry(0,240,400,281)
        self.vol_plot.setStyleSheet("color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        font = QtGui.QFont()
        font.setPointSize(20)
        self.key_label.setFont(font)
        self.key_label.setObjectName("key_label")
        self.delta_plot = PlotWidget(self.centralwidget)
        self.delta_plot.setGeometry(QtCore.QRect(720, 240, 400, 281))
        self.delta_plot.setObjectName("delta_plot")
        self.vol_plot.setStyleSheet("color: rgb(255, 255, 255);\n"
                                    "color: rgb(0, 0, 0);")
        self.disclaimer = QtWidgets.QLabel(self.centralwidget)
        self.disclaimer.setGeometry(QtCore.QRect(780, 0, 331, 20))
        font = QtGui.QFont()
        font.setPointSize(6)
        self.disclaimer.setFont(font)
        self.disclaimer.setObjectName("disclaimer")
        self.ticker_input = QtWidgets.QLineEdit(self.centralwidget)
        self.ticker_input.setGeometry(QtCore.QRect(410, 280, 130, 51))
        self.ticker_input.setStyleSheet("border-radius:20px;\n"
"background-color: rgb(153, 175, 255);\n"
"font: 75 32pt \"Arial\";")
        self.ticker_input.setObjectName("ticker_input")
        self.expiry_input = QtWidgets.QLineEdit(self.centralwidget)
        self.expiry_input.setGeometry(QtCore.QRect(580, 280, 130, 51))
        self.expiry_input.setStyleSheet("border-radius:20px;\n"
"background-color: rgb(153, 175, 255);\n"
"font: 75 18pt \"Arial\";")
        self.expiry_input.setObjectName("expiry_input")
        self.input_labels = QtWidgets.QLabel(self.centralwidget)
        self.input_labels.setGeometry(QtCore.QRect(420, 240, 291, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.input_labels.setFont(font)
        self.input_labels.setObjectName("input_labels")
        self.gamma_plot = PlotWidget(self.centralwidget)
        self.gamma_plot.setGeometry(QtCore.QRect(0, 570, 400, 281))
        self.gamma_plot.setObjectName("graphicsView_3")
        self.theta_plot = PlotWidget(self.centralwidget)
        self.theta_plot.setGeometry(QtCore.QRect(720, 570, 400, 281))
        self.theta_plot.setObjectName("graphicsView_4")
        self.strikes_input = QtWidgets.QLineEdit(self.centralwidget)
        self.strikes_input.setGeometry(QtCore.QRect(490, 610, 130, 51))
        self.strikes_input.setStyleSheet("border-radius:20px;\n"
"background-color: rgb(153, 175, 255);\n"
"font: 75 32pt \"Arial\";")
        self.strikes_input.setObjectName("strikes_input")
        self.input_labels_2 = QtWidgets.QLabel(self.centralwidget)
        self.input_labels_2.setGeometry(QtCore.QRect(490, 570, 200, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.input_labels_2.setFont(font)
        self.input_labels_2.setObjectName("input_labels_2")
        self.vol_label = QtWidgets.QLabel(self.centralwidget)
        self.vol_label.setGeometry(QtCore.QRect(80, 180, 221, 51))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.vol_label.setFont(font)
        self.vol_label.setObjectName("vol_label")
        self.delta_label = QtWidgets.QLabel(self.centralwidget)
        self.delta_label.setGeometry(QtCore.QRect(870, 190, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.delta_label.setFont(font)
        self.delta_label.setObjectName("delta_label")
        self.gamma_label = QtWidgets.QLabel(self.centralwidget)
        self.gamma_label.setGeometry(QtCore.QRect(120, 530, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.gamma_label.setFont(font)
        self.gamma_label.setObjectName("gamma_label")
        self.theta_label = QtWidgets.QLabel(self.centralwidget)
        self.theta_label.setGeometry(QtCore.QRect(850, 530, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.theta_label.setFont(font)
        self.theta_label.setObjectName("theta_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
         #absolute path to chromedriver

        def get_data():
            self.vol_plot.clear()
            self.delta_plot.clear()
            self.theta_plot.clear()
            self.gamma_plot.clear()
            ticker = self.ticker_input.text()
            expiry = self.expiry_input.text()  # type str in YYYY-MM-DD format
            try:
                c = auth.client_from_token_file(config.token_path, config.api_key)
            except FileNotFoundError:
                from selenium import webdriver
                with webdriver.Chrome(executable_path=config.chromedriver_path) as driver:
                    c = auth.client_from_login_flow(
                        driver, config.api_key, config.redirect_uri, config.token_path)
            start_date = datetime.datetime.strptime(expiry, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(expiry, '%Y-%m-%d').date()
            r = c.get_option_chain(ticker, contract_type=c.Options.ContractType.PUT, from_date=start_date,
                                   to_date=end_date, strike_count=str(self.strikes_input.text()))
            underlying_price = (r.json()['underlyingPrice'])
            dte = start_date - datetime.date.today()
            xx = (r.json()['putExpDateMap'][expiry + ":" + str(dte.days)])
            vols = {}
            deltas = {}
            vegas = {}
            thetas = {}
            gammas = {}
            for i in xx:
                vols[i] = xx[i][0]['volatility']
                deltas[i] = xx[i][0]['delta']
                vegas[i] = xx[i][0]['vega']
                thetas[i] = xx[i][0]['theta']
                gammas[i] = xx[i][0]['gamma']

            strikes = list(vols.keys())
            strikes = [float(x) for x in strikes]
            strikes = [int(x) for x in strikes]
            self.vol_plot.plot(strikes,list(vols.values()))
            self.delta_plot.plot(strikes,list(deltas.values()))
            self.gamma_plot.plot(strikes,list(gammas.values()))
            self.theta_plot.plot(strikes,list(thetas.values()))
            underlying_line=pg.InfiniteLine(pos=underlying_price,pen='r')
            self.delta_plot.addItem(underlying_line)
            self.gamma_plot.addItem(underlying_line)
            self.theta_plot.addItem(underlying_line)
            self.vol_plot.addItem(underlying_line)
        self.start_button.clicked.connect(lambda:get_data())
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.title.setText(_translate("MainWindow", "Option Data"))
        self.start_button.setText(_translate("MainWindow", "START"))
        self.key_label.setText(_translate("MainWindow", "Dev Key"))
        self.disclaimer.setText(_translate("MainWindow", "* Created by Ben A. All data is used and owned directly by TD Ameritrade through ToS API"))
        self.ticker_input.setText(_translate("MainWindow", "SPY"))
        self.expiry_input.setText(_translate("MainWindow", "2023-01-20"))
        self.input_labels.setText(_translate("MainWindow", "Ticker             Expiry"))
        self.strikes_input.setText(_translate("MainWindow", "50"))
        self.input_labels_2.setText(_translate("MainWindow", "# Strikes"))
        self.vol_label.setText(_translate("MainWindow", "Vol Surface"))
        self.delta_label.setText(_translate("MainWindow", "Delta"))
        self.gamma_label.setText(_translate("MainWindow", "Gamma"))
        self.theta_label.setText(_translate("MainWindow", "Theta"))
        self.key_input.setText(_translate("MainWindow","KEY"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
