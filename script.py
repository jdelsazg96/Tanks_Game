import pygame
import time
import random
import math

pygame.init()


display_width = 800
display_height = 600

red = (255, 0, 0)
light_red = (255, 100, 100)
brown = (128, 64, 0)
lightbrown = (164, 106, 0)
black = (0, 0, 0)
grey = (100, 100, 100)
dark_grey = (65, 65, 65)
lightgrey = (136, 136, 136)
white = (255, 255, 255)
yellow = (200, 200, 0)
light_yellow = (255, 255, 0)
green = (34, 177, 76)
light_green = (0, 255, 0)
wheat=(0,217,0)
blue = (4, 162, 221)
light_blue = (0, 255, 255)

smallfont = pygame.font.SysFont("arial", 25)
medfont = pygame.font.SysFont("italic", 50)
largefont = pygame.font.SysFont("impact", 85)
vsmallfont = pygame.font.SysFont("arial", 25)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('TANKS!')
clock = pygame.time.Clock()

earth_background = pygame.image.load('paisaje00.png')
moon_background = pygame.image.load('paisaje01.png')
tankpic = pygame.image.load('tank.png')
barrellpic = pygame.image.load('cañon.png')
barrellpicsim = pygame.image.load('cañonsim.png')
explosion = pygame.image.load('explosion.png')
explosion2 = pygame.image.load('explosion2.png')
intro_pic = pygame.image.load('portada_tanks.png')


def ground(thickness, color):
    pygame.draw.rect(gameDisplay, color, [0, display_height - thickness, display_width, thickness])


def barrier(x, width, height, color):
    pygame.draw.rect(gameDisplay, color, [x, display_height - 40 - height, width, height])


def tank(x, y):
    gameDisplay.blit(tankpic, (x, y))


def tank2(x, y):
    gameDisplay.blit(tankpic, (x, y))


def barrell(x, y, angle):
    # gameDisplay.blit(barrellpic, (x, y))
    barrelrot = pygame.transform.rotate(barrellpic, angle)
    gameDisplay.blit(barrelrot, (x, y))


def barrel22(x, y, angle):
    # gameDisplay.blit(barrellpic, (x, y))
    barrelrot = pygame.transform.rotate(barrellpicsim, angle)
    gameDisplay.blit(barrelrot, (x, y))


def barrel2(x, y):
    gameDisplay.blit(barrellpicsim, (x, y))


def barrell_angle(angle):
    font = pygame.font.SysFont(None, 25)
    text = font.render('Angle: ' + str(angle), True, black)
    gameDisplay.blit(text, (10, 25))


def shoot_power(power):
    font = pygame.font.SysFont(None, 25)
    text = font.render('Power: ' + str(power), True, black)
    gameDisplay.blit(text, (110, 25))


def shoot_power_bar(power):
    pygame.draw.rect(gameDisplay, black, [210, 10, 110, 40])
    pygame.draw.rect(gameDisplay, red, [215, 15, power, 30])


def textobjects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = textobjects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)


def message_to_screen(msg, color, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (int(display_width / 2), int(display_height / 2) + y_displace)
    gameDisplay.blit(textSurf, textRect)


def button(text, x, y, width, height, inactive_color, active_color, action=None,size=" "):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x, y, width, height))
        if click[0] == 1 and action != None:
            if action == 'quit':
                pygame.quit()
                quit()
            if action == 'controls':
                game_controls()
            if action == 'sec_screen':
                sec_screen()
            if action == 'main':
                game_intro()
            if action == "EARTH":
                game_loop_earth()
            if action == "MOON":
                game_loop_moon()
            if action == 'multiplayer':
                game_loop_earth2()
            if action == 'controls2':
                game_controls2()
    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x, y, width, height))

    text_to_button(text, black, x, y, width, height)



def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size="vsmall"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = ((buttonx + (buttonwidth / 2)), buttony + (buttonheight / 2))
    gameDisplay.blit(textSurf, textRect)


def text_objects(text, color, size="small"):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)
    if size == "vsmall":
        textSurface = vsmallfont.render(text, True, color)

    return textSurface, textSurface.get_rect()


