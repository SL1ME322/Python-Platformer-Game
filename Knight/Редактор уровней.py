import pygame #импортирование модуля pygame
import pickle #модуль python. позволяющий загружать в программу файла формата dat
from os import path #модуль, позволяющий импортировать в питон файлы с указанием пути 


pygame.init() #активация модуля pygame

#ограничение на кадры в секунду
clock = pygame.time.Clock() 
fps = 60


tile_size = 30 #размер клетки
cols = 42 #строки и столбцы
margin = 100 #поле для загрузки и сохранения 
screen_width = tile_size * cols + 400 #ширина равна клеткам умноженным на строки и столбцы
screen_height = (tile_size * cols) + margin - 510 #высота экрана 


screen = pygame.display.set_mode((screen_width, screen_height)) #функция, создающая окно
pygame.display.set_caption('Редактор уровней')#название окна


#загрузка изображений
bg_img = pygame.image.load('Спрайты/bg/bg1.png')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height - margin))
stone_img = pygame.image.load('Спрайты/блоки и враги/stone.png')
dirt_img = pygame.image.load('Спрайты/блоки и враги/dirt.jpg')
grass_img = pygame.image.load('Спрайты/блоки и враги/grass.png')
brick_img = pygame.image.load('Спрайты/блоки и враги/brick.png')
coin_img = pygame.image.load('Спрайты/блоки и враги/coin.png')
rogue_img = pygame.image.load('Спрайты/блоки и враги/rogue.png')
dragon_img = pygame.image.load('Спрайты/блоки и враги/dragon.png')
dragon2_img = pygame.image.load('Спрайты/блоки и враги/dragon2.png')
spike_img = pygame.image.load('Спрайты/блоки и враги/spike.png')
lava_img = pygame.image.load('Спрайты/блоки и враги/lava.png')
exit_img = pygame.image.load('Спрайты/блоки и враги/exit2.png')
save_img = pygame.image.load('Спрайты/кнопки/save.png')
save_img = pygame.transform.scale(save_img, (200, 70))
load_img = pygame.image.load('Спрайты/кнопки/load.png')
load_img = pygame.transform.scale(load_img, (200, 70))



#изначальные настройки
clicked = False 
level = 1 #загрузка редактора с 1 уровня

#добавление цветов
white = (255, 255, 255)#цвет сетки
green = (144, 201, 120)#цвет поля для загрузки и сохранения 

font = pygame.font.SysFont('Futura', 24) #функция для написания текста в редакторе (шрифт, размер текста)

#создание пустого листа клеток
world_data = []
for row in range(55): #количество строк 
	r = [0] * 55 #55 строк имеют нулевое значение,следовательно ничем не заполнены
	world_data.append(r)#присвоение переменной



#создание функции для вывода текста на экран 
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y)) #отображение на экран

def draw_grid(): #создание функции отрисовки сетки 
	for c in range(56):
		#вертикальные линии сетки
		pygame.draw.line(screen, white, (c * tile_size, 0), (c * tile_size, screen_height- margin  ))
		#горизонтальные линии сетки
		pygame.draw.line(screen, white, (0, c * tile_size), (screen_width  , c * tile_size ))


