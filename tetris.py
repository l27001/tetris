#!/usr/bin/python3
import pygame, os
from random import randint
from time import sleep

###
# Сделать:
#   Рекорд очков
#   Таблица лидеров (?)
#   Музыкальное сопровождение (?)
###

FPS = 60
WIN_WIDTH = 300
WIN_HEIGHT = 500
COLORS = [(0, 255, 0),
        (255, 0, 0),
        (0, 255, 255),
        (255, 255, 0),
        (255, 165, 0),
        (0, 0, 255),
        (128, 0, 128)]
FIGURES = [[[(-2, 0), (-1, 0), (0, 0), (1, 0)],[(0, -2), (0, -1), (0, 0), (0, 1)]], # I
               [[(0, -1), (-1, -1), (-1, 0), (0, 0)]], # o
               [[(0, -2), (0, -1), (-1, -1), (-1, 0)],[(1, 0), (0, 0), (0, -1), (-1 ,-1)]], # Z
               [[(0, 1), (0, 0), (-1, 0), (-1, -1)],[(0, -1), (-1, -1), (-1, 0), (-2, 0)]], # S
               [[(0, 0), (1, 0), (-1, 0), (1, 1)], [(0, 0), (0, 1), (0, -1), (1, -1)], [(0, 0), (1, 0), (-1, 0), (-1, -1)], [(0, 0), (0, 1), (0, -1), (-1, 1)]], # L
               [[(1, 0), (0, 0), (-1, 0), (1, -1)], [(-1, -1), (0, -1), (0, 0), (0, 1)], [(0, 0), (1, 0), (-1, 1), (-1, 0)], [(0, -1), (0, 0), (0, 1), (1, 1)]], # J
               [[(0, 0), (0, 1), (0, -1), (-1, 0)], [(0, 0), (0, 1), (1, 0), (-1, 0)], [(0 ,0), (1, 0), (0, 1), (0, -1)], [(0, -1), (0, 0), (-1, 0), (1, 0)]]] # T

pygame.init()
pygame.display.set_caption("Tetris") # заголовок окна
clock = pygame.time.Clock()
sc = pygame.display.set_mode(
    (WIN_WIDTH+200, WIN_HEIGHT))
pygame.font.init()
font1 = pygame.font.Font("CascadiaCode-Regular.ttf", 20)
font2 = pygame.font.Font("CascadiaCode-Regular.ttf", 60)
score = 0
game_over = 0
sounds = {"game_over":pygame.mixer.Sound("sounds/gameover.wav"),
    "stage_clear":pygame.mixer.Sound("sounds/stage-clear.wav")}

r = 25 # размер одного квадрата
W,H = WIN_WIDTH//r, WIN_HEIGHT//r # кол-во квадратов на поле
x = W//2 # середина поля
y = 0
grid = [[0 for i in range(0,W)] for i in range(0,H)]
anim_count, anim_limit, anim_speed, force_anim = 0, 20000, 600, 0

