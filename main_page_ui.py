# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Matheus\Dropbox\pyvac\main_page.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(950, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.full_menu_widget = QtWidgets.QWidget(self.centralwidget)
        self.full_menu_widget.setObjectName("full_menu_widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.full_menu_widget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.dados_btn_2 = QtWidgets.QPushButton(self.full_menu_widget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/icon/proj_detail_off.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/icon/icon/proj_detail_on.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.dados_btn_2.setIcon(icon)
        self.dados_btn_2.setIconSize(QtCore.QSize(19, 19))
        self.dados_btn_2.setCheckable(True)
        self.dados_btn_2.setAutoExclusive(True)
        self.dados_btn_2.setObjectName("dados_btn_2")
        self.verticalLayout_2.addWidget(self.dados_btn_2)
        self.zonas_btn_2 = QtWidgets.QPushButton(self.full_menu_widget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/icon/zones_off.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(":/icon/icon/zones_on.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.zonas_btn_2.setIcon(icon1)
        self.zonas_btn_2.setIconSize(QtCore.QSize(19, 19))
        self.zonas_btn_2.setCheckable(True)
        self.zonas_btn_2.setAutoExclusive(True)
        self.zonas_btn_2.setObjectName("zonas_btn_2")
        self.verticalLayout_2.addWidget(self.zonas_btn_2)
        self.resultados_btn_2 = QtWidgets.QPushButton(self.full_menu_widget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/icon/results_off.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(":/icon/icon/results_on.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.resultados_btn_2.setIcon(icon2)
        self.resultados_btn_2.setIconSize(QtCore.QSize(19, 19))
        self.resultados_btn_2.setCheckable(True)
        self.resultados_btn_2.setAutoExclusive(True)
        self.resultados_btn_2.setObjectName("resultados_btn_2")
        self.verticalLayout_2.addWidget(self.resultados_btn_2)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 373, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.att_btn_2 = QtWidgets.QPushButton(self.full_menu_widget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icon/icon/update_off.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.att_btn_2.setIcon(icon3)
        self.att_btn_2.setIconSize(QtCore.QSize(19, 19))
        self.att_btn_2.setObjectName("att_btn_2")
        self.verticalLayout_4.addWidget(self.att_btn_2)
        self.gridLayout.addWidget(self.full_menu_widget, 0, 1, 1, 1)
        self.icon_only_widget = QtWidgets.QWidget(self.centralwidget)
        self.icon_only_widget.setObjectName("icon_only_widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.icon_only_widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.dados_btn_1 = QtWidgets.QPushButton(self.icon_only_widget)
        self.dados_btn_1.setText("")
        self.dados_btn_1.setIcon(icon)
        self.dados_btn_1.setIconSize(QtCore.QSize(30, 30))
        self.dados_btn_1.setCheckable(True)
        self.dados_btn_1.setAutoExclusive(True)
        self.dados_btn_1.setObjectName("dados_btn_1")
        self.verticalLayout.addWidget(self.dados_btn_1)
        self.zonas_btn_1 = QtWidgets.QPushButton(self.icon_only_widget)
        self.zonas_btn_1.setText("")
        self.zonas_btn_1.setIcon(icon1)
        self.zonas_btn_1.setIconSize(QtCore.QSize(30, 30))
        self.zonas_btn_1.setCheckable(True)
        self.zonas_btn_1.setAutoExclusive(True)
        self.zonas_btn_1.setObjectName("zonas_btn_1")
        self.verticalLayout.addWidget(self.zonas_btn_1)
        self.resultados_btn_1 = QtWidgets.QPushButton(self.icon_only_widget)
        self.resultados_btn_1.setText("")
        self.resultados_btn_1.setIcon(icon2)
        self.resultados_btn_1.setIconSize(QtCore.QSize(30, 30))
        self.resultados_btn_1.setCheckable(True)
        self.resultados_btn_1.setAutoExclusive(True)
        self.resultados_btn_1.setObjectName("resultados_btn_1")
        self.verticalLayout.addWidget(self.resultados_btn_1)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 375, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.att_btn_1 = QtWidgets.QPushButton(self.icon_only_widget)
        self.att_btn_1.setText("")
        self.att_btn_1.setIcon(icon3)
        self.att_btn_1.setIconSize(QtCore.QSize(30, 30))
        self.att_btn_1.setObjectName("att_btn_1")
        self.verticalLayout_3.addWidget(self.att_btn_1)
        self.gridLayout.addWidget(self.icon_only_widget, 0, 0, 1, 1)
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.widget = QtWidgets.QWidget(self.widget_3)
        self.widget.setMinimumSize(QtCore.QSize(0, 40))
        self.widget.setObjectName("widget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 9, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.change_btn = QtWidgets.QPushButton(self.widget)
        self.change_btn.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icon/icon/menu.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.change_btn.setIcon(icon4)
        self.change_btn.setIconSize(QtCore.QSize(19, 19))
        self.change_btn.setCheckable(True)
        self.change_btn.setObjectName("change_btn")
        self.horizontalLayout_4.addWidget(self.change_btn)
        spacerItem2 = QtWidgets.QSpacerItem(236, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_4.addLayout(self.horizontalLayout)
        self.verticalLayout_5.addWidget(self.widget)
        self.stackedWidget = QtWidgets.QStackedWidget(self.widget_3)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.page)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.widget_2 = QtWidgets.QWidget(self.page)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.dados_clima_label = QtWidgets.QLabel(self.widget_2)
        self.dados_clima_label.setObjectName("dados_clima_label")
        self.verticalLayout_10.addWidget(self.dados_clima_label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.lat_label = QtWidgets.QLabel(self.widget_2)
        self.lat_label.setObjectName("lat_label")
        self.verticalLayout_6.addWidget(self.lat_label)
        self.lat_box = QtWidgets.QLineEdit(self.widget_2)
        self.lat_box.setObjectName("lat_box")
        self.verticalLayout_6.addWidget(self.lat_box)
        self.coord_model = QtWidgets.QLabel(self.widget_2)
        self.coord_model.setObjectName("coord_model")
        self.verticalLayout_6.addWidget(self.coord_model)
        self.horizontalLayout_2.addLayout(self.verticalLayout_6)
        self.label_spc_1 = QtWidgets.QLabel(self.widget_2)
        self.label_spc_1.setMinimumSize(QtCore.QSize(200, 0))
        self.label_spc_1.setText("")
        self.label_spc_1.setObjectName("label_spc_1")
        self.horizontalLayout_2.addWidget(self.label_spc_1)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.rad_lat_label = QtWidgets.QLabel(self.widget_2)
        self.rad_lat_label.setObjectName("rad_lat_label")
        self.verticalLayout_9.addWidget(self.rad_lat_label)
        self.rad_lat_box = QtWidgets.QLineEdit(self.widget_2)
        self.rad_lat_box.setEnabled(False)
        self.rad_lat_box.setObjectName("rad_lat_box")
        self.verticalLayout_9.addWidget(self.rad_lat_box)
        self.label_3 = QtWidgets.QLabel(self.widget_2)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_9.addWidget(self.label_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_9)
        self.verticalLayout_10.addLayout(self.horizontalLayout_2)
        self.label_spc_3 = QtWidgets.QLabel(self.widget_2)
        self.label_spc_3.setMinimumSize(QtCore.QSize(0, 20))
        self.label_spc_3.setText("")
        self.label_spc_3.setObjectName("label_spc_3")
        self.verticalLayout_10.addWidget(self.label_spc_3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.log_label = QtWidgets.QLabel(self.widget_2)
        self.log_label.setObjectName("log_label")
        self.verticalLayout_8.addWidget(self.log_label)
        self.log_box = QtWidgets.QLineEdit(self.widget_2)
        self.log_box.setObjectName("log_box")
        self.verticalLayout_8.addWidget(self.log_box)
        self.coord_model_2 = QtWidgets.QLabel(self.widget_2)
        self.coord_model_2.setObjectName("coord_model_2")
        self.verticalLayout_8.addWidget(self.coord_model_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_8)
        self.label_spc_2 = QtWidgets.QLabel(self.widget_2)
        self.label_spc_2.setMinimumSize(QtCore.QSize(200, 0))
        self.label_spc_2.setText("")
        self.label_spc_2.setObjectName("label_spc_2")
        self.horizontalLayout_3.addWidget(self.label_spc_2)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.cid_proj_label = QtWidgets.QLabel(self.widget_2)
        self.cid_proj_label.setObjectName("cid_proj_label")
        self.verticalLayout_7.addWidget(self.cid_proj_label)
        self.cid_proj_box = QtWidgets.QLineEdit(self.widget_2)
        self.cid_proj_box.setEnabled(False)
        self.cid_proj_box.setObjectName("cid_proj_box")
        self.verticalLayout_7.addWidget(self.cid_proj_box)
        self.label_4 = QtWidgets.QLabel(self.widget_2)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_7.addWidget(self.label_4)
        self.horizontalLayout_3.addLayout(self.verticalLayout_7)
        self.verticalLayout_10.addLayout(self.horizontalLayout_3)
        self.label_spc_7 = QtWidgets.QLabel(self.widget_2)
        self.label_spc_7.setMinimumSize(QtCore.QSize(0, 20))
        self.label_spc_7.setText("")
        self.label_spc_7.setObjectName("label_spc_7")
        self.verticalLayout_10.addWidget(self.label_spc_7)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.mes_label = QtWidgets.QLabel(self.widget_2)
        self.mes_label.setObjectName("mes_label")
        self.verticalLayout_11.addWidget(self.mes_label)
        self.mes_cbox = QtWidgets.QComboBox(self.widget_2)
        self.mes_cbox.setObjectName("mes_cbox")
        self.verticalLayout_11.addWidget(self.mes_cbox)
        self.horizontalLayout_5.addLayout(self.verticalLayout_11)
        self.label_spc_5 = QtWidgets.QLabel(self.widget_2)
        self.label_spc_5.setMinimumSize(QtCore.QSize(20, 0))
        self.label_spc_5.setText("")
        self.label_spc_5.setObjectName("label_spc_5")
        self.horizontalLayout_5.addWidget(self.label_spc_5)
        self.verticalLayout_16 = QtWidgets.QVBoxLayout()
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.verao_box = QtWidgets.QCheckBox(self.widget_2)
        self.verao_box.setChecked(True)
        self.verao_box.setObjectName("verao_box")
        self.verticalLayout_16.addWidget(self.verao_box)
        self.horizontalLayout_5.addLayout(self.verticalLayout_16)
        self.label_spc_6 = QtWidgets.QLabel(self.widget_2)
        self.label_spc_6.setMinimumSize(QtCore.QSize(20, 0))
        self.label_spc_6.setText("")
        self.label_spc_6.setObjectName("label_spc_6")
        self.horizontalLayout_5.addWidget(self.label_spc_6)
        self.verticalLayout_17 = QtWidgets.QVBoxLayout()
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.inverno_box = QtWidgets.QCheckBox(self.widget_2)
        self.inverno_box.setObjectName("inverno_box")
        self.verticalLayout_17.addWidget(self.inverno_box)
        self.horizontalLayout_5.addLayout(self.verticalLayout_17)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.verticalLayout_10.addLayout(self.horizontalLayout_5)
        self.label_spc_8 = QtWidgets.QLabel(self.widget_2)
        self.label_spc_8.setMinimumSize(QtCore.QSize(0, 70))
        self.label_spc_8.setText("")
        self.label_spc_8.setObjectName("label_spc_8")
        self.verticalLayout_10.addWidget(self.label_spc_8)
        self.dados_ambiente_label = QtWidgets.QLabel(self.widget_2)
        self.dados_ambiente_label.setObjectName("dados_ambiente_label")
        self.verticalLayout_10.addWidget(self.dados_ambiente_label)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.temp_label = QtWidgets.QLabel(self.widget_2)
        self.temp_label.setObjectName("temp_label")
        self.verticalLayout_12.addWidget(self.temp_label)
        self.temp_box = QtWidgets.QLineEdit(self.widget_2)
        self.temp_box.setObjectName("temp_box")
        self.verticalLayout_12.addWidget(self.temp_box)
        self.horizontalLayout_6.addLayout(self.verticalLayout_12)
        self.label = QtWidgets.QLabel(self.widget_2)
        self.label.setMinimumSize(QtCore.QSize(200, 0))
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout_6.addWidget(self.label)
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.umidade_label = QtWidgets.QLabel(self.widget_2)
        self.umidade_label.setObjectName("umidade_label")
        self.verticalLayout_13.addWidget(self.umidade_label)
        self.umidade_box = QtWidgets.QLineEdit(self.widget_2)
        self.umidade_box.setObjectName("umidade_box")
        self.verticalLayout_13.addWidget(self.umidade_box)
        self.horizontalLayout_6.addLayout(self.verticalLayout_13)
        self.verticalLayout_10.addLayout(self.horizontalLayout_6)
        self.label_spc_10 = QtWidgets.QLabel(self.widget_2)
        self.label_spc_10.setMinimumSize(QtCore.QSize(0, 20))
        self.label_spc_10.setText("")
        self.label_spc_10.setObjectName("label_spc_10")
        self.verticalLayout_10.addWidget(self.label_spc_10)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.hi_label = QtWidgets.QLabel(self.widget_2)
        self.hi_label.setObjectName("hi_label")
        self.verticalLayout_14.addWidget(self.hi_label)
        self.hi_box = QtWidgets.QLineEdit(self.widget_2)
        self.hi_box.setObjectName("hi_box")
        self.verticalLayout_14.addWidget(self.hi_box)
        self.hora_model = QtWidgets.QLabel(self.widget_2)
        self.hora_model.setObjectName("hora_model")
        self.verticalLayout_14.addWidget(self.hora_model)
        self.horizontalLayout_7.addLayout(self.verticalLayout_14)
        self.label_spc_9 = QtWidgets.QLabel(self.widget_2)
        self.label_spc_9.setMinimumSize(QtCore.QSize(200, 0))
        self.label_spc_9.setText("")
        self.label_spc_9.setObjectName("label_spc_9")
        self.horizontalLayout_7.addWidget(self.label_spc_9)
        self.verticalLayout_15 = QtWidgets.QVBoxLayout()
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.hf_label = QtWidgets.QLabel(self.widget_2)
        self.hf_label.setObjectName("hf_label")
        self.verticalLayout_15.addWidget(self.hf_label)
        self.hf_box = QtWidgets.QLineEdit(self.widget_2)
        self.hf_box.setObjectName("hf_box")
        self.verticalLayout_15.addWidget(self.hf_box)
        self.hora_model_2 = QtWidgets.QLabel(self.widget_2)
        self.hora_model_2.setObjectName("hora_model_2")
        self.verticalLayout_15.addWidget(self.hora_model_2)
        self.horizontalLayout_7.addLayout(self.verticalLayout_15)
        self.verticalLayout_10.addLayout(self.horizontalLayout_7)
        self.gridLayout_5.addLayout(self.verticalLayout_10, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.widget_2, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.page_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.widget_4 = QtWidgets.QWidget(self.page_2)
        self.widget_4.setObjectName("widget_4")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.widget_4)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout()
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.zona_label = QtWidgets.QLabel(self.widget_4)
        self.zona_label.setObjectName("zona_label")
        self.verticalLayout_18.addWidget(self.zona_label)
        self.zona_id = QtWidgets.QLineEdit(self.widget_4)
        self.zona_id.setObjectName("zona_id")
        self.verticalLayout_18.addWidget(self.zona_id)
        self.gridLayout_6.addLayout(self.verticalLayout_18, 0, 0, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem4)
        self.zona_ok_btn_1 = QtWidgets.QPushButton(self.widget_4)
        self.zona_ok_btn_1.setMinimumSize(QtCore.QSize(30, 30))
        self.zona_ok_btn_1.setMaximumSize(QtCore.QSize(30, 30))
        self.zona_ok_btn_1.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icon/icon/add_button.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.zona_ok_btn_1.setIcon(icon5)
        self.zona_ok_btn_1.setIconSize(QtCore.QSize(20, 20))
        self.zona_ok_btn_1.setObjectName("zona_ok_btn_1")
        self.horizontalLayout_8.addWidget(self.zona_ok_btn_1)
        self.gridLayout_6.addLayout(self.horizontalLayout_8, 1, 0, 1, 1)
        self.label_spc_11 = QtWidgets.QLabel(self.widget_4)
        self.label_spc_11.setMinimumSize(QtCore.QSize(0, 40))
        self.label_spc_11.setMaximumSize(QtCore.QSize(16777215, 40))
        self.label_spc_11.setText("")
        self.label_spc_11.setObjectName("label_spc_11")
        self.gridLayout_6.addWidget(self.label_spc_11, 2, 0, 1, 1)
        self.verticalLayout_19 = QtWidgets.QVBoxLayout()
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.tabela_zona = QtWidgets.QTableWidget(self.widget_4)
        self.tabela_zona.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tabela_zona.setShowGrid(False)
        self.tabela_zona.setRowCount(0)
        self.tabela_zona.setObjectName("tabela_zona")
        self.tabela_zona.setColumnCount(0)
        self.tabela_zona.horizontalHeader().setVisible(True)
        self.tabela_zona.verticalHeader().setVisible(False)
        self.verticalLayout_19.addWidget(self.tabela_zona)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_19.addItem(spacerItem5)
        self.gridLayout_6.addLayout(self.verticalLayout_19, 3, 0, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout_6, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.widget_4, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.page_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.widget_5 = QtWidgets.QWidget(self.page_3)
        self.widget_5.setObjectName("widget_5")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.widget_5)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.verticalLayout_20 = QtWidgets.QVBoxLayout()
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.label_2 = QtWidgets.QLabel(self.widget_5)
        self.label_2.setMinimumSize(QtCore.QSize(0, 100))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.verticalLayout_20.addWidget(self.label_2)
        self.tabela_resultado = QtWidgets.QTableWidget(self.widget_5)
        self.tabela_resultado.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tabela_resultado.setShowGrid(False)
        self.tabela_resultado.setObjectName("tabela_resultado")
        self.tabela_resultado.setColumnCount(0)
        self.tabela_resultado.setRowCount(0)
        self.tabela_resultado.verticalHeader().setVisible(False)
        self.verticalLayout_20.addWidget(self.tabela_resultado)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_20.addItem(spacerItem6)
        self.gridLayout_8.addLayout(self.verticalLayout_20, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.widget_5, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_3)
        self.verticalLayout_5.addWidget(self.stackedWidget)
        self.gridLayout.addWidget(self.widget_3, 0, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(1)
        self.change_btn.toggled['bool'].connect(self.icon_only_widget.setVisible) # type: ignore
        self.change_btn.toggled['bool'].connect(self.full_menu_widget.setHidden) # type: ignore
        self.dados_btn_1.toggled['bool'].connect(self.dados_btn_2.setChecked) # type: ignore
        self.zonas_btn_2.toggled['bool'].connect(self.zonas_btn_1.setChecked) # type: ignore
        self.resultados_btn_1.toggled['bool'].connect(self.resultados_btn_2.setChecked) # type: ignore
        self.resultados_btn_2.toggled['bool'].connect(self.resultados_btn_1.setChecked) # type: ignore
        self.dados_btn_2.toggled['bool'].connect(self.dados_btn_1.setChecked) # type: ignore
        self.zonas_btn_1.toggled['bool'].connect(self.zonas_btn_2.setChecked) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.dados_btn_2.setText(_translate("MainWindow", "Dados"))
        self.zonas_btn_2.setText(_translate("MainWindow", "Zonas"))
        self.resultados_btn_2.setText(_translate("MainWindow", "Resultados"))
        self.att_btn_2.setText(_translate("MainWindow", "Atualizar"))
        self.dados_clima_label.setText(_translate("MainWindow", "Dados de Clima"))
        self.lat_label.setText(_translate("MainWindow", "Latitude"))
        self.coord_model.setText(_translate("MainWindow", "xx°xx\'xx\'\'"))
        self.rad_lat_label.setText(_translate("MainWindow", "Latitude radiação"))
        self.label_3.setText(_translate("MainWindow", "a"))
        self.log_label.setText(_translate("MainWindow", "Longitude"))
        self.coord_model_2.setText(_translate("MainWindow", "xx°xx\'xx\'\'"))
        self.cid_proj_label.setText(_translate("MainWindow", "Cidade de projeto"))
        self.label_4.setText(_translate("MainWindow", "a"))
        self.mes_label.setText(_translate("MainWindow", "Mês"))
        self.verao_box.setText(_translate("MainWindow", "Verão"))
        self.inverno_box.setText(_translate("MainWindow", "Inverno"))
        self.dados_ambiente_label.setText(_translate("MainWindow", "Dados de Ambiente"))
        self.temp_label.setText(_translate("MainWindow", "Temperatura interna (°C)"))
        self.umidade_label.setText(_translate("MainWindow", "Umidade interna (%)"))
        self.hi_label.setText(_translate("MainWindow", "Hora inicial"))
        self.hora_model.setText(_translate("MainWindow", "xx:xx"))
        self.hf_label.setText(_translate("MainWindow", "Hora final"))
        self.hora_model_2.setText(_translate("MainWindow", "xx:xx"))
        self.zona_label.setText(_translate("MainWindow", "Zona ID"))
import resource_rc