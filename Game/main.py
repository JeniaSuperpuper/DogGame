import pygame
import random

clock = pygame.time.Clock()
pygame.init()

screen = pygame.display.set_mode((950, 555))
icon = pygame.image.load('img/icon.png').convert_alpha()
pygame.display.set_icon(icon)

run = True

fireball = pygame.image.load('img/fireball.png').convert_alpha()
fireballs = []

heart = pygame.image.load('img/heart.png').convert_alpha()
heart_in_start = 3
heart_x =  50

kills = 0
score = 0

add_fireball = 0


bg = pygame.image.load('img/bg.jpg').convert()
bg_x = 0

cat = pygame.image.load('img/cat.png').convert_alpha()
cat_in_game = []

bat = pygame.image.load('img/bat.png').convert_alpha()
bat_in_game = []

walk_right = [
    pygame.image.load('img/right/r1.png').convert_alpha(),
    pygame.image.load('img/right/r2.png').convert_alpha(),
    pygame.image.load('img/right/r3.png').convert_alpha(),
    pygame.image.load('img/right/r4.png').convert_alpha(),
]

walk_left = [
    pygame.image.load('img/left/l1.png').convert_alpha(),
    pygame.image.load('img/left/l2.png').convert_alpha(),
    pygame.image.load('img/left/l3.png').convert_alpha(),
    pygame.image.load('img/left/l4.png').convert_alpha(),
]

dog_speed = 8
dog_x = 150
dog_y = 280

is_jump = False
jump_count = 10

fireballs_in_start = 10

cat_timer = pygame.USEREVENT + 1
pygame.time.set_timer(cat_timer, 2000)

label = pygame.font.Font('fonts/main_font.ttf', 40)
lose_label = label.render("You lose!", False, (193, 196, 199))
restart_label = label.render("Play again", False, (193, 196, 199))
restart_label_rect = restart_label.get_rect(topleft=(380, 230))
label_score = label.render(f"Score: {score}", False, (193, 196, 199))
label_fireballs = label.render(f"Fireballs: {fireballs_in_start}", False, (193, 196, 199))

dog_anim_count = 0

gameplay = True



while run:

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 950, 0))

    if gameplay:
        dog_rect = walk_left[0].get_rect(topleft=(dog_x, dog_y))
        score += 0.1
        label_score = label.render(f"Score: {int(score)}", False, (193, 196, 199))
        screen.blit(label_score, (700, 30))
        label_fireballs = label.render(f"Fireballs: {fireballs_in_start}", False, (193, 196, 199))
        screen.blit(label_fireballs, (700, 80))

        heart_x = 30
        if heart_in_start >= 1:
            for i in range(heart_in_start):
                screen.blit(heart, (heart_x, 30))
                heart_x += 70
        else:
            gameplay = False



        if cat_in_game:
            for index, i in enumerate(cat_in_game):
                screen.blit(cat, i)
                i.x -= 10

                if i.x < -10:
                    cat_in_game.pop(index)

                if dog_rect.colliderect(i):
                    heart_in_start -= 1
                    cat_in_game.pop(index)

        if bat_in_game:
            for index, i in enumerate(bat_in_game):
                screen.blit(bat, i)
                i.x -= 20

                if i.x < -10:
                    bat_in_game.pop(index)

                if dog_rect.colliderect(i):
                    heart_in_start -= 1
                    bat_in_game.pop(index)


        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            screen.blit(walk_left[dog_anim_count], (dog_x, dog_y))
        elif keys[pygame.K_p]:
            heart_in_start += 1
        elif keys[pygame.K_o]:
            fireballs_in_start += 1
        else:
            screen.blit(walk_right[dog_anim_count], (dog_x, dog_y))


        if keys[pygame.K_a] and dog_x > 50:
            dog_x -= dog_speed
        elif keys[pygame.K_d] and dog_x < 650:
            dog_x += dog_speed

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -10:
                if jump_count > 0:
                    dog_y -= (jump_count ** 2) / 2
                else:
                    dog_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 10

        if dog_anim_count == 3:
            dog_anim_count = 0
        else:
            dog_anim_count += 1

        bg_x -= 3

        if bg_x <= -950:
            bg_x = 0

        if fireballs:
            for index, i in enumerate(fireballs):
                screen.blit(fireball, (i.x, i.y))
                i.x += 4

                if i.x > 1000:
                    fireballs.pop(index)

                if cat_in_game:
                    for inx, item in enumerate(cat_in_game):
                        if i.colliderect(item):
                            cat_in_game.pop(inx)
                            fireballs.pop(index)
                            kills += 1
                            score += 10

                if bat_in_game:
                    for inx, item in enumerate(bat_in_game):
                        if i.colliderect(item):
                            bat_in_game.pop(inx)
                            fireballs.pop(index)
                            kills += 1
                            score += 10

        if score - add_fireball * 50 > 50:
            add_fireball += 1
            fireballs_in_start += 1



    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (380, 130))
        screen.blit(restart_label, restart_label_rect)
        screen.blit(label_score, (380, 330))



        if restart_label_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            dog_x = 150
            cat_in_game.clear()
            bat_in_game.clear()
            fireballs.clear()
            bg_x = 0
            score = 0
            fireballs_in_start = 10
            heart_in_start = 3


    pygame.display.update()


    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False
            pygame.quit()
        if i.type == cat_timer:
            cat_in_game.append(cat.get_rect(topleft=(1000, 390)))
            if random.randint(1, 3) == 2:
                bat_in_game.append(bat.get_rect(topleft=(1000, 200)))
        if gameplay and i.type == pygame.KEYUP and i.key == pygame.K_w and fireballs_in_start > 0:
            fireballs.append(fireball.get_rect(topleft=(dog_x + 200, dog_y + 100)))
            fireballs_in_start -= 1

    clock.tick(20)

