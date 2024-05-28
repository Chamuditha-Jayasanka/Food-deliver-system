from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox,QTableWidgetItem
from PyQt5 import uic
import sys
import sqlite3
import bcrypt


conn = sqlite3.connect('food.db')
cursor = conn.cursor()

lodedUser = ''


class LoginUI(QMainWindow):
    def __init__(self):
        super(LoginUI, self).__init__()
        uic.loadUi("login.ui", self)

        self.pushButton_2.clicked.connect(self.openSignup)
        self.pushButton.clicked.connect(self.login)


    def openSignup(self):
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.hide()
        signup_ui.show()

    
    def login(self):
        global lodedUser
        lodedUser = username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if username != '' and password != '':
            cursor.execute('SELECT password FROM user WHERE username=?',[username])
            result = cursor.fetchone()
            if result:
                if bcrypt.checkpw(password.encode('utf-8'),result[0]):
                    QMessageBox.information(None, "Information", "logged in successfull")
                    self.lineEdit.setText("")
                    self.lineEdit_2.setText("")
                    self.hide()
                    home_ui.show()
                else:
                    QMessageBox.information(None, "Information", "Invalid password")
            else:
                QMessageBox.information(None, "Information", "Invalid username")
        else:
            QMessageBox.information(None, "Information", "All fields are required")
        
       
        




