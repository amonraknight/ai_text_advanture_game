# -*- coding: utf-8 -*-

import pygame
import sys
from game_components.game_status import GameStatus
from game_components.main_interface import MainInterface
from game_components.location_interface import LocationInterface
from game_components.conversation_interface import ConversationInterface


class Game:
    def __init__(self, width=800, height=600):
        # 初始化Pygame
        pygame.init()

        # 设置窗口大小
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("文字冒险游戏")

        # 初始化游戏状态
        self.main_interface = MainInterface(self.screen)
        self.location_interface = LocationInterface(self.screen)
        self.conversation_interface = ConversationInterface(self.screen)
        self.game_status = GameStatus()

    def play(self):
        # 游戏主循环
        try:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.game_status.get_current_state() == "main":
                            for button in self.main_interface.buttons:
                                button.handle_click(self.game_status)
                        elif self.game_status.get_current_state() == "location":
                            for button in self.location_interface.buttons:
                                button.handle_click(self.game_status)
                            for button in self.game_status.get_current_location().get_characters_buttons():
                                button.handle_click(self.game_status)
                        elif self.game_status.get_current_state() == "conversation":
                            for button in self.conversation_interface.buttons:
                                button.handle_click(self.game_status)
                    elif event.type == pygame.KEYDOWN and self.game_status.get_current_state() == "conversation":
                        try:
                            self.conversation_interface.handle_input(event)
                        except Exception as e:
                            print(f"处理输入时出错: {e}")

                if self.game_status.get_current_state() == "main":
                    self.main_interface.draw()
                elif self.game_status.get_current_state() == "location":
                    self.location_interface.draw(self.game_status.get_current_location())
                    # 重新绘制当前地点的人物按钮（因为Button类的draw方法在每次调用时需要重新计算鼠标位置）
                    for button in self.game_status.get_current_location().get_characters_buttons():
                        button.draw()
                elif self.game_status.get_current_state() == "conversation":
                    self.conversation_interface.draw()

                pygame.display.update()
        except Exception as e:
            print(f"游戏运行出错: {e}")
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    game = Game()
    game.play()
