import sys, sqlite3, os.path, platform, re
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream, Qt, QEvent, pyqtSignal
from PyQt5.QtGui import QIcon, QFontDatabase
from decimal import Decimal as dc
import auxiliar as ax
from load_page_ui import Ui_MainWindow

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class MainWindow(QMainWindow):
    updateSignal = pyqtSignal()
    
    def __init__(self, proj_name):
        super(MainWindow, self).__init__()
        
        self.proj_name = proj_name
        
        if platform.system() == 'Windows':
            self.path = os.path.expanduser(f'~/Documents/PyThermalLoad/{self.proj_name}.ptl')
        else:
            self.path = os.path.expanduser(f'~/PyThermalLoad/{self.proj_name}.ptl')
        
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute('SELECT valor FROM dados WHERE item=?', ('current',))
        self.zona = cursor.fetchone()[0]
        conn.close()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(f'{self.zona}')
        self.setWindowIcon(QIcon('logo.ico'))
        self.setGeometry(0, 0, 1200, 650)
        self.center()
        
        style_file = QFile("st_load_page.qss")
        style_file.open(QFile.ReadOnly | QFile.Text)
        style_stream = QTextStream(style_file)
        self.setStyleSheet(style_stream.readAll())
        
        self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.parede_btn_2.setChecked(True)
        
        self.init_load()
        
    def init_load(self):       
        self.loaddata_parede(), self.loaddata_porta(), self.loaddata_janela(), self.loaddata_cobertura(), self.loaddata_interna(), self.loaddata_outra()
        self.ui.tabela_parede.installEventFilter(self)
        self.ui.tabela_porta.installEventFilter(self)
        self.ui.tabela_janela.installEventFilter(self)
        self.ui.tabela_cobertura.installEventFilter(self)
        self.ui.tabela_interna.installEventFilter(self)
        self.ui.tabela_outra.installEventFilter(self)
        
        conn = sqlite3.connect(resource_path('data/materiais.db'))
        cursor = conn.cursor()
        cursor.execute('SELECT espessura, descricao FROM paredes')
        data = cursor.fetchall()
        for item in data:
            self.ui.parede_cbox.addItem((f'{item[0]:.2f}mm [{item[1]}]').replace('.',','))
         
        cursor.execute('SELECT nome, tipo FROM tintas')
        data = cursor.fetchall()
        for item in data:
            self.ui.tinta_cbox_pr.addItem(f'{item[1]} - {item[0]}')
            self.ui.tinta_cbox_pt.addItem(f'{item[1]} - {item[0]}')
            
        cursor.execute('SELECT material FROM portas')
        data = cursor.fetchall()
        for item in data:
            self.ui.porta_cbox.addItem(item[0])
        
        cursor.execute('SELECT fabricante, modelo, espessura FROM vidros')
        data = cursor.fetchall()
        for item in data:
            if item[0] == None:
                self.ui.janela_cbox.addItem(f'{item[1]} [{str(item[2]).replace(".",",")}mm]')
            else:
                self.ui.janela_cbox.addItem(f'{item[0]} - {item[1]} [{str(item[2]).replace(".",",")}mm]')
        
        cursor.execute('SELECT descricao FROM coberturas')
        data = cursor.fetchall()
        for item in data:
            self.ui.cobertura_cbox.addItem(item[0])
        conn.close()
         
        conn = sqlite3.connect(resource_path('data/radiacao.db'))
        cursor = conn.cursor()
        cursor.execute('SELECT orientacao FROM "30Sdez"')
        data = cursor.fetchall()
        valores = ('Sul', 'Sudeste', 'Leste', 'Nordeste', 'Norte', 'Noroeste', 'Oeste', 'Sudoeste')
        i = 0
        for item in data:
            if item[0] != 'H':
                self.ui.orientacao_cbox_pr.addItem(f'{item[0]} - {valores[i]}')
                self.ui.orientacao_cbox_pt.addItem(f'{item[0]} - {valores[i]}')
                self.ui.orientacao_cbox_jn.addItem(f'{item[0]} - {valores[i]}')
                i += 1
        conn.close()
        self.ui.tinta_cbox_pt.setEnabled(False)
        
        conn = sqlite3.connect(resource_path('data/carga_interna.db'))
        cursor = conn.cursor()
        cursor.execute('SELECT local FROM iluminacao')
        data = cursor.fetchall()
        for item in data:
            self.ui.iluminacao.addItem(item[0])
        
        conn = sqlite3.connect(resource_path('data/carga_interna.db'))
        cursor = conn.cursor()
        cursor.execute('SELECT local, atividade FROM pessoas')
        data = cursor.fetchall()
        for item in data:
            self.ui.pessoa_atv.addItem(f'{item[0]} - {item[1]}')
        
        conn = sqlite3.connect(resource_path('data/carga_interna.db'))
        cursor = conn.cursor()
        cursor.execute('SELECT equipamento FROM equipamentos')
        data = cursor.fetchall()
        for item in data:
            self.ui.equipamento.addItem(item[0])
        
        self.ui.parede_ok_btn_1.clicked.connect(self.parede_btn)
        self.ui.porta_ok_btn_1.clicked.connect(self.porta_btn)
        self.ui.janela_ok_btn_1.clicked.connect(self.janela_btn)
        self.ui.cobertura_ok_btn_1.clicked.connect(self.cobertura_btn)
        self.ui.iluminacao_ok_btn_1.clicked.connect(self.iluminacao_btn)
        self.ui.pessoa_ok_btn_1.clicked.connect(self.pessoa_btn)
        self.ui.equipamento_ok_btn_1.clicked.connect(self.equipamento_btn)
        self.ui.outra_ok_btn_1.clicked.connect(self.outra_btn)
        
        self.ui.watt_box.stateChanged.connect(self.unid_checkboxStateChanged)
        self.ui.btuh_box.stateChanged.connect(self.unid_checkboxStateChanged)
        self.ui.tr_box.stateChanged.connect(self.unid_checkboxStateChanged)
        
        self.ui.sensivel_box.stateChanged.connect(self.tipo_checkboxStateChanged)
        self.ui.latente_box.stateChanged.connect(self.tipo_checkboxStateChanged)
        
    
    def center(self):
        frame = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame.moveCenter(center_point)
        self.move(frame.topLeft())
    
    def on_parede_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    
    def on_parede_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_porta_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_porta_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_janela_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_janela_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_cobertura_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_cobertura_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_interna_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    def on_interna_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(4)
        
    def on_outras_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(5)

    def on_outras_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(5)
    
    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is self.ui.tabela_parede:
            menu = QMenu()
            menu.addAction('Remover')

            if menu.exec_(event.globalPos()):
                try:
                    item = self.ui.tabela_parede.currentIndex()
                    row = int(item.row())
                    it = self.ui.tabela_parede.item(row, 0).text()
                    
                    conn = sqlite3.connect(self.path)
                    cursor = conn.cursor()
                    cursor.execute(f'DELETE FROM {self.zona} WHERE id=? AND data_type=?', (it, 'pr'))
                    cursor.execute(f'DELETE FROM {self.zona}_print WHERE id=? AND data_type=?', (it, 'pr'))
                    conn.commit()
                    conn.close()
                    
                    self.loaddata_parede()
                except:
                    None
            return True
        
        elif event.type() == QEvent.ContextMenu and source is self.ui.tabela_porta:
            menu = QMenu()
            menu.addAction('Remover')

            if menu.exec_(event.globalPos()):
                try:
                    item = self.ui.tabela_porta.currentIndex()
                    row = int(item.row())
                    it = self.ui.tabela_porta.item(row, 0).text()
                    
                    conn = sqlite3.connect(self.path)
                    cursor = conn.cursor()
                    cursor.execute(f'DELETE FROM {self.zona} WHERE id=? AND data_type=?', (it, 'pt'))
                    cursor.execute(f'DELETE FROM {self.zona}_print WHERE id=? AND data_type=?', (it, 'pt'))
                    conn.commit()
                    conn.close()
                    
                    self.loaddata_porta()
                except:
                    None
            return True
        
        elif event.type() == QEvent.ContextMenu and source is self.ui.tabela_janela:
            menu = QMenu()
            menu.addAction('Remover')

            if menu.exec_(event.globalPos()):
                try:
                    item = self.ui.tabela_janela.currentIndex()
                    row = int(item.row())
                    it = self.ui.tabela_janela.item(row, 0).text()
                    
                    conn = sqlite3.connect(self.path)
                    cursor = conn.cursor()
                    cursor.execute(f'DELETE FROM {self.zona} WHERE id=? AND data_type=?', (it, 'jn'))
                    cursor.execute(f'DELETE FROM {self.zona}_print WHERE id=? AND data_type=?', (it, 'jn'))
                    conn.commit()
                    conn.close()
                    
                    self.loaddata_janela()
                except:
                    None
            return True
        
        elif event.type() == QEvent.ContextMenu and source is self.ui.tabela_cobertura:
            menu = QMenu()
            menu.addAction('Remover')

            if menu.exec_(event.globalPos()):
                try:
                    item = self.ui.tabela_cobertura.currentIndex()
                    row = int(item.row())
                    it = self.ui.tabela_cobertura.item(row, 0).text()
                    
                    conn = sqlite3.connect(self.path)
                    cursor = conn.cursor()
                    cursor.execute(f'DELETE FROM {self.zona} WHERE id=? AND data_type=?', (it, 'cb'))
                    cursor.execute(f'DELETE FROM {self.zona}_print WHERE id=? AND data_type=?', (it, 'cb'))
                    conn.commit()
                    conn.close()
                    
                    self.loaddata_cobertura()
                except:
                    None
            return True
        
        elif event.type() == QEvent.ContextMenu and source is self.ui.tabela_interna:
            menu = QMenu()
            menu.addAction('Remover')

            if menu.exec_(event.globalPos()):
                try:
                    item = self.ui.tabela_interna.currentIndex()
                    row = int(item.row())
                    it = self.ui.tabela_interna.item(row, 1).text()
                    
                    conn = sqlite3.connect(self.path)
                    cursor = conn.cursor()
                    cursor.execute(f'DELETE FROM {self.zona} WHERE id=?', (it,))
                    cursor.execute(f'DELETE FROM {self.zona}_print WHERE id=?', (it,))
                    conn.commit()
                    conn.close()
                    
                    self.loaddata_interna()
                except:
                    None
            return True
        
        elif event.type() == QEvent.ContextMenu and source is self.ui.tabela_outra:
            menu = QMenu()
            menu.addAction('Remover')

            if menu.exec_(event.globalPos()):
                try:
                    item = self.ui.tabela_outra.currentIndex()
                    row = int(item.row())
                    it = self.ui.tabela_outra.item(row, 0).text()
                    
                    conn = sqlite3.connect(self.path)
                    cursor = conn.cursor()
                    cursor.execute(f'DELETE FROM {self.zona} WHERE id=? AND data_type=?', (it, 'ot'))
                    cursor.execute(f'DELETE FROM {self.zona}_print WHERE id=? AND data_type=?', (it, 'ot'))
                    conn.commit()
                    conn.close()
                    
                    self.loaddata_outra()
                except:
                    None
            return True
        
        return super().eventFilter(source, event)
    
    def is_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def loaddata_parede(self):            
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute(f'SELECT id, tipo, area, tinta, orientacao, interno, amb_externo FROM {self.zona}_print WHERE data_type = "pr"')
        data = cursor.fetchall()
        conn.close()
                
        self.ids_pr = []
        row = 0
        self.ui.tabela_parede.setRowCount(len(data))
        self.ui.tabela_parede.setColumnCount(7)
        
        for item in data:
            for i in range(7):
                it = QTableWidgetItem('—') if item[i] is None else QTableWidgetItem(item[i])
                it.setTextAlignment(Qt.AlignCenter)
                self.ui.tabela_parede.setItem(row, i, it)
            row+=1
            self.ids_pr.append(item[0])
        
        self.ui.tabela_parede.setHorizontalHeaderLabels(['ID', 'Tipo', 'Área', 'Tinta', 'Orientação', 'Interna', 'Amb. Externo'])
        self.ui.tabela_parede.verticalHeader().setVisible(False)
        self.ui.tabela_parede.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        header = self.ui.tabela_parede.horizontalHeader()
        for c in range(7):
            if c == 1: header.setSectionResizeMode(c, QHeaderView.Stretch)
            else:  header.setSectionResizeMode(c, QHeaderView.ResizeToContents)
    
    def loaddata_porta(self):            
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute(f'SELECT id, tipo, area, tinta, orientacao, interno, amb_externo FROM {self.zona}_print WHERE data_type = "pt"')
        data = cursor.fetchall()
        conn.close()
                
        self.ids_pt = []
        row = 0
        self.ui.tabela_porta.setRowCount(len(data))
        self.ui.tabela_porta.setColumnCount(7)
        
        for item in data:
            for i in range(7):
                it = QTableWidgetItem('—') if i == 3 else QTableWidgetItem(item[i])
                it.setTextAlignment(Qt.AlignCenter)
                self.ui.tabela_porta.setItem(row, i, it)
            row+=1
            self.ids_pt.append(item[0])
        
        self.ui.tabela_porta.setHorizontalHeaderLabels(['ID', 'Tipo', 'Área', 'Tinta', 'Orientação', 'Interna', 'Amb. Externo'])
        self.ui.tabela_porta.verticalHeader().setVisible(False)
        self.ui.tabela_porta.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        header = self.ui.tabela_porta.horizontalHeader()
        for c in range(7):
            if c == 1: header.setSectionResizeMode(c, QHeaderView.Stretch)
            else:  header.setSectionResizeMode(c, QHeaderView.ResizeToContents)
    
    def loaddata_janela(self):            
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute(f'SELECT id, tipo, area, orientacao, interno, amb_externo FROM {self.zona}_print WHERE data_type = "jn"')
        data = cursor.fetchall()
        conn.close()
                
        self.ids_jn = []
        row = 0
        self.ui.tabela_janela.setRowCount(len(data))
        self.ui.tabela_janela.setColumnCount(6)
        
        for item in data:
            for i in range(6):
                it = QTableWidgetItem(item[i])
                it.setTextAlignment(Qt.AlignCenter)
                self.ui.tabela_janela.setItem(row, i, it)
            row+=1
            self.ids_jn.append(item[0])
        
        self.ui.tabela_janela.setHorizontalHeaderLabels(['ID', 'Tipo', 'Área', 'Orientação', 'Interna', 'Amb. Externo'])
        self.ui.tabela_janela.verticalHeader().setVisible(False)
        self.ui.tabela_janela.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        header = self.ui.tabela_janela.horizontalHeader()
        for c in range(6):
            if c == 1: header.setSectionResizeMode(c, QHeaderView.Stretch)
            else:  header.setSectionResizeMode(c, QHeaderView.ResizeToContents)
    
    def loaddata_cobertura(self):            
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute(f'SELECT id, tipo, area, interno, amb_externo FROM {self.zona}_print WHERE data_type = "cb"')
        data = cursor.fetchall()
        conn.close()
                
        self.ids_cb = []
        row = 0
        self.ui.tabela_cobertura.setRowCount(len(data))
        self.ui.tabela_cobertura.setColumnCount(5)
        
        for item in data:
            for i in range(5):
                it = QTableWidgetItem(item[i])
                it.setTextAlignment(Qt.AlignCenter)
                self.ui.tabela_cobertura.setItem(row, i, it)
            row+=1
            self.ids_cb.append(item[0])
        
        self.ui.tabela_cobertura.setHorizontalHeaderLabels(['ID', 'Tipo', 'Área', 'Interna', 'Amb. Externo'])
        self.ui.tabela_cobertura.verticalHeader().setVisible(False)
        self.ui.tabela_cobertura.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        header = self.ui.tabela_cobertura.horizontalHeader()
        for c in range(5):
            if c == 1: header.setSectionResizeMode(c, QHeaderView.Stretch)
            else:  header.setSectionResizeMode(c, QHeaderView.ResizeToContents)
    
    def loaddata_interna(self):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute(f'SELECT id, tipo, area, quantidade FROM {self.zona}_print WHERE data_type = "il"')
        data_i = cursor.fetchall()
        cursor.execute(f'SELECT id, tipo, area, quantidade FROM {self.zona}_print WHERE data_type = "ps"')
        data_p = cursor.fetchall()
        cursor.execute(f'SELECT id, tipo, area, quantidade FROM {self.zona}_print WHERE data_type = "eq"')
        data_e = cursor.fetchall()
        conn.close()
                
        self.ids_il = []
        self.ids_ps = []
        self.ids_eq = []
        row = 0
        self.ui.tabela_interna.setRowCount(len(data_i) + len(data_p) + len(data_e))
        self.ui.tabela_interna.setColumnCount(4)
        
        for item in data_i:
            for i in range(4):
                it = QTableWidgetItem(item[i]) if i == 1 or i == 2 else QTableWidgetItem('Iluminação') if i == 0 else QTableWidgetItem('—')
                it.setTextAlignment(Qt.AlignCenter)
                self.ui.tabela_interna.setItem(row, i, it)
            row+=1
            self.ids_il.append(item[1])
        
        for item in data_p:
            for i in range(4):
                it = QTableWidgetItem(f'{item[i]}') if i == 1 or i == 3 else QTableWidgetItem('Pessoa') if i == 0 else QTableWidgetItem('—')
                it.setTextAlignment(Qt.AlignCenter)
                self.ui.tabela_interna.setItem(row, i, it)
            row+=1
            self.ids_ps.append(item[1])
        
        for item in data_e:
            for i in range(4):
                it = QTableWidgetItem(f'{item[i]}') if i == 1 or i == 3 else QTableWidgetItem('Equipamento') if i == 0 else QTableWidgetItem('—')
                it.setTextAlignment(Qt.AlignCenter)
                self.ui.tabela_interna.setItem(row, i, it)
            row+=1
            self.ids_eq.append(item[1])
        
        self.ui.tabela_interna.setHorizontalHeaderLabels(['ID', 'Tipo', 'Área', 'Quantidade'])
        self.ui.tabela_interna.verticalHeader().setVisible(False)
        self.ui.tabela_interna.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        header = self.ui.tabela_interna.horizontalHeader()
        for c in range(4):
            if c == 1: header.setSectionResizeMode(c, QHeaderView.Stretch)
            else:  header.setSectionResizeMode(c, QHeaderView.ResizeToContents)
        
    def loaddata_outra(self):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute(f'SELECT id, tipo, quantidade FROM {self.zona}_print WHERE data_type = "ot"')
        data = cursor.fetchall()
        conn.close()
                
        self.ids_ot = []
        row = 0
        self.ui.tabela_outra.setRowCount(len(data))
        self.ui.tabela_outra.setColumnCount(3)
        
        for item in data:
            for i in range(3):
                it = QTableWidgetItem(f'{item[i]}')
                it.setTextAlignment(Qt.AlignCenter)
                self.ui.tabela_outra.setItem(row, i, it)
            row+=1
            self.ids_pt.append(item[0])
        
        self.ui.tabela_outra.setHorizontalHeaderLabels(['ID', 'Tipo', 'Carga (W)'])
        self.ui.tabela_outra.verticalHeader().setVisible(False)
        self.ui.tabela_outra.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        header = self.ui.tabela_outra.horizontalHeader()
        for c in range(3):
            if c == 1 or c == 2: header.setSectionResizeMode(c, QHeaderView.Stretch)
            else: header.setSectionResizeMode(c, QHeaderView.ResizeToContents)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.ui.tabela_parede.clearSelection()
            self.ui.tabela_porta.clearSelection()
            self.ui.tabela_janela.clearSelection()
            self.ui.tabela_cobertura.clearSelection()
            self.ui.tabela_interna.clearSelection()
            self.ui.tabela_outra.clearSelection()
      
    def mousePressEvent(self, event):
        if not self.ui.tabela_parede.underMouse():
            self.ui.tabela_parede.clearSelection()
            self.ui.tabela_porta.clearSelection()
            self.ui.tabela_janela.clearSelection()
            self.ui.tabela_cobertura.clearSelection()
            self.ui.tabela_interna.clearSelection()
            self.ui.tabela_outra.clearSelection()
    
    def on_vidro_box_pr_stateChanged(self, state):
        if state == 2:
            self.ui.tinta_cbox_pr.setEnabled(False)
            
            self.ui.parede_cbox.clear()
            
            conn = sqlite3.connect('data/materiais.db')
            cursor = conn.cursor()
            cursor.execute('SELECT fabricante, modelo, espessura FROM vidros')
            data = cursor.fetchall()
            
            for item in data:
                if item[0] == None:
                    self.ui.parede_cbox.addItem(f'{item[1]} [{str(item[2]).replace(".",",")}mm]')
                else:
                    self.ui.parede_cbox.addItem(f'{item[0]} - {item[1]} [{str(item[2]).replace(".",",")}mm]')
            conn.close()
            
        else:
            self.ui.tinta_cbox_pr.setEnabled(True)
            
            self.ui.parede_cbox.clear()
            
            conn = sqlite3.connect('data/materiais.db')
            cursor = conn.cursor()
            cursor.execute('SELECT espessura, descricao FROM paredes')
            data = cursor.fetchall()
            for item in data:
                self.ui.parede_cbox.addItem((f'{item[0]:.2f}mm [{item[1]}]').replace('.',','))
            conn.close()
    
    def on_vidro_box_pt_stateChanged(self, state):
        if state == 2:
            self.ui.tinta_cbox_pt.setEnabled(False)
            self.ui.pintura_box_pt.setChecked(False)
            self.ui.pintura_box_pt.setEnabled(False)
            
            self.ui.porta_cbox.clear()
            
            conn = sqlite3.connect('data/materiais.db')
            cursor = conn.cursor()
            cursor.execute('SELECT fabricante, modelo, espessura FROM vidros')
            data = cursor.fetchall()
            
            for item in data:
                if item[0] == None:
                    self.ui.porta_cbox.addItem(f'{item[1]} [{str(item[2]).replace(".",",")}mm]')
                else:
                    self.ui.porta_cbox.addItem(f'{item[0]} - {item[1]} [{str(item[2]).replace(".",",")}mm]')
            conn.close()
            
        else:
            self.ui.pintura_box_pt.setEnabled(True)
            
            self.ui.porta_cbox.clear()
            
            conn = sqlite3.connect('data/materiais.db')
            cursor = conn.cursor()
            cursor.execute('SELECT material FROM portas')
            data = cursor.fetchall()
            for item in data:
                self.ui.porta_cbox.addItem(item[0])
            conn.close()
    
    def on_pintura_box_pt_stateChanged(self, state):
        if self.ui.pintura_box_pt.checkState() == 0:
            self.ui.tinta_cbox_pt.setEnabled(False)
        else:
            self.ui.tinta_cbox_pt.setEnabled(True)
                
    def on_vidro_box_cb_stateChanged(self, state):
        if state == 2:           
            self.ui.cobertura_cbox.clear()
            
            conn = sqlite3.connect('data/materiais.db')
            cursor = conn.cursor()
            cursor.execute('SELECT fabricante, modelo, espessura FROM vidros')
            data = cursor.fetchall()
            
            for item in data:
                if item[0] == None:
                    self.ui.cobertura_cbox.addItem(f'{item[1]} [{str(item[2]).replace(".",",")}mm]')
                else:
                    self.ui.cobertura_cbox.addItem(f'{item[0]} - {item[1]} [{str(item[2]).replace(".",",")}mm]')
            conn.close()
            
        else:            
            self.ui.cobertura_cbox.clear()
            
            conn = sqlite3.connect('data/materiais.db')
            cursor = conn.cursor()
            cursor.execute('SELECT descricao FROM coberturas')
            data = cursor.fetchall()
            for item in data:
                self.ui.cobertura_cbox.addItem(item[0])
            conn.close()

    def unid_checkboxStateChanged(self, state):
        sender = self.sender()
        if state == 2:
            if sender == self.ui.watt_box:
                self.ui.btuh_box.setChecked(False)
                self.ui.tr_box.setChecked(False)

            elif sender == self.ui.btuh_box:
                self.ui.watt_box.setChecked(False)
                self.ui.tr_box.setChecked(False)
            
            else:
                self.ui.watt_box.setChecked(False)
                self.ui.btuh_box.setChecked(False)

        elif state == 0:
            if sender == self.ui.watt_box:
                if self.ui.tr_box.isChecked(): self.ui.btuh_box.setChecked(False), self.ui.tr_box.setChecked(True)
                else: self.ui.btuh_box.setChecked(True)

            elif sender == self.ui.btuh_box:
                if self.ui.tr_box.isChecked(): self.ui.watt_box.setChecked(False), self.ui.tr_box.setChecked(True)
                else: self.ui.watt_box.setChecked(True)
            
            else:
                if self.ui.btuh_box.isChecked(): self.ui.watt_box.setChecked(False), self.ui.tr_box.setChecked(False)
                else: self.ui.watt_box.setChecked(True)

    def tipo_checkboxStateChanged(self, state):
        sender = self.sender()
        if state == 2:
            if sender == self.ui.sensivel_box:
                self.ui.latente_box.setChecked(False)
                
            else:
                self.ui.sensivel_box.setChecked(False)
                
        if state == 0:
            if sender == self.ui.sensivel_box:
                self.ui.latente_box.setChecked(True)

            else:
                self.ui.sensivel_box.setChecked(True)
    
    def parede_btn(self):        
        if self.ui.parede_id.text() != '' and self.ui.area_box_pr.text() != '' and (self.is_float(self.ui.area_box_pr.text().replace(',','.')) or self.verifica_operacao(self.ui.area_box_pr.text().replace(',','.'))):
            self.ui.parede_id_label.setText('Parede ID')
            self.ui.parede_id_label.setStyleSheet("color: #001219;")
            self.ui.area_box_pr_label.setText('Área (m²)')
            self.ui.area_box_pr_label.setStyleSheet("color: #001219;")
            
            #Variáveis para a tabela dos cálculos 
            id = self.ui.parede_id.text().strip()
            id_pr = self.ui.parede_cbox.currentIndex() + 1
            area = eval(self.ui.area_box_pr.text().replace(',','.')) if self.verifica_operacao(self.ui.area_box_pr.text().replace(',','.')) else self.ui.area_box_pr.text().replace(',','.')
            orientacao = self.ui.orientacao_cbox_pr.currentText()[:self.ui.orientacao_cbox_pr.currentText().find(' ')]
            vidro = 1 if self.ui.vidro_box_pr.isChecked() else 0
            id_tinta = None if self.ui.vidro_box_pr.isChecked() else self.ui.tinta_cbox_pr.currentIndex() + 1           
            interno = 1 if self.ui.interna_box_pr.isChecked() else 0    
            amb_externo = 1 if self.ui.amb_externo_box_pr.isChecked() else 0
            
            #Variáveis para a tabela da tela
            tipo = self.ui.parede_cbox.currentText()
            tinta = None if self.ui.vidro_box_pr.isChecked() else self.ui.tinta_cbox_pr.currentText()
            interno_pt = '✔️' if self.ui.interna_box_pr.isChecked() else '❌'
            amb_externo_pt = 'Climatizado' if self.ui.amb_externo_box_pr.isChecked() else 'Não climatizado'
            
            if id in self.ids_pr:
                #Atualizar as varáveis na tabela dos cálculos
                conn = sqlite3.connect(self.path)
                cursor = conn.cursor()
                cursor.execute(f'''UPDATE {self.zona} SET id_table=?, area=?, orientacao=?, vidro=?, id_tinta=?, interno=?, amb_externo=? 
                            WHERE id=? AND data_type=?''', (id_pr, f'{area}', orientacao, vidro, id_tinta, interno, amb_externo, id, 'pr'))
                #Atualizar as varáveis na tabela da tela
                cursor.execute(f'''UPDATE {self.zona}_print SET tipo=?, area=?, tinta=?, orientacao=?, interno=?, amb_externo=?
                               WHERE id=? AND data_type=?''', (tipo, f'{area}'.replace('.',','), tinta, orientacao, interno_pt, amb_externo_pt, id, 'pr'))
                
                conn.commit()
                conn.close()
            else:
                #Inserir as varáveis na tabela dos cálculos
                conn = sqlite3.connect(self.path)
                cursor = conn.cursor()
                cursor.execute(f'''INSERT INTO {self.zona} (id, data_type, id_table, area, orientacao, vidro, id_tinta, interno, amb_externo) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (id, 'pr', id_pr, f'{area}', orientacao, vidro, id_tinta, interno, amb_externo))
                #Inserir as varáveis na tabela da tela
                cursor.execute(f'''INSERT INTO {self.zona}_print (id, data_type, tipo, area, tinta, orientacao, interno, amb_externo) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (id, 'pr', tipo, f'{area}'.replace('.',','), tinta, orientacao, interno_pt, amb_externo_pt))
                
                conn.commit()
                conn.close()
            
            self.ui.parede_id.clear()
            self.ui.area_box_pr.clear()
            self.ui.parede_cbox.setCurrentIndex(0)
            self.ui.tinta_cbox_pr.setCurrentIndex(0)
            self.ui.orientacao_cbox_pr.setCurrentIndex(0)
            self.ui.vidro_box_pr.setChecked(False)
            self.ui.interna_box_pr.setChecked(False)
            self.ui.amb_externo_box_pr.setChecked(False)
            self.loaddata_parede()

        else:
            if self.ui.parede_id.text() == '':
                self.ui.parede_id_label.setText('Parede ID *')
                self.ui.parede_id_label.setStyleSheet("color: #9B2226;")
            else:
                self.ui.parede_id_label.setText('Parede ID')
                self.ui.parede_id_label.setStyleSheet("color: #001219;")
                
            if self.ui.area_box_pr.text() == '' or not self.is_float(self.ui.area_box_pr.text().replace(',','.')):
                self.ui.area_box_pr_label.setText('Área (m²) *')
                self.ui.area_box_pr_label.setStyleSheet("color: #9B2226;")    
            else:
                self.ui.area_box_pr_label.setText('Área (m²)')
                self.ui.area_box_pr_label.setStyleSheet("color: #001219;")
    
    def porta_btn(self):        
        if self.ui.porta_id.text() != '' and self.ui.area_box_pt.text() != '' and (self.is_float(self.ui.area_box_pt.text().replace(',','.')) or self.verifica_operacao(self.ui.area_box_pt.text().replace(',','.'))):
            self.ui.porta_id_label.setText('Porta ID')
            self.ui.porta_id_label.setStyleSheet("color: #001219;")
            self.ui.area_box_pt_label.setText('Área (m²)')
            self.ui.area_box_pt_label.setStyleSheet("color: #001219;")
            
            #Variáveis para a tabela dos cálculos 
            id = self.ui.porta_id.text().strip()
            id_pt = self.ui.porta_cbox.currentIndex() + 1
            area = eval(self.ui.area_box_pt.text().replace(',','.')) if self.verifica_operacao(self.ui.area_box_pt.text().replace(',','.')) else self.ui.area_box_pt.text().replace(',','.')
            orientacao = self.ui.orientacao_cbox_pt.currentText()[:self.ui.orientacao_cbox_pt.currentText().find(' ')]
            vidro = 1 if self.ui.vidro_box_pt.isChecked() else 0
            id_tinta = None if self.ui.vidro_box_pt.isChecked() or not self.ui.pintura_box_pt.isChecked() else self.ui.tinta_cbox_pt.currentIndex() + 1           
            interno = 1 if self.ui.interna_box_pt.isChecked() else 0    
            amb_externo = 1 if self.ui.amb_externo_box_pt.isChecked() else 0
            
            #Variáveis para a tabela da tela
            tipo = self.ui.porta_cbox.currentText()
            tinta = None if self.ui.vidro_box_pr.isChecked() or not self.ui.pintura_box_pt.isChecked() else self.ui.tinta_cbox_pr.currentText()
            interno_pt = '✔️' if self.ui.interna_box_pt.isChecked() else '❌'
            amb_externo_pt = 'Climatizado' if self.ui.amb_externo_box_pt.isChecked() else 'Não climatizado'
            
            if id in self.ids_pt:
                #Atualizar as varáveis na tabela dos cálculos
                conn = sqlite3.connect(self.path)
                cursor = conn.cursor()
                cursor.execute(f'''UPDATE {self.zona} SET id_table=?, area=?, orientacao=?, vidro=?, id_tinta=?, interno=?, amb_externo=? 
                            WHERE id=? AND data_type=?''', (id_pt, f'{area}', orientacao, vidro, id_tinta, interno, amb_externo, id, 'pt'))
                #Atualizar as varáveis na tabela da tela
                cursor.execute(f'''UPDATE {self.zona}_print SET tipo=?, area=?, tinta=?, orientacao=?, interno=?, amb_externo=?
                               WHERE id=? AND data_type=?''', (tipo, f'{area}'.replace('.',','), tinta, orientacao, interno_pt, amb_externo_pt, id, 'pt'))
                
                conn.commit()
                conn.close()
            else:
                #Inserir as varáveis na tabela dos cálculos
                conn = sqlite3.connect(self.path)
                cursor = conn.cursor()
                cursor.execute(f'''INSERT INTO {self.zona} (id, data_type, id_table, area, orientacao, vidro, id_tinta, interno, amb_externo) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (id, 'pt', id_pt, f'{area}', orientacao, vidro, id_tinta, interno, amb_externo))
                #Inserir as varáveis na tabela da tela
                cursor.execute(f'''INSERT INTO {self.zona}_print (id, data_type, tipo, area, tinta, orientacao, interno, amb_externo) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (id, 'pt', tipo, f'{area}'.replace('.',','), tinta, orientacao, interno_pt, amb_externo_pt))
                
                conn.commit()
                conn.close()
            
            self.ui.porta_id.clear()
            self.ui.area_box_pt.clear()
            self.ui.porta_cbox.setCurrentIndex(0)
            self.ui.tinta_cbox_pt.setCurrentIndex(0)
            self.ui.orientacao_cbox_pt.setCurrentIndex(0)
            self.ui.vidro_box_pt.setChecked(False)
            self.ui.interna_box_pt.setChecked(False)
            self.ui.amb_externo_box_pt.setChecked(False)
            self.loaddata_porta()

        else:
            if self.ui.porta_id.text() == '':
                self.ui.porta_id_label.setText('Porta ID *')
                self.ui.porta_id_label.setStyleSheet("color: #9B2226;")
            else:
                self.ui.porta_id_label.setText('Porta ID')
                self.ui.porta_id_label.setStyleSheet("color: #001219;")
                
            if self.ui.area_box_pt.text() == '' or not self.is_float(self.ui.area_box_pt.text().replace(',','.')):
                self.ui.area_box_pt_label.setText('Área (m²) *')
                self.ui.area_box_pt_label.setStyleSheet("color: #9B2226;")    
            else:
                self.ui.area_box_pt_label.setText('Área (m²)')
                self.ui.area_box_pt_label.setStyleSheet("color: #001219;")
    
    def janela_btn(self):        
        if self.ui.janela_id.text() != '' and self.ui.area_box_jn.text() != '' and (self.is_float(self.ui.area_box_jn.text().replace(',','.')) or self.verifica_operacao(self.ui.area_box_jn.text().replace(',','.'))):
            self.ui.janela_id_label.setText('Janela ID')
            self.ui.janela_id_label.setStyleSheet("color: #001219;")
            self.ui.area_box_jn_label.setText('Área (m²)')
            self.ui.area_box_jn_label.setStyleSheet("color: #001219;")
            
            #Variáveis para a tabela dos cálculos 
            id = self.ui.janela_id.text().strip()
            id_jn = self.ui.janela_cbox.currentIndex() + 1
            area = eval(self.ui.area_box_jn.text().replace(',','.')) if self.verifica_operacao(self.ui.area_box_jn.text().replace(',','.')) else self.ui.area_box_jn.text().replace(',','.')
            orientacao = self.ui.orientacao_cbox_jn.currentText()[:self.ui.orientacao_cbox_jn.currentText().find(' ')]
            interno = 1 if self.ui.interna_box_jn.isChecked() else 0    
            amb_externo = 1 if self.ui.amb_externo_box_jn.isChecked() else 0
            
            #Variáveis para a tabela da tela
            tipo = self.ui.janela_cbox.currentText()
            interno_jn = '✔️' if self.ui.interna_box_jn.isChecked() else '❌'
            amb_externo_jn = 'Climatizado' if self.ui.amb_externo_box_jn.isChecked() else 'Não climatizado'
            
            if id in self.ids_jn:
                #Atualizar as varáveis na tabela dos cálculos
                conn = sqlite3.connect(self.path)
                cursor = conn.cursor()
                cursor.execute(f'''UPDATE {self.zona} SET id_table=?, area=?, orientacao=?, interno=?, amb_externo=? 
                            WHERE id=? AND data_type=?''', (id_jn, f'{area}', orientacao, interno, amb_externo, id, 'jn'))
                #Atualizar as varáveis na tabela da tela
                cursor.execute(f'''UPDATE {self.zona}_print SET tipo=?, area=?, orientacao=?, interno=?, amb_externo=?
                               WHERE id=? AND data_type=?''', (tipo, f'{area}'.replace('.',','), orientacao, interno_jn, amb_externo_jn, id, 'jn'))
                
                conn.commit()
                conn.close()
            else:
                #Inserir as varáveis na tabela dos cálculos
                conn = sqlite3.connect(self.path)
                cursor = conn.cursor()
                cursor.execute(f'''INSERT INTO {self.zona} (id, data_type, id_table, area, orientacao, interno, amb_externo) 
                            VALUES (?, ?, ?, ?, ?, ?, ?)''', (id, 'jn', id_jn, f'{area}', orientacao, interno, amb_externo))
                #Inserir as varáveis na tabela da tela
                cursor.execute(f'''INSERT INTO {self.zona}_print (id, data_type, tipo, area, orientacao, interno, amb_externo) 
                            VALUES (?, ?, ?, ?, ?, ?, ?)''', (id, 'jn', tipo, f'{area}'.replace('.',','), orientacao, interno_jn, amb_externo_jn))
                
                conn.commit()
                conn.close()
            
            self.ui.janela_id.clear()
            self.ui.area_box_jn.clear()
            self.ui.janela_cbox.setCurrentIndex(0)
            self.ui.orientacao_cbox_jn.setCurrentIndex(0)
            self.ui.interna_box_jn.setChecked(False)
            self.ui.amb_externo_box_jn.setChecked(False)
            self.loaddata_janela()

        else:
            if self.ui.janela_id.text() == '':
                self.ui.janela_id_label.setText('Janela ID *')
                self.ui.janela_id_label.setStyleSheet("color: #9B2226;")
            else:
                self.ui.janela_id_label.setText('Janela ID')
                self.ui.janela_id_label.setStyleSheet("color: #001219;")
                
            if self.ui.area_box_jn.text() == '' or not self.is_float(self.ui.area_box_jn.text().replace(',','.')):
                self.ui.area_box_jn_label.setText('Área (m²) *')
                self.ui.area_box_jn_label.setStyleSheet("color: #9B2226;")    
            else:
                self.ui.area_box_jn_label.setText('Área (m²)')
                self.ui.area_box_jn_label.setStyleSheet("color: #001219;")
    
    def cobertura_btn(self):        
        if self.ui.cobertura_id.text() != '' and self.ui.area_box_cb.text() != '' and (self.is_float(self.ui.area_box_cb.text().replace(',','.')) or self.verifica_operacao(self.ui.area_box_cb.text().replace(',','.'))):
            self.ui.cobertura_id_label.setText('Cobertura ID')
            self.ui.cobertura_id_label.setStyleSheet("color: #001219;")
            self.ui.area_box_cb_label.setText('Área (m²)')
            self.ui.area_box_cb_label.setStyleSheet("color: #001219;")
            
            #Variáveis para a tabela dos cálculos 
            id = self.ui.cobertura_id.text().strip()
            id_cb = self.ui.cobertura_cbox.currentIndex() + 1
            area = eval(self.ui.area_box_cb.text().replace(',','.'))if self.verifica_operacao(self.ui.area_box_cb.text().replace(',','.')) else self.ui.area_box_cb.text().replace(',','.')
            orientacao = 'H'
            vidro = 1 if self.ui.vidro_box_cb.isChecked() else 0         
            interno = 1 if self.ui.interna_box_cb.isChecked() else 0    
            amb_externo = 1 if self.ui.amb_externo_box_cb.isChecked() else 0
            
            #Variáveis para a tabela da tela
            tipo = self.ui.cobertura_cbox.currentText()
            interno_cb = '✔️' if self.ui.interna_box_cb.isChecked() else '❌'
            amb_externo_cb = 'Climatizado' if self.ui.amb_externo_box_cb.isChecked() else 'Não climatizado'
            
            if id in self.ids_cb:
                #Atualizar as varáveis na tabela dos cálculos
                conn = sqlite3.connect(self.path)
                cursor = conn.cursor()
                cursor.execute(f'''UPDATE {self.zona} SET id_table=?, area=?, orientacao=?, vidro=?, interno=?, amb_externo=? 
                            WHERE id=? AND data_type=?''', (id_cb, f'{area}', orientacao, vidro, interno, amb_externo, id, 'cb'))
                #Atualizar as varáveis na tabela da tela
                cursor.execute(f'''UPDATE {self.zona}_print SET tipo=?, area=?, interno=?, amb_externo=?
                               WHERE id=? AND data_type=?''', (tipo, f'{area}'.replace('.',','), interno_cb, amb_externo_cb, id, 'cb'))
                
                conn.commit()
                conn.close()
            else:
                #Inserir as varáveis na tabela dos cálculos
                conn = sqlite3.connect(self.path)
                cursor = conn.cursor()
                cursor.execute(f'''INSERT INTO {self.zona} (id, data_type, id_table, area, orientacao, vidro, interno, amb_externo) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (id, 'cb', id_cb, f'{area}', orientacao, vidro, interno, amb_externo))
                #Inserir as varáveis na tabela da tela
                cursor.execute(f'''INSERT INTO {self.zona}_print (id, data_type, tipo, area, interno, amb_externo) 
                            VALUES (?, ?, ?, ?, ?, ?)''', (id, 'cb', tipo, f'{area}'.replace('.',','), interno_cb, amb_externo_cb))
                
                conn.commit()
                conn.close()
            
            self.ui.cobertura_id.clear()
            self.ui.area_box_cb.clear()
            self.ui.cobertura_cbox.setCurrentIndex(0)
            self.ui.vidro_box_cb.setChecked(False)
            self.ui.interna_box_cb.setChecked(False)
            self.ui.amb_externo_box_cb.setChecked(False)
            self.loaddata_cobertura()

        else:
            if self.ui.cobertura_id.text() == '':
                self.ui.cobertura_id_label.setText('Cobertura ID *')
                self.ui.cobertura_id_label.setStyleSheet("color: #9B2226;")
            else:
                self.ui.cobertura_label.setText('Cobertura ID')
                self.ui.cobertura_label.setStyleSheet("color: #001219;")
                
            if self.ui.area_box_cb.text() == '' or not self.is_float(self.ui.area_box_cb.text().replace(',','.')):
                self.ui.area_box_cb_label.setText('Área (m²) *')
                self.ui.area_box_cb_label.setStyleSheet("color: #9B2226;")    
            else:
                self.ui.area_box_cb_label.setText('Área (m²)')
                self.ui.area_box_cb_label.setStyleSheet("color: #001219;")
    
    def iluminacao_btn(self):
        if self.ui.area_ilu.text() != '' and (self.is_float(self.ui.area_ilu.text().replace(',','.')) or self.verifica_operacao(self.ui.area_ilu.text().replace(',','.'))):
            self.ui.area_ilu_label.setText('Área (m²)')
            self.ui.area_ilu_label.setStyleSheet("color: #001219;")
            
            id_il = self.ui.iluminacao.currentIndex() + 1
            tipo = self.ui.iluminacao.currentText()
            area = eval(self.ui.area_ilu.text().replace(',','.')) if self.verifica_operacao(self.ui.area_ilu.text().replace(',','.')) else self.ui.area_ilu.text().replace(',','.')
            
            if not self.ids_il:
                #Inserir as varáveis na tabela dos cálculos
                conn = sqlite3.connect(self.path)
                cursor = conn.cursor()
                cursor.execute(f'INSERT INTO {self.zona} (id, data_type, id_table, area) VALUES (?, ?, ?, ?)', (tipo, 'il', id_il, f'{area}'))
                #Inserir as varáveis na tabela da tela
                cursor.execute(f'INSERT INTO {self.zona}_print (id, data_type, tipo, area) VALUES (?, ?, ?, ?)', (tipo, 'il', tipo, f'{area}'.replace('.',',')))
                
                conn.commit()
                conn.close()
            
            else:
                #Atualizar as varáveis na tabela dos cálculos
                conn = sqlite3.connect(self.path)
                cursor = conn.cursor()
                cursor.execute(f'UPDATE {self.zona} SET id=?, id_table=?, area=? WHERE data_type=?', (tipo, id_il, f'{area}', 'il'))
                #Atualizar as varáveis na tabela da tela
                cursor.execute(f'UPDATE {self.zona}_print SET id=?, tipo=?, area=? WHERE data_type=?', (tipo, tipo, f'{area}'.replace('.',','), 'il'))
                
                conn.commit()
                conn.close()
            
            self.ui.area_ilu.clear()
            self.ui.iluminacao.setCurrentIndex(0)
            self.loaddata_interna()
                
        else:
            self.ui.area_ilu_label.setText('Área (m²) *')
            self.ui.area_ilu_label.setStyleSheet("color: #9B2226;") 
    
    def pessoa_btn(self):
        if self.ui.quantidade_pessoas.text() != '' and self.ui.quantidade_pessoas.text().isdigit():
            self.ui.quantidade_pessoas_label.setText('Quant. Pessoas')
            self.ui.quantidade_pessoas_label.setStyleSheet("color: #001219;")
            
            id_ps = self.ui.pessoa_atv.currentIndex() + 1
            tipo = self.ui.pessoa_atv.currentText()
            quant = self.ui.quantidade_pessoas.text()
            
            if tipo not in self.ids_ps:
                #Inserir as varáveis na tabela dos cálculos
                conn = sqlite3.connect(self.path)
                cursor = conn.cursor()
                cursor.execute(f'INSERT INTO {self.zona} (id, data_type, id_table, qt) VALUES (?, ?, ?, ?)', (tipo, 'ps', id_ps, f'{quant}'))
                #Inserir as varáveis na tabela da tela
                cursor.execute(f'INSERT INTO {self.zona}_print (id, data_type, tipo, quantidade) VALUES (?, ?, ?,? )', (tipo, 'ps', tipo, f'{quant}'))
                
                conn.commit()
                conn.close()
            
            else:
                #Atualizar as varáveis na tabela dos cálculos
                conn = sqlite3.connect(self.path)
                cursor = conn.cursor()
                cursor.execute(f'UPDATE {self.zona} SET id_table=?, area=? WHERE id=? AND data_type=?', (id_ps, f'{quant}', tipo, 'ps'))
                #Atualizar as varáveis na tabela da tela
                cursor.execute(f'UPDATE {self.zona}_print SET tipo=?, area=? WHERE id=? AND data_type=?', (tipo, f'{quant}', tipo, 'ps'))
                
                conn.commit()
                conn.close()
            
            self.ui.quantidade_pessoas.clear()
            self.ui.pessoa_atv.setCurrentIndex(0)
            self.loaddata_interna()
                
        else:
            self.ui.quantidade_pessoas_label.setText('Quant. Pessoas *')
            self.ui.quantidade_pessoas_label.setStyleSheet("color: #9B2226;") 
    
    def equipamento_btn(self):
        if self.ui.quantidade_equipamentos.text() != '' and self.ui.quantidade_equipamentos.text().isdigit():
            self.ui.quantidade_equipamentos_label.setText('Quant. Equipamentos')
            self.ui.quantidade_equipamentos_label.setStyleSheet("color: #001219;")
            
            id_ps = self.ui.equipamento.currentIndex() + 1
            tipo = self.ui.equipamento.currentText()
            quant = self.ui.quantidade_equipamentos.text()
            
            if tipo not in self.ids_eq:
                #Inserir as varáveis na tabela dos cálculos
                conn = sqlite3.connect(self.path)
                cursor = conn.cursor()
                cursor.execute(f'INSERT INTO {self.zona} (id, data_type, id_table, qt) VALUES (?, ?, ?, ?)', (tipo, 'eq', id_ps, f'{quant}'))
                #Inserir as varáveis na tabela da tela
                cursor.execute(f'INSERT INTO {self.zona}_print (id, data_type, tipo, quantidade) VALUES (?, ?, ?, ?)', (tipo, 'eq', tipo, f'{quant}'))
                
                conn.commit()
                conn.close()
            
            else:
                #Atualizar as varáveis na tabela dos cálculos
                conn = sqlite3.connect(self.path)
                cursor = conn.cursor()
                cursor.execute(f'UPDATE {self.zona} SET id_table=?, area=? WHERE id=? AND data_type=?', (id_ps, f'{quant}', tipo, 'eq'))
                #Atualizar as varáveis na tabela da tela
                cursor.execute(f'UPDATE {self.zona}_print SET tipo=?, area=? WHERE id=? AND data_type=?', (tipo, f'{quant}', tipo, 'eq'))
                
                conn.commit()
                conn.close()
            
            self.ui.quantidade_equipamentos.clear()
            self.ui.pessoa_atv.setCurrentIndex(0)
            self.loaddata_interna()
                
        else:
            self.ui.quantidade_equipamentos_label.setText('Quant. Equipamentos *')
            self.ui.quantidade_equipamentos_label.setStyleSheet("color: #9B2226;") 

    def outra_btn(self):
        if self.ui.outra_id.text() != '' and self.ui.valor_outra.text() != '' and self.is_float(self.ui.valor_outra.text().replace(',','.')):
            self.ui.outra_label.setText('Carga ID')
            self.ui.outra_label.setStyleSheet("color: #001219;")
            self.ui.valor_outra_label.setText('Valor')
            self.ui.valor_outra_label.setStyleSheet("color: #001219;")
            
            #Variáveis para a tabela dos cálculos 
            id = self.ui.outra_id.text().strip()
            id_ot = 0 if self.ui.sensivel_box.isChecked() else 1
            valor_i = dc(self.ui.valor_outra.text().replace(',','.'))
            
            if self.ui.btuh_box.isChecked(): valor = ax.converter_potencia(valor_i, 'btuh', 'w')
            elif self.ui.tr_box.isChecked(): valor = ax.converter_potencia(valor_i, 'tr', 'w')
            else: valor = valor_i
            
            #Variáveis para a tabela da tela
            tipo = 'Sensível' if self.ui.sensivel_box.isChecked() else 'Latente'
            
            if id in self.ids_ot:
                #Atualizar as varáveis na tabela dos cálculos
                conn = sqlite3.connect(self.path)
                cursor = conn.cursor()
                cursor.execute(f'UPDATE {self.zona} SET id_table=?, qt=? WHERE id=? AND data_type=?', (id_ot, f'{valor}', id, 'ot'))
                #Atualizar as varáveis na tabela da tela
                cursor.execute(f'UPDATE {self.zona}_print SET tipo=?, quantidade=? WHERE id=? AND data_type=?', (tipo, f'{valor}'.replace('.',','), id, 'ot'))
                
                conn.commit()
                conn.close()
            else:
                #Inserir as varáveis na tabela dos cálculos
                conn = sqlite3.connect(self.path)
                cursor = conn.cursor()
                cursor.execute(f'INSERT INTO {self.zona} (id, data_type, id_table, qt) VALUES (?, ?, ?, ?)', (id, 'ot', id_ot, f'{valor}'))
                #Inserir as varáveis na tabela da tela
                cursor.execute(f'INSERT INTO {self.zona}_print (id, data_type, tipo, quantidade) VALUES (?, ?, ?, ?)', (id, 'ot', tipo, f'{valor}'.replace('.',',')))
                
                conn.commit()
                conn.close()
            
            self.ui.outra_id.clear()
            self.ui.valor_outra.clear()
            self.ui.watt_box.setChecked(True)
            self.ui.sensivel_box.setChecked(True)
            self.loaddata_outra()

        else:
            if self.ui.cobertura_id.text() == '':
                self.ui.cobertura_id_label.setText('Carga ID *')
                self.ui.cobertura_id_label.setStyleSheet("color: #9B2226;")
            else:
                self.ui.cobertura_label.setText('Carga ID')
                self.ui.cobertura_label.setStyleSheet("color: #001219;")
                
            if self.ui.area_box_cb.text() == '' or not self.is_float(self.ui.area_box_cb.text().replace(',','.')):
                self.ui.area_box_cb_label.setText('Valor *')
                self.ui.area_box_cb_label.setStyleSheet("color: #9B2226;")    
            else:
                self.ui.area_box_cb_label.setText('Valor')
                self.ui.area_box_cb_label.setStyleSheet("color: #001219;")
   
    def verifica_operacao(self, string):
        padrao = r'^\s*([-+*/]?\s*\d+(\.\d+)?\s*)*([-+*/]\s*\d+(\.\d+)?\s*)+$'
        
        if re.match(padrao, string):
            return True
        else:
            return False
    
    def emitSignal(self):
        self.updateSignal.emit()
    
    def closeEvent(self, event):
        self.emitSignal()
        event.accept()

            
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    QFontDatabase.addApplicationFont('font/OpenSans_SemiCondensed-Medium.ttf')
    QFontDatabase.addApplicationFont('font/OpenSans-Bold.ttf')

    style_file = QFile("st_load_page.qss")
    style_file.open(QFile.ReadOnly | QFile.Text)
    style_stream = QTextStream(style_file)
    app.setStyleSheet(style_stream.readAll())


    window = MainWindow('proj_1')

    
    window.show()
    print()
    sys.exit(app.exec())



