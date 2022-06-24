import sys
import threading
import time
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtCore
import serial_function
import qt_tab1, qt_tab2
from homepage import ui_mainwindow

'''class MyComboBox(QtWidgets.QComboBox):
    clicked = QtCore.pyqtSignal()  # 创建一个信号

    def showPopup(self):  # 重写showPopup函数
        self.clicked.emit()  # 发送信号        
        super(MyComboBox, self).showPopup()   # 调用父类的showPopup()'''
#Abs comment

class MyMainForm(QMainWindow, ui_mainwindow.Ui_MainWindow):
    log_signal = QtCore.pyqtSignal(str, str)  # log显示数据信号，第一个str为显示内容，第二个str为字体颜色
    rx_signal = QtCore.pyqtSignal(str, str)  # 串口助手显示数据信号，第一个str为显示内容，第二个str为字体颜色
    serial_command_signal = QtCore.pyqtSignal(str, str, int)
    serial_status_signal = QtCore.pyqtSignal(bool)
    serial_return_data_signal = QtCore.pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)

        self.serial_command = {'connect': self.serial_device_connect,
                               'disconnect': self.serial_device_disconnect,
                               'serial_device_scan': self.serial_device_scan,
                               'iic_device_scan': self.iic_device_scan,
                               'bq_id_read': self.bq_manufacture_id_read,
                               'eeprom_data_read': self.eeprom_data_read,
                               'atecc508a_data_read': self.atecc508a_data_read,
                               'serial_send_data': self.serial_send_data}

        self.serial_device = serial_function.SerialFunction()  # 实例化串口对象

        self.serial_on_use = False

        self.setupUi(self)
        self.setWindowTitle("VPD Toolbox V1.0")
        self.tab1 = qt_tab1.QTTab1(self, self.window_tab_1)
        self.tab2 = qt_tab2.QTTab2(self, self.window_tab_2)

        self.log_signal.connect(self.tab1.log_signal)
        self.rx_signal.connect(self.tab2.rx_signal)

        self.tab1.serial_command_signal.connect(self.serial_command_signal)
        self.tab2.serial_command_signal.connect(self.serial_command_signal)
        self.serial_command_signal.connect(self.serial_command_thread)
        self.serial_status_signal.connect(self.tab1.serial_status_signal)
        self.serial_status_signal.connect(self.tab2.serial_status_signal)

        self.serial_return_data_signal.connect(self.tab1.serial_return_data_signal)
        self.serial_return_data_signal.connect(self.tab2.serial_return_data_signal)

        self.rx_data_buffer = ''

    def serial_command_thread(self, command, parameter, set_thread):
        if not self.serial_on_use:
            self.serial_on_use = True
            if set_thread:
                log_thread = threading.Thread(target=self.serial_command[command], args=(parameter,), daemon=True)
                log_thread.start()
            else:
                self.serial_command[command](parameter)
        else:
            QMessageBox(QMessageBox.Warning, 'Warning', '请等待串口操作完成').exec()

    def serial_device_connect(self, parameter):
        """
        串口设备连接
        """
        connect_parameter = parameter.split(',')
        connect_com = connect_parameter[0]
        connect_bps = connect_parameter[1]
        if self.serial_device.serial_connect(connect_com, connect_bps):
            rx_thread = threading.Thread(target=self.serial_rx_data)
            rx_thread.setDaemon(True)
            rx_thread.start()
            self.serial_status_signal.emit(True)
        else:
            # 连接失败警报
            QMessageBox(QMessageBox.Warning, 'Warning', '连接失败，请检查串口是否被占用。').exec()
        self.serial_on_use = False

    def serial_device_disconnect(self, parameter=None):
        """
        串口连接断开
        """
        self.serial_device.serial_disconnect()
        self.serial_status_signal.emit(False)
        self.serial_on_use = False

    def serial_device_scan(self, parameter=None):
        """
        扫描电脑上的串口设备
        """
        return_device_list = ''
        serial_device_list = serial_function.SerialFunction.serial_list()
        for i in serial_device_list:
            return_device_list += i[0] + ' #' + i[1] + ','
        self.serial_return_data_signal.emit('serial_device', return_device_list[:-1])
        self.serial_on_use = False

    def serial_send_data(self, parameter):
        self.serial_device.write_data(parameter)
        self.serial_on_use = False

    def iic_device_scan(self, parameter=None):
        iic_device_list = self.serial_device.device_address_scan()
        self.serial_return_data_signal.emit('iic_device', str(iic_device_list))
        self.serial_on_use = False

    def bq_manufacture_id_read(self, parameter=None):
        bq_id = self.serial_device.eeprom_data(0xaa >> 1, 0x6a, 8, 8)
        self.serial_return_data_signal.emit('bq_manufacture_id', str(bq_id))
        self.serial_on_use = False

    def eeprom_data_read(self, parameter):
        eeprom_parameter = parameter.split(',')
        for i in range(int(len(eeprom_parameter) / 4)):
            data = self.serial_device.eeprom_data(int(eeprom_parameter[i * 4], 16) >> 1,
                                                  int(eeprom_parameter[i * 4 + 1], 16),
                                                  int(eeprom_parameter[i * 4 + 2]), int(eeprom_parameter[i * 4 + 3]))
            return_data = '{0},{1},{2},{3},{4},'.format(eeprom_parameter[i * 4], eeprom_parameter[i * 4 + 1],
                                                        eeprom_parameter[i * 4 + 2], eeprom_parameter[i * 4 + 3], data)
            if i >= 1:
                return_data += 'append'
            else:
                return_data += 'update'
            self.serial_return_data_signal.emit('eeprom_data', return_data)
        self.serial_on_use = False

    def atecc508a_data_read(self, parameter):
        atecc508a_parameter = parameter.split(',')
        device_addr = atecc508a_parameter[0]
        slot_data_length = atecc508a_parameter[1:]
        for i in range(len(slot_data_length)):
            if str(slot_data_length[i]).isdigit():
                data = self.serial_device.atecc508a_data(int(device_addr, 16) >> 1, i, slot_data_length[i])
                return_data = '%d,%s' % (i, data)
                self.serial_return_data_signal.emit('atecc508a_data', return_data)
        self.serial_on_use = False

    def serial_rx_data(self):
        """
        串口助手信息打印
        :return: None
        """
        stop_time = 0
        time_flag = True

        data_buffer = ''
        while True:
            data = self.serial_device.esp32_serial()
            if data:
                data_buffer += data

            elif data == False:
                if self.serial_device.connect_status:
                    # 当数据读取错误时，串口自动断开连接，并输出错误信息
                    self.log_signal.emit('[%s] ' % datetime.now(), 'grey')
                    self.log_signal.emit('Serial disconnects with error.\n\n', 'red')
                    self.serial_device_disconnect()
                break
            elif time.time() - stop_time > 0.5:
                # 在一定时间内未打印信息，时间信息标志置位
                time_flag = True

            if time.time()-stop_time >= 0.05 and data_buffer != '':
                if time_flag:
                    # 在一定时间内未打印，下一次打印会输出时间信息，方便读取
                    self.rx_signal.emit("\n\n[%s] RECV\n" % datetime.now(), 'grey')
                time_flag = False  # 取消时间标志
                self.rx_signal.emit(data_buffer, 'green')
                stop_time = time.time()  # 刷新最后打印时间
                data_buffer = ''  # 清空数据缓存


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())