def score(angle, power, tank_initx, tank2_initx, tank_inity, tank_width, ground_thickness, barrier_x, barrier_width,
          barrier_height, hits, misses):
    barrell_length = 60

    time = 0

    speed_y = ((power*3) * math.sin(angle * math.pi / 180))
    speed_x = (power*3) * math.cos(angle * math.pi / 180)

    ball_initx = int(round(tank_initx + tank_width / 2 + barrell_length * math.cos(angle * math.pi / 180)))
    ball_inity = int(round(tank_inity + 13 - barrell_length * math.sin(angle * (math.pi / 180))))

    # while ball_initx < display_width and ball_inity < display_height - ground_thickness:

    gameExit = False
    hit_hit = False
    miss_miss = False

    while not gameExit:

        pygame.draw.circle(gameDisplay, black, (ball_initx, ball_inity), 5)
        gameDisplay.blit(explosion, (ball_initx - 30, ball_inity - 30))

        ball_x = round(ball_initx + speed_x * time)
        ball_y = round(ball_inity - speed_y * time - ((-50 * (time)**2)/2))

        pygame.draw.circle(gameDisplay, black, (ball_x, ball_y), 5)

        time += 0.05

        if ball_x > barrier_x and ball_x < barrier_x + barrier_width and \
                ball_y > display_height - barrier_height - ground_thickness:
            misses += 1
            miss()
            miss_miss = True
            break

        elif ball_x > tank2_initx and ball_y > tank_inity and \
                ball_x < tank2_initx + tank_width and ball_y < display_height - ground_thickness:
            hits += 1
            hit(tank2_initx, tank_inity)
            hit_hit = True
            break

        elif ball_x > display_width or ball_y > display_height - ground_thickness:
            misses += 1
            miss()
            miss_miss = True
            break

        pygame.display.update()
        clock.tick(120)

    return misses, hits, miss_miss, hit_hit


def score_moon(angle, power, tank_initx, tank2_initx, tank_inity, tank_width, ground_thickness, barrier_x, barrier_width,
          barrier_height, hits, misses):
    barrell_length = 60

    time = 0

    speed_y = ((power*3) * math.sin(angle * math.pi / 180))
    speed_x = (power*3) * math.cos(angle * math.pi / 180)

    ball_initx = int(round(tank_initx + tank_width / 2 + barrell_length * math.cos(angle * math.pi / 180)))
    ball_inity = int(round(tank_inity + 13 - barrell_length * math.sin(angle * (math.pi / 180))))

    # while ball_initx < display_width and ball_inity < display_height - ground_thickness:

    gameExit = False
    hit_hit = False
    miss_miss = False

    while not gameExit:

        pygame.draw.circle(gameDisplay, black, (ball_initx, ball_inity), 5)
        gameDisplay.blit(explosion, (ball_initx - 30, ball_inity - 30))

        ball_x = round(ball_initx + speed_x * time)
        ball_y = round(ball_inity - speed_y * time - ((-20 * (time)**2)/2))

        pygame.draw.circle(gameDisplay, black, (ball_x, ball_y), 5)

        time += 0.05

        if ball_x > barrier_x and ball_x < barrier_x + barrier_width and \
                ball_y > display_height - barrier_height - ground_thickness:
            misses += 1
            miss()
            miss_miss = True
            break

        elif ball_x > tank2_initx and ball_y > tank_inity and \
                ball_x < tank2_initx + tank_width and ball_y < display_height - ground_thickness:
            hits += 1
            hit(tank2_initx, tank_inity)
            hit_hit = True
            break

        elif ball_x > display_width or ball_y > display_height - ground_thickness:
            misses += 1
            miss()
            miss_miss = True
            break

        pygame.display.update()
        clock.tick(120)

    return misses, hits, miss_miss, hit_hit


