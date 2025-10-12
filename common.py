import pygame
import defs as f
import random as r

logo = pygame.image.load("logo_32x32.png")
pygame.display.set_icon(logo)
basic_x = 1048  # 1280
basic_y = 691   # 720

pygame.init()
pygame.mixer.init()
channelhonk = pygame.mixer.Channel(0)
channelboom = pygame.mixer.Channel(1)
#info = pygame.display.Info() (.current_w, .current_h)
screen = pygame.display.set_mode((basic_x+232, basic_y+24), pygame.RESIZABLE)
pygame.display.set_caption("Keep Honking and Nobody Explodes")
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)

import img_load as il

modul_kesz = []
for _ in range(6):#mivel csak hat hely van a bonbán
    modul_kesz.append(None)


#Szöveg stílus és kiíráshoz függ.
family = "Grand9K Pixel.ttf"
font = pygame.font.Font(family, 36) #õ -> ő

def text_draw(text, x, y, color=(255,255,255), font=font):
    img = font.render(text, True, color)
    screen.blit(img,(x,y))

def display_text(text, pos, width=800, font=font, color=(255,255,255)):
    collection = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]
    x,y = pos

    for lines in collection:
        for words in lines:
            word_surface = font.render(words, True, color)
            word_width , word_height = word_surface.get_size()
            if x + word_width >= width:
                x = pos[0]
                y += word_height
            screen.blit(word_surface, (x,y))
            x += word_width + space
        x = pos[0]
        y += word_height


#Fontos! Ez a függvény a külön álló elemek újra méretezéséért felel (máshol ez az updateben van).
def scaled(update: list = None):
    global g_scale , pos_coordinate, screen_x, screen_y, bomb_pos_x, bomb_pos_y #g_scale = global_scaling

    screen_x, screen_y = screen.get_size()

    if screen_x < basic_x:
        screen_x = basic_x
    if screen_y < basic_y:
        screen_y = basic_y

    scale_x = screen_x//basic_x
    scale_y = screen_y//basic_y

    if scale_x < scale_y:
        g_scale = scale_x

    else:
        g_scale = scale_y

    bomb_pos_x = (screen_x - basic_x*g_scale)//2 # 116
    bomb_pos_y = (screen_y - basic_y*g_scale)//2 # 12

    # ([197, 81], [528, 81], [859, 81], [197, 416], [528, 416], [859, 416])
    pos_coordinate = ((bomb_pos_x+81*g_scale, bomb_pos_y+66*g_scale), (bomb_pos_x+412*g_scale, bomb_pos_y+66*g_scale), (bomb_pos_x+743*g_scale, bomb_pos_y+66*g_scale), (bomb_pos_x+81*g_scale, bomb_pos_y+401*g_scale), (bomb_pos_x+412*g_scale, bomb_pos_y+401*g_scale), (bomb_pos_x+743*g_scale, bomb_pos_y+401*g_scale))
    #position_coordinates

    if update != None:
        for i in range(len(update)):
            update[i].update()



def generate_bomb():
    global spec_chart, szeria_root, stickers, cells, explosion

    explosion = False

    spec_chart = bool(r.randint(0, 1))
    szeria_root = f.szerianumber(spec_chart)
    # 0 fehér; 1 narancssárga; 2 fekete
    stickers = [bool(r.randint(0, 1)), bool(r.randint(0, 1)), bool(r.randint(0, 1))]
    # 0-1: balra; 2-3: jobbra
    cells = [bool(r.randint(0, 1)), bool(r.randint(0, 1)), bool(r.randint(0, 1)), bool(r.randint(0, 1))]



def random_pos_modul(moduls:list, not_use:list): # a modulok szét szórása
    r_list = []
    for i in range(6): #mivel csak hat hely van a bonbán
        r_list.append(i)

    for i in range(len(moduls)):
        if i not in not_use:
            rand_index = r.randint(0, len(r_list) - 1)
            moduls[i].index = r_list[rand_index]
            del r_list[rand_index]


def change_image(x: int, y: int, images: tuple[pygame.surface.Surface], scaling: float|int = 1, close: bool = None): #Jelek amikkel jelöljük a bombák állapotát
    pos = pygame.mouse.get_pos()

    alap = Image(x, y, images[0], scaling)

    if close is not None and len(images) > 2 and close:
        Image(x, y, images[2], scaling)

    elif alap.rect.collidepoint(pos):
        Image(x, y, images[1], scaling)


def modul_draw(self): #kirajzolja a modult, figyelembe veszi hogy kész van-e
    global modul_kesz, g_scale, pos_coordinate

    modul_kesz[self.index] = self.done

    if self.pos == (0, 0) and self.index is not None:
        self.pos = pos_coordinate[self.index]

    screen.blit(self.image, self.pos)
    change_image(self.pos[0] + 1, self.pos[1] + 1, il.jelek, g_scale, self.done)

# Osztály tipusok def.

