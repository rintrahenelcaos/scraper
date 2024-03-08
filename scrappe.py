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


def scrapper(url_list, codes_list):
    scrapped=[]
    
    for ind_url in url_list:
        info = []
        req =requests.get(ind_url)
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

def actualize_scrapper(url_lits, codes_list):
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
    data = scrapper(urls_list,code_list2)
    print(data)
      
    
    

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
    table = "CREATE TABLE IF NOT EXISTS cedears(symbol TEXT NOT NULL, description TEXT, value REAL, variation REAL,  lastopeartion TEXT, opening REAL, closing REAL, volume INTEGER, minimun REAL, maximun REAL)"
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
        self.table.setGeometry(10,30,800,700)
        column_names = ["Symbol", "Description", "$", "Variation", "last operation", "opening $", "closing $", "Volume", "Min.$", "Max.$"]
        self.table.setHorizontalHeaderLabels(column_names)
        
        
        
        
        
        
        self.table_loader()
            
        self.table.setWordWrap(True)
        self.table.resizeColumnsToContents()
        
        actualize_scrapper(urls, code_list)
        
        
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
    tableconstructor(conector)
    db_charger(conector, comma_dot_cleaner(scrapper(urls,code_list)))
    app = QtWidgets.QApplication(sys.argv)
    
    
    ui = Main_window()
    
    
    
    
    

    

    sys.exit(app.exec_())
     

     

       