def score1(angle, power, tank_initx, tank2_initx, tank_inity, tank_width, ground_thickness, barrier_x, barrier_width,
          barrier_height, hits1, hits2):
    barrell_length = 60

    time = 0

    hits2 = hits2
    hits1 = hits1

    speed_y = ((power*3) * math.sin(angle * math.pi / 180))
    speed_x = (power*3) * math.cos(angle * math.pi / 180)

    ball_initx = int(round(tank_initx + tank_width / 2 + barrell_length * math.cos(angle * math.pi / 180)))
    ball_inity = int(round(tank_inity + 13 - barrell_length * math.sin(angle * (math.pi / 180))))

    # while ball_initx < display_width and ball_inity < display_height - ground_thickness:

    gameExit = False

    while not gameExit:

        pygame.draw.circle(gameDisplay, black, (ball_initx, ball_inity), 5)
        gameDisplay.blit(explosion, (ball_initx - 30, ball_inity - 30))

        ball_x = round(ball_initx + speed_x * time)
        ball_y = round(ball_inity - speed_y * time - ((-50 * (time)**2)/2))

        pygame.draw.circle(gameDisplay, black, (ball_x, ball_y), 5)

        time += 0.05

        if ball_x > barrier_x and ball_x < barrier_x + barrier_width and \
                ball_y > display_height - barrier_height - ground_thickness:
            miss()
            break

        elif ball_x > tank2_initx and ball_y > tank_inity and \
                ball_x < tank2_initx + tank_width and ball_y < display_height - ground_thickness:
            hits1 += 1
            hit(tank2_initx, tank_inity)
            break

        elif ball_x > display_width or ball_y > display_height - ground_thickness:
            miss()
            break

        pygame.display.update()
        clock.tick(120)

    return hits1, hits2


def score2(angle, power, tank_initx, tank2_initx, tank_inity, tank_width, ground_thickness, barrier_x, barrier_width,
          barrier_height, hits1, hits2):
    barrell_length = 60

    time = 0

    hits2 = hits2
    hits1 = hits1

    speed_y = ((power*3) * math.sin(angle * math.pi / 180))
    speed_x = (power*3) * math.cos(angle * math.pi / 180)

    ball_initx = int(round(tank_initx + tank_width / 2 - barrell_length * math.cos(-angle * math.pi / 180)))
    ball_inity = int(round(tank_inity + 13 - barrell_length * math.sin(-angle * (math.pi / 180))))

    # while ball_initx < display_width and ball_inity < display_height - ground_thickness:

    gameExit = False

    while not gameExit:

        pygame.draw.circle(gameDisplay, black, (ball_initx, ball_inity), 5)
        gameDisplay.blit(explosion, (ball_initx - 30, ball_inity - 30))

        ball_x = round(ball_initx - speed_x * time)
        ball_y = round(ball_inity + speed_y * time - ((-50 * (time)**2)/2))

        pygame.draw.circle(gameDisplay, black, (ball_x, ball_y), 5)

        time += 0.05

        if ball_x > barrier_x and ball_x < barrier_x + barrier_width and \
                ball_y > display_height - barrier_height - ground_thickness:
            miss()
            break

        elif ball_x > tank2_initx and ball_y > tank_inity and \
                ball_x < tank2_initx + tank_width and ball_y < display_height - ground_thickness:
            hits2 += 1
            hit(tank2_initx, tank_inity)
            break

        elif ball_x > display_width or ball_y > display_height - ground_thickness:
            miss()
            break

        pygame.display.update()
        clock.tick(120)

    return hits1, hits2


def miss():
    message_display('MISS!')


def hit(x, y):
    gameDisplay.blit(explosion2, (x - 2, y - 15))
    message_display('HIT!')


def game_over(hits):
    gameDisplay.fill(white)
    message_display('GAME OVER!')

    final_score(hits)


def game_over1():
    gameDisplay.fill(white)
    message_display('P1 WINS!')

    game_intro()


def game_over2():
    gameDisplay.fill(white)
    message_display('P2 WINS!')

    game_intro()


def tie():
    gameDisplay.fill(white)
    message_display("IT'S A TIE")

    game_intro()


def final_score(hits):
    gameDisplay.fill(white)
    message_display('Your Score: ' + str(hits))

    game_intro()


def miss_count(misses):
    font = pygame.font.SysFont(None, 25)
    text = font.render('Misses: ' + str(misses), True, black)
    gameDisplay.blit(text, (350, 25))
    misses += 1


def hit_count(hits):
    font = pygame.font.SysFont(None, 25)
    text = font.render('Hits: ' + str(hits), True, black)
    gameDisplay.blit(text, (450, 25))
    hits += 1

def hit_count1(hits1):
    font = pygame.font.SysFont(None, 25)
    text = font.render('Hits P1: ' + str(hits1), True, black)
    gameDisplay.blit(text, (350, 25))
    hits1 += 1


def hit_count2(hits2):
    font = pygame.font.SysFont(None, 25)
    text = font.render('Hits P2: ' + str(hits2), True, black)
    gameDisplay.blit(text, (450, 25))
    hits2 += 1

