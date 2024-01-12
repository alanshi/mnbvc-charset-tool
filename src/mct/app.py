"""
for mnbvc-charset develop
"""
import subprocess
import os
import ast

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT


EXT_ENCODING = [
    'utf-8',
    "gb2312",  # 简体中文 (GB2312)
    'gbk',  # 简体中文 (GB2312)
    'gb18030',  # 简体中文 (GB2312)
    'big5',  # 繁体中文 (BIG5)
    'shift_jis',  # 日本語 (cp932)
    'euc_kr',  # 한국어 (cp949)
    'ascii',  # ASCII
    'utf_16',  # Unicode (UTF-16)
    'cp1252',  # Western European (Windows)
]

# copy text to clipboard


def set_clipboard_data(data):

    if os.name == 'nt':
        command = 'echo | set /p nul=' + data.strip() + '| clip'
        os.system(command)
    else:
        p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        p.stdin.write(data)
        p.stdin.close()
        p.communicate()


def fix_data(s: str) -> list:
    """
    :param s: text
    :return: list
    """

    result = []

    for item in EXT_ENCODING:
        guess_text = s.encode(encoding=item, errors='replace')
        for target in EXT_ENCODING:
            if item == target:
                continue
            fixed_text = guess_text.decode(encoding=target, errors='replace')
            dic = {"origin": s, "guess": fixed_text,
                   "from": item, "to": target}
            result.append(dic)
    return result


class MNBVCCharsetTool(toga.App):

    def encode_button_handler(self, widget):
        origin_value = self.convert_source_str_input.value
        encode_value = origin_value.encode(
            encoding=self.convert_encode_selection.value, errors='replace')
        self.convert_source_str_input.value = encode_value

    def decode_button_handler(self, widget):
        origin_value = self.convert_source_str_input.value
        # convert origin_value bytes str to bytes
        origin_value = ast.literal_eval(origin_value)
        decode_value = origin_value.decode(
            encoding=self.convert_encode_selection.value, errors='replace')
        self.convert_source_str_input.value = decode_value

    def guess_button_handler(self, widget):
        origin_value = self.guess_str_input.value
        return_values = fix_data(origin_value)
        table_data = [
            (
                item.get("from"), item.get("to"), item.get("guess")
            )
            for item in return_values
        ]
        self.guess_result_table.data = table_data

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        cricket_icon = "icons/cricket-72.png"
        guess_encode_main_box = toga.Box()
        guess_encode_box = toga.Box()
        covert_encode_main_box = toga.Box()
        covert_encode_box = toga.Box()
        container = toga.OptionContainer(
            content=[
                toga.OptionItem(
                    "编码猜测",
                    guess_encode_main_box,
                ),
                toga.OptionItem(
                    "编码互转",
                    covert_encode_main_box
                )
            ]
        )
        # guess encode
        self.guess_str_input = toga.TextInput(
            placeholder="请输入需要编码猜测的原始文本",
            style=Pack(flex=1, height=30)
        )
        guess_button = toga.Button(
            "编码猜测",
            on_press=self.guess_button_handler,
            style=Pack(height=30)
        )
        self.guess_result_table = toga.Table(
            headings=["原始编码", "转换编码", "结果"],
            style=Pack(height=480, width=750, padding_top="5")
        )
        # code convert
        self.convert_source_str_input = toga.TextInput(
            placeholder="请输入需要转换的文本",
            style=Pack(flex=1,height=30)
        )
        self.convert_encode_selection = toga.Selection(
            items=EXT_ENCODING,
            style=Pack(height=30)
        )
        self.convert_encode_button = toga.Button(
            "Encode",
            on_press=self.encode_button_handler,
            style=Pack(height=30)
        )
        self.convert_decode_button = toga.Button(
            "Decode",
            on_press=self.decode_button_handler,
            style=Pack(height=30)
        )
        covert_encode_box.add(self.convert_source_str_input)
        covert_encode_box.add(self.convert_encode_selection)
        covert_encode_box.add(self.convert_encode_button)
        covert_encode_box.add(self.convert_decode_button)
        covert_encode_main_box.add(covert_encode_box)
        covert_encode_main_box.style.update(direction=COLUMN, padding=20)


        guess_encode_box.add(self.guess_str_input)
        guess_encode_box.add(guess_button)
        guess_encode_main_box.add(guess_encode_box)
        guess_encode_main_box.add(self.guess_result_table)
        guess_encode_main_box.style.update(direction=COLUMN, padding=20)

        self.main_window = toga.MainWindow(
            title=self.formal_name,
            size=(800, 600),
            position=(400, 300)
        )

        self.main_window.content = container
        self.main_window.show()

def main():
    return MNBVCCharsetTool()
