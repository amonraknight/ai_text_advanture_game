from src.game_components.button import Button
import src.contants as CST
from src.game_components.game_status import GameStatus


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


def leave_location(game_status: GameStatus):
    game_status.set_current_state("main")
    return game_status