def draw_world():
        for row in range(54): #максимальное кол-во строк
                for col in range(54): #максимальное кол-во столбцов
                        if world_data[row][col] > 0:  
                                if world_data[row][col] == 1:
                                        #создание блока травы
                                        img = pygame.transform.scale(grass_img, (tile_size, tile_size))#размеры
                                        screen.blit(img, (col * tile_size, row * tile_size)) #вывод на экран
                                if world_data[row][col] == 2:
                                        #создание блока земли
                                        img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                                        screen.blit(img, (col * tile_size, row * tile_size))
                                if world_data[row][col] == 3:
                                        #создание блока камня
                                        img = pygame.transform.scale(stone_img, (tile_size, tile_size))
                                        screen.blit(img, (col * tile_size, row * tile_size))
                                if world_data[row][col] == 4:
                                        #создание блока кирпича
                                        img = pygame.transform.scale(brick_img, (tile_size, tile_size)) 
                                        screen.blit(img, (col * tile_size, row * tile_size))
                                if world_data[row][col] == 5:
                                        #создание врага
                                        img = pygame.transform.scale(rogue_img, (tile_size, int(tile_size * 0.75)))
                                        screen.blit(img, (col * tile_size, row * tile_size + (tile_size * 0.25)))
                                if world_data[row][col] == 6:
                                        #создание лавы
                                        img = pygame.transform.scale(spike_img, (tile_size, tile_size // 2))
                                        screen.blit(img, (col * tile_size, row * tile_size + (tile_size // 2)))
                                if world_data[row][col] == 7:
                                        #создание монетки
                                        img = pygame.transform.scale(coin_img, (tile_size , tile_size ))
                                        screen.blit(img, (col * tile_size, row * tile_size))
                                if world_data[row][col] == 8:
                                        #создание блока лавы
                                        img = pygame.transform.scale(lava_img, (tile_size, tile_size // 2))
                                        screen.blit(img, (col * tile_size, row * tile_size + (tile_size // 2)))
                                if world_data[row][col] == 9:
                                        #создание врага
                                        img = pygame.transform.scale(dragon_img, (tile_size, tile_size // 2))
                                        screen.blit(img, (col * tile_size, row * tile_size + (tile_size // 2)))
                                if world_data[row][col] == 10:
                                        #создание врага
                                        img = pygame.transform.scale(dragon2_img, (tile_size, tile_size // 2))
                                        screen.blit(img, (col * tile_size, row * tile_size + (tile_size // 2)))
                                if world_data[row][col] == 11:
                                        #создание выхода
                                        img = pygame.transform.scale(exit_img, (tile_size, int(tile_size * 1.5)))
                                        screen.blit(img, (col * tile_size, row * tile_size - (tile_size // 2)))
                                
                                
                                



class Button(): #создание класса кнопок 
	def __init__(self, x, y, image):#создание функции
		self.image = image #изображение 
		self.rect = self.image.get_rect() #хитбокс
		self.rect.topleft = (x, y) #координаты
		self.clicked = False #состояние мыши (по стандарту игрок не нажимает на лкм)

	def draw(self):
		action = False #нажатие на кнопку

		#выявление позиции мыши
		pos = pygame.mouse.get_pos()

		#проверка наводки мыши на кнопку и нажатия
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: #если кнопка нажимается и уже не находится в состоянии нажатия 
				action = True #осуществляется нажатие на кнопку
				self.clicked = True #лкм нажата

		if pygame.mouse.get_pressed()[0] == 0: # если кнопка больше не нажимается
			self.clicked = False #то состояние кнопки становится ненажатым

		#отрисовка кнопки
		screen.blit(self.image, (self.rect.x, self.rect.y))

		return action #позволяет неоднократно нажимать на кнопку

#создание кнопок сохранения и загрузки уровня
save_button = Button(screen_width // 2 - 50, screen_height - 80, save_img)
load_button = Button(screen_width // 2 + 175, screen_height - 80, load_img)

#основной цикл
run = True
while run:

	clock.tick(fps)

	#отрисовка фона
	screen.fill(green)
	screen.blit(bg_img, (0, 0))

	#загрузка и сохранение уровня
	if save_button.draw(): #при нажатии кнопки 'сохранить'
		#сохранение уровня
		pickle_out = open(f'level{level}_data', 'wb')#запись изменений в существующем уровне
		pickle.dump(world_data, pickle_out)#сохраняет изменения в файле dat.
		pickle_out.close() #закрытие функции
	if load_button.draw(): #при нажатии кнопки 'загрузить'
		#загрузка уровня
		if path.exists(f'level{level}_data'): #редактор будет открывать только существующие уровни
			pickle_in = open(f'level{level}_data', 'rb') #функция, загружающая уровни по порядку их наименования 1,2,3...
			world_data = pickle.load(pickle_in)#переменная world_data содержит в себе определенный уровнень


	#отрисовка сетки и блоков в сетке
	draw_grid()
	draw_world()


	#текст, показывающий уровень (на разных строках)
	draw_text(f'Уровень: {level}', font, white, tile_size, screen_height - 80)
	draw_text('Нажмите "вверх" или "вниз" для ', font, white, tile_size, screen_height - 60)
	draw_text('смены уровня', font, white, tile_size, screen_height - 42)
        
	#закрытие программы
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False
		#изменение клеток на нажатия мыши
		if event.type == pygame.MOUSEBUTTONDOWN and clicked == False: #если игрок нажимает на лкм и при этом лкм был не нажат до этого
			clicked = True #лкм нажимается
			pos = pygame.mouse.get_pos() #определяется позиция мыши
			#клетка заполняется ровно на текущей позиции мыши
			x = pos[0] // tile_size
			y = pos[1] // tile_size
			#ограничения на создания клеток (54 по x, 25 по y)
			if x < 54 and y < 25:
				if pygame.mouse.get_pressed()[0] == 1: #если нажимается лкм 
					world_data[y][x] += 1 #то отображается следующий объект 
					if world_data[y][x] > 11: #если нажатия лкм превышают 11 (максимум объектов)
						world_data[y][x] = 0 #клетка пуста
				elif pygame.mouse.get_pressed()[2] == 1:#если нажимается пкм 
					world_data[y][x] -= 1 #то отображается предыдущий объект  
					if world_data[y][x] < 0: #если номер объекта меньше нуля 
						world_data[y][x] = 11 #отображается 11 объект 
		if event.type == pygame.MOUSEBUTTONUP:
			clicked = False
		#смена уровней на клавиши ВВЕРХ и ВНИЗ
		if event.type == pygame.KEYDOWN: #если нажата клавиша 
			if event.key == pygame.K_UP: #вверх
				level += 1 #просматривается след.уровень 
			elif event.key == pygame.K_DOWN and level > 1: #если нажата клавиша вниз и уровень хотя бы второй 
				level -= 1 # просматривается пред.уровень

	
	pygame.display.update()#вывод на экран

pygame.quit()#возможность закрытия программы
