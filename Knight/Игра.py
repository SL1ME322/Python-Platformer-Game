#импортирование модуля pygame
import pygame 
from pygame.locals import*
from pygame import mixer #импортирование модуля позволяющего проигрывать звуки и музыку в игре
import pickle #модуль python. позволяющий загружать в программу файла формата dat
from os import path #модуль, позволяющий импортировать в питон файлы с указанием пути 
 

pygame.mixer.pre_init(44100,-16,2,512) #предварительные настройки модуля
mixer.init()#активация звукового модуля
pygame.init() #активация модуля pygame

#ограничение на кадры в секунду
clock = pygame.time.Clock() 
fps = 60

screen_width = 1600 #размеры окна (ширина и высота) 
screen_height = 745

screen = pygame.display.set_mode((screen_width,screen_height)) #функция, создающая окно
pygame.display.set_caption('Игра') #название окна

#шрифт для текста
font = pygame.font.SysFont('Times New Roman', 70) #шрифт для отображения текста о победе или поражении 
font_score = pygame.font.SysFont('Times New Roman ',30) #шрифт для отображения кол-ва очков персонажа


tile_size = 30 #размер клетки
game_over = 0 #состояние окончания игры (по умолчанию  нулевое)
main_menu = True # главное меню (по умолчанию - запущено)
level = 1 #игра начинается с 1 уровня
max_levels = 9
score = 0 #изначальные очки

#цвета текста
white = (255, 255, 255) 
red = (255,0,0)
green = (0,255,0)

#загрузка фото
bg_menu_img = pygame.image.load('Спрайты/bg/bgmenu.png')#фоновое изображение в меню
bg_img = pygame.image.load('Спрайты/bg/bg1.png')#фоновое изображение
bg2_img= pygame.image.load('Спрайты/bg/bg2.png')#второе фоновое изображение
bg3_img = pygame.image.load ('Спрайты/bg/bg3.png')#третье фоновое изображение
restart_img = pygame.image.load('Спрайты/Кнопки/restart.png')#кнопка рестарта
start_img = pygame.image.load('Спрайты/Кнопки/start.png')#кнопка старта
exit_img = pygame.image.load('Спрайты/Кнопки/exit.png')#кнопка выхода

#звуки игры
coin_fx = pygame.mixer.Sound('Звуки/coin.mp3')#проигрывание звука подбирания монетки
coin_fx.set_volume(0.09)#регулирование звука
jump_fx = pygame.mixer.Sound('Звуки/jump.wav')#проигрывание звука прыжка
jump_fx.set_volume(0.1)#регулирование звука
game_over_fx = pygame.mixer.Sound('Звуки/game_over.wav')#проигрывание звука проигрыша
game_over_fx.set_volume(0.1)#регулирование звука

pygame.mixer.music.load('Звуки/music.mp3')#загрузка фоновой музыки
pygame.mixer.music.play(-1,0.0,5000)#найстройки миксера (5000 - задержка перед проигрыванием)
pygame.mixer.music.set_volume(0.03)#регулирование звука

#создание функции отображающей текст
def draw_text(text,font, text_col, x, y ): 
        img =font.render(text,True, text_col)
        screen.blit(img,(x,y))
        


def reset_level(level): #функция обновления уровня (при поражении, либо переходе на след. уровень)
        player.reset(65, screen_height - 100) #создание игрока по заданным координатам
        #удаление врагов при обновлении уровня для того, чтобы они не наслаивались друг на друга
        rogue_group.empty() 
        spike_group.empty()
        dragon_group.empty()
        dragon2_group.empty()
        lava_group.empty()
        exit_group.empty()
        #загрузка уровня и создание мира
        if path.exists(f'level{level}_data'): #игра будет открывать только существующие уровни 
                pickle_in = open(f'level{level}_data','rb')#функция, загружающая уровни по порядку их наименования 1,2,3...
                world_data = pickle.load(pickle_in) #переменная world_data содержит в себе определенный уровнень 
        world =World(world_data) #переменная причисляется к классу (который хранит в себе уровень) 
        return world #возвращение переменной для последующей загрузки уровней


