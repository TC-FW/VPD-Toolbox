import time
import serial
import serial.tools.list_ports


class SerialFunction:
    """ ESP32 MicroPython 固件串口驱动"""
    def __init__(self):
        self.serial = serial.Serial()
        self.connect_status = 0  # 连接状态标志位
        self.data = ''  # 获取的数据缓存
        self.catch_data_flag = 0  # 获取数据标志位
        self.data_length = 0  # 获取数据长度

    def serial_connect(self, port, bps):
        """
        串口设备连接
        :param port: 串口编号
        :param bps: 波特率
        :return: Bool
        """
        if port and self.connect_status == 0:
            try:
                self.serial = serial.Serial(port, bps)
                self.connect_status = 1
                return True
            except:
                return False

    def serial_disconnect(self):
        """
        断开串口设备连接
        :return: None
        """
        if self.connect_status == 1:
            self.connect_status = 0
            self.serial.close()

    def serial_open_status(self):
        """
        串口状态查询
        :return: Bool
        """
        if self.serial.isOpen():
            return True
        else:
            return False

    def esp32_serial(self):
        """
        串口数据获取
        :return: String or False
        """
        data_buffer = ''
        if self.connect_status:
            try:
                if self.serial.in_waiting:
                    data_buffer = self.serial.read_all().decode('utf-8')
            except:
                return ''
        else:
            return False
        # 当获取数据标志位置位时，数据会保存到self.data中
        if self.catch_data_flag:
            self.data += data_buffer
        return data_buffer

    def catch_data(self):
        """
        从串口数据获取有用信息
        :return: String or False
        """
        self.data = ''
        self.catch_data_flag = 1
        data_length_catch = 0
        data_length_catch_count = 0
        start_time = time.time()
        error_false_count = 0
        while True:
            if (time.time() - start_time) / 1 > data_length_catch_count*1:
                data_length_catch = len(self.data)
                data_length_catch_count += 1

            time.sleep(0.1)

            if 'start' in self.data and 'done' in self.data:
                self.catch_data_flag = 0
                break
            elif len(self.data) != data_length_catch:
                error_false_count = 0
            elif (time.time() - start_time) > (self.data_length * 16/100000)+1 and len(self.data) == data_length_catch:
                error_false_count += 1
                if error_false_count >= 3:
                    return False

        data = self.data.split('\r\n')
        return data[data.index('start') + 1]

    def device_address_scan(self):
        self.serial.flushInput()
        self.serial.write('device_scan_command()\r\n'.encode("utf-8"))
        data = self.catch_data()
        return data

    def eeprom_data(self, device_addr, memory_addr, data_length, memory_addr_size):
        self.serial.flushInput()
        self.data_length = int(data_length)
        self.serial.write('read_eeprom_command(device_addr={0}, mem_addr={1}, data_length={2}, addr_size={3})\r\n'.
                          format(device_addr, memory_addr, data_length, memory_addr_size).encode("utf-8"))
        data = self.catch_data()
        return data

    def atecc508a_data(self, device_addr, slot_num, data_length):
        self.serial.flushInput()
        self.data_length = int(data_length)
        self.serial.write('read_508a_command(device_addr={0}, slot_num={1}, data_lenth={2})\r\n'.
                          format(device_addr, slot_num, data_length).encode("utf-8"))
        data = self.catch_data()
        return data

    def write_data(self, write_buffer):
        self.serial.flushInput()
        self.serial.write(write_buffer.encode("utf-8"))

    @staticmethod
    def serial_list():
        port_list = serial.tools.list_ports.comports()
        return port_list
