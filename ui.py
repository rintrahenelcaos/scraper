from bs4 import BeautifulSoup
import requests

import sqlite3

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QLabel,
    QComboBox,
    QSpinBox,
)

from PyQt5.QtGui import QIcon, QPixmap, QPainter, QBrush, QPen, QMouseEvent, QHoverEvent, QFont, QColor,QPalette
from PyQt5.QtCore import Qt, QTimer, QTime, QThread, QObject, pyqtSignal

import sys

print(QTime.toString(QTime.currentTime()))
