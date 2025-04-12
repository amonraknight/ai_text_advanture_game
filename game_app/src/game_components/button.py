import pygame
import src.contants as CST
from src.common_util.utils import get_font
from src.game_components.game_status import GameStatus


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
