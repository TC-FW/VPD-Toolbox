import os
import re


def file_write(write_path, lines):
    write_hex = open(write_path, 'w')
    for i in range(len(lines)):
        write_hex.write(lines[i])
        if i != len(lines) - 1:
            write_hex.write('\n')

    write_hex.close()


class MakeHex:
    def __init__(self, length):
        self.length = length
        pass

    def text_2_hex(self, data):
        """
        将数据转为标准HEX格式
        :param data: 待处理数据
        :return: hex格式数据
        """
        data = data.replace('\n', '')
        process_data = re.findall(r'.{%s}' % (2 * self.length), data)
        if len(process_data) * 2 * self.length < len(data):
            process_data.append(data[len(process_data) * self.length * 2:])
        hex_data = []
        extend_address_count = 0
        for i in range(len(process_data)):
            if int(i * self.length / 0x10000) > extend_address_count:
                hex_data.append(":020000021000EC")
                extend_address_count += 1
            hex_data.append("{0}{1:02X}{2:04X}{3}{4}".format(":", int(len(process_data[i]) / 2),
                                                             (i * self.length % 0x10000), '00', process_data[i]))
            hex_data[-1] = hex_data[-1] + self.checksum(hex_data[-1])

        hex_data.append(":00000001FF")

        return hex_data

    @staticmethod
    def checksum(line):
        """
        计算HEX检验值
        :param line: hex line data
        :return: checksum value
        """
        i = 1
        sum = 0
        while i < len(line) and line[i] != '\n':
            sum += int(line[i:i + 2], 16)
            i += 2
        checksum = "{:02X}".format((256 - sum % 256) % 256).upper()

        return checksum

    # 运行程序
    def main(self, file_path, file_name, data):
        new_lines = self.text_2_hex(data)

        if not os.path.exists(file_path):
            os.mkdir(file_path)

        file_write("{0}{1}".format(file_path, file_name), new_lines)
