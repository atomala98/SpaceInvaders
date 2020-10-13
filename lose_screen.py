from game_load import *
import pygame

BUTTON_SIZE = (150, 75)
restart_button = Button(BUTTON_SIZE, WIDTH // 2, HEIGHT // 2, 'MENU')
quit_button = Button(BUTTON_SIZE, WIDTH // 2, HEIGHT // 2 + BUTTON_SIZE[1] + 5, 'QUIT')


def lose_screen():
    win.blit(bcg, (0, 0))
    lose_text = font.render("You lost!", 1, WHITE)
    win.blit(lose_text, ((WIDTH - lose_text.get_width()) // 2, (HEIGHT - lose_text.get_height()) // 4))
    restart_button.draw(win, RED, font)
    quit_button.draw(win, RED, font)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if pos[0] in range(restart_button.x - restart_button.size[0], restart_button.x + restart_button.size[0]) \
                    and pos[1] in range(restart_button.y - restart_button.size[1],
                                        restart_button.y + restart_button.size[1]):
                return "RESTART"
            if pos[0] in range(quit_button.x - quit_button.size[0]//2, quit_button.x + quit_button.size[0]//2) \
                    and pos[1] in range(quit_button.y - quit_button.size[1]//2, quit_button.y + quit_button.size[1]//2):
                return "QUIT"
