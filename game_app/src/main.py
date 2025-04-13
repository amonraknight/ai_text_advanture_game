import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit


class CharacterSelectorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("荣国府和宁国府人物选择器")
        self.setGeometry(100, 100, 400, 300)

        # 创建中心窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 第一部分：地点按钮
        location_layout = QHBoxLayout()

        self.rongguofu_button = QPushButton("荣国府")
        self.rongguofu_button.clicked.connect(lambda: self.show_characters("荣国府"))

        self.ningguofu_button = QPushButton("宁国府")
        self.ningguofu_button.clicked.connect(lambda: self.show_characters("宁国府"))

        location_layout.addWidget(self.rongguofu_button)
        location_layout.addWidget(self.ningguofu_button)
        main_layout.addLayout(location_layout)

        # 第二部分：人物按钮
        self.characters_widget = QWidget()
        self.characters_layout = QHBoxLayout(self.characters_widget)

        # 定义每个地点的人物按钮
        self.character_buttons = {
            "荣国府": {
                "贾宝玉": QPushButton("贾宝玉"),
                "贾母": QPushButton("贾母")
            },
            "宁国府": {
                "贾珍": QPushButton("贾珍"),
                "贾蓉": QPushButton("贾蓉")
            }
        }

        # 将所有人物按钮添加到布局中并初始隐藏
        for location_buttons in self.character_buttons.values():
            for btn in location_buttons.values():
                btn.hide()
                btn.clicked.connect(self.handle_character_selection)
                self.characters_layout.addWidget(btn)

        main_layout.addWidget(self.characters_widget)

        # 第三部分：文本框和确认按钮
        self.text_edit = QLineEdit()
        self.text_edit.setPlaceholderText("在此输入文本")

        confirm_buttons_layout = QHBoxLayout()

        self.confirm_button1 = QPushButton("确认")
        self.confirm_button2 = QPushButton("确认")

        self.confirm_button1.clicked.connect(lambda: self.handle_confirmation(1))
        self.confirm_button2.clicked.connect(lambda: self.handle_confirmation(2))

        confirm_buttons_layout.addWidget(self.confirm_button1)
        confirm_buttons_layout.addWidget(self.confirm_button2)

        # 文本部分布局：文本框在上，确认按钮在下
        text_part_layout = QVBoxLayout()
        text_part_layout.addWidget(self.text_edit)
        text_part_layout.addLayout(confirm_buttons_layout)

        main_layout.addLayout(text_part_layout)

        self.current_location = None  # 记录当前选择的地点

    def show_characters(self, location):
        """显示对应地点的人物按钮"""
        # 隐藏所有人物按钮
        for location_buttons in self.character_buttons.values():
            for btn in location_buttons.values():
                btn.hide()

        # 显示当前地点的人物按钮
        self.current_location = location
        for btn in self.character_buttons[location].values():
            btn.show()

    def handle_character_selection(self):
        """处理人物按钮选择事件"""
        selected_character = self.sender().text()
        self.text_edit.setText(selected_character)

    def handle_confirmation(self, button_number):
        """处理确认按钮点击事件"""
        text = self.text_edit.text()
        print(f"确认按钮 {button_number} 被点击，输入的文本是: {text}")


def main():
    app = QApplication(sys.argv)
    window = CharacterSelectorWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
