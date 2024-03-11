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
    
)

from PyQt5.QtGui import QIcon, QPixmap, QPainter, QBrush, QPen, QMouseEvent, QHoverEvent, QFont, QColor,QPalette
from PyQt5.QtCore import Qt, QLine, QPointF, QRectF, QLine, QEvent, QPropertyAnimation, pyqtProperty

import sys

url = "https://www.cohen.com.ar/Bursatil/Especie/AAL"

result = requests.get(url)

soup = BeautifulSoup(result.text, 'html.parser')

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
symbol = soup.find("h2").contents
#print(symbol)
information.append(soup.find("h2").contents[0])
#print(information)

description = soup.find(class_="tdSimbolo" )
#print(description.string)

code_list = ["tdSimbolo","tdDescripcionNombre", "tdCotizEspecie", "tdVariacion",  "lblFechaHora","lblPrecioCierrer", "lblApertura", "lblVolumen", "lblMaximo", "lblMinimo"]
urls = ["https://www.cohen.com.ar/Bursatil/Especie/AAL", "https://www.cohen.com.ar/Bursatil/Especie/AALD", "https://www.cohen.com.ar/Bursatil/Especie/AMX", "https://www.cohen.com.ar/Bursatil/Especie/GOLD"]
code_list2 = ["tdDescripcionNombre", "tdCotizEspecie", "tdVariacion",  "lblFechaHora","lblPrecioCierrer", "lblApertura", "lblVolumen", "lblMaximo", "lblMinimo"]
species = ["AAL", "AALD", "AMX", "GOLD", "BIOX" ]
dollar_urls = "https://www.cronista.com/MercadosOnline/moneda.html?id=ARSCONT"
dollar_code = "sell-value"

def dollar_scrapper(dollarurl, dollarcodes):
    
    req = requests.get(dollarurl)
    soupdollar = BeautifulSoup(req.text, 'html.parser')
    dollar_value = soupdollar.find(class_ = dollarcodes).text
    print("DOLAR", dollar_value)
    dollar_ccl = dollar_value[1:]
    dollar_ccl = dollar_ccl.replace(".","")
    dollar_ccl = dollar_ccl.replace(",",".")
    print(dollar_ccl)
    
    return dollar_ccl
    
    
    
        

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
    scrapped = "SELECT symbol FROM cedears"
    pointer.execute(scrapped)
    existing_scrapped = pointer.fetchall()
    already_scrapped = []
    for scrap in existing_scrapped:
        already_scrapped.append(scrap[0])
    urls_list = []
    for symbol in already_scrapped:
        urls_list.append("https://www.cohen.com.ar/Bursatil/Especie/"+symbol)
    data = comma_dot_cleaner(scrapper(urls_list,code_list))
    print("DATA: ",data)
    for dat in data:
        updater = "UPDATE cedears SET description = ?, value = ?, variation = ?, lastoperation = ?, opening = ?, closing = ?, volume = ?, minimun = ?, maximun = ? WHERE symbol = ?;"
        setter = (dat[1], float(dat[2])/dollar, dat[3], dat[4], float(dat[5])/dollar, float(dat[6])/dollar, dat[7], float(dat[8])/dollar, float(dat[9])/dollar, dat[0])
        pointer.execute(updater, setter)
        conector.commit()
    
def specie_loader(specie):
    
    to_add = (str(specie),)
    pointer = conector.cursor() 
    adding = "INSERT INTO cedears (symbol) VALUES (?) ;"
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


# interface
class Main_window(QMainWindow):
    
    """Game by itself
    """
    
    def __init__(self):
        super(Main_window, self).__init__()
        
        self.setObjectName("MainWindow")
        self.resize(1000, 800)
        self.setWindowTitle("MainWindow")
        #self.setStyleSheet("QWidget { background-color: black}")
        self.setWindowTitle("CEDEAr - scrapper")
        
        self.table = QTableWidget(self)
        self.table.setColumnCount(10)
        self.table.setGeometry(10,50,980,700)
        column_names = ["Symbol", "Description", "$", "Var.", "last op.", "opening $", "closing $", "Volume", "Min.$", "Max.$"]
        self.table.setHorizontalHeaderLabels(column_names)
        
        self.dollar_label = QLabel(self)
        self.dollar_label.setGeometry(QtCore.QRect(10, 10, 200, 30))
        self.dollar_label.setText("CCL-Dollar: $")
        
        
        
        self.specie_loader = QPushButton(self)
        self.specie_loader.setGeometry(QtCore.QRect(300, 10, 200, 30))
        
        self.
        
        
        
        
        
        
        
        
            
        self.table.setWordWrap(True)
        self.table.resizeColumnsToContents()
        dollar = dollar_scrapper(dollar_urls, dollar_code)
        actualize_scrapper(code_list, float(dollar))
        self.dollar_label.setText("CCL-Dollar: $"+str(dollar))
        self.table_loader()
        
        self.show()
        
    def table_loader(self):
        pointer = conector.cursor()
        loader = "SELECT * FROM cedears"
        pointer.execute(loader)
        items = pointer.fetchall()
        self.table.setRowCount(len(items))
        print(items)
        row = 0
        for item in items:
            column = 0
            for individual in item:
                self.table.setItem(row, column, QTableWidgetItem(str(individual)))
                column += 1
            row += 1
        
        
        



if __name__ == "__main__":
    conector = conection_sql()
    #tableconstructor(conector)
    #db_charger(conector, comma_dot_cleaner(scrapper(urls,code_list)))
    app = QtWidgets.QApplication(sys.argv)
    #
    #
    ui = Main_window()
    
    sys.exit(app.exec_())
    
    #species_loader(species)
    #actualize_scrapper(code_list)
    
    
    
    
    

    

    
     

     

       


