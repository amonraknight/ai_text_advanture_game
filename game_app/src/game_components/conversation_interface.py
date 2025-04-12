import pygame
from src.game_components.button import Button
import src.contants as CST
from src.game_components.game_status import GameStatus
from src.common_util.utils import get_font


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


def end_conversation(game_status: GameStatus):
    game_status.set_current_state("location")
    return game_status

def dummy_action(game_satus: GameStatus):
    pass