# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_tab2.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class MyComboBox(QtWidgets.QComboBox):
    clicked = QtCore.pyqtSignal()  # 创建一个信号

    def showPopup(self):  # 重写showPopup函数
        self.clicked.emit()  # 发送信号
        super(MyComboBox, self).showPopup()


class Ui_Tab2(object):
    def setupUi(self, Tab2):
        Tab2.setObjectName("Tab2")
        Tab2.resize(1024, 768)
        self.gridLayout = QtWidgets.QGridLayout(Tab2)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.serial_data_display = QtWidgets.QTextBrowser(Tab2)
        self.serial_data_display.setObjectName("serial_data_display")
        self.verticalLayout_2.addWidget(self.serial_data_display)
        self.serial_tx_input = QtWidgets.QPlainTextEdit(Tab2)
        self.serial_tx_input.setObjectName("serial_tx_input")
        self.verticalLayout_2.addWidget(self.serial_tx_input)
        self.verticalLayout_2.setStretch(0, 2)
        self.verticalLayout_2.setStretch(1, 1)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Tab2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.serial_select_combobox = MyComboBox(Tab2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serial_select_combobox.sizePolicy().hasHeightForWidth())
        self.serial_select_combobox.setSizePolicy(sizePolicy)
        self.serial_select_combobox.setObjectName("serial_select_combobox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.serial_select_combobox)
        self.label_2 = QtWidgets.QLabel(Tab2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.serial_connect_button = QtWidgets.QPushButton(Tab2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serial_connect_button.sizePolicy().hasHeightForWidth())
        self.serial_connect_button.setSizePolicy(sizePolicy)
        self.serial_connect_button.setObjectName("serial_connect_button")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.serial_connect_button)
        self.baud_select_combobox = MyComboBox(Tab2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.baud_select_combobox.sizePolicy().hasHeightForWidth())
        self.baud_select_combobox.setSizePolicy(sizePolicy)
        self.baud_select_combobox.setObjectName("baud_select_combobox")
        self.baud_select_combobox.addItem("")
        self.baud_select_combobox.addItem("")
        self.baud_select_combobox.addItem("")
        self.baud_select_combobox.addItem("")
        self.baud_select_combobox.addItem("")
        self.baud_select_combobox.addItem("")
        self.baud_select_combobox.addItem("")
        self.baud_select_combobox.addItem("")
        self.baud_select_combobox.addItem("")
        self.baud_select_combobox.addItem("")
        self.baud_select_combobox.addItem("")
        self.baud_select_combobox.addItem("")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.baud_select_combobox)
        self.serial_disconnect_button = QtWidgets.QPushButton(Tab2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serial_disconnect_button.sizePolicy().hasHeightForWidth())
        self.serial_disconnect_button.setSizePolicy(sizePolicy)
        self.serial_disconnect_button.setObjectName("serial_disconnect_button")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.serial_disconnect_button)
        self.verticalLayout_3.addLayout(self.formLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.rx_line_wrap_mode_checkbox = QtWidgets.QCheckBox(Tab2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rx_line_wrap_mode_checkbox.sizePolicy().hasHeightForWidth())
        self.rx_line_wrap_mode_checkbox.setSizePolicy(sizePolicy)
        self.rx_line_wrap_mode_checkbox.setObjectName("rx_line_wrap_mode_checkbox")
        self.verticalLayout_3.addWidget(self.rx_line_wrap_mode_checkbox)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.tx_send_data_button = QtWidgets.QPushButton(Tab2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tx_send_data_button.sizePolicy().hasHeightForWidth())
        self.tx_send_data_button.setSizePolicy(sizePolicy)
        self.tx_send_data_button.setMinimumSize(QtCore.QSize(0, 60))
        self.tx_send_data_button.setObjectName("tx_send_data_button")
        self.verticalLayout_3.addWidget(self.tx_send_data_button)
        self.tx_newline_checkbox = QtWidgets.QCheckBox(Tab2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tx_newline_checkbox.sizePolicy().hasHeightForWidth())
        self.tx_newline_checkbox.setSizePolicy(sizePolicy)
        self.tx_newline_checkbox.setObjectName("tx_newline_checkbox")
        self.verticalLayout_3.addWidget(self.tx_newline_checkbox)
        self.tx_escape_checkbox = QtWidgets.QCheckBox(Tab2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tx_escape_checkbox.sizePolicy().hasHeightForWidth())
        self.tx_escape_checkbox.setSizePolicy(sizePolicy)
        self.tx_escape_checkbox.setObjectName("tx_escape_checkbox")
        self.verticalLayout_3.addWidget(self.tx_escape_checkbox)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.verticalLayout_3.setStretch(0, 5)
        self.verticalLayout_3.setStretch(1, 5)
        self.verticalLayout_3.setStretch(2, 5)
        self.verticalLayout_3.setStretch(3, 5)
        self.verticalLayout_3.setStretch(4, 5)
        self.verticalLayout_3.setStretch(5, 5)
        self.verticalLayout_3.setStretch(6, 5)
        self.verticalLayout_3.setStretch(7, 4)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 10)
        self.gridLayout.setColumnStretch(1, 1)

        self.retranslateUi(Tab2)
        self.baud_select_combobox.setCurrentIndex(6)
        QtCore.QMetaObject.connectSlotsByName(Tab2)

    def retranslateUi(self, Tab2):
        _translate = QtCore.QCoreApplication.translate
        Tab2.setWindowTitle(_translate("Tab2", "Form"))
        self.label.setText(_translate("Tab2", "串口号"))
        self.label_2.setText(_translate("Tab2", "波特率"))
        self.serial_connect_button.setText(_translate("Tab2", "串口连接"))
        self.baud_select_combobox.setItemText(0, _translate("Tab2", "9600"))
        self.baud_select_combobox.setItemText(1, _translate("Tab2", "14400"))
        self.baud_select_combobox.setItemText(2, _translate("Tab2", "19200"))
        self.baud_select_combobox.setItemText(3, _translate("Tab2", "38400"))
        self.baud_select_combobox.setItemText(4, _translate("Tab2", "56000"))
        self.baud_select_combobox.setItemText(5, _translate("Tab2", "57600"))
        self.baud_select_combobox.setItemText(6, _translate("Tab2", "115200"))
        self.baud_select_combobox.setItemText(7, _translate("Tab2", "128000"))
        self.baud_select_combobox.setItemText(8, _translate("Tab2", "230400"))
        self.baud_select_combobox.setItemText(9, _translate("Tab2", "256000"))
        self.baud_select_combobox.setItemText(10, _translate("Tab2", "460800"))
        self.baud_select_combobox.setItemText(11, _translate("Tab2", "921600"))
        self.serial_disconnect_button.setText(_translate("Tab2", "断开连接"))
        self.rx_line_wrap_mode_checkbox.setText(_translate("Tab2", "自动换行"))
        self.tx_send_data_button.setText(_translate("Tab2", "发送"))
        self.tx_newline_checkbox.setText(_translate("Tab2", "自动添加换行符\\r\\n"))
        self.tx_escape_checkbox.setText(_translate("Tab2", "字符转义"))
