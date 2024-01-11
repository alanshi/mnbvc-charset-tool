"""
for mnbvc-charset develop
"""
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

    def button_handler(self, widget):
        origin_value = self.origin_str_input.value
        return_values = fix_data(origin_value)
        table_data = [
            (
                item.get("from"), item.get("to"), item.get("guess")
            )
            for item in return_values
        ]
        self.table.data = table_data

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box()
        input_box = toga.Box()
        self.origin_str_input = toga.TextInput(placeholder="请输入原始文本", style=Pack(flex=1, height=30))
        guess_button = toga.Button("猜测编码", on_press=self.button_handler, style=Pack(height=30))
        #self.table = toga.DetailedList(style=Pack(height=600, padding_top="20"))
        self.table = toga.Table(headings=["原始编码", "转换编码", "结果"], style=Pack(height=600, padding_top="20"))
        input_box.add(self.origin_str_input)
        input_box.add(guess_button)
        main_box.add(input_box)
        main_box.add(self.table)

        main_box.style.update(direction=COLUMN, padding=20)
        self.main_window = toga.MainWindow(title=self.formal_name, size=(800, 600), position=(400, 300))
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return MNBVCCharsetTool()
