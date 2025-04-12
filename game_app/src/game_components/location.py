import src.contants as CST
from src.game_components.button import Button
from src.game_components.game_status import GameStatus


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


def start_conversation(game_status: GameStatus):
    game_status.set_current_state("conversation")
    return game_status