class Button(): #класс кнопок (старт, рестарт, выход)
        def __init__(self, x, y, image): 
                self.image = image #загрузка картинки кнопки
                self.image = pygame.transform.scale(image,(300, 100)) #преобразование изображения на заданный размер
                self.rect = self.image.get_rect() #загрузка прямоугольника картинки
                self.rect.x = x #координаты прямоугольника 
                self.rect.y = y
                self.clicked = False #мышь изначально не находится в состоянии нажатия
        def draw (self):
                action = False #игрок не нажал на кнопку 
                pos = pygame.mouse.get_pos() #программа узнаёт позицию мыши в данный момент
                #проверка соприкосновения мыши с кнопкой и проверка нажатия мыши
                if self.rect.collidepoint(pos): #если мышь наведена на кнопку
                        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: #если кнопка нажимается и уже не находится в состоянии нажатия 
                                action = True #кнопка нажата
                                self.clicked = True #лкм нажата
                if pygame.mouse.get_pressed()[0] == 0: # если кнопка больше не нажимается
                        self.clicked = False #то состояние кнопки становится ненажатым                        
                screen.blit(self.image, self.rect)#прорисовка кнопок

                return action 


class Player(): #класс игрока
        def __init__(self, x, y):
                self.reset(x, y) #создание функции заново создающей персонажа
        def update(self,game_over): #выдача персонажу характеристик, 
            dx = 0 #у персонажа изначально нулевая скорость по x и по y
            dy = 0
            walk_cooldown = 6 #время до обновления номера спрайта
            if game_over == 0 : #если игра не окончена то управление, анимация и передвижение игрока будут работать 
                     #управление персонажем
                    key = pygame.key.get_pressed()
                    #если персонаж не в состоянии прыжка, то он может прыгать
                    if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False :#прыжок на пробел (при условии если игрок уже не находится в состоянии прыжка или в воздухе во избежание спама кнопки прыжка)
                        jump_fx.play()
                        self.vel_y= -18 #передвижение на 15 пикселей вверх при прыжке
                        self.jumped = True #персонаж входит в состоянии прыжка при нажатии пробела
                    #если персонаж в состоянии прыжка, то он не может прыгать    
                    if key[pygame.K_SPACE] == False:
                        self.jumped = False  
                    if key[pygame.K_LEFT]: #движение влево на левую стрелку
                        dx -= 5.9 #передвижение на 1 пиксель влево
                        self.counter +=1 #скорость анимации увеличивается
                        self.direction = -1 #при движение влево отрицательное направление
                    if key[pygame.K_RIGHT]:#движение вправо на правую стрелку
                        dx += 5.9 #передвижение на 1 пиксель вправо
                        self.counter += 1
                        self.direction = 1 #при движение влево положительное направление
                    if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False: #если персонаж не идет налево или направо
                    #то анимация не проигрывается
                        self.counter = 0
                        self.index = 0
                        
                        #персонаж при остановке движения смотрит по направлениию движения
                        if self.direction == 1: # если переменная direction равна 1
                                self.image = self.images_right[self.index] #то применяются спрайты на движение вправо
                        if self.direction == -1: # если переменная direction равна -1
                                self.image = self.images_left[self.index] #то применяются спрайты на движение влево
            

                    #анимация
                    if self.counter > walk_cooldown: #если скорость анимации превышает время до обновления номера спрайта
                        self.counter = 0 #то скорость обнулится
                        self.index +=1 #номер спрайта будет постоянно увеличиваться и спрайты будут меняться
                            
                        if self.index >= len(self.images_right): #если номер спрайта, превышает количество спрайтов в листе,
                                self.index = 0 #то номер спрайта обнулится
                        if self.direction == 1: # если переменная direction равна 1
                                self.image = self.images_right[self.index] #то применяются спрайты на движение вправо
                        if self.direction == -1: # если переменная direction равна -1
                                self.image = self.images_left[self.index] #то применяются спрайты на движение влево
                    
                        
                    #гравитация
                    self.vel_y+=1 #персонаж постоянно находится в состоянии падения
                    #скорость падения
                    if self.vel_y>10:
                        self.vel_y = 8.5 
                    dy+=self.vel_y #перемещение вверх по y при прыжке


                    self.in_air = True #персонаж постоянно находится в воздухе
                    for tile in world.tile_list: #цикл для клетки в листе клеток
                                #коллизия по x
                                #коллизия проверяется с помощью команды colliderect с учетом координаты x и координаты передвижения по x
                                #(для того, чтобы игра заранее расчитала перемещение во избежание застревания в блоке) ,
                                #координаты y, ширины и высоты игрока
                                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height): 
                                        dx = 0 #если персонаж соприкоснулся с блоком, то он перестаёт двигаться дальше
                                #коллизия по y
                                #коллизия проверяется с помощью команды colliderect с учетом координаты y и координаты передвижения по y , координаты x, ширины и высоты игрока
                                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                                        #если игрок соприкоснулся с нижней частью блока при прыжке (во избежание застревания в блоке)
                                        if self.vel_y < 0: #состояние прыжка 
                                                dy = tile[1].bottom - self.rect.top #при перемещении вврех должна быть дистанция между нижней частью блока и верхней частью прямоугольника(хитбокса) игрока 
                                                self.vel_y = 0 #когда персонаж ударяется головой о блок, то он не ждет пока значение состояния падения станет вновь положительным, а падает сразу
                                        #если игрок падает (во избежание проваливания под блок)
                                        elif self.vel_y >= 0: #состояние падения
                                                dy = tile[1].top - self.rect.bottom  #при перемещении вниз должна быть дистанция между верхней частью блока и нижней частью прямоугольника(хитбокса) игрока
                                                self.vel_y = 0 #персонаж не падает дальше достигнув блока
                                                self.in_air = False     
                                #коллизия с противниками
                    if pygame.sprite.spritecollide(self, rogue_group, False): #проверка коллизии с группой противников, а не каждым отдельным (переменная False позволяет не удалять спрайты врагов с экрана)
                            game_over = -1 #при столкновении игра заканчивается
                            game_over_fx.play()
                    if pygame.sprite.spritecollide(self, spike_group, False): #проверка коллизии с группой шипов 
                            game_over = -1 #при столкновении игра заканчивается
                            game_over_fx.play()
                    if pygame.sprite.spritecollide(self, lava_group, False): #проверка коллизии с лавой
                            game_over = -1 #при столкновении игра заканчивается
                            game_over_fx.play()
                    if pygame.sprite.spritecollide(self, dragon_group, False): #проверка коллизии с лавой
                            game_over = -1 #при столкновении игра заканчивается
                            game_over_fx.play()
                    if pygame.sprite.spritecollide(self, dragon2_group, False): #проверка коллизии с лавой
                            game_over = -1 #при столкновении игра заканчивается
                            game_over_fx.play()
                    if pygame.sprite.spritecollide(self, exit_group, False): #проверка коллизии с группой шипов, а не каждым отдельным
                            game_over = 1 #при столкновении игра заканчивается
                    
                    #координаты игрока
                    self.rect.x += dx
                    self.rect.y += dy
            
            elif game_over == -1: #если игра окончена
                    self.image = self.dead_image #спрайт героя сменяется на спрайт призрака
                    draw_text('Игра окончена',font,red, (screen_width//2)-700,screen_height //2) #отображается текст
                    self.rect.y -=3 #призрак движется вверх
            
            #отображает персонажа на экране (изображение и прямоугольник (хитбокс))
            screen.blit(self.image,self.rect)
            

            return game_over #возвращает переменную в первоначальное значение для возможности рестарта уровня


        def reset(self,x ,y): #метод, позволяющий пересоздавать персонажа после окончании игры и при нажатии кнопки рестарта со всеми заданными переменными
                self.images_right = [] #лист спрайтов главного героя, движущегося направо
                self.images_left = [] #лист спрайтов главного героя, движущегося налево
                self.index = 0 #номер спрайта в листе
                self.counter = 0 #скорость анимации
                for num in range(2, 11): #цикл загрузки спрайтов по очереди 
                    img_right = pygame.image.load (f'Спрайты/гг/{num}.png') #загрузка изображений главного героя
                    img_right = pygame.transform.scale(img_right,(60, 60))#изменяет размер гл.героя на заданные параметры
                    img_left = pygame.transform.flip(img_right, True, False) #переворачивает картинку главного героя по x и оставляет по y
                    self.images_right.append(img_right) #добавляет переменную в лист спрайтов
                    self.images_left.append(img_left)   #добавляет переменную в лист спрайтов
                self.dead_image = pygame.image.load ('ghost.png')#загрузка изображения смерти главного героя
                self.dead_image = pygame.transform.scale(self.dead_image,(120,120 ))#изменяет размер призрака гл.героя на заданные параметры
                self.dead_image = pygame.transform.flip(self.dead_image, True, False)#переворачивает картинку главного героя по x и оставляет по y
                self.image = self.images_right[self.index] #загрузка фотографий по определенному цифровому индексу (например img1,img2...)
                self.rect = self.image.get_rect()#создание прямоугольника персонажа 40x80
                self.rect.x = x  #координаты персонажа по x и y
                self.rect.y = y
                self.width = self.image.get_width()# ширина изображения игрока
                self.height = self.image.get_height()#высота изображения игрока
                self.vel_y = 0 #состояние падения
                self.jumped = False #состояние прыжка
                self.direction = 0 #направление
                self.in_air = True #нахождение персонажа в воздухе


class World(): #класс уровня
        def __init__(self, data): #создание функции
                self.tile_list = [] #переменная содержащая в себе значения при которых клетка изменяется на выбранную пользователем 

                #загрузка изображений блоков
                dirt_img = pygame.image.load('Спрайты/блоки и враги/dirt.jpg')
                grass_img = pygame.image.load('Спрайты/блоки и враги/grass.png')
                stone_img = pygame.image.load ('Спрайты/блоки и враги/stone.png')
                brick_img = pygame.image.load ('Спрайты/блоки и враги/brick.png')
                row_count = 0 #счетчик строк для определения координаты y
                for row in data: #для каждой строки в сетке
                        col_count = 0 #счетчик столбцов для определения координаты x
                        for tile in row: #для каждой клетки в строке
                                if tile == 1: #если клетка имеет значение 1, cоздаётся клетка травы
                                                                                #по x      #по y
                                        img = pygame.transform.scale(grass_img, (tile_size, tile_size)) #изменяет заданную картику до размеров клетки
                                        #функция преобразует картинку в прямоугольник для хранения информации, например координат
                                        img_rect = img.get_rect()
                                        #выдача координат прямоугольникам
                                        img_rect.x = col_count * tile_size #координата x будет увеличиваться при каждом новом столбце в сетке 
                                        img_rect.y = row_count * tile_size #координата y будет увеличиваться при каждой новой строчке в сетке
                                        tile = (img, img_rect) #в значении клетки хранится изображение и прямоугольник изображения 
                                        self.tile_list.append(tile) #добавление 
                                if tile == 2: #если клетка имеет значение 2, создаётся клетка земли
                                        img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                                        img_rect = img.get_rect()
                                        img_rect.x = col_count * tile_size
                                        img_rect.y = row_count * tile_size
                                        tile = (img, img_rect)
                                        self.tile_list.append(tile)
                                if tile == 3: #если клетка имеет значение 3, создаётся клетка камня  
                                        img = pygame.transform.scale(stone_img, (tile_size, tile_size))
                                        img_rect = img.get_rect()
                                        img_rect.x = col_count * tile_size
                                        img_rect.y = row_count * tile_size
                                        tile = (img, img_rect)
                                        self.tile_list.append(tile)
                                if tile == 4: #если клетка имееет значение 4, создается клетка кирпича
                                        img = pygame.transform.scale(brick_img, (tile_size, tile_size))
                                        img_rect = img.get_rect()
                                        img_rect.x = col_count * tile_size
                                        img_rect.y = row_count * tile_size
                                        tile = (img, img_rect)
                                        self.tile_list.append(tile)
                                if tile == 5: #если клетка имеет значение 5, создаётся враг
                                        rogue = Enemy(col_count * tile_size, row_count * tile_size - 20 )#создание противника из класса врагов (x и y координаты - столбцы и строчки) 
                                        rogue_group.add(rogue) #добавление противника в пустой лист
                                if tile == 6: #если клетка имеет значение 6, создаётся шип
                                        spike = Spike(col_count * tile_size, row_count * tile_size )
                                        spike_group.add(spike)
                                if tile == 7:#если клетка имеет значение 7, создаётся шип
                                        coin = Coin(col_count * tile_size , row_count * tile_size) 
                                        coin_group.add(coin)
                                if tile == 8:#если клетка имеет значение 8, создаётся лава
                                        lava = Lava(col_count * tile_size , row_count * tile_size)
                                        lava_group.add(lava)
                                if tile == 9: #если клетка имеет значение 9, создаётся враг
                                        dragon = Enemy2(col_count * tile_size, row_count * tile_size )#создание противника из класса врагов (x и y координаты - столбцы и строчки) 
                                        dragon_group.add(dragon) #добавление противника в пустой переменную
                                if tile == 10: #если клетка имеет значение 10, создаётся враг
                                        dragon2 = Enemy3(col_count * tile_size, row_count * tile_size )#создание противника из класса врагов (x и y координаты - столбцы и строчки) 
                                        dragon2_group.add(dragon2) #добавление противника в переменную
                                if tile == 11:
                                        exit = Exit(col_count * tile_size, row_count * tile_size )
                                        exit_group.add(exit)#добавление выхода в переменную
                                
                                
                                col_count += 1 #при движении персонажа на следующий столбец счетчик столбцов увеличивается на 1 
                        row_count += 1 #при движении персонажа на следующую строчку счетчик строк увеличивается на 1
                        
                                
        #вывод клеток на экран
        def draw(self): 
                for tile in self.tile_list:  #в tile 2 объекта: изображение (tile[0]) и прямоугольник (tile[1])
                        screen.blit(tile[0], tile[1]) #вывод на экран
                        
			




class Enemy(pygame.sprite.Sprite): #класс врагов
        def __init__(self,x,y): #создание функции 
                pygame.sprite.Sprite.__init__(self) #вызов спрайтов
                self.image = pygame.image.load('Спрайты/блоки и враги/rogue.png') #загрузка спрайтов
                self.image = pygame.transform.scale(self.image,(40, 55))#уменьшение спрайта до размеров 70x90
                self.rect = self.image.get_rect()#создание прямоугольника
                self.rect.x = x #выдача x и y координат
                self.rect.y = y
                self.move_direction = 1 #направление движения
                self.move_counter =0 #количество пикселей пройденное при передвижении
                
                        
        #выдача действий противникам
        def update(self): #подкласс создаваемый для движения спрайтов противников
                self.rect.x += self.move_direction #увеличивает координату x и противник двигается
                self.move_counter +=1 #с увеличением x  увеличивается и расстояние
                if abs(self.move_counter) > 80: #если превышает 80 
                        self.move_direction *= -1 #направление сменяется на противоположное
                        self.move_counter *= -1 #обновление пройденного расстояния



class Enemy2(pygame.sprite.Sprite): #класс врагов
        def __init__(self,x,y):
                pygame.sprite.Sprite.__init__(self) #вызов спрайтов
                self.image = pygame.image.load('Спрайты/блоки и враги/dragon.png') #загрузка спрайтов
                self.image = pygame.transform.scale(self.image,(50, 50))#уменьшение спрайта до размеров 70x90
                self.rect = self.image.get_rect()#создание прямоугольника
                self.rect.x = x #выдача x и y координат
                self.rect.y = y
                self.move_direction = -1 #направление движения
                
                        
        #выдача действий противникам
        def update(self): #подкласс создаваемый для движения спрайтов противников
                self.rect.x += self.move_direction -1 #увеличивает координату x и противник двигается


class Enemy3(pygame.sprite.Sprite): #класс врагов
        def __init__(self,x,y):# создание функции
                pygame.sprite.Sprite.__init__(self) #вызов спрайтов
                self.image = pygame.image.load('Спрайты/блоки и враги/dragon2.png') #загрузка спрайтов
                self.image = pygame.transform.scale(self.image,(50, 50))#уменьшение спрайта до размеров 70x90
                self.rect = self.image.get_rect()#создание прямоугольника
                self.rect.x = x-1200 #выдача x и y координат (драконы вылетают с задержкой)
                self.rect.y = y
                self.move_direction = 1 #направление движения
                
                
                        
        #выдача действий противникам
        def update(self): #подкласс создаваемый для движения спрайтов противников
                self.rect.x += self.move_direction +1 #увеличивает координату x и противник двигается
                
                

class Spike(pygame.sprite.Sprite):
        def __init__(self,x,y): 
                pygame.sprite.Sprite.__init__(self) #вызов спрайтов
                img = pygame.image.load('Спрайты/блоки и враги/spike.png') #загрузка спрайтов
                self.image = pygame.transform.scale(img,(tile_size -10, tile_size))#уменьшение спрайта до заданных размеров 
                self.rect = self.image.get_rect()#создание прямоугольника
                self.rect.x = x #выдача x и y координат
                self.rect.y = y


class Lava(pygame.sprite.Sprite):
        def __init__(self,x,y): 
                pygame.sprite.Sprite.__init__(self) #вызов спрайтов
                img = pygame.image.load('Спрайты/блоки и враги/lava.png') #загрузка спрайтов
                self.image = pygame.transform.scale(img,(tile_size, tile_size ))#уменьшение спрайта до размеров клетки
                self.rect = self.image.get_rect()#создание прямоугольника
                self.rect.x = x #выдача x и y координат
                self.rect.y = y

class Coin(pygame.sprite.Sprite):
        def __init__(self,x,y):
                pygame.sprite.Sprite.__init__(self) #вызов спрайтов
                img = pygame.image.load('Спрайты/блоки и враги/coin.png') #загрузка спрайтов
                self.image = pygame.transform.scale(img,(tile_size, tile_size))#уменьшение спрайта до размеров клетки
                self.rect = self.image.get_rect()#создание прямоугольника
                self.rect.center = (x,y) #создание монет в центре клетки 
                

class Exit(pygame.sprite.Sprite):#класс перехода на следующий уровень
        def __init__(self,x,y):
                pygame.sprite.Sprite.__init__(self) #вызов спрайтов
                img = pygame.image.load('Спрайты/блоки и враги/exit2.png') #загрузка спрайтов
                self.image = pygame.transform.scale(img,(tile_size, int(tile_size *2   )))#уменьшение спрайта до размеров клетки
                self.rect = self.image.get_rect()#создание прямоугольника
                self.rect.x = x #выдача x и y координат
                self.rect.y = y



player = Player(65, screen_height - 100) #создание игрока по заданным координатам        

#загрузка спрайтов объектов
rogue_group = pygame.sprite.Group() 
spike_group = pygame.sprite.Group() 
lava_group = pygame.sprite.Group()  
dragon_group = pygame.sprite.Group()
dragon2_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group() 
exit_group = pygame.sprite.Group() 
                   
			


#загрузка файлов уровней и создание мира
if path.exists(f'level{level}_data'): #игра будет открывать только существующие уровни 
        pickle_in = open(f'level{level}_data','rb')#функция, загружающая уровни по порядку их наименования 1,2,3...
        world_data = pickle.load(pickle_in)
world =World(world_data)  




#создание кнопок
exit_button = Button(screen_width //2 +130, screen_height //2, exit_img) #размер кнопки
restart_button = Button(screen_width //2-100, screen_height //2 , restart_img) #размер кнопки
start_button = Button(screen_width //2-330, screen_height //2 , start_img) #размер кнопки

#приложение будет работать до закрытия игроком
run = True #переменная обозначающая, что игра запущена
while run: #при нажатии на крестик игра будет закрываться

    
    clock.tick(fps) #ограничение на кадры в секунду
    
    screen.blit(bg3_img,(0,0))#функция, выводящая задний фон на экран


    if level == 1:#если в игре первый уровень
            screen.blit(bg_img,(0,0)) #отрисовывается первый задний фон
    if level == 2: #если в игре второй уровень
            screen.blit(bg_img,(0,0))  #отрисовывается первый задний фон
    if level == 3: #если в игре третий уровень
            screen.blit(bg2_img,(0,0)) #отрисовывается второй задний фон
    if level == 4: #если в игре третий уровень
            screen.blit(bg2_img,(0,0)) #отрисовывается второй задний фон
    if level == 5:#если в игре третий уровень
            screen.blit(bg3_img,(0,0)) #отрисовывается третий задний фон
    if level == 6:
            screen.blit(bg3_img,(0,0))
    if level == 7:
            screen.blit(bg3_img,(0,0))
    if level == 8:
            screen.blit(bg3_img,(0,0))
    if level == 9:
            screen.blit(bg3_img,(0,0))
    
    if main_menu == True: #если главное меню запущено, то
            screen.blit(bg_menu_img,(0,0)) #отрисовывается задний фон главного меню
            if exit_button.draw(): #отображается кнопка начала игры
                   run = False #при нажатии на кнопку выхода, осуществляется выход из игры
            if start_button.draw():#отображается кнопка выхода из игры
                    main_menu = False #при нажатии на кнопку старта осуществляется старт игры
            
                       
    else:
    #вызов функции отрисовки клеток  
            world.draw()
            if game_over == 0: #если игра заканчивается, то противники замедляются
                    rogue_group.update()#обновление 
                    #прибавление очков
                    #если монета была собрана
                    if pygame.sprite.spritecollide(player, coin_group, True): #если игрок соприкасается с монеткой
                            score += 10 #ему прибавляется 10 очков
                            coin_fx.play() #проигрывается звук подбирания монетки
                    draw_text(str(score),font_score,white,tile_size -25, 2)#отрисовывается число очков в левом верхнем углу
            #все функции действую на группу, а не на противников по отдельности    
            rogue_group.update()
            dragon_group.update()
            dragon2_group.update()
            #отображение спрайтов на экране
            rogue_group.draw(screen) 
            spike_group.draw(screen) 
            coin_group.draw(screen)
            lava_group.draw(screen)
            dragon_group.draw(screen)
            dragon2_group.draw(screen)
            exit_group.draw(screen)
            game_over = player.update(game_over) #вызов функции отрисовки игрока 

            if game_over == -1:#если игрок умер
                    if restart_button.draw():#то отображается кнопка повторения уровня
                            
                            world = reset_level(level)#уровень обновляется
                            game_over = 0 #игра не считается оконченной
                            score = 0 #счет очков обнуляется   

            #если игрок завершил уровень
            if game_over == 1:
                    #обновление игры и переход на след.уровень
                    level += 1
                    if level <= max_levels: #если игрок не привысил максимальное количество уровней
                            #обновление уровня
                            world_data = [] #очистка уровня
                            world = reset_level(level) #уровень создаётся заново 
                            game_over = 0 #игра не считается завершенной
                    #если игрок не привысил максимальное количество уровней        
                    else:                                                   #x                  #y
                            draw_text('ВЫ ПОБЕДИЛИ !', font,green, (screen_width) -850, screen_height // 2 -160) #отрисовка текста 
                            if restart_button.draw(): #при выводе кнопки рестарта
                                level = 1 #игрок появляется на 1 уровне
                                world_data= []#очистка уровня
                                world = reset_level(level) #уровень создаётся заново
                                game_over = 0 #игра не считается завершенной
                                score = 0 #счет обнуляется

                            
    #при нажатии на крестик программа закроется              
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()#отображение всей игры на экране
    
pygame.quit() #возможность выхода из игры 
