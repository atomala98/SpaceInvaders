from game_load import *
import pygame
from string import ascii_uppercase

buttons = [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_i,
           pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_m, pygame.K_n, pygame.K_o,pygame.K_p, pygame.K_q,
           pygame.K_r, pygame.K_s, pygame.K_t, pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x, pygame.K_y, pygame.K_z]

BUTTON_SIZE = (150, 75)
start_button = Button(BUTTON_SIZE, WIDTH // 2, HEIGHT // 2, 'START')
score_button = Button(BUTTON_SIZE, WIDTH // 2, HEIGHT // 2 + BUTTON_SIZE[1] + 5, 'SCORE')
quit_button = Button(BUTTON_SIZE, WIDTH // 2, HEIGHT // 2 + 2 * (BUTTON_SIZE[1] + 5), 'QUIT')
menu_button = Button(BUTTON_SIZE, WIDTH // 2, HEIGHT // 2 + BUTTON_SIZE[1] + 5, 'MENU')
reset_button = Button(BUTTON_SIZE, WIDTH // 2, HEIGHT // 2 + 2 * (BUTTON_SIZE[1] + 5), 'RESET')


def front_screen():
    win.blit(bcg, (0, 0))
    start_text = font.render("WELCOME TO SPACE INVADERS", 1, WHITE)
    win.blit(start_text, ((WIDTH - start_text.get_width()) // 2, (HEIGHT - start_text.get_height()) // 4))
    start_button.draw(win, RED, font)
    score_button.draw(win, RED, font)
    quit_button.draw(win, RED, font)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if pos[0] in range(start_button.x - start_button.size[0]//2, start_button.x + start_button.size[0]//2) \
                    and pos[1] in range(start_button.y - start_button.size[1]//2, start_button.y + start_button.size[1]//2):
                return "START"
            if pos[0] in range(score_button.x - score_button.size[0]//2, score_button.x + score_button.size[0]//2) \
                    and pos[1] in range(score_button.y - score_button.size[1]//2, score_button.y + score_button.size[1]//2):
                return "SCORE"
            if pos[0] in range(quit_button.x - quit_button.size[0]//2, quit_button.x + quit_button.size[0]//2) \
                    and pos[1] in range(quit_button.y - quit_button.size[1]//2, quit_button.y + quit_button.size[1]//2):
                return "QUIT"


def choose_name():
    playername = ''
    choosename = font.render("CHOOSE NAME:", 1, WHITE)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
            if event.type == pygame.KEYDOWN:
                for i in range(len(buttons)):
                    if event.key == buttons[i]:
                        playername = playername + ascii_uppercase[i]
                    if event.key == pygame.K_BACKSPACE:
                        playername = ''
                    if event.key == pygame.K_RETURN:
                        return playername
        win.blit(bcg, (0, 0))
        name = font.render(playername, 1, WHITE)
        win.blit(choosename, ((WIDTH - choosename.get_width()) // 2, HEIGHT // 6))
        win.blit(name, ((WIDTH - name.get_width()) // 2, HEIGHT // 4))
        pygame.display.update()
    return playername


def load_score():
    win.blit(bcg, (0, 0))
    menu_button.draw(win, RED, font)
    reset_button.draw(win, RED, font)
    scoreboard = scoreboard_load()
    for i in scoreboard:
        temp_id = font.render(i + ". ", 1, WHITE)
        temp_name = font.render(scoreboard[i]["name"], 1, WHITE)
        temp_score = font.render(str(scoreboard[i]["score"]), 1, WHITE)
        win.blit(temp_id, (WIDTH // 8, (HEIGHT * int(i) // 12)))
        win.blit(temp_name, (WIDTH // 2 - temp_name.get_width()//2, (HEIGHT * int(i) // 12)))
        win.blit(temp_score, (WIDTH * 0.8, (HEIGHT * int(i) // 12)))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if pos[0] in range(menu_button.x - menu_button.size[0] // 2, menu_button.x + menu_button.size[0] // 2) \
                    and pos[1] in range(menu_button.y - menu_button.size[1] // 2, menu_button.y + menu_button.size[1] // 2):
                return "MENU"
            if pos[0] in range(reset_button.x - reset_button.size[0] // 2, reset_button.x + reset_button.size[0] // 2) \
                    and pos[1] in range(reset_button.y - reset_button.size[1] // 2,
                                        reset_button.y + reset_button.size[1] // 2):
                return "RESET"


def reset():
    file = open("score.txt", "w")
    for i in range(1, 6):
        file.write(str(i) + " ------- 0/")


