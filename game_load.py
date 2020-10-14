from game_objects import *
import pygame


# function loading and reloading player object, and empty enemies array, called every time game is started
def game_reload():
    player = Player(WIDTH // 2, HEIGHT * 0.75, 0, 0, PLAYER_COOLDOWN, PLAYER_SIZE, 3)
    enemies = []
    return player, enemies


# loading best scores from file
def scoreboard_load():
    scoreboard = {}
    file = open("score.txt", "r")
    scores = file.read()
    for i in scores.split('/'):
        if i != "":
            scoreboard[i.split(" ")[0]] = {
                "name": i.split(" ")[1],
                "score": int(i.split(" ")[2])
            }
    file.close()
    return scoreboard


# preloading some variables
pygame.font.init()
player, enemies = game_reload()
font = pygame.font.SysFont("Arial", 30)
win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