# def earth_moon():


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        gameDisplay.blit(intro_pic,(0,0))
        message_to_screen("TANKS!", white, -150, size="large")
        message_to_screen("Created by : Javier & Sergio", wheat, 265)
        # message_to_screen("Press C to play, P to pause or Q to quit",black,180)


        button("Arcade", 150, 250, 210, 50, wheat, light_green, action="sec_screen",size="vsmall")
        button("Arcade Controls", 450, 250, 210, 50, wheat, light_yellow, action="controls", size="vsmall")
        button("Multiplayer", 150, 320, 210, 50, wheat, light_green, action="multiplayer", size="vsmall")
        button("Multiplayer Controls", 450, 320, 210, 50, wheat, light_yellow, action="controls2", size="vsmall")
        button("Quit", 300, 450, 210, 50, wheat, red, action="quit", size="vsmall")

        pygame.display.update()

        clock.tick(15)


def game_controls():
    gcont1 = True

    while gcont1:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(black)
        message_to_screen("Arcade Controls", white, -200, size="large")
        message_to_screen("Fire: Spacebar released, Power: Time pressed", wheat, -30)
        message_to_screen("Move Turret: Up and Down arrows", wheat, 15)
        message_to_screen("You have 5 tries for each level!", wheat, 60)
        message_to_screen("Try to pass as many levels as you can!", wheat, 105)

        button("Mode", 150, 500, 100, 50, green, light_green, action="sec_screen")
        button("Main", 350, 500, 100, 50, yellow, light_yellow, action="main")
        button("Quit", 550, 500, 100, 50, light_red, red, action="quit")

        pygame.display.update()

        clock.tick(15)


def game_controls2():
    gcont2 = True

    while gcont2:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(black)
        message_to_screen("Multiplayer Controls", white, -200, size="large")
        message_to_screen("Fire: Spacebar released, Power: Time pressed", wheat, -30)
        message_to_screen("Move Turret: Up and Down arrows", wheat, 15)
        message_to_screen("Each player has 1 shot at each level!", wheat, 60)
        message_to_screen("The first player to reach 5 HITS wins!", wheat, 105)

        button("Main", 250, 500, 100, 50, yellow, light_yellow, action="main")
        button("Quit", 450, 500, 100, 50, light_red, red, action="quit")

        pygame.display.update()

        clock.tick(15)


def sec_screen():
    intro = True


    while intro:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        gameDisplay.blit(intro_pic,(0,0))
        message_to_screen("GAME MODE!", white, -150, size="large")


        button("EARTH", 150, 300, 200, 50, wheat, brown, action="EARTH",size="vsmall")
        button("MOON", 450, 300, 200, 50, wheat, lightgrey, action="MOON", size="vsmall")
        button("Main", 300, 400, 200, 50, yellow, light_yellow, action="main",size="vsmall")

        pygame.display.update()

        clock.tick(15)


