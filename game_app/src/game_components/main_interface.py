import pygame
import sys
from src.game_components.location import Location
from src.game_components.button import Button
import src.contants as CST
from src.game_components.game_status import GameStatus


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


def exit_game(game_satus: GameStatus):
    pygame.quit()
    sys.exit()
