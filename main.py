from random import randint
from front_screen import *
from lose_screen import *


def data():
    global win, player
    text = font.render("Lives: " + str(player.lives), 1, WHITE)
    win.blit(text, (10, 10))
    text = font.render("Score: " + str(player.score), 1, WHITE)
    win.blit(text, (WIDTH - text.get_width() - 10, 10))


def refresh():
    global win, player, enemies
    win.blit(bcg, (0, 0))
    player.draw(win)
    for bullet in player.bullets:
        bullet.draw(win, playerbullet)
    data()
    for enemy in enemies:
        enemy.draw(win)
        for bullet in enemy.bullets:
            bullet.draw(win, enemybullet)


def enemy_move():
    global player, enemies
    if randint(0, ENEMY_SPAWN) == 4:
        enemies.insert(0, (Enemy(randint(15, WIDTH - 45), 0, ENEMY_VELOCITY, 0, ENEMY_COOLDOWN, ENEMY_SIZE, 1)))
    for enemy in enemies:
        enemy.y += enemy.velocity_x
        if enemy.y > HEIGHT:
            player.lives -= 1
            get_shot()
        if enemy.cooldown == 0:
            enemy.shot()
        enemy.bullet_move()
        enemy.cooldown -= 1


def collision(obj1, obj2):
    for i in range(int(obj1.x - obj1.size[0] // 2), int(obj1.x + obj1.size[0] // 2)):
        for j in range(int(obj1.y - obj1.size[1] // 2), int(obj1.y + obj1.size[1] // 2)):
            if i in range(int(obj2.x - obj2.size[0] // 2), int(obj2.x + obj2.size[0] // 2)) and \
                    j in range(int(obj2.y - obj2.size[1] // 2), int(obj2.y + obj2.size[1] // 2)):
                obj1.lives -= 1
                obj2.lives -= 1
                return True
    return False


def check_collisions():
    global player, enemies
    for enemy in enemies:
        if collision(player, enemy):
            get_shot()
        for bullet in enemy.bullets:
            if collision(player, bullet):
                get_shot()
        for bullet in player.bullets:
            if collision(bullet, enemy):
                player.score += 1


def delete_objects():
    global player, enemies
    for enemy in reversed(enemies):
        if enemy.lives <= 0:
            del enemies[enemies.index(enemy)]
        for bullet in enemy.bullets:
            if bullet.lives <= 0:
                del enemy.bullets[enemy.bullets.index(bullet)]
    for bullet in player.bullets:
        if bullet.lives <= 0:
            del player.bullets[player.bullets.index(bullet)]


def get_shot():
    global enemies
    for enemy in reversed(enemies):
        enemies.remove(enemy)


def check_scoreboard():
    scoreboard = scoreboard_load()
    for i in scoreboard:
        if player.score > scoreboard[i]["score"]:
            for j in range(4, int(i) - 1, -1):
                scoreboard[str(j + 1)] = scoreboard[str(j)]
            scoreboard[i] = {
                "name" : player.name,
                "score" : player.score
            }
            break
    save_scoreboard(scoreboard)


def save_scoreboard(scoreboard):
    file = open("score.txt", "w")
    for i in scoreboard:
        file.write(str(i) + ' ' + scoreboard[i]["name"] + ' ' + str(scoreboard[i]["score"]) + '/')


def game():
    global player, enemies
    alive = True
    while alive:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x > 0:
            player.velocity_x = -PLAYER_VELOCITY
        if keys[pygame.K_s] and player.y < HEIGHT - player.size[1]:
            player.velocity_y = PLAYER_VELOCITY
        if keys[pygame.K_d] and player.x < WIDTH - player.size[0]:
            player.velocity_x = PLAYER_VELOCITY
        if keys[pygame.K_w] and player.y > 0:
            player.velocity_y = -PLAYER_VELOCITY
        if keys[pygame.K_SPACE] and player.cooldown == 0:
            player.shot()
        if player.cooldown > 0:
            player.cooldown -= 1
        player.x += player.velocity_x
        player.y += player.velocity_y
        player.velocity_x = 0
        player.velocity_y = 0
        player.bullet_move()
        enemy_move()
        check_collisions()
        delete_objects()
        refresh()
        if player.lives <= 0:
            check_scoreboard()
            alive = False
        pygame.display.update()


def menu():
    global player, enemies
    RUN = True
    while RUN:
        clock.tick(FPS)
        while RUN:
            click = front_screen()
            if click == "START":
                player.name = choose_name()
                game()
                break
            if click == "SCORE":
                while True:
                    click = load_score()
                    if click == "MENU":
                        break
                    if click == "RESET":
                        reset()
            if click == "QUIT":
                RUN = False
        while RUN:
            click = lose_screen()
            if click == "RESTART":
                menu()
                break
            if click == "QUIT":
                RUN = False
    pygame.quit()


menu()