def game_loop_earth():

    tank_width = 86
    tank_hight = 60
    ground_thickness = 40
    barrier_width = 80
    barrier_height = random.randrange(90, 400)
    barrier_x = random.randrange(display_width*0.3, display_width*0.7 - barrier_width)
    tank_initx = 10
    tank_inity = display_height - ground_thickness - tank_hight
    tank_changex = 0
    tank2_initx = random.randrange(display_width*0.7 + 10, display_width - tank_width)
    angle = 0
    angle_change = 0
    power = 0
    power_change = 0
    misses = 0
    hits = 0


    gameExit = False

    while not gameExit:

        if misses > 4:
            game_over(hits)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    angle_change += 1
                elif event.key == pygame.K_DOWN:
                    angle_change -= 1
                elif event.key == pygame.K_SPACE:
                    power_change += 2
                elif event.key == pygame.K_LEFT:
                    tank_changex -= 3
                elif event.key == pygame.K_RIGHT:
                    tank_changex += 3

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    angle_change = 0
                elif event.key == pygame.K_SPACE:
                    power_change = 0
                    # shoot(angle, power, tank_initx, tank2_initx tank_inity, tank_width, ground_thickness, barrier_x,
                    # barrier_width, barrier_height, hits, misses):
                    misses, hits, miss_miss, hit_hit = score(angle, power, tank_initx, tank2_initx, tank_inity, tank_width, ground_thickness, barrier_x, barrier_width,
                          barrier_height, hits, misses)
                    # misses, hits = score(angle, power, tank_initx, tank_inity, tank_width, ground_thickness, barrier_x, barrier_width,
                    #       barrier_height, hits, misses)
                    angle = 0
                    power = 0
                    if hit_hit == True:
                        barrier_height = random.randrange(90, 400)
                        barrier_x = random.randrange(display_width * 0.3, display_width * 0.7 - barrier_width)
                        tank2_initx = random.randrange(display_width * 0.7 + 10, display_width - tank_width)
                        misses = 0

                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    tank_changex = 0

        angle += angle_change
        power += power_change
        tank_initx += tank_changex
        barrell_length = 60
        barrell_initx = tank_initx + tank_width / 2 - 5
        barrell_inity = tank_inity + 13 - barrell_length*math.sin(angle*(math.pi/180))

        if angle > 89:
            angle_change = 0
            angle = 90
        if angle < 1:
            angle_change = 0
            angle = 0
        if power > 99:
            power_change = 0
            power = 100
        if tank_initx < 0:
            tank_changex = 0
            tank_initx = 0
        if tank_initx + tank_width/2 + barrell_length > barrier_x:
            tank_changex = 0
            tank_initx = barrier_x - tank_width/2 - barrell_length

        gameDisplay.blit(earth_background, (0, 0))

        pygame.draw.rect(gameDisplay, wheat, [0, 0, 800, 65])

        button("Main", 600, 10, 70, 50, yellow, light_yellow, action="main", size="vsmall")
        button("Mode", 700, 10, 70, 50, blue, light_blue, action="sec_screen", size="vsmall")

        # ground(thickness, color):
        ground(ground_thickness, brown)

        # barrier(x, width, height, color):
        barrier(barrier_x, barrier_width, barrier_height, brown)

        # barrel (x, y, angle):
        barrell(barrell_initx, barrell_inity, angle)
        barrel2(tank2_initx, display_height - ground_thickness - 45)

        # tank(x, y):
        tank(tank_initx, tank_inity)
        tank2(tank2_initx, tank_inity)

        barrell_angle(angle)
        shoot_power(power)
        shoot_power_bar(power)
        hit_count(hits)
        miss_count(misses)


        pygame.display.update()
        clock.tick(60)

def game_loop_moon():

    tank_width = 86
    tank_hight = 60

    ground_thickness = 40

    barrier_width = 80
    barrier_height = random.randrange(90, 400)
    barrier_x = random.randrange(display_width*0.3, display_width*0.7 - barrier_width)

    tank_initx = 10
    tank_inity = display_height - ground_thickness - tank_hight
    tank_changex = 0

    tank2_initx = random.randrange(display_width*0.7 + 10, display_width - tank_width)

    angle = 0
    angle_change = 0

    power = 0
    power_change = 0

    misses = 0
    hits = 0

    gameExit = False
    moon = False

    while not gameExit:

        if misses > 4:
            game_over(hits)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    angle_change += 1
                elif event.key == pygame.K_DOWN:
                    angle_change -= 1
                elif event.key == pygame.K_SPACE:
                    power_change += 2
                elif event.key == pygame.K_LEFT:
                    tank_changex -= 3
                elif event.key == pygame.K_RIGHT:
                    tank_changex += 3

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    angle_change = 0
                elif event.key == pygame.K_SPACE:
                    power_change = 0
                    # shoot(angle, power, tank_initx, tank2_initx tank_inity, tank_width, ground_thickness, barrier_x,
                    # barrier_width, barrier_height, hits, misses):
                    misses, hits, miss_miss, hit_hit = score_moon(angle, power, tank_initx, tank2_initx, tank_inity, tank_width, ground_thickness, barrier_x, barrier_width,
                          barrier_height, hits, misses)
                    # misses, hits = score(angle, power, tank_initx, tank_inity, tank_width, ground_thickness, barrier_x, barrier_width,
                    #       barrier_height, hits, misses)
                    angle = 0
                    power = 0
                    if hit_hit == True:
                        barrier_height = random.randrange(90, 400)
                        barrier_x = random.randrange(display_width * 0.3, display_width * 0.7 - barrier_width)
                        tank2_initx = random.randrange(display_width * 0.7 + 10, display_width - tank_width)
                        misses = 0

                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    tank_changex = 0

        angle += angle_change
        power += power_change
        tank_initx += tank_changex
        barrell_length = 60
        barrell_initx = tank_initx + tank_width / 2 - 5
        barrell_inity = tank_inity + 13 - barrell_length*math.sin(angle*(math.pi/180))

        if angle > 89:
            angle_change = 0
            angle = 90
        if angle < 1:
            angle_change = 0
            angle = 0
        if power > 99:
            power_change = 0
            power = 100
        if tank_initx < 0:
            tank_changex = 0
            tank_initx = 0
        if tank_initx + tank_width/2 + barrell_length > barrier_x:
            tank_changex = 0
            tank_initx = barrier_x - tank_width/2 - barrell_length

        gameDisplay.blit(moon_background, (0, 0))

        pygame.draw.rect(gameDisplay, wheat, [0, 0, 800, 65])

        button("Main", 600, 10, 70, 50, yellow, light_yellow, action="main", size="vsmall")
        button("Mode", 700, 10, 70, 50, blue, light_blue, action="sec_screen", size="vsmall")

        # ground(thickness, color):
        ground(ground_thickness, grey)

        # barrier(x, width, height, color):
        barrier(barrier_x, barrier_width, barrier_height, grey)

        # barrel (x, y, angle):
        barrell(barrell_initx, barrell_inity, angle)
        barrel2(tank2_initx, display_height - ground_thickness - 45)

        # tank(x, y):
        tank(tank_initx, tank_inity)
        tank2(tank2_initx, tank_inity)

        barrell_angle(angle)
        shoot_power(power)
        shoot_power_bar(power)
        hit_count(hits)
        miss_count(misses)


        pygame.display.update()
        clock.tick(60)


