import sys, sqlite3, os.path, platform, re
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream, Qt, QEvent, QTranslator, QLocale, QLibraryInfo
from PyQt5.QtGui import QIcon, QFontDatabase
from decimal import Decimal as dc
from decimal import getcontext
import auxiliar as ax
from main_page_ui import Ui_MainWindow
from init_page_ui import Ui_Dialog
import load

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Dialog(QDialog):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        if platform.system() == 'Windows':
            self.path = os.path.expanduser(f'~/Documents/PyThermalLoad/')
        else:
            self.path = os.path.expanduser(f'~/PyThermalLoad/')
        
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle('PyThermalLoad')
        self.setWindowIcon(QIcon(resource_path('logo.ico')))
        self.setGeometry(0, 0, 400, 400)
        self.center()
        
        style_file = QFile(resource_path('st_main_page.qss'))
        style_file.open(QFile.ReadOnly | QFile.Text)
        style_stream = QTextStream(style_file)
        self.setStyleSheet(style_stream.readAll())
        
        self.ui.title.setAlignment(Qt.AlignCenter)
        
        self.ui.novo_proj.clicked.connect(self.novo)
        self.ui.load_proj.clicked.connect(self.load)
        
        self.verificar_pasta()
        self.ler_pasta()
    
    def center(self):
        frame = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame.moveCenter(center_point)
        self.move(frame.topLeft())
        
    def ler_pasta(self):
        diretorio = self.path
        nomes_arquivos_ptl = []
        for arquivo in os.listdir(diretorio):
            if arquivo.endswith('.ptl'):
                nomes_arquivos_ptl.append(arquivo)
                
        if not nomes_arquivos_ptl:
            self.ui.load_proj.setEnabled(False)
    
    def verificar_pasta(self):
        caminho_pasta = self.path
        if not os.path.exists(caminho_pasta):
            os.makedirs(caminho_pasta)
        else:
            None
    
    def novo(self):
        dialog = Novo_Proj_Dialog(self)
        if dialog.exec_():
            self.line_edit_text = dialog.line_edit.text()
            self.close()
        
    def load(self):
        dialog = Load_Proj_Dialog(self)
        if dialog.exec_():
            self.selected_item = dialog.combo_box.currentText()
            self.close()
        
class Novo_Proj_Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle('PyThermalLoad')
        self.setGeometry(0, 0, 135, 50)
        self.center()
        
        self.line_edit = QLineEdit()
        self.ok_button = QPushButton('OK')
        self.ok_button.setFixedSize(30, 30)
        self.ok_button.clicked.connect(self.btn)

        layout.addWidget(self.line_edit)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)
    
    def center(self):
        frame = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame.moveCenter(center_point)
        self.move(frame.topLeft())
    
    def btn(self):
        if not self.line_edit.text():
            self.line_edit.setStyleSheet("border: 2px solid #9B2226;")
        else:
            self.accept()

