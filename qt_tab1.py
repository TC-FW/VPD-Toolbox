import os
import re
import threading
import time
from datetime import datetime
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QFileDialog
from PyQt5 import QtCore
import data_process
from PyQt5.QtCore import Qt

from homepage import ui_tab1


data_dict = {'EEPROM': None, 'Slot 0': None, 'Slot 1': None, 'Slot 2': None, 'Slot 3': None, 'Slot 4': None,
             'Slot 5': None, 'Slot 6': None, 'Slot 7': None, 'Slot 8': None, 'Slot 9': None, 'Slot 10': None,
             'Slot 11': None, 'Slot 12': None, 'Slot 13': None, 'Slot 14': None, 'Slot 15': None, }


class QTTab1(QMainWindow, ui_tab1.Ui_Tab1):
    log_signal = QtCore.pyqtSignal(str, str)  # log显示数据信号，第一个str为显示内容，第二个str为字体颜色
    rx_signal = QtCore.pyqtSignal(str, str)  # 串口助手显示数据信号，第一个str为显示内容，第二个str为字体颜色

    serial_command_signal = QtCore.pyqtSignal(str, str, int)
    serial_status_signal = QtCore.pyqtSignal(bool)
    serial_return_data_signal = QtCore.pyqtSignal(str, str)

    def __init__(self, parent, tab):
        super(QTTab1, self).__init__(parent)
        self.read_status = False

        self.setupUi(tab)

        self.serial_data_process = {'serial_device': self.serial_device_update,
                                    'iic_device': self.iic_device_update,
                                    'bq_manufacture_id': self.bq_manufacture_id_update,
                                    'eeprom_data': self.eeprom_data_update,
                                    'atecc508a_data': self.atecc508a_data_update, }

        ''' 初始化串口 '''
        self.serial_device_list = ''
        '''设置选项框状态和默认数值'''
        self.eeprom_device_address_combobox.setEditable(True)
        self.eeprom_device_address_combobox.setEditText('A0')
        self.atecc508a_device_address_combobox.setEditable(True)
        self.atecc508a_device_address_combobox.setEditText('D0')
        self.baud_select_combobox.setEditable(True)

        ''' 设置默认输出文件夹 '''
        self.folder_select_input.setText(os.getcwd().replace('\\', '/') + '/result/')  # 文件夹为软件运行目录下的result文件夹

        ''' 设置连接状态 '''
        self.connect_status_label.setAlignment(Qt.AlignCenter)
        self.connect_status_label.setStyleSheet('background-color:yellow;color:red;border:1px solid grey')
        self.connect_status_label.setText('Disconnect')

        '''设置组件默认状态'''
        self.serial_connect_button.setEnabled(True)
        self.serial_disconnect_button.setEnabled(False)
        self.iic_device_scan_button.setEnabled(False)
        self.eeprom_read_button.setEnabled(False)
        self.manufacture_id_read_button.setEnabled(False)
        self.atecc508a_read_button.setEnabled(False)
        self.manufacture_id_display.setReadOnly(True)
        self.log_data_display.setLineWrapMode(0)

        ''' 设置信号和槽函数 '''
        self.serial_select_combobox.clicked.connect(
            lambda: self.serial_command_signal.emit('serial_device_scan', '', False))  # 按下串口选择下拉栏扫描串口设备
        self.serial_connect_button.clicked.connect(self.serial_device_connect)  # 串口连接
        self.serial_disconnect_button.clicked.connect(
            lambda: self.serial_command_signal.emit('disconnect', '', False))  # 串口断开连接

        self.iic_device_scan_button.clicked.connect(self.iic_device_scan)  # IIC设备扫描 (仅为ESP32功能)
        self.eeprom_read_button.clicked.connect(self.eeprom_data_read)  # 数据读取
        self.atecc508a_read_button.clicked.connect(self.atecc508a_data_read)

        self.manufacture_id_read_button.clicked.connect(self.bq_manufacture_id_read)  # BQ ID读取

        self.data_copy_button.clicked.connect(self.data_copy)  # 数据复制
        self.data_clear_button.clicked.connect(self.data_clear)  # 数据清除
        self.file_expect_button.clicked.connect(self.data_expect_thread)  # 数据导出到文件
        self.data_select_combobox.currentTextChanged.connect(self.data_table_display)  # 数据选择显示
        self.folder_select_button.clicked.connect(self.expect_folder_select)  # 导出文件夹选择

        self.log_signal.connect(self.log_display)  # log数据显示信号传入

        self.serial_status_signal.connect(self.serial_connect_status)

        self.serial_return_data_signal.connect(self.return_data_process)

    def return_data_process(self, data, parameter):
        if data in self.serial_data_process.keys():
            self.serial_data_process[data](parameter)

    def log_display(self, text, color):
        """
        软件log数据显示
        :param text: 显示数据
        :param color: 字体颜色
        """
        self.log_data_display.moveCursor(self.log_data_display.textCursor().End)
        self.log_data_display.setTextColor(QColor(color))
        self.log_data_display.insertPlainText(text)
        self.log_data_display.moveCursor(self.log_data_display.textCursor().End)

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

    def serial_connect_status(self, connect_status):
        """
        串口设备连接
        """
        if connect_status:
            self.connect_status_label.setStyleSheet(
                'background-color:rgb(240,240,240);color:green;border:1px solid grey')
            self.connect_status_label.setText('Connected')
            # 更改按键状态
            self.serial_connect_button.setEnabled(False)
            self.serial_disconnect_button.setEnabled(True)
            self.iic_device_scan_button.setEnabled(True)
            self.manufacture_id_read_button.setEnabled(True)
            self.eeprom_read_button.setEnabled(True)
            self.manufacture_id_read_button.setEnabled(True)
            self.atecc508a_read_button.setEnabled(True)
        else:
            ''' 更新状态 '''
            self.connect_status_label.setStyleSheet(
                'background-color:yellow;color:red;border:1px solid grey')
            self.connect_status_label.setText('Disconnect')
            self.serial_connect_button.setEnabled(True)
            self.serial_disconnect_button.setEnabled(False)
            self.iic_device_scan_button.setEnabled(False)
            self.manufacture_id_read_button.setEnabled(False)
            self.eeprom_read_button.setEnabled(False)
            self.manufacture_id_read_button.setEnabled(False)
            self.atecc508a_read_button.setEnabled(False)

    def iic_device_scan(self):
        """
        串口扫描
        """
        self.log_signal.emit('[%s] ' % datetime.now(), 'grey')
        self.log_signal.emit('IIC Device Scanning\n', 'black')
        self.serial_command_signal.emit('iic_device_scan', '', True)

    def iic_device_update(self, return_data):
        if return_data != 'False' and return_data != 'false' and return_data:
            if return_data[-1] == ' ':
                device_address_list = return_data[:-1].split(' ')
            else:
                device_address_list = return_data.split(' ')
            # 更新EEPROM设备IIC地址列表
            self.eeprom_device_address_combobox.clear()
            self.eeprom_device_address_combobox.addItems(device_address_list)
            if 'A0' in device_address_list:  # 自动选择A0为默认地址
                self.eeprom_device_address_combobox.setCurrentIndex(device_address_list.index('A0'))
            # 更新508A设备IIC地址列表
            self.atecc508a_device_address_combobox.clear()
            self.atecc508a_device_address_combobox.addItems(device_address_list)
            if 'D0' in device_address_list:  # 自动选择D0或C2为默认地址
                self.atecc508a_device_address_combobox.setCurrentIndex(device_address_list.index('D0'))
            elif 'C2' in device_address_list:
                self.atecc508a_device_address_combobox.setCurrentIndex(device_address_list.index('C2'))
            # 输出数据
            self.log_signal.emit('[%s] ' % datetime.now(), 'grey')
            self.log_signal.emit('IIC Device: %s\n\n' % return_data, 'green')
        elif return_data == '':
            self.eeprom_device_address_combobox.clear()
            self.atecc508a_device_address_combobox.clear()
            self.log_signal.emit('[%s] ' % datetime.now(), 'grey')
            self.log_signal.emit('No IIC Device\n\n', 'red')
        else:
            self.eeprom_device_address_combobox.clear()
            self.atecc508a_device_address_combobox.clear()
            self.log_signal.emit('[%s] ' % datetime.now(), 'grey')
            self.log_signal.emit('IIC Device Scan False\n\n', 'red')

    def eeprom_data_read(self):
        if self.eeprom_device_address_combobox.currentText() and self.eeprom_memory_address_input.text() and \
                self.eeprom_read_data_length_input.text() and self.eeprom_memory_length_input.text():  # 检查参数输入
            parameter = ''
            for i, j, k, l in zip(self.eeprom_device_address_combobox.currentText().split(' '),
                                  self.eeprom_memory_address_input.text().split(' '),
                                  self.eeprom_read_data_length_input.text().split(' '),
                                  self.eeprom_memory_length_input.text().split(' ')):
                parameter += '{0},{1},{2},{3},'.format(i, j, k, l)
            self.log_signal.emit('[%s] ' % datetime.now(), 'grey')
            self.log_signal.emit('EEPROM Data Reading\n', 'black')
            self.serial_command_signal.emit('eeprom_data_read', parameter, True)

    def eeprom_data_update(self, return_data):
        all_data = return_data.split(',')
        if all_data[4] != 'False' and all_data[4] != 'false' and all_data[4]:
            if all_data[5] == 'update':
                data_dict['EEPROM'] = all_data[4][:-1].replace(' ', '\n')
            elif all_data[5] == 'append':
                data_dict['EEPROM'] += ('\n' + all_data[4][:-1].replace(' ', '\n'))

            self.log_signal.emit('[%s] ' % datetime.now(), 'grey')
            self.log_signal.emit('EEPROM Data(Address: 0x{0}, Memory: 0x{1}, Length: {2}): \n'.
                                 format(all_data[0], all_data[1], all_data[2]), 'blue')
            self.log_signal.emit('[%s] ' % datetime.now(), 'grey')
            self.log_signal.emit('%s\n\n' % all_data[4], 'green')
        else:
            self.log_signal.emit('[%s] ' % datetime.now(), 'grey')
            self.log_signal.emit('EEPROM Reading False\n\n', 'red')
        self.data_select_list()  # 刷新数据显示列表

    def atecc508a_data_read(self):
        device_addr = self.atecc508a_device_address_combobox.currentText()
        if device_addr:
            parameter = device_addr + ','
            slot_data_length = [
                self.slot_0_length.text(), self.slot_1_length.text(), self.slot_2_length.text(),
                self.slot_3_length.text(), self.slot_4_length.text(), self.slot_5_length.text(),
                self.slot_6_length.text(), self.slot_7_length.text(), self.slot_8_length.text(),
                self.slot_9_length.text(), self.slot_10_length.text(), self.slot_11_length.text(),
                self.slot_12_length.text(), self.slot_13_length.text(), self.slot_14_length.text(),
                self.slot_15_length.text()]

            for i in range(len(slot_data_length)):
                parameter += (slot_data_length[i] + ',')

            self.log_signal.emit('[%s] ' % datetime.now(), 'grey')
            self.log_signal.emit('Atecc508a Data Reading\n', 'black')
            self.serial_command_signal.emit('atecc508a_data_read', parameter, True)

    def atecc508a_data_update(self, return_data):
        slot_data = return_data.split(',')
        if slot_data[1] != 'False' and slot_data[1] != 'false' and slot_data[1]:
            data_dict['Slot ' + slot_data[0]] = slot_data[1][:-1].replace(' ', '\n')

            self.log_signal.emit('[%s] ' % datetime.now(), 'grey')
            self.log_signal.emit('Atecc508a Slot %s Data: \n' % slot_data[0], 'blue')
            self.log_signal.emit('[%s] ' % datetime.now(), 'grey')
            self.log_signal.emit('%s\n\n' % slot_data[1], 'green')
        else:
            self.log_signal.emit('[%s] ' % datetime.now(), 'grey')
            self.log_signal.emit('Atecc508a Slot %s Reading False\n\n' % slot_data[0], 'red')
        self.data_select_list()  # 刷新数据显示列表

    def bq_manufacture_id_read(self):
        """
        BQ ID读取线程
        :return: None
        """
        self.log_signal.emit('[%s] ' % datetime.now(), 'grey')
        self.log_signal.emit('BQ Manufacture ID Reading\n', 'black')
        self.serial_command_signal.emit('bq_id_read', '', True)

    def bq_manufacture_id_update(self, return_data):
        """
        BQ ID读取 (仅为读取SN27541 ID的功能)
        :return: None
        """
        if return_data != 'False' and return_data != 'false' and return_data:
            self.manufacture_id_display.setText(return_data.replace(' ', ''))  # ID显示
            self.log_signal.emit('[%s] ' % datetime.now(), 'grey')
            self.log_signal.emit('Manufacture ID: %s\n\n' % return_data.replace(' ', ''), 'green')
        else:
            self.manufacture_id_display.clear()
            self.log_signal.emit('[%s] ' % datetime.now(), 'grey')
            self.log_signal.emit('Manufacture ID Reading False\n\n', 'red')

    def serial_rx_data(self):
        """
        串口助手信息打印
        :return: None
        """
        stop_time = 0
        time_flag = True
        while True:
            data = self.serial_device.esp32_serial()
            if data:
                if time_flag:
                    # 在一定时间内未打印，下一次打印会输出时间信息，方便读取
                    self.rx_signal.emit("\n\n[%s] RECV\n" % datetime.now(), 'grey')
                time_flag = False  # 取消时间标志
                self.rx_signal.emit(data, 'green')
                stop_time = time.time()  # 刷新最后打印时间
            elif data == False:
                if self.serial_device.connect_status:
                    # 当数据读取错误时，串口自动断开连接，并输出错误信息
                    self.log_signal.emit('Serial disconnects with error. [%s]\n\n' % datetime.now(), 'red')
                    self.serial_device_disconnect()
                break
            elif time.time() - stop_time > 0.5:
                # 在一定时间内未打印信息，时间信息标志置位
                time_flag = True

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
        self.serial_device.write_data(data_buffer)

    def data_select_list(self):
        """
        数据显示列表刷新
        :return: None
        """
        self.data_select_combobox.clear()  # 清空列表
        # 检查字典中的数据，有数据就添加到列表中
        for i in data_dict:
            if data_dict[i]:
                self.data_select_combobox.addItem(i)
        self.data_select_combobox.update()
        # 如有数据，默认选择第一个数据显示；没有就清空数据显示表格
        if self.data_select_combobox.count() > 0:
            self.data_select_combobox.setCurrentIndex(0)
        else:
            self.data_table.clear()

    def data_table_display(self):
        """
        显示所选的数据到表格中
        :return: None
        """
        self.data_table.clear()  # 清空表格
        if self.data_select_combobox.currentText():
            data = data_dict[self.data_select_combobox.currentText()].split('\n')
            self.data_table.setColumnCount(2)  # 设定列数
            self.data_table.setRowCount(len(data))  # 设定行数
            self.data_table.setHorizontalHeaderLabels(['Address', 'Data'])  # 设定列的标题
            for i in range(len(data)):
                self.data_table.setItem(i, 0, QTableWidgetItem('{0:0X}'.format(i)))  # 添加数据的16进制地址
                self.data_table.setItem(i, 1, QTableWidgetItem(data[i]))  # 添加数据

    def data_copy(self):
        """
        将所选的数据复制到剪切板
        :return: None
        """
        clipboard = QApplication.clipboard()
        if self.data_select_combobox.currentText():
            clipboard.setText(data_dict[self.data_select_combobox.currentText()])

    def data_clear(self):
        """
        清空数据
        :return: None
        """
        # 清空数据字典信息
        for i in data_dict:
            data_dict[i] = ''
        self.log_data_display.clear()  # 清空log显示数据
        self.data_select_combobox.clear()  # 清空数据选择列表
        self.data_table.clear()  # 清空数据表格
        self.manufacture_id_display.clear()  # 清空BQ ID数据

    def expect_folder_select(self):
        """
        导出文件夹选择
        :return: None
        """
        file_path = QFileDialog.getExistingDirectory(self, '选择保存文件夹')
        # 自动在文件夹目录最后添加 "/"
        if file_path and file_path[-1] != '/':
            self.folder_select_input.setText(file_path + '/')

    def data_expect_thread(self):
        """
        文件导出线程
        :return: None
        """
        if not self.read_status:
            self.read_status = True
            log_thread = threading.Thread(target=self.data_expect)
            log_thread.setDaemon(True)
            log_thread.start()
        else:
            QMessageBox(QMessageBox.Warning, 'Warning', '请等待数据导出完成').exec()

    def data_expect(self):
        """
        数据导出，EEPROM和508A导出为HEX数据，导出log日记数据
        :return:
        """
        self.log_signal.emit('[%s] ' % datetime.now(), 'grey')
        self.log_signal.emit('Expect Data\n', 'black')
        # 自动在文件夹目录最后添加 "/"
        if self.folder_select_input.text()[-1] != '/':
            self.folder_select_input.setText(self.folder_select_input.text() + '/')
        # HEX长度设置为16位
        make_hex = data_process.MakeHex(16)
        # 导出各个EEPROM和508A Slot数据
        for i in data_dict:
            if data_dict[i]:
                make_hex.main(file_path=(self.folder_select_input.text()), file_name=(i + '.hex'), data=data_dict[i])
                self.log_signal.emit('[%s] ' % datetime.now(), 'grey')
                self.log_signal.emit('Expect %s Hex Data Success\n' % i, 'green')
        # 导出整个508A数据
        atecc508a_data = ''
        for i in range(16):
            if data_dict['Slot ' + str(i)]:
                atecc508a_data += data_dict['Slot ' + str(i)]  # 将所有Slot数据拼合在一起
        if atecc508a_data != '':
            make_hex.main(file_path=(self.folder_select_input.text()), file_name=('508A.hex'), data=atecc508a_data)
            self.log_signal.emit('[%s] ' % datetime.now(), 'grey')
            self.log_signal.emit('Expect ATECC508A Hex Data Success\n', 'green')

        if self.manufacture_id_display.text():
            data_process.file_write(self.folder_select_input.text() + 'id.txt', [self.manufacture_id_display.text()])
            self.log_signal.emit('[%s] ' % datetime.now(), 'grey')
            self.log_signal.emit('Expect BQ ID Success\n', 'green')

        self.log_signal.emit('[%s] ' % datetime.now(), 'grey')
        self.log_signal.emit('Expect Data Done\n\n', 'black')
        time.sleep(0.01)
        # 导出log日记数据
        data_process.file_write(self.folder_select_input.text() + 'log.txt',
                                self.log_data_display.toPlainText().split('\n'))
        self.read_status = False