def game_loop_earth2():

    tank_width = 86
    tank_hight = 60

    ground_thickness = 40

    barrier_width = 80
    barrier_height = random.randrange(90, 400)
    barrier_x = random.randrange(display_width*0.3, display_width*0.7 - barrier_width)

    tank_initx = 10
    tank_inity = display_height - ground_thickness - tank_hight
    tank_changex = 0

    tank2_initx = display_width - tank_width - 10

    angle = 0
    angle_change = 0

    power = 0
    power_change = 0

    hits1 = 0
    hits2 = 0


    gameExit = False

    while not gameExit:

        # if misses > 4:
        #     game_over(hits)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    angle_change += 1
                elif event.key == pygame.K_DOWN:
                    angle_change -= 1
                elif event.key == pygame.K_SPACE:
                    power_change += 2
                elif event.key == pygame.K_LEFT:
                    tank_changex -= 3
                elif event.key == pygame.K_RIGHT:
                    tank_changex += 3

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    angle_change = 0
                elif event.key == pygame.K_SPACE:
                    power_change = 0
                    # shoot(angle, power, tank_initx, tank2_initx tank_inity, tank_width, ground_thickness, barrier_x,
                    # barrier_width, barrier_height, hits, misses):
                    hits1, hits2 = score1(angle, power, tank_initx, tank2_initx, tank_inity, tank_width, ground_thickness, barrier_x, barrier_width,
                          barrier_height, hits1, hits2)
                    # misses, hits = score(angle, power, tank_initx, tank_inity, tank_width, ground_thickness, barrier_x, barrier_width,
                    #       barrier_height, hits, misses)
                    angle = 0
                    power = 0
                    # game_loop_earth22(tank1_initx, tank1_inity, barrier_height, barrier_x, tank_initx, ):
                    game_loop_earth22(tank_initx, tank_inity, barrier_height, barrier_x, tank2_initx, hits1, hits2)

                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    tank_changex = 0

        angle += angle_change
        power += power_change
        tank_initx += tank_changex
        barrell_length = 60
        barrell_initx = tank_initx + tank_width / 2 - 5
        barrell_inity = tank_inity + 13 - barrell_length*math.sin(angle*(math.pi/180))

        if angle > 89:
            angle_change = 0
            angle = 90
        if angle < 1:
            angle_change = 0
            angle = 0
        if power > 99:
            power_change = 0
            power = 100
        if tank_initx < 0:
            tank_changex = 0
            tank_initx = 0
        if tank_initx + tank_width/2 + barrell_length > barrier_x:
            tank_changex = 0
            tank_initx = barrier_x - tank_width/2 - barrell_length

        gameDisplay.blit(earth_background, (0, 0))

        pygame.draw.rect(gameDisplay, wheat, [0, 0, 800, 65])

        button("Main", 650, 10, 70, 50, yellow, light_yellow, action="main", size="vsmall")


        # ground(thickness, color):
        ground(ground_thickness, brown)

        # barrier(x, width, height, color):
        barrier(barrier_x, barrier_width, barrier_height, brown)

        # barrel (x, y, angle):
        barrell(barrell_initx, barrell_inity, angle)
        barrel2(tank2_initx + tank_width/2 + 5 - barrell_length, display_height - ground_thickness - 45)

        # tank(x, y):
        tank(tank_initx, tank_inity)
        tank2(tank2_initx, tank_inity)

        barrell_angle(angle)
        shoot_power(power)
        shoot_power_bar(power)

        hit_count1(hits1)
        hit_count2(hits2)


        pygame.display.update()
        clock.tick(60)


