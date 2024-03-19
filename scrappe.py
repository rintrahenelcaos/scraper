from bs4 import BeautifulSoup
import requests
import pprint
import sqlite3

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QApplication,
    QWidget,
    QPushButton,
    QScrollArea,
    QLabel,
    QDialog,
    QGraphicsView,
    QGraphicsScene,
    QFrame,
    QGridLayout,
    QComboBox,
    QSpinBox,
    QTableView
    
)

from PyQt5.QtGui import QIcon, QPixmap, QPainter, QBrush, QPen, QMouseEvent, QHoverEvent, QFont, QColor,QPalette
from PyQt5.QtCore import Qt, QLine, QPointF, QRectF, QLine, QEvent, QPropertyAnimation, pyqtProperty, QTime

import sys

url = "https://www.cohen.com.ar/Bursatil/Especie/AAL"

#result = requests.get(url)

#soup = BeautifulSoup(result.text, 'html.parser')

def conection_sql():
    global conector
    conector = sqlite3.connect("cedearsdb.db")
    return conector

"""tabla = soup.find_all('div', id= "CotizacionesUltimaOperacion")
print(tabla)"""

"""for div in soup.find_all('div'):
    print(div.get('class'))"""

"""tables = soup.find_all('table')

table = soup.find('table', class_='wikitable sortable sticky-header static-row-numbers')

print(table)
"""
information = []
"""symb=soup.h2
symbol = symb.contents"""
#symbol = soup.find("h2").contents
#print(symbol)
#information.append(soup.find("h2").contents[0])
#print(information)

#description = soup.find(class_="tdSimbolo" )
#print(description.string)

code_list = ["tdSimbolo","tdDescripcionNombre", "tdCotizEspecie", "tdVariacion",  "lblFechaHora","lblPrecioCierrer", "lblApertura", "lblVolumen", "lblMaximo", "lblMinimo"]
urls = ["https://www.cohen.com.ar/Bursatil/Especie/AAL", "https://www.cohen.com.ar/Bursatil/Especie/AALD", "https://www.cohen.com.ar/Bursatil/Especie/AMX", "https://www.cohen.com.ar/Bursatil/Especie/GOLD"]
code_list2 = ["tdDescripcionNombre", "tdCotizEspecie", "tdVariacion",  "lblFechaHora","lblPrecioCierrer", "lblApertura", "lblVolumen", "lblMaximo", "lblMinimo"]
species = ["AAL", "AALD", "AMX", "GOLD", "BIOX" ]
dollar_urls = "https://dolarhoy.com/cotizacion-dolar-ccl"
dollar_code = "sell-value"



def dollar_scrapper(dollarurl, dollarcodes):
    
    req = requests.get(dollarurl)
    soupdollar = BeautifulSoup(req.text, 'html.parser')
    dollar_value = soupdollar.find_all(class_ = "value")[1].contents[0]
    print("DOLAR", dollar_value)
    dollar_ccl = dollar_value[1:]
    
    
    print(dollar_ccl)
    
    return dollar_ccl
    
def cedears_list_scrapper():
    
    cedears_complete_list = []
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    cedears = soup.findAll("option")
    
    for ind in cedears:
        cedears_complete_list.append(ind.string)
    cedears_complete_list = list(set(cedears_complete_list))
    cedears_complete_list.sort()
    cedears_complete_list.remove("Ninguna")
    cedears_complete_list.insert(0, "")
    return cedears_complete_list         
    
        

def scrapper(url_list, codes_list):
    scrapped=[]
    
    for ind_url in url_list:
        info = []
        req = requests.get(ind_url)
        soup = BeautifulSoup(req.text, 'html.parser')
        #inf = soup.find(class_="tdSimbolo").string
        #print(inf)
        for code in codes_list:
            try:
                inf = soup.find(class_ = code).text
                if inf.find("$") != -1:
                    inf = inf[inf.rfind(" ")+1:]
                elif inf.find("%") != -1:
                    inf = inf[1:inf.rfind(" ")]
                info.append(inf)
            except:
                inf = soup.find(id = code).text
                #print(code, inf)
                inf = inf[inf.rindex(" ")+1:]
                if inf.isdigit():
                    info.append(inf)
                else:
                    
                    while inf[0].isalpha():
                        inf = inf[1:]
                    else: info.append(inf)
        scrapped.append(info)
    return scrapped

#pprint.pprint(scrapper(urls, code_list)) 