class SignupUI(QMainWindow):
    def __init__(self):
        super(SignupUI, self).__init__()
        uic.loadUi("signup.ui", self)

        self.pushButton_2.clicked.connect(self.goBackToLogin)
        self.pushButton.clicked.connect(self.goBackToLogin2)

    def goBackToLogin2(self):
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.hide()
        login_ui.show()

    def goBackToLogin(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        if username != '' and password != '' :
            cursor.execute('SELECT username FROM user WHERE username=?',[username])
            if cursor.fetchone() is not None:
                QMessageBox.information(None, "Information", "Username already exists.")
            else:
                encodePassword = password.encode('utf-8')
                hashedPassword = bcrypt.hashpw(encodePassword,bcrypt.gensalt())
                cursor.execute('INSERT INTO user VALUES (?,?)',[username,hashedPassword])
                conn.commit()
                QMessageBox.information(None, "Information", "Signup successfull")
                self.lineEdit.setText("")
                self.lineEdit_2.setText("")
                self.hide()
                login_ui.show()
        else:
            QMessageBox.information(None, "Information", "All fields are required")

class homeUI(QMainWindow):
    def __init__(self):
        super(homeUI, self).__init__()
        uic.loadUi("home.ui", self)

        self.pushButton.clicked.connect(self.restaurant)
        self.pushButton_2.clicked.connect(self.goToResMesus)
        self.pushButton_3.clicked.connect(self.goToCart)
        self.pushButton_5.clicked.connect(self.goToOders)
        self.pushButton_4.clicked.connect(self.logOut)

    def goToOders(self):
        self.hide()
        oder_ui.show()

    def logOut(self):
        self.hide()
        login_ui.show()

    def restaurant(self):
        self.hide()
        restaurant_ui.show()

    def goToResMesus(self):
        self.hide()
        restaurant_menus.show()

    def goToCart(self):
        self.hide()
        view_cart.show()

class RestaurantUI(QMainWindow):
    def __init__(self):
        super(RestaurantUI, self).__init__()
        uic.loadUi("restaurant.ui", self)
        self.load_items()

        self.pushButton.clicked.connect(self.createRestaurant)
        self.pushButton_3.clicked.connect(self.saveItem)
        self.pushButton_7.clicked.connect(self.searchItem)
        self.pushButton_4.clicked.connect(self.removeItem)
        self.pushButton_5.clicked.connect(self.updateItem)
        self.pushButton_2.clicked.connect(self.deleteRestaurant)
        self.pushButton_8.clicked.connect(self.backhome)

    def backhome(self):
        self.lineEdit.setText("")
        self.clearItemsFileds()
        self.hide()
        home_ui.show()

    def createRestaurant(self):
        name = self.lineEdit.text()
        if name != '':
            cursor.execute('SELECT name FROM restaurant WHERE name=?',[name])
            if cursor.fetchone() is not None:
                QMessageBox.information(None, "Information", "Restaurant already exists.")
            else:
                cursor.execute('INSERT INTO restaurant VALUES (?)',[name])
                conn.commit()
                QMessageBox.information(None, "Information", "Restaurant Added.")
                self.load_items()
                
        else:
            print('Restaurant Name is required')

    def load_items(self):
        self.comboBox.clear()
        cursor.execute("SELECT name FROM restaurant")
        items = cursor.fetchall()
        for item in items:
            self.comboBox.addItem(item[0])   

    def saveItem(self):
        itemCode = int(self.lineEdit_4.text())
        itemName = self.lineEdit_2.text()
        Price = int(self.lineEdit_3.text())
        name = self.comboBox.currentText()

        if itemCode != '' and itemName != '' and Price != '' and name != '':
            cursor.execute('SELECT itemcode FROM items WHERE name=? AND itemcode=?',[name,itemCode])
            if cursor.fetchone() is not None:
                QMessageBox.information(None, "Information", "Item coad is already exists.")
            else:
                cursor.execute('INSERT INTO items VALUES (?,?,?,?)',[itemCode,itemName,Price,name])
                conn.commit()
                QMessageBox.information(None, "Information", "Item is added.")
                self.clearItemsFileds()
        else:
            QMessageBox.information(None, "Information", "All fields are required")

    def clearItemsFileds(self):
        self.lineEdit_4.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")

    def searchItem(self):
        itemCode = self.lineEdit_4.text()
        name = self.comboBox.currentText()
        if itemCode != '' and name != '':
            try:
                itemCode= int(itemCode)
                cursor.execute('SELECT * FROM items WHERE itemcode=? AND name=?', [itemCode,name])
                item = cursor.fetchone()
                if item:
                    self.lineEdit_2.setText(item[1]) 
                    self.lineEdit_3.setText(str(item[2]))
                    self.comboBox.setCurrentText(item[3])  
                else:
                    QMessageBox.information(None, "Information", "Item is not found.")
                    self.clearItemsFileds()
            except ValueError:
                QMessageBox.information(None, "Information", "Item itemcode must be an number.")
                self.clearItemsFileds()
        else:
            QMessageBox.information(None, "Information", "Please enter an item code.")
            self.clearItemsFileds()
       
    def removeItem(self):
        try:
            itemCode = int(self.lineEdit_4.text())
            name = self.comboBox.currentText()
        except ValueError:
            QMessageBox.information(None, "Information", "Item code must be number.")
            return
        if itemCode != '' and name != '':
            cursor.execute('SELECT * FROM items WHERE itemcode=? AND name=?', [itemCode,name])
            item = cursor.fetchone()
            if item and QMessageBox.question(None, "Question", "Do you want to delete item?", QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Ok:
                cursor.execute('DELETE FROM items WHERE itemcode=? AND name=?', [itemCode,name])
                conn.commit()
                self.clearItemsFileds()
                QMessageBox.information(None, "Information", "Item with code {} removed successfully.".format(itemCode))
            else:
                self.clearItemsFileds()
        else:
            QMessageBox.information(None, "Information", "All fields are required")

    def updateItem(self):
        
        name = self.comboBox.currentText()
        itemName = self.lineEdit_2.text()
        
        try:
            itemCode = int(self.lineEdit_4.text())
            itemPrice = int(self.lineEdit_3.text())
        except ValueError:
            QMessageBox.information(None, "Information", "Item code must be an number.")
            return
        if itemCode != '' and itemName != '' and itemPrice != '' and name != '':
            cursor.execute('SELECT * FROM items WHERE itemcode=? AND name=?', [itemCode,name])
            item = cursor.fetchone()
            if item:
                cursor.execute('UPDATE items SET itemname=?,itemprice=? WHERE itemcode=? AND name=?', [itemName, itemPrice, itemCode,name])
                conn.commit()
                self.clearItemsFileds()
                QMessageBox.information(None, "Information", "Item details updated successfully.")

            else:
                QMessageBox.warning(None, "Warning", "Item with code {} not found.".format(itemCode))
        else:
            QMessageBox.information(None, "Information", "All fields are required")

    def deleteRestaurant(self):
        name = self.comboBox.currentText()
        if name != '':
            if QMessageBox.question(None, "Question", "Do you want to delete restaurant?", QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Ok:
                try:
                    cursor.execute('DELETE FROM items WHERE name=?', [name])
                    cursor.execute('DELETE FROM restaurant WHERE name=?', [name])
                    conn.commit()
                    self.load_items()
                    QMessageBox.information(None, "Information", "Restaurant removed successfully.")
                except sqlite3.Error as e:
                    QMessageBox.information(None, "Information", "Error:", e)
        else:
            QMessageBox.information(None, "Information", "Select restaurant name")

class RestaurantMenusUI(QMainWindow):
    def __init__(self):
        super(RestaurantMenusUI, self).__init__()
        uic.loadUi("rest&menu.ui", self)
        self.comboBox.currentIndexChanged.connect(self.loadItems)

        self.pushButton_2.clicked.connect(self.backhome)
        self.pushButton.clicked.connect(self.getItem)
        self.pushButton_3.clicked.connect(self.loadRestaurants)

    def backhome(self):
        self.comboBox.clear()
        self.comboBox_2.clear()
        self.lineEdit_4.setText("")
        self.hide()
        home_ui.show()

    def loadRestaurants(self):
        self.comboBox.clear()
        cursor.execute("SELECT name FROM restaurant")
        items = cursor.fetchall()
        for item in items:
            self.comboBox.addItem(item[0])
        self.loadItems()
        
    def loadItems(self):
        name = self.comboBox.currentText()
        if name != '':
            self.comboBox_2.clear()
            cursor.execute('SELECT itemcode,itemname, itemprice FROM items WHERE name=?', [name])
            items = cursor.fetchall()

            for item in items:
                icode,iname, iprice = item
                self.comboBox_2.addItem(f"{icode} - {iname} - ${iprice}")
        else:
            QMessageBox.information(None, "Information", "Select restaurant name")

    def getItem(self):
        
        odername = self.comboBox.currentText()
        itemname = self.comboBox_2.currentText().split(' ')[2]
        status = "cart"
        try:
            
            itemcode = int(self.comboBox_2.currentText().split(' ')[0])
            itemprice = int(self.comboBox_2.currentText().split('$')[1])
            quantity = int(self.lineEdit_4.text())
        except ValueError:
            QMessageBox.information(None, "Information", "Item code must be  number.")
            return
        if odername != '' and itemcode != '' and quantity != '' and quantity > 0:
            cursor.execute('INSERT INTO oders (odername,name,itemcode,itemname,itemprice,qty,status) VALUES (?,?,?,?,?,?,?)',[lodedUser,odername,itemcode,itemname,itemprice,quantity,status])
            conn.commit()
            QMessageBox.information(None, "Information", "item added to the cart")
        else:
            QMessageBox.information(None, "Information", "All fields are required or quantity should be positive")  

class ViewCart(QMainWindow):
    def __init__(self):
        super(ViewCart, self).__init__()
        uic.loadUi("viewcart.ui", self)
        self.setWindowTitle("Table Widget Example")
        
        self.pushButton_4.clicked.connect(self.loadCart)
        self.pushButton_3.clicked.connect(self.removeItems)
        self.pushButton_2.clicked.connect(self.backhome)
        self.pushButton.clicked.connect(self.buyItems)

    def backhome(self):
        self.tableWidget.setRowCount(0)
        self.label.setText("Total = $0")
        self.hide()
        home_ui.show()

    def loadCart(self):
        total = 0
        temp = 0
        cursor.execute("SELECT odername,name,itemname,itemprice,qty FROM oders WHERE status='cart'")
        conn.commit()
        rows = cursor.fetchall()
        self.tableWidget.setRowCount(len(rows))
        column_names = ['Name','Restaurant Name','Item Name','Price','Quantity']
        self.tableWidget.setColumnCount(len(column_names))
        self.tableWidget.setHorizontalHeaderLabels(column_names)
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(i,j, item)
                if j == 3:
                    temp = value
                if j==4:
                    total+= temp*value
                    
                    
        self.label.setText("Total = $" + str(total))

    def buyItems(self):
        try:
            price = int(self.label.text().split('$')[1])
        except ValueError:
            print("Item code must be number.")
            return
        if price > 0 :
            cursor.execute("UPDATE oders SET status ='confirmed' WHERE odername = ? AND status ='cart'", [lodedUser])
            QMessageBox.information(None, "Information", "Item is bought ")
            conn.commit()
            self.loadCart()
        else:
            QMessageBox.information(None, "Information", "load cart or add item to cart")
      
      
    def removeItems(self):
      try:
        if QMessageBox.question(None, "Question", "Do you want to remove items from cart?", QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Ok:
            cursor.execute("SELECT * FROM oders WHERE odername=? AND status='cart'", [lodedUser])
            result = cursor.fetchall()
            if result:
                cursor.execute("DELETE FROM oders WHERE odername = ? AND status='cart'", (lodedUser,))
                conn.commit()
                self.loadCart()
            else:
                QMessageBox.information(None, "Information", "Cart is empty")
      except Exception as e:
        print("Error:", e)
        conn.rollback()  # Rollback the transaction in case of an error

class Oder(QMainWindow):
    def __init__(self):
        super(Oder, self).__init__()
        uic.loadUi("oder.ui", self)

        self.pushButton_2.clicked.connect(self.backhome)
        self.pushButton_4.clicked.connect(self.loadOrders)
        self.pushButton_5.clicked.connect(self.goToodermanage)

    def goToodermanage(self):  
        managerPass = self.lineEdit.text()
        if managerPass != '':
            if managerPass == '1234':
                self.tableWidget.setRowCount(0)
                self.lineEdit.setText("")
                self.hide()
                manage_oder_ui.show()
            else:
                QMessageBox.information(None, "Information", "Password is worng !")
        else:
            QMessageBox.information(None, "Information", "Enter manager password !")

    def backhome(self):
        self.tableWidget.setRowCount(0)
        self.hide()
        home_ui.show()

    def loadOrders(self):
        cursor.execute("SELECT odername,name,itemname,itemprice,qty,status FROM oders WHERE status!='cart' AND odername =?",[lodedUser])
        conn.commit()
        rows = cursor.fetchall()
        self.tableWidget.setRowCount(len(rows))
        column_names = ['Name','Restaurant Name','Item Name','Price','Quantity','Status']
        self.tableWidget.setColumnCount(len(column_names))
        self.tableWidget.setHorizontalHeaderLabels(column_names)
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(i,j, item)

class ManageOders(QMainWindow):
    def __init__(self):
        super(ManageOders, self).__init__()
        uic.loadUi("odermanage.ui", self)

        self.pushButton_2.clicked.connect(self.backhome)
        self.pushButton_4.clicked.connect(self.display)
        self.pushButton_3.clicked.connect(self.updateStatus)

    def backhome(self):
        self.tableWidget.setRowCount(0)
        self.comboBox_4.clear()
        self.lineEdit.setText("")
        self.hide()
        oder_ui.show()             

    def display(self):
        cursor.execute("SELECT oderid,odername,name,itemcode,itemname,itemprice,qty,status FROM oders WHERE status!='cart'")
        conn.commit()
        rows = cursor.fetchall()
        self.tableWidget.setRowCount(len(rows))
        column_names = ['Order ID','Name','Restaurant Name','Item Code','Item Name','Price','Quantity','Status']
        self.tableWidget.setColumnCount(len(column_names))
        self.tableWidget.setHorizontalHeaderLabels(column_names)
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(i,j, item)

        self.comboBox_4.setCurrentIndex(-1)
        self.lineEdit.setText("")

    def updateStatus(self):

        orderId = self.lineEdit.text()
        status = self.comboBox_4.currentText()

        if orderId != '' and status != '':
            try:
                id = int(orderId)
                cursor.execute("SELECT oderid FROM oders WHERE oderid=?",[id])
                result = cursor.fetchone()
                if result:
                    cursor.execute('UPDATE oders SET status=? WHERE oderid=?', [status, id])
                    conn.commit()
                    self.display()
                    QMessageBox.information(None, "Information", "Order details updated successfully.")
                else:
                    QMessageBox.information(None, "Information", "Item is not found")    
            except ValueError:
                QMessageBox.information(None, "Information", "Item code must be number.")
            
            
        else:
            QMessageBox.information(None, "Information", "All fields are required")




app = QApplication(sys.argv)
login_ui = LoginUI()
signup_ui = SignupUI()
home_ui = homeUI()
restaurant_ui = RestaurantUI()
restaurant_menus = RestaurantMenusUI()
view_cart = ViewCart()
oder_ui = Oder()
manage_oder_ui = ManageOders()
login_ui.show()
sys.exit(app.exec_())