def game_loop_earth21(tank2_initx, tank2_inity, barrier_height, barrier_x, tank_initx, hits1, hits2):

    tank_width = 86
    tank_hight = 60

    ground_thickness = 40

    barrier_width = 80
    barrier_height = barrier_height
    barrier_x = barrier_x

    tank_initx = tank_initx
    tank_inity = tank2_inity
    tank2_inity = tank2_inity
    tank2_initx = tank2_initx
    tank_changex = 0

    angle = 0
    angle_change = 0

    power = 0
    power_change = 0

    hits1 = hits1
    hits2 = hits2

    gameExit = False

    while not gameExit:

        if hits1 > 4 and hits2 < 5:
            game_over1()
        if hits2 > 4 and hits1 < 5:
            game_over2()
        if hits1 > 4 and hits2 > 4:
            tie()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    angle_change += 1
                elif event.key == pygame.K_DOWN:
                    angle_change -= 1
                elif event.key == pygame.K_SPACE:
                    power_change += 2
                elif event.key == pygame.K_LEFT:
                    tank_changex -= 3
                elif event.key == pygame.K_RIGHT:
                    tank_changex += 3

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    angle_change = 0
                elif event.key == pygame.K_SPACE:
                    power_change = 0
                    # shoot(angle, power, tank_initx, tank2_initx tank_inity, tank_width, ground_thickness, barrier_x,
                    # barrier_width, barrier_height, hits, misses):
                    hits1, hits2 = score1(angle, power, tank_initx, tank2_initx, tank_inity, tank_width, ground_thickness,
                                  barrier_x, barrier_width,barrier_height, hits1, hits2)
                    # score2(angle, power, tank_initx, tank2_initx, tank_inity, tank_width, ground_thickness, barrier_x, barrier_width,
                    #           barrier_height, hits):
                    angle = 0
                    power = 0
                    game_loop_earth22(tank_initx, tank_inity, barrier_height, barrier_x, tank2_initx, hits1, hits2)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    tank_changex = 0

        angle += angle_change
        power += power_change
        tank_initx += tank_changex
        barrell_length = 60
        barrell_initx = tank_initx + tank_width / 2 - 5
        barrell_inity = tank_inity + 13 - barrell_length * math.sin(angle * (math.pi / 180))

        if angle > 89:
            angle_change = 0
            angle = 90
        if angle < 1:
            angle_change = 0
            angle = 0
        if power > 99:
            power_change = 0
            power = 100
        if tank_initx < 0:
            tank_changex = 0
            tank_initx = 0
        if tank_initx + tank_width / 2 + barrell_length > barrier_x:
            tank_changex = 0
            tank_initx = barrier_x - tank_width / 2 - barrell_length

        gameDisplay.blit(earth_background, (0, 0))

        pygame.draw.rect(gameDisplay, wheat, [0, 0, 800, 65])

        button("Main", 650, 10, 70, 50, yellow, light_yellow, action="main", size="vsmall")


        # ground(thickness, color):
        ground(ground_thickness, brown)

        # barrier(x, width, height, color):
        barrier(barrier_x, barrier_width, barrier_height, brown)

        # barrel (x, y, angle):
        barrell(barrell_initx, barrell_inity, angle)
        barrel2(tank2_initx + tank_width / 2 + 5 - barrell_length, display_height - ground_thickness - 45)

        # tank(x, y):
        tank(tank_initx, tank_inity)
        tank2(tank2_initx, tank_inity)

        barrell_angle(angle)
        shoot_power(power)
        shoot_power_bar(power)
        hit_count1(hits1)
        hit_count2(hits2)


        pygame.display.update()
        clock.tick(60)