def actualize_scrapper(code_list, dollar):
    pointer = conector.cursor() 
    scrapped = "SELECT symbol,amount FROM cedears"
    pointer.execute(scrapped)
    existing_scrapped = pointer.fetchall()
    already_scrapped = []
    specie_amount = []
    for scrap in existing_scrapped:
        already_scrapped.append(scrap[0])
        """specie_amount.append(scrap[1])
        update_total = "UPDATE cedears SET total = ? WHERE symbol = ?;"
        setting = (scrap[1]*dollar, scrap[0])
        pointer.execute(update_total, setting)
        conector.commit()"""
        
    
    urls_list = []
    
    
    for symbol in already_scrapped:
        urls_list.append("https://www.cohen.com.ar/Bursatil/Especie/"+symbol)
    data = comma_dot_cleaner(scrapper(urls_list,code_list))
    print("DATA: ",data)
    
    for dat in data:
        updater = "UPDATE cedears SET description = ?, value = ?, variation = ?, lastoperation = ?, opening = ?, closing = ?, volume = ?, minimun = ?, maximun = ? WHERE symbol = ?;"
        setter = (dat[1], round(float(dat[2])/dollar, 2), dat[3], dat[4], round(float(dat[5])/dollar,2), round(float(dat[6])/dollar, 2), dat[7], round(float(dat[8])/dollar,2), round(float(dat[9])/dollar,2), dat[0])
        pointer.execute(updater, setter)
        conector.commit()
        
        update_total = "SELECT amount FROM cedears WHERE symbol = ?;"
        pointer.execute(update_total, (dat[0],))
        total_to_update = pointer.fetchall()[0][0]
        updater = "UPDATE cedears SET total = ? WHERE symbol = ?"
        setter = (round(total_to_update*float(dat[2])/dollar, 2), dat[0])
        pointer.execute(updater, setter)
        conector.commit()
    
    """for symbol in already_scrapped:
        update_total = "SELECT amount FROM cedears WHERE symbol = ?;"
        print(symbol)
        pointer.execute(update_total, (symbol,))
        total_to_update = pointer.fetchall()[0][0]
        updater = "UPDATE cedears SET total = ? WHERE symbol = ?"
        setter = (total_to_update*dollar, symbol)
        pointer.execute(updater, setter)
        conector.commit()"""
        
        
    
def specie_loader(specie):
    
    to_add = (specie)
    pointer = conector.cursor() 
    adding = "INSERT INTO cedears (symbol, amount) VALUES (?, ?) ;"
    pointer.execute(adding, to_add)
    conector.commit()
      
def species_loader(species):   #temporal
    for sp in species:
        specie_loader(sp)    
    

def comma_dot_cleaner(scrapped):
    for info in scrapped: 
        for ind in range(2, len(info)):
            info[ind] = info[ind].replace(".","")
            info[ind] = info[ind].replace(",",".")
        
    pprint.pprint(scrapped)
    return scrapped

#comma_dot_cleaner(scrapper(urls, code_list))
            
        
            
    



def tableconstructor(conection):
    pointer = conection.cursor()
    table = "CREATE TABLE IF NOT EXISTS cedears(symbol TEXT NOT NULL, description TEXT, value REAL, variation REAL,  lastoperation TEXT, opening REAL, closing REAL, volume INTEGER, minimun REAL, maximun REAL, amount INTEGER, total FLOAT)"
    pointer.execute(table)
    conection.commit()
    
def db_charger(conection, scrapped):
    
    
    
    for inf in scrapped:
        
        loadtuple = (inf)
        
        
    
        pointer = conection.cursor()
        load = "INSERT INTO cedears(symbol, description, value, variation, lastopeartion, opening, closing, volume, minimun, maximun) VALUES (?,?,?,?,?,?,?,?,?,?)"
        pointer.execute(load, loadtuple)
        conection.commit()
    
def db_charger(conection, scrapped):
    
    for inf in scrapped:
        
        loadtuple = (inf)
        
        
    
        pointer = conection.cursor()
        load = "INSERT INTO cedears(symbol, description, value, variation, lastopeartion, opening, closing, volume, minimun, maximun) VALUES (?,?,?,?,?,?,?,?,?,?)"
        pointer.execute(load, loadtuple)
        conection.commit()

def mod_specie(value): print(value)


