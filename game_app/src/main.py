# -*- coding: utf-8 -*-

import pygame
import sys
import contants as CST
from common_util.utils import get_font
from game_components.game_status import GameStatus


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


class Button:
    def __init__(self, text, pos, size, color, highlight_color, action, screen):
        self.text = text
        self.pos = pos
        self.size = size
        self.color = color
        self.highlight_color = highlight_color
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.action = action
        self.screen = screen

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.highlight_color, self.rect)
        else:
            pygame.draw.rect(self.screen, self.color, self.rect)
        text_surface = get_font(CST.FONT_LISHU, 36).render(self.text, True, CST.BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def handle_click(self, status: GameStatus):
        if self.rect and self.rect.collidepoint(pygame.mouse.get_pos()):
            return self.action(status)
        else:
            return status


class Location:
    def __init__(self, name, characters, screen):
        self.name = name
        self.characters = characters
        self.screen = screen

    def get_characters_buttons(self):
        buttons = []
        for i, character in enumerate(self.characters):
            y = 100 + i * 50
            buttons.append(
                Button(character, (CST.WIDTH // 2, y), (200, 50), CST.GRAY, CST.BLACK, start_conversation,
                       self.screen))
        return buttons


class MainInterface:
    def __init__(self, screen):
        self.screen = screen
        self.locations = [
            Location("大观园", ["贾宝玉", "林黛玉"], self.screen),
            Location("宁国府", ["贾母", "王夫人"], self.screen)
        ]

        self.buttons = [
            Button("大观园", (CST.WIDTH // 2, 150), (200, 50), CST.GRAY, CST.BLACK, self.enter_location, self.screen),
            Button("宁国府", (CST.WIDTH // 2, 250), (200, 50), CST.GRAY, CST.BLACK, self.enter_location, self.screen),
            Button("退出游戏", (CST.WIDTH // 2, 350), (200, 50), CST.GRAY, CST.BLACK, exit_game, self.screen)
        ]

    def enter_location(self, game_satus: GameStatus):
        mouse_y = pygame.mouse.get_pos()[1]
        if 100 < mouse_y < 150 + 50:  # 大观园按钮区域
            game_satus.set_current_location(self.locations[0])
        elif 200 < mouse_y < 250 + 50:  # 宁国府按钮区域
            game_satus.set_current_location(self.locations[1])
        game_satus.set_current_state("location")
        return game_satus

    def draw(self):
        self.screen.fill(CST.WHITE)
        for button in self.buttons:
            button.draw()


class LocationInterface:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = [
            Button("离开", (CST.WIDTH // 2, CST.HEIGHT - 50), (200, 50), CST.GRAY, CST.BLACK, leave_location,
                   self.screen)
        ]

    def draw(self, current_location):
        self.screen.fill(CST.WHITE)
        for button in self.buttons:
            button.draw()
        for button in current_location.get_characters_buttons():
            button.draw()


class ConversationInterface:
    def __init__(self, screen):
        self.screen = screen
        self.text_input = ""
        self.input_box = pygame.Rect(100, CST.HEIGHT - 100, CST.WIDTH - 200, 50)
        self.buttons = [
            Button("结束对话", (CST.WIDTH // 2, CST.HEIGHT - 50), (200, 50), CST.GRAY, CST.BLACK,
                   end_conversation, self.screen),
            Button("确认", (CST.WIDTH - 150, CST.HEIGHT - 50), (100, 50), CST.GRAY, CST.BLACK, dummy_action,
                   self.screen)
        ]
        self.response = "嗯"

    def draw(self):
        self.screen.fill(CST.WHITE)
        for button in self.buttons:
            button.draw()
        pygame.draw.rect(self.screen, CST.BLACK, self.input_box, 2)
        text_surface = get_font(CST.FONT_LISHU, 36).render(self.text_input, True, CST.BLACK)
        self.screen.blit(text_surface, (self.input_box.x + 5, self.input_box.y + 5))
        # 显示响应
        response_surface = get_font(CST.FONT_LISHU, 36).render(self.response, True, CST.BLACK)
        self.screen.blit(response_surface, (100, CST.HEIGHT - 160))

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text_input = self.text_input[:-1]
            elif event.key == pygame.K_RETURN:
                self.text_input = ""
            else:
                self.text_input += event.unicode


def leave_location(game_status: GameStatus):
    game_status.set_current_state("main")
    return game_status


def start_conversation(game_status: GameStatus):
    game_status.set_current_state("conversation")
    return game_status


def end_conversation(game_status: GameStatus):
    game_status.set_current_state("location")
    return game_status


def exit_game(game_satus: GameStatus):
    pygame.quit()
    sys.exit()


def dummy_action(game_satus: GameStatus):
    pass


if __name__ == '__main__':
    game = Game()
    game.play()