class Load_Proj_Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        if platform.system() == 'Windows':
            self.path = os.path.expanduser(f'~/Documents/PyThermalLoad/')
        else:
            self.path = os.path.expanduser(f'~/PyThermalLoad/')
            
        layout = QVBoxLayout()
        
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle('PyThermalLoad')
        
        self.setGeometry(0, 0, 135, 50)
        self.center()
        
        self.ler_pasta()
        self.combo_box = QComboBox()
        lista = []
        for item in self.proj_list: lista.append(f'{item[:-4]}')
        self.combo_box.addItems(lista)
        self.ok_button = QPushButton('OK')
        self.ok_button.setFixedSize(30, 30)
        self.ok_button.clicked.connect(self.accept)

        layout.addWidget(self.combo_box)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def center(self):
        frame = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame.moveCenter(center_point)
        self.move(frame.topLeft())
    
    def ler_pasta(self):
        diretorio = self.path
        nomes_arquivos_ptl = []
        for arquivo in os.listdir(diretorio):
            if arquivo.endswith('.ptl'):
                nomes_arquivos_ptl.append(arquivo)
        self.proj_list = nomes_arquivos_ptl
    
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.init_dialog()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        try:
            self.proj_name = self.dialog.selected_item
            self.set_path()
            self.load_proj()
            self.loaddata_zona()
            self.calc_loads()
            self.loaddata_resultado()
        except:
            try:
                self.proj_name = self.dialog.line_edit_text
            except:
                sys.exit()
            self.set_path()
            self.novo_proj()
            self.loaddata_zona()

        self.setWindowTitle(self.proj_name)
        self.setWindowIcon(QIcon(resource_path('logo.ico')))
        self.setGeometry(0, 0, 1200, 650)
        self.center()
        
        style_file = QFile(resource_path('st_main_page.qss'))
        style_file.open(QFile.ReadOnly | QFile.Text)
        style_stream = QTextStream(style_file)
        self.setStyleSheet(style_stream.readAll())
        
        self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.dados_btn_2.setChecked(True)
        
        self.ui.mes_cbox.addItems(('Dezembro', 'Março'))
        
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()         
        cursor.execute('UPDATE dados SET valor=? WHERE item=?', ('verao', 'estacao'))
        cursor.execute('UPDATE dados SET valor=? WHERE item=?', ('dez', 'mes'))
        conn.commit()
        conn.close()
        
        self.ui.lat_box.returnPressed.connect(self.onReturnPressed)
        self.ui.log_box.returnPressed.connect(self.onReturnPressed)
        self.ui.temp_box.returnPressed.connect(self.onReturnPressed)
        self.ui.umidade_box.returnPressed.connect(self.onReturnPressed)
        self.ui.hi_box.returnPressed.connect(self.onReturnPressed)
        self.ui.hf_box.returnPressed.connect(self.onReturnPressed)
        
        self.ui.verao_box.stateChanged.connect(self.checkboxStateChanged)
        self.ui.inverno_box.stateChanged.connect(self.checkboxStateChanged)
        self.ui.mes_cbox.currentIndexChanged.connect(self.onComboBoxIndexChanged)
        
        self.ui.tabela_zona.installEventFilter(self)
        self.ui.zona_ok_btn_1.clicked.connect(self.zona_btn)
        
        self.ui.att_btn_1.clicked.connect(self.att_btn)
        self.ui.att_btn_2.clicked.connect(self.att_btn)
 
    def set_path(self):
        if platform.system() == 'Windows':
            self.path = os.path.expanduser(f'~/Documents/PyThermalLoad/{self.proj_name}.ptl')
        else:
            self.path = os.path.expanduser(f'~/PyThermalLoad/{self.proj_name}.ptl')
    
    def novo_proj(self):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS dados (
            "item" TEXT PRIMARY KEY,
            "valor" TEXT)''')
        
        dados = [('lat'),
                 ('log'),
                 ('lat_dc'),
                 ('log_dc'),
                 ('cidade_proj'),
                 ('rad_proj'),
                 ('estacao'),
                 ('mes'),
                 ('t_ext'),
                 ('ur_ext'),
                 ('t_int'),
                 ('ur_int'),
                 ('hi'),
                 ('hf'),
                 ('current'),
        ]
        for item in dados:
            cursor.execute('INSERT OR IGNORE INTO dados (item) VALUES (?)', (item,))

        cursor.execute(f'CREATE TABLE IF NOT EXISTS zonas ("zonas_id" TEXT PRIMARY KEY)')
        
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS resultados (
            "zona"	TEXT,
            "qs_w"	TEXT,
            "ql_w"	TEXT,
            "total_w"	TEXT,
            "total_btuh"	TEXT,
            "total_tr"	TEXT)''')
        
        conn.commit()
        conn.close()

    def load_proj(self):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute('SELECT valor FROM dados WHERE item IN (?, ?, ?, ?, ?, ?, ?, ?) ORDER BY rowid', ('lat', 'log', 'estacao', 'mes', 't_int', 'ur_int', 'hi', 'hf'))
        data = cursor.fetchall()
        dados = []
        for item in data:
            dados.append(item[0])
            
        self.ui.lat_box.setText(dados[0])
        self.ui.log_box.setText(dados[1])
        self.ui.temp_box.setText(dados[4])
        self.ui.umidade_box.setText(dados[5])
        self.ui.hi_box.setText(dados[6])
        self.ui.hf_box.setText(dados[7])
        
        if dados[2] == 'verao':
            if dados[3] == 'Março':
                self.ui.mes_cbox.setCurrentIndex(2)
                
        else:
            self.ui.inverno_box.setChecked(True)
            self.ui.verao_box.setChecked(False)
            self.ui.mes_cbox.setEnabled(False)
            self.ui.mes_cbox.clear()
            self.ui.mes_cbox.addItem('Junho')
        
        conn.close()
    
    def center(self):
        frame = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame.moveCenter(center_point)
        self.move(frame.topLeft())
    
    def init_dialog(self):
        self.dialog = Dialog()
        self.dialog.exec_()
    
    def on_dados_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    
    def on_dados_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_zonas_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_zonas_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_resultados_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_resultados_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)
    
    def corrigir_coordenada(self, coordenada):
        return coordenada.strip().replace('º','°').replace('"','\'\'').replace(',','.')
    
    def corrigir_nome_zona(self, texto):
        texto = texto.replace(' ', '_')

        texto = re.sub(r'[^\w_]', '', texto)

        if re.match(r'^\d', texto):
            texto = '_' + texto

        palavras_reservadas_sql = ['select', 'insert', 'update', 'delete', 'from', 'where', 'and', 'or', 'not']
        if texto.lower() in palavras_reservadas_sql:
            texto = '_' + texto

        return texto
    
    def is_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def validar_coordenada(self, coord, tipo):
        valor = self.corrigir_coordenada(coord)
        simb = []
        for letra in valor:
            try:
                int(letra)
            except:
                simb.append(letra) 
        
        try:
            if simb[0] != '°' or simb[1] != '\'' or (simb[2] != '\'' and simb[3] != '\''):
                return False
        except:
            None
        
        try:
            grau = int(valor[:valor.find('°')]) if '°' in valor else 0
            minuto = int(valor[valor.find('°')+1:valor.find('\'')]) if '\'' in valor else 0
            segundo = int(valor[valor.find('\'')+1:valor.find('\'\'')]) if '\'\'' in valor else 0
        except:
            return False
        
        if tipo == 'lat':
            if not(0 <= grau <= 180) or not(0 <= minuto <= 59) or not(0 <= segundo <= 59):
                return False
        else:
            if not(0 <= grau <= 360) or not(0 <= minuto <= 59) or not(0 <= segundo <= 59):
                return False

        return True
    
    def validar_hora(self, hora):
        padrao = r'^(?:0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$'

        if re.match(padrao, hora):
            return True
        else:
           return False
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.ui.tabela_zona.clearSelection()
            self.ui.tabela_resultado.clearSelection()
            
    def mousePressEvent(self, event):
        if not self.ui.tabela_zona.underMouse():
            self.ui.tabela_zona.clearSelection()
            self.ui.tabela_resultado.clearSelection()
    
    def cargas_window(self):
        self.second_window = load.MainWindow(self.proj_name)
        self.second_window.updateSignal.connect(self.loaddata_zona)
        self.second_window.show()
    
    def conf_lat_box(self):
        if self.validar_coordenada(coord=self.ui.lat_box.text(), tipo='lat') and self.ui.lat_box.text().strip() != '':
            self.ui.lat_label.setText('Latitude')
            self.ui.lat_label.setStyleSheet("color: #001219;")
            
            latitude = self.corrigir_coordenada(self.ui.lat_box.text())
            
            conn = sqlite3.connect(self.path)
            cursor = conn.cursor()
            
            cursor.execute('UPDATE dados SET valor=? WHERE item=?', (latitude, 'lat'))
            cursor.execute('UPDATE dados SET valor=? WHERE item=?', (str(ax.coord_grau_decimal(latitude)), 'lat_dc'))
            cursor.execute('UPDATE dados SET valor=? WHERE item=?', (ax.distancia_rad(ax.coord_grau_decimal(latitude)), 'rad_proj'))
            
            conn.commit()
            conn.close()
            
            if '.' in ax.distancia_rad(ax.coord_grau_decimal(latitude)):
                self.ui.rad_lat_box.setText(ax.distancia_rad(ax.coord_grau_decimal(latitude)).replace('.', '°').replace('S', ' Sul'))
            else:
                self.ui.rad_lat_box.setText(ax.distancia_rad(ax.coord_grau_decimal(latitude)).replace('S', '° Sul'))
                
            if self.validar_coordenada(coord=self.ui.log_box.text(), tipo='log') and self.ui.log_box.text().strip() != '':
                longitude = self.corrigir_coordenada(self.ui.log_box.text())
                self.cidade = ax.distancia_cid(ax.coord_grau_decimal(latitude), ax.coord_grau_decimal(longitude))
                
                conn = sqlite3.connect(self.path)
                cursor = conn.cursor()
            
                cursor.execute('UPDATE dados SET valor=? WHERE item=?', (self.cidade, 'cidade_proj'))
                conn.commit()
                conn.close()
                
                conn = sqlite3.connect('data/dados_externos.db')
                cursor = conn.cursor()
                
                cursor.execute('SELECT uc FROM mar WHERE cidade=?', (self.cidade,))
                estado=cursor.fetchone()
                
                conn.close()
                
                self.ui.cid_proj_box.setText(f'{self.cidade}/{estado[0]}')
                
                if self.ui.verao_box.isChecked():
                    estacao = 'verao'
                    mes = self.ui.mes_cbox.currentText()[:3].lower()
                else:
                    estacao = 'inverno'
                    mes = 'jun'
                    
                conn = sqlite3.connect(self.path)
                cursor = conn.cursor()
                
                cursor.execute('UPDATE dados SET valor=? WHERE item=?', (estacao, 'estacao'))
                cursor.execute('UPDATE dados SET valor=? WHERE item=?', (mes, 'mes'))
                cursor.execute('UPDATE dados SET valor=? WHERE item=?', (str(ax.externo(self.cidade, estacao, mes)[0]), 't_ext'))
                cursor.execute('UPDATE dados SET valor=? WHERE item=?', (str(ax.externo(self.cidade, estacao, mes)[1]), 'ur_ext'))
                
                conn.commit()                    
                conn.close()

        else:
            self.ui.lat_label.setText('Latitude *')
            self.ui.lat_label.setStyleSheet("color: #9B2226;")
    
    def conf_log_box(self):
        if self.validar_coordenada(coord=self.ui.log_box.text(), tipo='log') and self.ui.log_box.text().strip() != '':
            self.ui.log_label.setText('Longitude')
            self.ui.log_label.setStyleSheet("color: #001219;")
            
            longitude = self.corrigir_coordenada(self.ui.log_box.text())
            
            conn = sqlite3.connect(self.path)
            cursor = conn.cursor()
            
            cursor.execute('''UPDATE dados SET valor=? WHERE item=?''', (longitude, 'log'))
            cursor.execute('''UPDATE dados SET valor=? WHERE item=?''', (str(ax.coord_grau_decimal(longitude)), 'log_dc'))
            cursor.execute('''UPDATE dados SET valor=? WHERE item=?''', (ax.distancia_rad(ax.coord_grau_decimal(longitude)), 'rad_proj'))
            
            conn.commit()
            conn.close()
                
            if self.validar_coordenada(coord=self.ui.lat_box.text(), tipo='lat') and self.ui.lat_box.text().strip() != '':
                latitude = self.corrigir_coordenada(self.ui.lat_box.text())
                self.cidade = ax.distancia_cid(ax.coord_grau_decimal(latitude), ax.coord_grau_decimal(longitude))
                
                conn = sqlite3.connect(self.path)
                cursor = conn.cursor()
            
                cursor.execute('''UPDATE dados SET valor=? WHERE item=?''', (self.cidade, 'cidade_proj'))
                conn.commit()
                conn.close()
                
                conn = sqlite3.connect('data/dados_externos.db')
                cursor = conn.cursor()
                
                cursor.execute('''SELECT uc FROM mar WHERE cidade=?''', (self.cidade,))
                estado=cursor.fetchone()
                
                conn.close()
                
                self.ui.cid_proj_box.setText(f'{self.cidade}/{estado[0]}')
                
                if self.ui.verao_box.isChecked():
                    estacao = 'verao'
                    mes = self.ui.mes_cbox.currentText()[:3].lower()
                else:
                    estacao = 'inverno'
                    mes = 'jun'
                    
                conn = sqlite3.connect(self.path)
                cursor = conn.cursor()
                
                cursor.execute('UPDATE dados SET valor=? WHERE item=?', (estacao, 'estacao'))
                cursor.execute('UPDATE dados SET valor=? WHERE item=?', (mes, 'mes'))
                cursor.execute('UPDATE dados SET valor=? WHERE item=?', (str(ax.externo(self.cidade, estacao, mes)[0]), 't_ext'))
                cursor.execute('UPDATE dados SET valor=? WHERE item=?', (str(ax.externo(self.cidade, estacao, mes)[1]), 'ur_ext'))
                
                conn.commit()                    
                conn.close()
                
        else:
            self.ui.log_label.setText('Longitude *')
            self.ui.log_label.setStyleSheet("color: #9B2226;")
    
    def conf_temp_box(self):
        if self.is_float(self.ui.temp_box.text().replace(',','.')):
            if dc(self.ui.temp_box.text().replace(',','.')) > 26 or dc(self.ui.temp_box.text().replace(',','.')) < 20:
                self.ui.temp_label.setText('Temperatura interna (°C) *Fora dos limites de conforto térmico')
                self.ui.temp_label.setStyleSheet("color: #005F73;")
            else:
                self.ui.temp_label.setText('Temperatura interna (°C)')
                self.ui.temp_label.setStyleSheet("color: #001219;")
                
            conn = sqlite3.connect(self.path)
            cursor = conn.cursor()
                
            cursor.execute('''UPDATE dados SET valor=? WHERE item=?''', (self.ui.temp_box.text().replace(',','.'), 't_int'))
            
            conn.commit()
            conn.close()
            
        else:
            self.ui.temp_label.setText('Temperatura interna (°C) *')
            self.ui.temp_label.setStyleSheet("color: #9B2226;")
    
    def conf_umidade_box(self):
        if self.is_float(self.ui.umidade_box.text().replace(',','.')):
            if dc(self.ui.umidade_box.text().replace(',','.')) > 65 or dc(self.ui.umidade_box.text().replace(',','.')) < 35:
                self.ui.umidade_label.setText('Umidade interna (%) *Fora dos limites de conforto térmico')
                self.ui.umidade_label.setStyleSheet("color: #005F73;")
            else:
                self.ui.umidade_label.setText('Umidade interna (%)')
                self.ui.umidade_label.setStyleSheet("color: #001219;")
                
            conn = sqlite3.connect(self.path)
            cursor = conn.cursor()
                
            cursor.execute('''UPDATE dados SET valor=? WHERE item=?''', (self.ui.umidade_box.text().replace(',','.'), 'ur_int'))
            
            conn.commit()
            conn.close()
            
        else:
            self.ui.umidade_label.setText('Umidade interna (%) *')
            self.ui.umidade_label.setStyleSheet("color: #9B2226;")
        
    def conf_hi_box(self):
        if self.validar_hora(self.ui.hi_box.text()):
            self.ui.hi_label.setText('Hora inicial')
            self.ui.hi_label.setStyleSheet("color: #001219;")
            
            conn = sqlite3.connect(self.path)
            cursor = conn.cursor()
                
            cursor.execute('UPDATE dados SET valor=? WHERE item=?', (self.ui.hi_box.text(), 'hi'))
            
            conn.commit()
            conn.close()
            
        else:
            self.ui.hi_label.setText('Hora inicial *')
            self.ui.hi_label.setStyleSheet("color: #9B2226;")
    
    def conf_hf_box(self):
        if self.validar_hora(self.ui.hf_box.text()):
            self.ui.hf_label.setText('Hora final')
            self.ui.hf_label.setStyleSheet("color: #001219;")
            
            conn = sqlite3.connect(self.path)
            cursor = conn.cursor()
                
            cursor.execute('UPDATE dados SET valor=? WHERE item=?', (self.ui.hf_box.text(), 'hf'))
            
            conn.commit()
            conn.close()
            
        else:
            self.ui.hf_label.setText('Hora final *')
            self.ui.hf_label.setStyleSheet("color: #9B2226;")
   
    def onReturnPressed(self):
        sender = self.sender()
    
        if sender == self.ui.lat_box:
            self.conf_lat_box()
                
        if sender == self.ui.log_box:
            self.conf_log_box()
        
        if sender == self.ui.temp_box:
            self.conf_temp_box()
        
        if sender == self.ui.umidade_box:
            self.conf_umidade_box
        
        if sender == self.ui.hi_box:
            self.conf_hi_box()
                
        if sender == self.ui.hf_box:
            self.conf_hf_box()
    
    def checkboxStateChanged(self, state):
        sender = self.sender()
        if state == 2:
            if sender == self.ui.verao_box:
                self.ui.inverno_box.setChecked(False)
                self.ui.mes_cbox.setEnabled(True)
                self.ui.mes_cbox.clear()
                self.ui.mes_cbox.addItems(('Dezembro', 'Março'))
            else:
                self.ui.verao_box.setChecked(False)
                self.ui.mes_cbox.setEnabled(False)
                self.ui.mes_cbox.clear()
                self.ui.mes_cbox.addItem('Junho')
        if state == 0:
            if sender == self.ui.verao_box:
                self.ui.inverno_box.setChecked(True)
                self.ui.mes_cbox.setEnabled(False)
                self.ui.mes_cbox.clear()
                self.ui.mes_cbox.addItem('Junho')
            else:
                self.ui.verao_box.setChecked(True)
                self.ui.mes_cbox.setEnabled(True)
                self.ui.mes_cbox.clear()
                self.ui.mes_cbox.addItems(('Dezembro', 'Março'))
    
    def onComboBoxIndexChanged(self, index):
        if self.ui.verao_box.isChecked():
            mes = self.ui.mes_cbox.currentText()[:3].lower()
            estacao = 'verao'
        else:
            mes = 'jun'
            estacao = 'inverno'
        
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()

        cursor.execute('UPDATE dados SET valor=? WHERE item=?', (mes, 'mes'))
        cursor.execute('UPDATE dados SET valor=? WHERE item=?', (estacao, 'estacao'))
        
        try:
            cursor.execute('UPDATE dados SET valor=? WHERE item=?', (str(ax.externo(self.cidade, estacao, mes)[0]), 't_ext'))
            cursor.execute('UPDATE dados SET valor=? WHERE item=?', (str(ax.externo(self.cidade, estacao, mes)[1]), 'ur_ext'))
        except:
            None
                    
        conn.commit()                    
        conn.close()
    
    def loaddata_zona(self): 
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute('SELECT zonas_id FROM zonas')
        
        data = cursor.fetchall()
        
        self.zonas_id = []
        
        for item in data:
            self.zonas_id.append(item[0])
        
        zonas = {}
        
        for item in self.zonas_id:
            cursor.execute(f'SELECT * from {item}_print')
            data = cursor.fetchall()
            zonas[item] = data

        conn.close()
        
        zonas_print = {}
        
        for k,v in zonas.items():
            pr = jn = ps = eq = 0
            cb_i = il_i = ''
            
            for item in v:
                pr += item.count('pr')
                jn += item.count('jn')
                if item[1] == 'ps':
                    ps += int(item[8])
                elif item[1] == 'eq':
                    eq += int(item[8])
                elif item[1] == 'cb':
                    if cb_i == '':
                        cb_i = item[2]
                    else:
                        cb_i = f'{cb_i}, {item[2]}'
                elif item[1] == 'il':
                    il_i = item[2]

            zonas_print[k] = [pr, jn, cb_i, ps, il_i, eq]
          
        self.ui.tabela_zona.setRowCount(len(self.zonas_id))
        self.ui.tabela_zona.setColumnCount(7)
        
        row = 0
        
        for k,v in zonas_print.items():
            if k[0] == '_': it = QTableWidgetItem(k[1:])
            else: it = QTableWidgetItem(k)
                
            it.setTextAlignment(Qt.AlignCenter)
            self.ui.tabela_zona.setItem(row, 0, it)
            
            for i in range(6):
                it = QTableWidgetItem(f'{v[i]}')
                it.setTextAlignment(Qt.AlignCenter)
                self.ui.tabela_zona.setItem(row, i+1, it)
            row += 1
        
        self.ui.tabela_zona.setHorizontalHeaderLabels(['ID', 'Quant. Parede', 'Quant. Janela', 'Cobertura', 'Ocupação', 'Iluminação', 'Equipamentos'])
        self.ui.tabela_zona.verticalHeader().setVisible(False)
        self.ui.tabela_zona.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        header = self.ui.tabela_zona.horizontalHeader()
        for i in range(7):
            if i == 3: header.setSectionResizeMode(i, QHeaderView.Stretch)
            else:  header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is self.ui.tabela_zona:
            menu = QMenu()
    
            editar_action = menu.addAction('Editar')
            remover_action = menu.addAction('Remover')

            editar_action.triggered.connect(self.editar_item)
            remover_action.triggered.connect(self.remover_item)
            
            if menu.exec_(event.globalPos()):
                None
            
            return True

        return super().eventFilter(source, event)
    
    def editar_item(self):
        try:
            item = self.ui.tabela_zona.currentIndex()
            row = int(item.row())
            it = self.ui.tabela_zona.item(row, 0).text() if not self.ui.tabela_zona.item(row, 0).text().isdigit() else f'_{self.ui.tabela_zona.item(row, 0).text()}'
            
            conn = sqlite3.connect(self.path)
            cursor = conn.cursor()
            
            cursor.execute('UPDATE dados SET valor=? WHERE item=?', (it, 'current'))
            
            conn.commit()                    
            conn.close()
            
            self.cargas_window()
            
        except:
            None
    
    def remover_item(self):
        item = self.ui.tabela_zona.currentIndex()
        row = int(item.row())
        it = self.ui.tabela_zona.item(row, 0).text() if not self.ui.tabela_zona.item(row, 0).text().isdigit() else f'_{self.ui.tabela_zona.item(row, 0).text()}'
        
        msgbox = QMessageBox()
        msgbox.setWindowIcon(QIcon('icon/delete.svg'))
        msgbox.setIcon(QMessageBox.Question)
        msgbox.setWindowTitle('Confirmar Exclusão')
        msgbox.setText('Excluir zona')
        msgbox.setInformativeText(f'Confirmar exclusão da zona {it if it[0] != "_" else it[1:]}?')
        buttonoptionA = msgbox.addButton('Confirmar', QMessageBox.YesRole)    
        buttonoptionB = msgbox.addButton('Cancelar', QMessageBox.AcceptRole)
        msgbox.exec_()
        
        if msgbox.clickedButton() == buttonoptionA:
            QMessageBox.information(self, "Zona Excluída", f'Zona {it if it[0] != "_" else it[1:]} excluída')
            
            conn = sqlite3.connect(self.path)
            cursor = conn.cursor()
            
            cursor.execute(f'DROP TABLE IF EXISTS {it}')
            cursor.execute(f'DROP TABLE IF EXISTS {it}_print')
            cursor.execute(f'DELETE FROM zonas WHERE zonas_id=?', (it,))
            
            conn.commit()
            conn.close()
                    
            self.loaddata_zona()
            
        elif msgbox.clickedButton() == buttonoptionB:
            QMessageBox.information(self, 'Exclusão Cancelada', 'Exclusão Cancelada') 
    
    def zona_btn(self):
        if self.ui.zona_id.text().strip() != '' and (self.ui.zona_id.text().strip()[-5:] != '_int' and self.ui.zona_id.text().strip()[-5:] != '_ext'):
            try:
                self.ui.zona_label.setText('Zona ID')
                self.ui.zona_label.setStyleSheet("color: #001219;")
                
                zona_nova = self.corrigir_nome_zona(self.ui.zona_id.text().strip())
                
                conn = sqlite3.connect(self.path)
                cursor = conn.cursor()    
                
                cursor.execute('UPDATE dados SET valor=? WHERE item=?', (zona_nova, 'current'))
                
                conn.commit()
                conn.close()
                
                if self.ui.zona_id.text().strip() not in self.zonas_id:
                    conn = sqlite3.connect(self.path)
                    cursor = conn.cursor()
                    
                    cursor.execute(f'''CREATE TABLE {zona_nova} (
                        "id" TEXT,
                        "data_type" TEXT,
                        "id_table" INTEGER,
                        "vidro" INTEGER,
                        "id_tinta" INTEGER,
                        "orientacao" INTEGER,
                        "area" TEXT,
                        "interno" INTEGER,
                        "amb_externo" INTEGER,
                        "qt" INTEGER)''')
                    
                    cursor.execute(f'''CREATE TABLE {zona_nova}_print (
                        "id" TEXT,
                        "data_type" TEXT,
                        "tipo" TEXT,
                        "area" TEXT,
                        "tinta" TEXT,
                        "orientacao" TEXT,
                        "interno" TEXT,
                        "amb_externo" TEXT,
                        "quantidade" INTEGER)''')
                    
                    cursor.execute(f'INSERT INTO zonas (zonas_id) VALUES (?)', (zona_nova,))
                    
                    conn.commit()
                    conn.close()
                    
                self.cargas_window()
            except:
                self.ui.zona_label.setText('Zona ID *')
                self.ui.zona_label.setStyleSheet("color: #9B2226;")
        else:
            self.ui.zona_label.setText('Zona ID *')
            self.ui.zona_label.setStyleSheet("color: #9B2226;")
    
    def att_btn(self):
        self.conf_lat_box()
        self.conf_log_box()
        self.conf_temp_box()
        self.conf_umidade_box()
        self.conf_hi_box()
        self.conf_hf_box()
        
        try:
            self.calc_loads()
            self.loaddata_resultado()
        except:
            None
            
        try:
            self.loaddata_resultado()
        except:
            print('erro load')
    
    def data_list(self):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        
        self.pr = {}
        for item in self.zonas_id:
            self.pr[item]=[]
        for item in self.zonas_id:
            cursor.execute(f'SELECT * FROM {item} WHERE data_type="pr"')
            data = cursor.fetchall()
            for parede in data:
                self.pr[item].append(parede)
                
        self.pt = {}
        for item in self.zonas_id:
            self.pt[item]=[]
        for item in self.zonas_id:
            cursor.execute(f'SELECT * FROM {item} WHERE data_type="pt"')
            data = cursor.fetchall()
            for porta in data:
                self.pt[item].append(porta)
                
        self.jn = {}
        for item in self.zonas_id:
            self.jn[item]=[]
        for item in self.zonas_id:
            cursor.execute(f'SELECT * FROM {item} WHERE data_type="jn"')
            data = cursor.fetchall()
            for janela in data:
                self.jn[item].append(janela)
        
        self.cb = {}
        for item in self.zonas_id:
            self.cb[item]=[]
        for item in self.zonas_id:
            cursor.execute(f'SELECT * FROM {item} WHERE data_type="cb"')
            data = cursor.fetchall()
            for cobertura in data:
                self.cb[item].append(cobertura)
        
        self.il = {}
        for item in self.zonas_id:
            self.il[item]=[]
        for item in self.zonas_id:
            cursor.execute(f'SELECT * FROM {item} WHERE data_type="il"')
            data = cursor.fetchall()
            for iluminacao in data:
                self.il[item].append(iluminacao)
        
        self.ps = {}
        for item in self.zonas_id:
            self.ps[item]=[]
        for item in self.zonas_id:
            cursor.execute(f'SELECT * FROM {item} WHERE data_type="ps"')
            data = cursor.fetchall()
            for pessoa in data:
                self.ps[item].append(pessoa)
        
        self.eq = {}
        for item in self.zonas_id:
            self.eq[item]=[]
        for item in self.zonas_id:
            cursor.execute(f'SELECT * FROM {item} WHERE data_type="eq"')
            data = cursor.fetchall()
            for equipamento in data:
                self.eq[item].append(equipamento)
        
        self.ot = {}
        for item in self.zonas_id:
            self.ot[item]=[]
        for item in self.zonas_id:
            cursor.execute(f'SELECT * FROM {item} WHERE data_type="ot"')
            data = cursor.fetchall()
            for outra in data:
                self.ot[item].append(outra)

        conn.close()
        
    def prop_list(self):
        conn = sqlite3.connect(resource_path('data/materiais.db'))
        cursor = conn.cursor()
        
        self.pr_prop = {}
        for item in self.zonas_id:
            self.pr_prop[item]=[]
        for k, v in self.pr.items():
            i=0
            for item in v:
                self.pr_prop[k].append(['', '', ''])
                if item[3] == 1:
                    row = int(item[2])
                    cursor.execute('SELECT U, FS FROM vidros WHERE rowid=?', (row,))
                    data = cursor.fetchall()
                    self.pr_prop[k][i][0] = dc(f'{data[0][0]}')
                    self.pr_prop[k][i][1] = dc(f'{data[0][1]}')
                else:
                    row = int(item[2])
                    cursor.execute('SELECT U FROM paredes WHERE rowid=?', (row,))
                    self.pr_prop[k][i][0] = dc(f'{cursor.fetchone()[0]}')
                    
                    row = int(item[4])
                    cursor.execute('SELECT absortancia FROM tintas WHERE rowid=?', (row,))
                    self.pr_prop[k][i][2] = dc(f'{cursor.fetchone()[0]}')
                i += 1        
                    
        self.pt_prop = {}
        for item in self.zonas_id:
            self.pt_prop[item]=[]
        for k, v in self.pt.items():
            i=0
            for item in v:
                self.pt_prop[k].append(['', '', ''])
                if item[3] == 1:
                    row = int(item[2])
                    cursor.execute('SELECT U, FS FROM vidros WHERE rowid=?', (row,))
                    data = cursor.fetchall()
                    self.pt_prop[k][i][0] = dc(f'{data[0][0]}')
                    self.pt_prop[k][i][1] = dc(f'{data[0][1]}')
                else:
                    if item[4] is None:
                        row = int(item[2])
                        cursor.execute('SELECT U, absortancia FROM portas WHERE rowid=?', (row,))
                        data = cursor.fetchall()
                        self.pt_prop[k][i][0] = dc(f'{data[0][0]}')
                        self.pt_prop[k][i][2] = dc(f'{data[0][1]}')
                    else:
                        row = int(item[2])
                        cursor.execute('SELECT U FROM portas WHERE rowid=?', (row,))
                        self.pt_prop[k][i][0] = dc(f'{cursor.fetchone()[0]}')
                        
                        row = int(item[4])
                        cursor.execute('SELECT absortancia FROM tintas WHERE rowid=?', (row,))
                        self.pt_prop[k][i][2] = dc(f'{cursor.fetchone()[0]}')         
                i += 1        
        
        self.jn_prop = {}
        for item in self.zonas_id:
            self.jn_prop[item]=[]
        for k, v in self.jn.items():
            i=0
            for item in v:
                self.jn_prop[k].append(['', '', ''])
                row = int(item[2])
                cursor.execute('SELECT U, FS FROM vidros WHERE rowid=?', (row,))
                data = cursor.fetchall()
                self.jn_prop[k][i][0] = dc(f'{data[0][0]}')
                self.jn_prop[k][i][1] = dc(f'{data[0][1]}')       
                i += 1
        
        self.cb_prop = {}
        for item in self.zonas_id:
            self.cb_prop[item]=[]
        for k, v in self.cb.items():
            i=0
            for item in v:
                self.cb_prop[k].append(['', '', ''])
                if item[3] == 1:
                    row = int(item[2])
                    cursor.execute('SELECT U, FS FROM vidros WHERE rowid=?', (row,))
                    data = cursor.fetchall()
                    self.cb_prop[k][i][0] = dc(f'{data[0][0]}')
                    self.cb_prop[k][i][1] = dc(f'{data[0][1]}')
                else:
                    if item[4] is None:
                        row = int(item[2])
                        cursor.execute('SELECT U, absortancia FROM coberturas WHERE rowid=?', (row,))
                        data = cursor.fetchall()
                        self.cb_prop[k][i][0] = dc(f'{data[0][0]}')
                        self.cb_prop[k][i][2] = dc(f'{data[0][1]}')
                    else:
                        row = int(item[2])
                        cursor.execute('SELECT U FROM coberturas WHERE rowid=?', (row,))
                        self.cb_prop[k][i][0] = dc(f'{cursor.fetchone()[0]}')
                        
                        row = int(item[4])
                        cursor.execute('SELECT absortancia FROM tintas WHERE rowid=?', (row,))
                        self.cb_prop[k][i][2] = dc(f'{cursor.fetchone()[0]}')    
                i += 1                     
        conn.close()
    
    def interna_list(self):
        conn = sqlite3.connect(resource_path('data/carga_interna.db'))
        cursor = conn.cursor()
        
        self.ps_prop = {}
        for item in self.zonas_id:
            self.ps_prop[item]=[]
        for k, v in self.ps.items():
            i=0
            for item in v:
                self.ps_prop[k].append(['', '', ''])
                row = int(item[2])
                cursor.execute('SELECT qs, ql FROM pessoas WHERE rowid=?', (row,))
                data = cursor.fetchall()
                self.ps_prop[k][i][0] = dc(f'{data[0][0]}')
                self.ps_prop[k][i][1] = dc(f'{data[0][1]}')
                self.ps_prop[k][i][2] = item[9]
                i += 1
        
        self.eq_prop = {}
        for item in self.zonas_id:
            self.eq_prop[item]=[]
        for k, v in self.eq.items():
            i=0
            for item in v:
                self.eq_prop[k].append(['', '', ''])
                row = int(item[2])
                cursor.execute('SELECT qs, ql FROM equipamentos WHERE rowid=?', (row,))
                data = cursor.fetchall()
                self.eq_prop[k][i][0] = dc(f'{data[0][0]}')
                self.eq_prop[k][i][1] = dc(f'{data[0][1]}')
                self.eq_prop[k][i][2] = item[9]
                i += 1
                      
        self.il_prop = {}
        for item in self.zonas_id:
            self.il_prop[item]=[]
        for k, v in self.il.items():
            for item in v:
                row = int(item[2])
                cursor.execute('SELECT potencia FROM iluminacao WHERE rowid=?', (row,))
                self.il_prop[k].append(dc(f'{cursor.fetchone()[0]}'))
        
        self.ot_prop = {}
        for item in self.zonas_id:
            self.ot_prop[item]=[]
        for k, v in self.ot.items():
            i=0
            self.ot_prop[k].extend((0, 0))
            for item in v:
                if item[2] == 0:
                    self.ot_prop[k][0] = dc(f'{self.ot_prop[k][0]}') + dc(f'{item[9]}')
                else:
                    self.ot_prop[k][1] = dc(f'{self.ot_prop[k][1]}') + dc(f'{item[9]}')         
        conn.close()
    
    def calc_loads(self):
        self.data_list()
        self.prop_list()
        self.interna_list()
        
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        
        cursor.execute(f'DELETE FROM resultados')
        conn.commit()
        
        cursor.execute('SELECT name FROM sqlite_master WHERE type="table";')
        tabelas = cursor.fetchall()
        nomes_das_tabelas = [tabela[0] for tabela in tabelas]
        tabelas_filtrada = [item for item in nomes_das_tabelas if item.endswith('_int') or item.endswith('_ext')]
        
        for tabela in tabelas_filtrada:
            cursor.execute(f'DROP TABLE IF EXISTS {tabela}')
        
        cursor.execute('SELECT valor FROM dados WHERE item IN (?, ?, ?, ?, ?, ?, ?) ORDER BY rowid', ('rad_proj', 'estacao', 'mes', 't_ext', 't_int', 'hi', 'hf'))
        data = cursor.fetchall()
        dados = []
        for item in data:
            dados.append(item[0])

        horas = ax.hora_rad((dados[5], dados[6]))
        
        colunas = f'id TEXT, {", ".join(f"_{item} TEXT" for item in horas)}, conv TEXT'

        for item in self.zonas_id:
            cursor.execute(f'CREATE TABLE IF NOT EXISTS {item}_ext ({colunas})')
            
            i = 0
            for it in self.pr_prop[item]:
                area = dc(f'{self.pr[item][i][6]}')
                u = it[0]
                rad = ax.rad(dados[1], dados[2], dados[0], horas, self.pr[item][i][5], 0 if self.pr[item][i][7] == 0 else 1)
                t_int = dc(f'{dados[4]}')
                t_ext = dc(f'{dados[3]}') if self.pr[item][i][8] == 0 else t_int
                Q_conv = ax.Q_conv(area, u, t_int, t_ext)
                if it[1] == '':
                    absortancia = it[2]
                    Q_rad = ax.Q_rad(area, absortancia, u, rad)
                else:
                    fs = it[1]
                    Q_rad = ax.Q_rad(area, 0, 0, rad, fs, 'tr')
                list_ins = [self.pr[item][i][0]]
                
                for k, v in Q_rad.items():
                    list_ins.append(f'{v}')
                list_ins.append(f'{Q_conv}')
                
                col = ['?' for c in range(len(horas)+2)]
                question_mark = f'{", ".join(f"{item}" for item in col)}'
                cursor.execute(f'INSERT INTO {item}_ext VALUES ({question_mark})', list_ins)
                i += 1
            
            i = 0
            for it in self.pt_prop[item]:
                area = dc(f'{self.pt[item][i][6]}')
                u = it[0]
                rad = ax.rad(dados[1], dados[2], dados[0], horas, self.pt[item][i][5], 0 if self.pt[item][i][7] == 0 else 1)
                t_int = dc(f'{dados[4]}')
                t_ext = dc(f'{dados[3]}') if self.pt[item][i][8] == 0 else t_int
                Q_conv = ax.Q_conv(area, u, t_int, t_ext)
                if it[1] == '':
                    absortancia = it[2]
                    Q_rad = ax.Q_rad(area, absortancia, u, rad)
                else:
                    fs = it[1]
                    Q_rad = ax.Q_rad(area, 0, 0, rad, fs, 'tr')
                
                list_ins = [self.pt[item][i][0]]
                
                for k, v in Q_rad.items():
                    list_ins.append(f'{v}')
                list_ins.append(f'{Q_conv}')
                
                col = ['?' for c in range(len(horas)+2)]
                question_mark = f'{", ".join(f"{item}" for item in col)}'
                cursor.execute(f'INSERT INTO {item}_ext VALUES ({question_mark})', list_ins)
                i += 1
                
            i = 0
            for it in self.jn_prop[item]:
                area = dc(f'{self.jn[item][i][6]}')
                u = it[0]
                fs = it[1]
                rad = ax.rad(dados[1], dados[2], dados[0], horas, self.jn[item][i][5], 0 if self.jn[item][i][7] == 0 else 1)
                t_int = dc(f'{dados[4]}')
                t_ext = dc(f'{dados[3]}') if self.jn[item][i][8] == 0 else t_int
                Q_conv = ax.Q_conv(area, u, t_int, t_ext)
                Q_rad = ax.Q_rad(area, 0, 0, rad, fs, 'tr')
                
                list_ins = [self.jn[item][i][0]]
                
                for k, v in Q_rad.items():
                    list_ins.append(f'{v}')
                list_ins.append(f'{Q_conv}')
                
                col = ['?' for c in range(len(horas)+2)]
                question_mark = f'{", ".join(f"{item}" for item in col)}'
                cursor.execute(f'INSERT INTO {item}_ext VALUES ({question_mark})', list_ins)
                i += 1 
            
            i = 0
            for it in self.cb_prop[item]:
                area = dc(f'{self.cb[item][i][6]}')
                u = it[0]
                rad = ax.rad(dados[1], dados[2], dados[0], horas, self.cb[item][i][5], 0 if self.cb[item][i][7] == 0 else 1)
                t_int = dc(f'{dados[4]}')
                t_ext = dc(f'{dados[3]}') if self.cb[item][i][8] == 0 else t_int
                Q_conv = ax.Q_conv(area, u, t_int, t_ext)
                if it[1] == '':
                    absortancia = it[2]
                    Q_rad = ax.Q_rad(area, absortancia, u, rad)
                else:
                    fs = it[1]
                    Q_rad = ax.Q_rad(area, 0, 0, rad, fs, 'tr')
                
                list_ins = [self.cb[item][i][0]]
                
                for k, v in Q_rad.items():
                    list_ins.append(f'{v}')
                list_ins.append(f'{Q_conv}')
                
                col = ['?' for c in range(len(horas)+2)]
                question_mark = f'{", ".join(f"{item}" for item in col)}'
                cursor.execute(f'INSERT INTO {item}_ext VALUES ({question_mark})', list_ins)
                i += 1 
            
            conn.commit()
            
            total = ['total']
            cursor.execute(f'PRAGMA table_info({item}_ext)')
            column_titles = [row[1] for row in cursor.fetchall()]
            for title in column_titles:
                if title != 'id':
                    cursor.execute(f'SELECT SUM({title}) FROM {item}_ext')
                    data = cursor.fetchone()[0]
                    total.append(0 if data is None else round(data, 2))
            col = ['?' for c in range(len(horas)+2)]
            question_mark = f'{", ".join(f"{item}" for item in col)}'
            cursor.execute(f'INSERT INTO {item}_ext VALUES ({question_mark})', total)

            conv = total[-1]
            total.pop()
            total = total[1:]
            pico = max(total)
            
            cursor.execute(f'CREATE TABLE IF NOT EXISTS {item}_int (tipo TEXT, qs TEXT, ql TEXT)')
            ps_s = ps_l = 0
            for it in self.ps_prop[item]:
                ps_s = ps_s + dc(f'{it[0]}') * it[2]
                ps_l = ps_l + dc(f'{it[1]}') * it[2]
            
            eq_s = eq_l = 0
            for it in self.eq_prop[item]:
                eq_s = eq_s + dc(f'{it[0]}') * it[2]
                eq_l = eq_l + dc(f'{it[1]}') * it[2]
                
            try:
                il = self.il_prop[item][0] * dc(f'{self.il[item][0][6]}')
            except:
                il = 0  
            
            ot_s = self.ot_prop[item][0]
            ot_l = self.ot_prop[item][1]
            
            internos = [
                ('ps', f'{ps_s}', f'{ps_l}'), ('eq', f'{eq_s}', f'{eq_l}'), ('il', f'{il}', None), ('ot', f'{ot_s}', f'{ot_l}'),
                ('total', f'{ps_s+eq_s+il+ot_s}', f'{ps_l+eq_l+ot_l}')]
            
            cursor.executemany(f'INSERT INTO {item}_int VALUES (?, ?, ?)', internos)

            conn.commit()
            
            carga_s = dc(f'{pico}') + dc(f'{ps_s}') + dc(f'{eq_s}') + dc(f'{il}') + dc(f'{ot_s}') + dc(f'{conv}')
            carga_l = dc(f'{ps_l}') + dc(f'{eq_l}') + dc(f'{ot_l}')
            carga = carga_s + carga_l
            resultado = [item, f'{carga_s}', f'{carga_l}', f'{carga}', f'{round(ax.converter_potencia(carga, "w", "btuh"), 5)}', f'{round(ax.converter_potencia(carga, "w", "tr"), 5)}']
            
            cursor.execute('INSERT INTO resultados VALUES (?, ?, ?, ?, ?, ?)', resultado)
            conn.commit()
        
        
        total = ['TOTAL']
        column_titles = ['zona', 'qs_w', 'ql_w', 'total_w', 'total_btuh', 'total_tr']
        for title in column_titles:
            if title != 'zona':
                cursor.execute(f'SELECT SUM({title}) FROM resultados')
                data = cursor.fetchall()
                for it in data: total.append(it[0])
        cursor.execute(f'INSERT INTO resultados VALUES (?, ?, ?, ?, ?, ?)', total)
        conn.commit()
        conn.close()
    
    def loaddata_resultado(self):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM resultados')
        data = cursor.fetchall()
        
        row = 0
        self.ui.tabela_resultado.setRowCount(len(data))
        self.ui.tabela_resultado.setColumnCount(6)
        
        for item in data:
            for i in range(6):
                it = QTableWidgetItem(item[i])
                it.setTextAlignment(Qt.AlignCenter)
                self.ui.tabela_resultado.setItem(row, i, it)
            row+=1
            
        self.ui.tabela_resultado.setHorizontalHeaderLabels(['Zona', 'QS (W)', 'QL (W)', 'Total (W)', 'Total (Btu/h)', 'Total (TR)'])
        self.ui.tabela_resultado.verticalHeader().setVisible(False)
        self.ui.tabela_resultado.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        header = self.ui.tabela_resultado.horizontalHeader()
        for c in range(6): header.setSectionResizeMode(c, QHeaderView.Stretch)   
    
    def closeEvent(self, event):
            for window in QApplication.topLevelWidgets():
                window.close()
       
if __name__ == "__main__":
    app = QApplication(sys.argv)

    QFontDatabase.addApplicationFont(resource_path('font/OpenSans_SemiCondensed-Medium.ttf'))
    QFontDatabase.addApplicationFont(resource_path('font/OpenSans-Bold.ttf'))
    QFontDatabase.addApplicationFont(resource_path('font/Roboto-Bold.ttf'))

    window = MainWindow()
    window.show()
    print()
    sys.exit(app.exec())