# interface
class Main_window(QMainWindow):
    
    
    def __init__(self):
        super(Main_window, self).__init__()
        
        self.setObjectName("MainWindow")
        self.resize(1000, 800)
        self.setWindowTitle("MainWindow")
        #self.setStyleSheet("QWidget { background-color: black}")
        self.setWindowTitle("CEDEAr - scrapper")
        
        self.table = QTableWidget(self)
        self.table.setGeometry(10,50,980,700)
        self.column_names = ["Symbol", "Description", "$", "Var.", "last op.", "opening $", "closing $", "Volume", "Min.$", "Max.$", "Am.Owned", "Holding $", "Edit"]
        self.table.setColumnCount(len(self.column_names))
        self.table.setHorizontalHeaderLabels(self.column_names)
        
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.itemDoubleClicked.connect(lambda: self.mod_specie(self.table.currentRow()))
        
        self.dollar_label = QLabel(self)
        self.dollar_label.setGeometry(QtCore.QRect(10, 10, 200, 30))
        self.dollar_label.setText("CCL-Dollar: $")
        
        
        
        self.specie_loader = QPushButton(self)
        self.specie_loader.setGeometry(QtCore.QRect(300, 10, 100, 30))
        self.specie_loader.clicked.connect(lambda: self.to_add_specie())
        
        
        self.specie_combobox = QComboBox(self)
        self.specie_combobox.addItems(cedears_list_scrapper())
        self.specie_combobox.setGeometry(QtCore.QRect(450,10, 200, 30))
        
        self.owned = QSpinBox(self)
        self.owned.setGeometry(QtCore.QRect(650, 10, 100, 30))
        
        #self.infolabel = QLabel(self)
        
        
        
        
        
        
        
        
        
        
        
            
        self.table.setWordWrap(True)
        
        self.dollar = dollar_scrapper(dollar_urls, dollar_code)
        actualize_scrapper(code_list, float(self.dollar))
        self.dollar_label.setText("CCL-Dollar: $"+str(self.dollar))
        self.table_loader()
        self.table.resizeColumnsToContents()
        self.table.setColumnWidth(1, 350)
        self.show()
        
    def table_loader(self):
        pointer = conector.cursor()
        loader = "SELECT * FROM cedears"
        pointer.execute(loader)
        data = pointer.fetchall()
        self.table.setRowCount(len(data))
        
        row = 0
        for dat in data:
            column = 0
            for individual in dat:
                self.table.setItem(row, column, QTableWidgetItem(str(individual)))
                column += 1
            delete_button = QPushButton("DEL.")
            
            
            self.table.setCellWidget(row,12,delete_button)
            delete_button.clicked.connect(self.delete_specie)
            
            row += 1
            
    def to_add_specie(self):
        print(self.specie_combobox.currentText())
        print(self.owned.value())
        new_specie = str(self.specie_combobox.currentText()), str(self.owned.value())
        specie_loader(new_specie)
        #self.infolabel.setText("Adding specie to db, please wait")
        actualize_scrapper(code_list, float(dollar_scrapper(dollar_urls, dollar_code)))
        pointer = conector.cursor()
        new_specie_symbol =  new_specie[0]
        updater = "SELECT * FROM cedears WHERE symbol = ?"
        setter = (new_specie_symbol,)
        pointer.execute(updater, (new_specie_symbol,))
        data = pointer.fetchall()[0]
        print(data)
        row = self.table.rowCount()
        self.table.insertRow(row)
        column =0
        for dat in data:
            self.table.setItem(row, column, QTableWidgetItem(str(dat)))
            column += 1
        delete_button = QPushButton("DEL.")
            
        self.table.setCellWidget(row,12,delete_button)
        delete_button.clicked.connect(self.delete_specie)
        #self.table_loader()
        
    def mod_specie(self, clickedIndex):
        
        row = clickedIndex.row()
        item_to_mod = self.table.item(row, 10)
        specie = self.table.item(row, 0).text()
        price = self.table.item(row, 2).text()
        print(specie)
        
        self.table.setCurrentItem(item_to_mod)
        previous_value = self.table.currentItem().text()
        self.table.editItem(item_to_mod)
        value = self.table.currentItem().text()
        
        self.table.itemChanged.connect(self.to_change_amount)
    
    def mod_specie(self, row):
        print(row)
        #row = clickedIndex.row()
        item_to_mod = self.table.item(row, 10)
        specie = self.table.item(row, 0).text()
        price = self.table.item(row, 2).text()
        print(specie)
        
        self.table.setCurrentItem(item_to_mod)
        previous_value = self.table.currentItem().text()
        self.table.editItem(item_to_mod)
        value = self.table.currentItem().text()
        
        self.table.itemChanged.connect(self.to_change_amount)
        
    def to_change_amount(self, item):
        
        row = item.row()
        value = self.table.item(row, 10).text()
        specie = self.table.item(row, 0).text()
        price = self.table.item(row, 2).text()
            
        pointer2 = conector.cursor()
        updater = "UPDATE cedears SET amount = ? WHERE symbol = ?"
        setter = (value, specie)
        pointer2.execute(updater, setter)
        conector.commit()
        
        updater2 = "UPDATE cedears SET total = ? WHERE symbol = ?"
        setter = (float(value)*float(price), specie)
        pointer2.execute(updater2,setter)
        conector.commit()
        
        #actualize_scrapper(code_list, float(self.dollar))
        
        loader = "SELECT total FROM cedears WHERE symbol = ?;"
        selector = (specie,)
        pointer2.execute(loader, selector)
        new_holding = pointer2.fetchall()[0][0]
        item_holding = self.table.item(row,11)
        item_holding.setText(str(new_holding))
        
    def delete_specie(self):
        button = self.sender()
        if button:
            row = self.table.indexAt(button.pos()).row()
            specie = self.table.item(row, 0).text()
            deleter = "DELETE FROM cedears WHERE symbol = ?"
            pointer3 = conector.cursor()
            pointer3.execute(deleter, (specie,))
            conector.commit()
            self.table.removeRow(row)
            
        
        
        
    
        
        
        
        
        



if __name__ == "__main__":
    conector = conection_sql()
    tableconstructor(conector)
    
    app = QtWidgets.QApplication(sys.argv)
    
    ui = Main_window()
    
    
    
    sys.exit(app.exec_())
    
    #species_loader(species)
    #actualize_scrapper(code_list)
    
    
    
    
    

    

    
     

     

       