def draw(anim_speed):
    sc.fill((49, 54, 59))
    for h in range(H): # рисуем фигуры
        for w in range(W):
            if(grid[h][w] > 1): # упавшие      
                pygame.draw.rect(sc, COLORS[grid[h][w]-2],
                (w*r, h*r, r, r))
                anim_speed += 3
            elif(grid[h][w] == 1): # падающая
                pygame.draw.rect(sc, COLORS[figure],
                (w*r, h*r, r, r))
            elif(grid[h][w] == -1):
                pygame.draw.rect(sc, (0,0,0),
                (w*r, h*r, r, r))
        ### сетка
    [pygame.draw.rect(sc, (40, 40, 40), i_rect, 1) for i_rect in
    [pygame.Rect(x * r, y * r, r, r) for x in range(W) for y in range(H)]]
    textnext = font1.render('Next figure:', True, (255, 255, 0))
    sc.blit(textnext, (WIN_WIDTH+200//2-textnext.get_width()//2, 140/2.2))
    scoretext = font1.render(f'Score: {score}', True, (0, 255, 0))
    sc.blit(scoretext, (WIN_WIDTH+200//2-textnext.get_width()//2, 140-100))
    for i in FIGURES[nextfigure][0]:
        coord = ((WIN_WIDTH+200//2.1)+i[1]*r, 140+i[0]*r, r, r)
        pygame.draw.rect(sc, COLORS[nextfigure],
                coord)
        pygame.draw.rect(sc, (40, 40, 40),
                coord, 1)
    return anim_speed

def select_new():
    rand = randint(0, len(FIGURES)-1)
    nextrand = randint(0, len(FIGURES)-1)
    return rand

nextfigure = select_new()
figure = select_new()
rotate = 0
game = True

while game == True:
    for i in pygame.event.get():
        if(i.type == pygame.QUIT):
            game = False
        elif(i.type == pygame.KEYDOWN): # нажатие кнопок
            test = 0
            if(i.key == pygame.K_LEFT): # нажатие левой стрелки
                for k in FIGURES[figure][rotate]:
                    if(grid[y+k[0]][x-1+k[1]] > 1 or x-1+k[1] < 0):
                        test = 1
                        break
                if(test == 0):
                    x -= 1
            elif(i.key == pygame.K_RIGHT): # нажатие правой стрелки
                try:
                    for k in FIGURES[figure][rotate]:
                        if(grid[y+k[0]][x+1+k[1]] > 1):
                            test = 1
                            break
                except IndexError:
                    test = 1
                if(test == 0):
                    x += 1
            elif(i.key == pygame.K_UP):
                test = 0
                if(rotate < len(FIGURES[figure])-1):
                    nrotate = rotate + 1
                else:
                    nrotate = 0
                for k in FIGURES[figure][nrotate]:
                    if(y+k[0] > H-1 or y+k[0] < 0 or x+k[1] > W-1 or x+k[1] < 0 or grid[y+k[0]][x+k[1]] > 1):
                        test = 1
                        break
                if(test == 0):
                    rotate = nrotate
            elif(i.key == pygame.K_DOWN):
                force_anim = 1

    if(anim_count > anim_limit):
        anim_count = 0
        test = 0
        for w in range(W): # упала ли фигура на дно
            if(grid[-1][w] == 1):
                test = 1
                break
        try: # проверка упала ли фигура на другую
            for k in FIGURES[figure][rotate]:
                if(grid[y+1+k[0]][x+k[1]] > 1):
                    test = 1
        except IndexError: # ошибка, которая ни на что не влияет
            pass            # игнорируем
        if(test == 0):
            y += 1
        else: # сохранение упавшей фигуры
            # и выбор новой
            for h in range(H):
                for w in range(W):
                    if(grid[h][w] == 1):
                        grid[h][w] = figure+2
            rotate = 0
            figure = nextfigure
            nextfigure = select_new()
            while(figure == nextfigure):
                nextfigure = select_new()
            x = W//2 # Возврат значений в
            y = 0   # исходное сосотояние
            force_anim = 0
            for w in range(W):
                if(grid[0][w] > 1): # если поле заполнено по вертикали завершаем игру
                    game_over = 1
                    break # стоит выводить текст в окне и предлагать начать новую игру
            ### Удаление горизонтальных линий
            del_range = []
            for h in range(H-1, -1, -1):
                cnt = 0
                for w in range(W):
                    if(grid[h][w] > 1):
                        cnt += 1
                    else:
                        break
                if(cnt == W):
                    del_range.append(h)
            score_multiplier = 1
            if(del_range != []):
                sounds['stage_clear'].play()
            for h in list(reversed(del_range)):
                for n in range(W):
                    grid[h][n] = -1
                    draw(anim_speed)
                    pygame.display.update()
                    sleep(.05)
                del(grid[h])
                grid.insert(1, [0 for i in range(W)])
                score += 100*score_multiplier
                score_multiplier += 1
        ###
    if(force_anim == 0):
        anim_count += anim_speed
        anim_speed = 600
    else:
        anim_count += anim_speed*12
    if(y == 0): # вставляем новую фигуру в игровое поле
        for k in FIGURES[figure][rotate]:
            if(k[0] < -y):
                y = -k[0]
        for k in FIGURES[figure][rotate]:
            if(grid[y+k[0]][x+k[1]] == 0):
                grid[y+k[0]][x+k[1]] = 1
    else: # опускаем уже имеющуюся фигуру
        for h in range(H):
            for w in range(W):
                if(grid[h][w] == 1):
                    grid[h][w] = 0
        for k in FIGURES[figure][rotate]:
            grid[y+k[0]][x+k[1]] = 1
    anim_speed = draw(anim_speed)
    pygame.display.update()
    textnext = font2.render(f'GAME OVER!', True, (255, 165, 0))
    while(game_over == 1):
        sounds["game_over"].play()
        for i in range(H-1, -1, -1):
            for n in range(W):
                if(i%2 == 0):
                    grid[i][n] = -1
                else:
                    grid[i][W-n-1] = -1
                draw(anim_speed)
                sc.blit(textnext, ((WIN_WIDTH+200)//2-textnext.get_width()//2, WIN_HEIGHT//2-textnext.get_height()))
                pygame.display.update()
                sleep(.01)
        game_over = 0
        score = 0
        y = 0
        rotate = 0
        x = W//2
        grid = [[0 for i in range(0,W)] for i in range(0,H)]
        anim_count, anim_limit, anim_speed, force_anim = 0, 20000, 600, 0
        figure = select_new()
        nextfigure = select_new()
        pygame.event.clear()
    clock.tick(FPS)