def game_loop_earth22(tank1_initx, tank1_inity, barrier_height, barrier_x, tank_initx, hits1, hits2):

    tank_width = 86
    tank_hight = 60

    ground_thickness = 40

    barrier_width = 80
    barrier_height = barrier_height
    barrier_x = barrier_x

    tank1_initx = tank1_initx
    tank1_inity = tank1_inity
    tank_inity = tank1_inity
    tank_initx = tank_initx
    tank_changex = 0

    angle = 0
    angle_change = 0

    power = 0
    power_change = 0

    hits1 = hits1
    hits2 = hits2

    gameExit = False

    while not gameExit:

        # if misses > 4:
        #     game_over(hits)
        barrell_length = 60

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    angle_change += 1
                elif event.key == pygame.K_DOWN:
                    angle_change -= 1
                elif event.key == pygame.K_SPACE:
                    power_change += 2
                elif event.key == pygame.K_LEFT:
                    tank_changex -= 3
                elif event.key == pygame.K_RIGHT:
                    tank_changex += 3

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    angle_change = 0
                elif event.key == pygame.K_SPACE:
                    power_change = 0
                    # shoot(angle, power, tank_initx, tank2_initx tank_inity, tank_width, ground_thickness, barrier_x,
                    # barrier_width, barrier_height, hits, misses):
                    hits1, hits2 = score2(angle, power, tank_initx, tank1_initx, tank_inity, tank_width, ground_thickness, barrier_x, barrier_width,
                          barrier_height, hits1, hits2)
                    # score2(angle, power, tank_initx, tank2_initx, tank_inity, tank_width, ground_thickness, barrier_x, barrier_width,
                    #           barrier_height, hits):
                    angle = 0
                    power = 0
                    barrier_height = random.randrange(90, 400)
                    barrier_x = random.randrange(display_width * 0.3, display_width * 0.7 - barrier_width)
                    if tank_initx + tank_width > display_width:
                        tank_changex = 0
                        tank_initx = display_width - tank_width
                    if tank_initx + tank_width / 2 - barrell_length + 5 < barrier_x + barrier_width:
                        tank_changex = 0
                        tank_initx = barrier_x + barrier_width + barrell_length - 5 - tank_width / 2
                    game_loop_earth21(tank_initx, tank1_inity, barrier_height, barrier_x, tank1_initx, hits1, hits2)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    tank_changex = 0

        angle -= angle_change
        power += power_change
        tank_initx += tank_changex
        barrell_length = 60
        barrell_initx = tank_initx + tank_width/2 - barrell_length + 5 + (barrell_length - barrell_length*math.cos((-angle)*(math.pi/180)) - math.sin((-angle)*math.pi/180)*12)
        barrell_inity = tank_inity + 13 - barrell_length*math.sin((-angle)*(math.pi/180))

        if angle < -89:
            angle_change = 0
            angle = -90
        if angle > -1:
            angle_change = 0
            angle = 0
        if power > 99:
            power_change = 0
            power = 100
        if tank_initx + tank_width > display_width:
            tank_changex = 0
            tank_initx = display_width - tank_width
        if tank_initx + tank_width/2 - barrell_length + 5 < barrier_x + barrier_width:
            tank_changex = 0
            tank_initx = barrier_x + barrier_width + barrell_length - 5 - tank_width/2

        gameDisplay.blit(earth_background, (0, 0))

        pygame.draw.rect(gameDisplay, wheat, [0, 0, 800, 65])

        button("Main", 650, 10, 70, 50, yellow, light_yellow, action="main", size="vsmall")


        # ground(thickness, color):
        ground(ground_thickness, brown)

        # barrier(x, width, height, color):
        barrier(barrier_x, barrier_width, barrier_height, brown)

        # barrel (x, y, angle):
        barrel22(barrell_initx, barrell_inity, angle)
        barrell(tank1_initx + tank_width/2 - 5, display_height - ground_thickness - 45, 0)

        # tank(x, y):
        tank(tank1_initx, tank1_inity)
        tank2(tank_initx, tank_inity)

        barrell_angle(-angle)
        shoot_power(power)
        shoot_power_bar(power)
        hit_count1(hits1)
        hit_count2(hits2)


        pygame.display.update()
        clock.tick(60)


game_intro()
# game_loop_earth2()
pygame.quit()
quit()
