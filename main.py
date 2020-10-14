from random import randint
from front_screen import *
from lose_screen import *


# printing lives and score data on screen
def data():
    global win, player
    text = font.render("Lives: " + str(player.lives), 1, WHITE)
    win.blit(text, (10, 10))
    text = font.render("Score: " + str(player.score), 1, WHITE)
    win.blit(text, (WIDTH - text.get_width() - 10, 10))


# refreshing screen on every clock tick (reloading background, player, enemies, all bullets and data)
def refresh():
    global win, player, enemies
    win.blit(bcg, (0, 0))
    player.draw(win)
    for bullet in player.bullets:
        bullet.draw(win, playerbullet)
    for enemy in enemies:
        enemy.draw(win)
        for bullet in enemy.bullets:
            bullet.draw(win, enemybullet)
    data()


# function defining spawning new enemies, moving them, and making them shot
def enemy_move():
    global player, enemies
    # new enemy is spawned on every tick randomly
    if randint(0, ENEMY_SPAWN) == 4:
        enemies.insert(0, (Enemy(randint(15, WIDTH - 45), 0, 0, ENEMY_VELOCITY, ENEMY_COOLDOWN, ENEMY_SIZE, 1)))
    for enemy in enemies:
        enemy.y += enemy.velocity_y
        if enemy.y > HEIGHT:
            player.lives -= 1
            get_shot()
        if enemy.cooldown == 0:
            enemy.shot()
        enemy.bullet_move()
        enemy.cooldown -= 1


# huge loop checking, if two objects collide with each other - each object have hitbox defined as rectangle, with center
# in center of object's graphic reflection - this way one function can check collisions between every two objects
def collision(obj1, obj2):
    for i in range(int(obj1.x - obj1.size[0] // 2), int(obj1.x + obj1.size[0] // 2)):
        for j in range(int(obj1.y - obj1.size[1] // 2), int(obj1.y + obj1.size[1] // 2)):
            if i in range(int(obj2.x - obj2.size[0] // 2), int(obj2.x + obj2.size[0] // 2)) and \
                    j in range(int(obj2.y - obj2.size[1] // 2), int(obj2.y + obj2.size[1] // 2)):
                # every object in game have lives (player - 3, rest - 1). When obj.lives == 0, object is deleted
                obj1.lives -= 1
                obj2.lives -= 1
                return True
    return False


# function that check collisions in every case we need (player - enemy, player - enemy bullet, enemy - player bullet)
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


# function checking, if any object that is not player should be deleted (obj.lives == 0)
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


# if player lose life, all enemies gets removed to give player some time to rest
def get_shot():
    global enemies
    for enemy in reversed(enemies):
        enemies.remove(enemy)


# when player lose, this function is called to check if his score should be written to scoreboard and in case it should,
# function changes scoreboard
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


# saving scoreboard to file
def save_scoreboard(scoreboard):
    file = open("score.txt", "w")
    for i in scoreboard:
        file.write(str(i) + ' ' + scoreboard[i]["name"] + ' ' + str(scoreboard[i]["score"]) + '/')


# this function is a core of whole game - calling it start whole space journey
def game():
    global player, enemies
    alive = True
    while alive:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
        # if any (w, a, s, d) key is pressed, ship velocity change
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x > 0:
            player.velocity_x = -PLAYER_VELOCITY
        if keys[pygame.K_s] and player.y < HEIGHT - player.size[1]:
            player.velocity_y = PLAYER_VELOCITY
        if keys[pygame.K_d] and player.x < WIDTH - player.size[0]:
            player.velocity_x = PLAYER_VELOCITY
        if keys[pygame.K_w] and player.y > 0:
            player.velocity_y = -PLAYER_VELOCITY
        # if player have no cooldown on shot, hitting spacebar spawns deadly laser
        if keys[pygame.K_SPACE] and player.cooldown == 0:
            player.shot()
        # with every tick cooldown is going down by one (eg. player.cooldown = 10 means,
        # that you have to wait 10 frames to shot)
        if player.cooldown > 0:
            player.cooldown -= 1
        # ship moves with predefined velocity
        player.x += player.velocity_x
        player.y += player.velocity_y
        # velocity get reset, in case player let go button
        player.velocity_x = 0
        player.velocity_y = 0
        # calling functions
        player.bullet_move()
        enemy_move()
        check_collisions()
        delete_objects()
        refresh()
        # checking if player still have lives
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