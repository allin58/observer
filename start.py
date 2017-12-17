import sys
import datetime
import time
from smsc.messages import SMSMessage
from smsc.api import SMSC
import threading
# Импортируем наш интерфейс из файла
from MainW import *
from bittrex import Bittrex
from PyQt5 import QtCore, QtGui, QtWidgets

login = ""
password = ""
phone  = ""




class MainWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui =  Ui_MainWindow()
        self.ui.setupUi(self)

        # Здесь прописываем событие нажатия на кнопку
        self.ui.pushButton.clicked.connect(self.MyFunctionAdd)
        self.ui.pushButton_2.clicked.connect(self.MyFunctionAccept)
        self.ui.pushButton_3.clicked.connect(self.MyFunctionDelete)


    # Пока пустая функция которая выполняется
    # при нажатии на кнопку



    def MyFunctionAccept(self):
        global login
        global password
        global phone

        login = self.ui.textEdit.toPlainText()
        password = self.ui.textEdit_2.toPlainText()
        phone = self.ui.textEdit_3.toPlainText()

    def MyFunctionAdd(self):
        pair = self.ui.textEdit_5.toPlainText()
        price = self.ui.textEdit_4.toPlainText()
        self.ui.listWidget.addItem(pair+ " " + price)

    def MyFunctionDelete(self):
        item = self.ui.listWidget.takeItem(self.ui.listWidget.currentRow())
        item = None






def observe():

    while True:
     amount =myapp.ui.listWidget.count()
     time.sleep(1)
     if(amount>0):

        for index in range(myapp.ui.listWidget.count()):

            request = myapp.ui.listWidget.item(index)

            data = request.text().split(" ")

            ticker = data[0]
            price = float(data[1])

            bittrex_request = bot_Bittrex.get_ticker(ticker)

            d=datetime.datetime.now()
            print(d)
            print(bittrex_request)

            time.sleep(10)


            if(bittrex_request["success"]):

                div = price/float(bittrex_request["result"]["Ask"])*100

                if(div>99.5 and div<100.5):

                    mesage = ticker + " " + str(price)

                    client = SMSC(login=login, password=password)
                    cost = client.send(to=phone, message=SMSMessage(text=mesage))
                    print(cost)
                    item = myapp.ui.listWidget.takeItem(index)
                    item = None


if __name__=="__main__":

    Key_Bittrex = "0"
    Secret_Bittrex = "0"
    bot_Bittrex = Bittrex(Key_Bittrex, Secret_Bittrex)



    app = QtWidgets.QApplication(sys.argv)
    myapp = MainWin()
    myapp.show()
    t = threading.Thread(target=observe)
    t.start()
    sys.exit(app.exec_())



