# -*- coding: utf-8 -*-


import pygame
import sys

# 初始化Pygame
pygame.init()

# 设置窗口大小
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("文字冒险游戏")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# 定义字体
FONT = pygame.font.Font('../resources/fonts/SIMLI.TTF', 36)


class Button:
    def __init__(self, text, pos, size, color, highlight_color, action):
        self.text = text
        self.pos = pos
        self.size = size
        self.color = color
        self.highlight_color = highlight_color
        self.action = action
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.highlight_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        text_surface = FONT.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_click(self):
        if self.rect and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.action()


class Location:
    def __init__(self, name, characters):
        self.name = name
        self.characters = characters

    def get_characters_buttons(self):
        buttons = []
        for i, character in enumerate(self.characters):
            y = 100 + i * 50
            buttons.append(Button(character, (WIDTH // 2, y), (200, 50), GRAY, BLACK, self.start_conversation))
        return buttons

    def start_conversation(self):
        global current_state
        current_state = "conversation"


class MainInterface:
    def __init__(self):
        self.locations = [
            Location("大观园", ["贾宝玉", "林黛玉"]),
            Location("宁国府", ["贾母", "王夫人"])
        ]
        self.buttons = [
            Button("大观园", (WIDTH // 2, 150), (200, 50), GRAY, BLACK, self.enter_location),
            Button("宁国府", (WIDTH // 2, 250), (200, 50), GRAY, BLACK, self.enter_location),
            Button("退出游戏", (WIDTH // 2, 350), (200, 50), GRAY, BLACK, self.exit_game)
        ]

    def enter_location(self):
        global current_state, current_location
        mouse_y = pygame.mouse.get_pos()[1]
        if 100 < mouse_y < 150 + 50:  # 大观园按钮区域
            current_location = self.locations[0]
        elif 200 < mouse_y < 250 + 50:  # 宁国府按钮区域
            current_location = self.locations[1]
        current_state = "location"

    def exit_game(self):
        pygame.quit()
        sys.exit()

    def draw(self):
        screen.fill(WHITE)
        for button in self.buttons:
            button.draw()


class LocationInterface:
    def __init__(self):
        self.buttons = [
            Button("离开", (WIDTH // 2, HEIGHT - 50), (200, 50), GRAY, BLACK, self.leave_location)
        ]

    def leave_location(self):
        global current_state
        current_state = "main"

    def draw(self):
        screen.fill(WHITE)
        for button in self.buttons:
            button.draw()
        for button in current_location.get_characters_buttons():
            button.draw()


class ConversationInterface:
    def __init__(self):
        self.text_input = ""
        self.input_box = pygame.Rect(100, HEIGHT - 100, WIDTH - 200, 50)
        self.buttons = [
            Button("结束对话", (WIDTH // 2, HEIGHT - 50), (200, 50), GRAY, BLACK, self.end_conversation)
        ]

    def end_conversation(self):
        global current_state
        current_state = "location"

    def draw(self):
        screen.fill(WHITE)
        for button in self.buttons:
            button.draw()
        pygame.draw.rect(screen, BLACK, self.input_box, 2)
        text_surface = FONT.render(self.text_input, True, BLACK)
        screen.blit(text_surface, (self.input_box.x + 5, self.input_box.y + 5))

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text_input = self.text_input[:-1]
            elif event.key == pygame.K_RETURN:
                self.text_input = ""
            else:
                self.text_input += event.unicode


# 初始化游戏状态
current_state = "main"
main_interface = MainInterface()
location_interface = LocationInterface()
conversation_interface = ConversationInterface()
current_location = None

# 游戏主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == "main":
                for button in main_interface.buttons:
                    button.handle_click()
            elif current_state == "location":
                for button in location_interface.buttons:
                    button.handle_click()
                for button in current_location.get_characters_buttons():
                    button.handle_click()
            elif current_state == "conversation":
                for button in conversation_interface.buttons:
                    button.handle_click()
        elif event.type == pygame.KEYDOWN and current_state == "conversation":
            conversation_interface.handle_input(event)

    if current_state == "main":
        main_interface.draw()
    elif current_state == "location":
        location_interface.draw()
        # 重新绘制当前地点的人物按钮（因为Button类的draw方法在每次调用时需要重新计算鼠标位置）
        for button in current_location.get_characters_buttons():
            button.draw()
    elif current_state == "conversation":
        conversation_interface.draw()

    pygame.display.update()