class Image:
    def __init__(self, x: int, y: int, image: pygame.surface.Surface, scaling: float|int = 1, delay: bool = False, trans: tuple[bool, int] = (False, 255)):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scaling), int(height * scaling)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        if trans[0]:
            self.image.set_alpha(trans[1])
        if not delay: #Vannak képek amik esztétikai okok miatt csak későbbi program állapotban jellenek meg.
            screen.blit(self.image, (self.rect.x, self.rect.y))

    def delay_draw(self): #Később megjelenő kép kirajzolása.
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Button:
    def __init__(self, x: int, y: int, image: pygame.surface.Surface, scale: float|int = 1):
        width = image.get_width()
        height = image.get_height()
        self.scale = scale
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.click = False
        self.animate = 1

    def puss_button_draw(self, puss_img:pygame.surface.Surface , close:bool=None):
        action = False

        #egér helyzete:
        if close is not None and close:
            Image(self.rect.x + 1*self.scale, self.rect.y + 1*self.scale, puss_img, self.scale)

        else:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos) or self.click:
                if pygame.mouse.get_pressed()[0] == 1: #le van nyomva
                    self.click = True
                    Image(self.rect.x + 1*self.scale, self.rect.y + 1*self.scale, puss_img, self.scale)#mit jelenítsen meg helyete
                        

                elif pygame.mouse.get_pressed()[0] == 0 and self.click:
                    self.click = False
                    action = True
                    if close is not None:
                        close = True
                        self.click = True

            if not self.click:
                screen.blit(self.image, (self.rect.x, self.rect.y))
            
            if close is not None and close:
                Image(self.rect.x + 1*self.scale, self.rect.y + 1*self.scale, puss_img, self.scale)
                self.click = False

        return action

    def cable_draw(self, action: bool, images: tuple[pygame.surface.Surface]):

        if action:
            if self.animate < len(images) - 1:
                self.animate += 0.1
                Image(self.rect.x, self.rect.y, images[int(self.animate)], self.scale)

            else:
                Image(self.rect.x, self.rect.y, images[-1], self.scale)

        else:
            screen.blit(self.image, (self.rect.x, self.rect.y))

            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                Image(self.rect.x, self.rect.y, images[0], self.scale)

                if pygame.mouse.get_pressed()[0] == 1:
                    action = True

        return action

    def button_draw(self, images:tuple[pygame.surface.Surface], close:bool=None):
        action = False

        if close is not None:
            if not close:

                pos = pygame.mouse.get_pos()
                if self.rect.collidepoint(pos) or self.click:
                    if pygame.mouse.get_pressed()[0] == 1:
                        self.click = True
                        Image(self.rect.x, self.rect.y, images[1], self.scale)
                            

                    elif pygame.mouse.get_pressed()[0] == 0 and self.click:
                        Image(self.rect.x, self.rect.y, images[2], self.scale)
                        self.click = False
                        action = True

                    elif not self.click:
                        Image(self.rect.x, self.rect.y, images[0], self.scale)

                elif not self.click:
                    screen.blit(self.image, (self.rect.x, self.rect.y))

            else:
                Image(self.rect.x, self.rect.y, images[2], self.scale)

        else:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos) or self.click:
                if pygame.mouse.get_pressed()[0] == 1:
                    self.click = True
                    Image(self.rect.x, self.rect.y, images[1], self.scale)

                elif pygame.mouse.get_pressed()[0] == 0 and self.click:
                    Image(self.rect.x, self.rect.y, images[0], self.scale)
                    self.click = False
                    action = True

                elif not self.click:
                    Image(self.rect.x, self.rect.y, images[0], self.scale)

            elif not self.click:
                screen.blit(self.image, (self.rect.x, self.rect.y))

        return action, self.click

    def pos_button_draw(self, pos_image:pygame.surface.Surface):
        action = False

        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            Image(self.rect.x, self.rect.y, pos_image, self.scale)
            if pygame.mouse.get_pressed()[0] == 1 and not self.click:
                self.click = True
                action = True

        else:
            screen.blit(self.image, (self.rect.x, self.rect.y))

        if pygame.mouse.get_pressed()[0] == 0:
            self.click = False

        return action


class Timer:
    def __init__(self, x: int, y: int, text_size:int, time: int = 300) -> None:
        self.x = x
        self.y = y
        self.text_size = text_size
        self.current_seconds = time
        self.changing_ind = 0

    def timer_draw(self, color: tuple[int, int, int] = (255, 255, 255)):
        display_minutes = self.current_seconds // 60
        display_seconds = self.current_seconds % 60

        self.changing_ind = (self.current_seconds // 5) % 3

        text_draw(f"{display_minutes:02}:{display_seconds:02}", self.x, self.y, color, pygame.font.Font(family, self.text_size))


class Input:
    def __init__(self, x: int, y: int, w: int, h: int, text_size: int, update_list, enter: bool=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.text_size = text_size
        self.max = w // self.text_size
        self.buffer = ""
        self.enter = enter
        self.active = False
        self.value = ""
        self.update_list = update_list

    def input_draw(self, running: bool, timer = None, plus_x:int = 5, plus_y:int = 5, background=(20,20,20), active_color=(255,255,255), passive_color=(88,88,88), text_color=(255,255,255), mask = None):

        pos = pygame.mouse.get_pos()
        if mask is None:
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1:
                    self.active = True

            elif pygame.mouse.get_pressed()[0] == 1:
                self.active = False

        else:
            if mask.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1:
                    self.active = True

            elif pygame.mouse.get_pressed()[0] == 1:
                self.active = False

        if self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    # sortörést nem mindig fogadunk el.
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        if self.enter:
                            if len(self.buffer) == self.max:
                                self.value = self.buffer
                                self.buffer = ""

                        else:
                            self.active = False

                    elif event.key == pygame.K_BACKSPACE:
                        self.buffer = self.buffer[0:-1]
                    elif len(self.buffer) < self.max:
                        self.buffer += event.unicode

                elif event.type == pygame.VIDEORESIZE:
                    scaled(self.update_list)

                if running and event.type == pygame.USEREVENT:
                    timer.szamlalo.current_seconds -= 1

        if self.active:
            color = active_color
        else:
            color = passive_color

        pygame.draw.rect(screen, background, self.rect)
        pygame.draw.rect(screen, color, self.rect, 2)
        text_draw(self.buffer, self.rect.x + plus_x, self.rect.y + plus_y, text_color, pygame.font.Font("Grand9K Pixel.ttf", self.text_size))

        return self.value
