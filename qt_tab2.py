import re
from datetime import datetime
from multiprocessing import Process

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore
from homepage import ui_tab2


class QTTab2(QMainWindow, ui_tab2.Ui_Tab2):
    log_signal = QtCore.pyqtSignal(str, str)  # log显示数据信号，第一个str为显示内容，第二个str为字体颜色
    rx_signal = QtCore.pyqtSignal(str, str)  # 串口助手显示数据信号，第一个str为显示内容，第二个str为字体颜色

    serial_command_signal = QtCore.pyqtSignal(str, str, int)
    serial_status_signal = QtCore.pyqtSignal(bool)
    serial_return_data_signal = QtCore.pyqtSignal(str, str)

    def __init__(self, parent, tab):
        super(QTTab2, self).__init__(parent)
        self.setupUi(tab)

        self.serial_data_process = {'serial_device': self.serial_device_update,}
        '''设置组件默认状态'''
        self.tx_send_data_button.setEnabled(False)
        self.serial_connect_button.setEnabled(True)
        self.serial_disconnect_button.setEnabled(False)
        self.tx_newline_checkbox.setChecked(True)
        self.serial_data_display.setLineWrapMode(0)
        self.baud_select_combobox.setEditable(True)

        ''' 设置信号和槽函数 '''
        self.tx_send_data_button.clicked.connect(self.serial_send_data)  # 串口助手数据发送
        self.serial_connect_button.clicked.connect(self.serial_device_connect)
        '''self.serial_select_combobox.clicked.connect(self.test1)
        self.serial_disconnect_button.clicked.connect(self.test2)'''
        self.serial_select_combobox.clicked.connect(
            lambda: self.serial_command_signal.emit('serial_device_scan', '', False))  # 按下串口选择下拉栏扫描串口设备
        self.serial_disconnect_button.clicked.connect(
            lambda: self.serial_command_signal.emit('disconnect', '', False))  # 串口断开连接

        self.rx_signal.connect(self.serial_rx_tx_data_display_thread)  # 串口助手显示信号传入
        self.rx_line_wrap_mode_checkbox.toggled.connect(self.serial_rx_line_wrap_change)  # 串口助手自动换行

        self.serial_status_signal.connect(self.serial_connect_status)
        self.serial_return_data_signal.connect(self.return_data_process)

    '''def test1(self):
        self.serial_command_signal.emit('serial_device_scan', '', False)

    def test2(self):
        self.serial_command_signal.emit('disconnect', '', False)'''

    def return_data_process(self, data, parameter):
        if data in self.serial_data_process.keys():
            self.serial_data_process[data](parameter)

    def serial_connect_status(self, connect_status):
        """
        串口设备连接
        """
        if connect_status:
            # self.connect_status_label.setStyleSheet('background-color:rgb(240,240,240);color:green;border:1px solid grey')
            # self.connect_status_label.setText('Connected')
            # 更改按键状态
            self.serial_connect_button.setEnabled(False)
            self.serial_disconnect_button.setEnabled(True)
            self.tx_send_data_button.setEnabled(True)
        else:
            # self.connect_status_label.setStyleSheet('background-color:yellow;color:red;border:1px solid grey')
            # self.connect_status_label.setText('Disconnect')
            self.serial_connect_button.setEnabled(True)
            self.serial_disconnect_button.setEnabled(False)
            self.tx_send_data_button.setEnabled(False)
            # self.tx_send_data_button.setEnabled(False)

    def serial_device_update(self, parameter):
        """
        扫描电脑上的串口设备
        """
        serial_device_list = parameter.split(',')

        self.serial_select_combobox.clear()  # 清空设备选项列表
        for i in serial_device_list:
            self.serial_select_combobox.addItem(str(i))  # 添加设备到列表
        if serial_device_list:
            current_port = 0
            for i in range(len(serial_device_list)):
                if 'CP210x' in str(serial_device_list[i]):  # 默认选择ESP32设备
                    current_port = i
                    self.baud_select_combobox.setCurrentText('921600')
            self.serial_select_combobox.setCurrentIndex(current_port)

    def serial_device_connect(self):
        """
        串口设备连接
        """
        if self.serial_select_combobox.currentText():
            connect_com = re.match(r'(.*?) #', str(self.serial_select_combobox.currentText())).group(1)
            connect_bps = self.baud_select_combobox.currentText()
            parameter = str(connect_com) + ',' + str(connect_bps)
            self.serial_command_signal.emit('connect', parameter, False)

    def serial_rx_tx_data_display_thread(self, text, color):
        log_thread = Process(target=self.serial_rx_tx_data_display, args=(text, color,))
        log_thread.run()

    def serial_rx_tx_data_display(self, text, color):
        """
        串口助手数据显示
        :param text: 显示数据
        :param color: 字体颜色
        """
        self.serial_data_display.moveCursor(self.serial_data_display.textCursor().End)
        self.serial_data_display.setTextColor(QColor(color))
        self.serial_data_display.insertPlainText(text)
        self.serial_data_display.moveCursor(self.serial_data_display.textCursor().End)

    def serial_send_data(self):
        """
        串口助手信息发送
        :return: None
        """
        # 检查是否在发送信息的末尾加入换行符
        if self.tx_newline_checkbox.isChecked():
            data_buffer = self.serial_tx_input.toPlainText() + '\r\n'
        else:
            data_buffer = self.serial_tx_input.toPlainText()

        # 检查是否将字符转义
        if self.tx_escape_checkbox.isChecked():
            data_buffer = data_buffer.replace('\\r', '\r')
            data_buffer = data_buffer.replace('\\n', '\n')
            data_buffer = data_buffer.replace('\\t', '\t')
        # 输出发送信息
        self.rx_signal.emit("\n\n[%s] SEND\n" % datetime.now(), 'grey')
        self.rx_signal.emit(data_buffer, 'blue')
        # 发送数据到串口
        self.serial_command_signal.emit('serial_send_data', data_buffer, True)
        # self.serial_device.write_data(data_buffer)

    def serial_rx_line_wrap_change(self):
        """
        串口助手数据显示模式
        :return: None
        """
        if self.rx_line_wrap_mode_checkbox.isChecked():
            self.serial_data_display.setLineWrapMode(1)  # 自动换行显示
            self.serial_data_display.moveCursor(self.serial_data_display.textCursor().End)
        else:
            self.serial_data_display.setLineWrapMode(0)  # 不换行显示
            self.serial_data_display.moveCursor(self.serial_data_display.textCursor().End)
