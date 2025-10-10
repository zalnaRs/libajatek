import os, pygame
import random as r
from sys import exit
import defs as f


# Állandok

changing_colors = [(255, 0, 0), (255, 135, 35), (235, 35, 200)]     #Kötelező időzitő modul
changing_back_color = [(155, 0, 40), (210, 80, 25), (135, 35, 200)] #Globális színei

logo = pygame.image.load("logo_32x32.png")
pygame.display.set_icon(logo)
basic_x = 1048  # 1280
basic_y = 691   # 720

"""
FONTOS!!
cells[0-1: balra; 2-3: jobbra]
stickers[0 fehér; 1 narancssárga; 2 fekete]
moduls[0: SimaDrót; 1: KomplexKábel; 2: Gomb; 3: Jelszó; 4: Libamondja; 5: Kérdés; 6: Idözítő]
"""

#Változók

start_page = True       #Kezdő lap aktív vagy sem
miss_write = False      #El fogatható-e a csapat/osztály név
menu = False            #Menü lap aktív vagy sem
game = False            #Játék lap aktív vagy sem
explosion = None        #Fel robbant-e egy játék útán a bomba vagy sem
end_page = False        #Végeredmény lap aktív vagy sem
running = False         #Játték épp fut-e vagy sem
zoom_in = False         #Matricák nagyított ablaka aktív-e
choose_sticker = None   #Az aktív matrica indexe
levels = [True, False, False, False] #Melyik szint aktív éppen (vagyis melyik fog elindulni)

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

#Fontos! Ez a függvény a külön álló elemek újra méretezéséért felel (máshol ez az updateben van).
def scaled(update:bool = True):
    global g_scale , pos_coordinate, screen_x, screen_y, bomb_pos_x, bomb_pos_y, running #g_scale = global_scaling

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

    if update:
        global resume_button, quit_button, start_button, back_button, lvl1_button, lvl2_button, lvl3_button, lvl4_button, left_button, right_button, csapat_input

        resume_button = Button(bomb_pos_x+304*g_scale, bomb_pos_y+228*g_scale, il.resume_img, 10*g_scale)
        quit_button = Button(bomb_pos_x+394*g_scale, bomb_pos_y+378*g_scale, il.quit_img, 10*g_scale)
        start_button = Button(bomb_pos_x+363*g_scale, bomb_pos_y+288*g_scale, il.start_img, 10*g_scale)
        back_button = Button(bomb_pos_x+5*g_scale, bomb_pos_y+8*g_scale, il.back_img, 5*g_scale)
        lvl1_button = Button(bomb_pos_x+46*g_scale, bomb_pos_y+68*g_scale, il.lvl1_img, 5*g_scale)
        lvl2_button = Button(bomb_pos_x+44*g_scale, bomb_pos_y+228*g_scale, il.lvl2_img, 5*g_scale)
        lvl3_button = Button(bomb_pos_x+44*g_scale, bomb_pos_y+388*g_scale, il.lvl3_img, 5*g_scale)
        lvl4_button = Button(bomb_pos_x+44*g_scale, bomb_pos_y+548*g_scale, il.lvl4_img, 5*g_scale)
        left_button = Button(bomb_pos_x+5*g_scale, bomb_pos_y+282*g_scale, il.left_img, 4*g_scale)
        right_button = Button(bomb_pos_x+basic_x-19*4*g_scale-5*g_scale, bomb_pos_y+286*g_scale, il.right_img, 4*g_scale)

        try:
            save = csapat_input.buffer
        except:
            save = ""

        csapat_input = Input(bomb_pos_x+384*g_scale, bomb_pos_y+218*g_scale, 200*g_scale, 40*g_scale, 28*g_scale)
        csapat_input.buffer = save

        if running:
            global moduls, not_use_m, properties

            properties.update()

            for i in range(len(moduls)):
                if i not in not_use_m:
                    moduls[i].update()

scaled(False)

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
    def __init__(self, x: int, y: int, w: int, h: int, text_size: int, enter: bool=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.text_size = text_size
        self.max = w // self.text_size
        self.buffer = ""
        self.enter = enter
        self.active = False
        self.value = ""

    def input_draw(self, plus_x:int = 5, plus_y:int = 5, background=(20,20,20), active_color=(255,255,255), passive_color=(88,88,88), text_color=(255,255,255), mask = None):

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
                    scaled()

                if running and event.type == pygame.USEREVENT:
                    moduls[6].szamlalo.current_seconds -= 1

        if self.active:
            color = active_color
        else:
            color = passive_color

        pygame.draw.rect(screen, background, self.rect)
        pygame.draw.rect(screen, color, self.rect, 2)
        text_draw(self.buffer, self.rect.x + plus_x, self.rect.y + plus_y, text_color, pygame.font.Font("Grand9K Pixel.ttf", self.text_size))

        return self.value



class SimaDrot:
    def __init__(self, index: int, image: pygame.surface.Surface, pos:tuple=(0, 0), done:bool=False, scaling:float|int = 1) -> None:
        self.pos = pos
        self.scaling = scaling
        self.index = index
        self.image = image
        self.done = done

        self.colors = (
        (il.fekete_drot_img, il.fekete_drot_action), (il.kek_drot_img, il.kek_drot_action), (il.piros_drot_img, il.piros_drot_action),
        (il.sarga_drot_img, il.sarga_drot_action))
        self.drotok = f.generate_drotok()
        self.animate_button = None

        self.drotok_color = []

        for i in range(len(self.drotok)):
            if self.drotok[i] is not None:
                self.drotok_color.append(self.drotok[i][0])

        sarga = False

        #self.drotok_color[i]: 0-fekete, 1-kék, 2-piros, 3-sárga

        if f.count(self.drotok_color, 2) >= 2:
            sarga = True
            for i in range(len(self.drotok_color)):
                if i != 2:
                    if f.count(self.drotok_color, i) >= 2:
                        sarga = False
                        break

            if sarga:
                if szeria_root[1] == 3:
                    self.correct = 3

                elif szeria_root[1] % 2 == 0 and stickers[2]:
                    self.correct = 2

                elif szeria_root[1] % 2 == 1:
                    self.correct = 3

                elif stickers[1]:
                    self.correct = 1

                else:
                    if szeria_root[1] / 2 + 7 == 8:
                        self.correct = 0

                    elif szeria_root[1] / 2 + 7 == 9:
                        self.correct = 2

                    elif szeria_root[1] / 2 + 7 == 10:
                        self.correct = 3

                    else:
                        self.correct = 1

        if not sarga and self.drotok_color[2] == 0 and cells[2:4] == [True, True]:
            self.correct = 0

        elif f.count(self.drotok_color, 1) == 2 and f.count(self.drotok_color, 2) == 0:
            self.correct = 1

        elif f.count(self.drotok_color, 2) == 1:
            self.correct = 3

        elif f.count(self.drotok_color, 0) == 0:
            if szeria_root[1] == 6:
                self.correct = 0

            elif True in cells[0:2] and True not in cells[2:4]:
                self.correct = 1

            else:
                self.correct = 3

        elif self.drotok_color[0] == 3 and stickers[1]:
            self.correct = 3

        elif not stickers[2]:
            self.correct = 0

        else:
            self.correct = 2

    def draw(self):
        modul_draw(self)
        c = 0
        for i in range(len(self.drotok)):
            if i < 3:
                half = 0
            else:
                half = 6*self.scaling

            if self.drotok[i] is not None and self.done:
                if self.drotok[i][1]:
                    if self.animate_button is None:
                        self.animate_button = Button(self.pos[0] + 35*self.scaling, self.pos[1] + 34*self.scaling + 28 * i*self.scaling + half, self.colors[self.drotok[i][0]][0], self.scaling)
                    self.animate_button.cable_draw(self.drotok[i][1], self.colors[self.drotok[i][0]][1])

                else:
                    Image(self.pos[0] + 35*self.scaling, self.pos[1] + 34*self.scaling + 28 * i*self.scaling + half, self.colors[self.drotok[i][0]][0], self.scaling)

            elif self.drotok[i] is not None:
                self.drotok[i][1] = Button(self.pos[0] + 35*self.scaling, self.pos[1] + 34*self.scaling + 28 * i*self.scaling + half, self.colors[self.drotok[i][0]][0]).cable_draw(self.drotok[i][1], self.colors[self.drotok[i][0]][1])
                if self.drotok[i][1]:
                    if i - c == self.correct:
                        self.done = self.drotok[i][1]

                    else:
                        boom()

            else:
                c += 1

    def update(self):
        self.scaling = g_scale
        self.pos = (0, 0)


class KomplexKabel:
    def __init__(self, index: int, image: pygame.surface.Surface, pos:tuple=(0, 0), done:bool=False, scaling:float|int = 1) -> None:
        self.pos = pos
        self.scaling = scaling
        self.index = index
        self.image = image
        self.done = done

        self.num = ((il.kabel_1_img, il.kabel_1_action), (il.kabel_2_img, il.kabel_2_action), (il.kabel_3_img, il.kabel_3_action),
                    (il.kabel_4_img, il.kabel_4_action))
        self.kabelek = []
        for _ in range(6):
            self.kabelek.append([r.randint(0, 3), False])

        self.num_kabel = [0, 1, 2, 3, 4, 5]

        self.cut_them = []
        self.feher = None

        # sárga lap
        if szeria_root[1] == 5:
            self.cut_them.append(4)

        else:
            if True in cells:
                self.feher = 1

            self.cut_them.append(0)

        # zöld lap
        if szeria_root[1] == 3 or szeria_root[1] == 9:
            self.cut_them.append(2)

        elif szeria_root[1] == 4:
            self.cut_them.append(3)

        elif stickers[2] or szeria_root[1] == 8:
            self.cut_them.append(3)

        else:
            if True not in cells:
                self.feher = 4

            if not stickers[0]:
                self.cut_them.append(3)

            else:
                self.cut_them.append(2)

        # fehér 4. oldal
        if self.feher == 1:
            if szeria_root[1] > 7:
                self.cut_them.append(5)

            elif stickers[0]:
                self.cut_them.append(5)

            elif szeria_root[1] < 5:
                self.cut_them.append(1)

            else:
                self.feher = 4

        if self.feher == 4:
            if szeria_root[1] < 5:
                current_root = szeria_root[1] + 5

            else:
                current_root = szeria_root[1]

            if current_root == 5:
                self.cut_them.append(5)

            elif current_root == 6:
                self.cut_them.append(1)

    def draw(self):
        if self.pos == (0, 0):
            make = True
        else:
            make = False

        modul_draw(self)

        if make:
            for i in range(len(self.kabelek)):
                self.num_kabel[i] = Button(self.pos[0] + 22*self.scaling + 28 * i*self.scaling, self.pos[1] + 23*self.scaling, self.num[self.kabelek[i][0]][0], self.scaling)

        for i in range(len(self.kabelek)):
            if self.done:
                if self.kabelek[i][1]:

                    for j in range(len(self.kabelek)):
                        if self.kabelek[j][1]:
                            self.num_kabel[i].cable_draw(self.kabelek[i][1], self.num[self.kabelek[i][0]][1])

                else:
                    Image(self.pos[0] + 22*self.scaling + 28 * i*self.scaling, self.pos[1] + 23*self.scaling, self.num[self.kabelek[i][0]][0], self.scaling)

            else:
                self.kabelek[i][1] = self.num_kabel[i].cable_draw(self.kabelek[i][1], self.num[self.kabelek[i][0]][1])

                if self.kabelek[i][1]:
                    if i in self.cut_them:

                        c = 0
                        for j in range(len(self.kabelek)):
                            if self.kabelek[j][1]:
                                c += 1

                        if c == len(self.cut_them):
                            self.done = True

                    else:
                        boom()

    def update(self):
        self.scaling = g_scale
        self.pos = (0, 0)


class Gomb:
    def __init__(self, index: int, image: pygame.surface.Surface, pos:tuple=(0, 0), done:bool=False, scaling:float|int = 1) -> None:
        self.pos = pos
        self.scaling = scaling
        self.index = index
        self.image = image
        self.done = done

        self.colors = ((il.kek_gomb_img, il.kek_gomb_action), (il.piros_gomb_img, il.piros_gomb_action), (il.zold_gomb_img, il.zold_gomb_action))
        self.symbols = (il.lud_szimbolum, il.talp_szimbolum, il.tojas_szimbolum)
        self.gomb_data = (r.randint(0, 2), r.randint(0, 2))

        self.puss = None
        if self.gomb_data[0] == 0 and f.count(cells[0:2], True) > 0:
            self.puss = True

        elif spec_chart and self.gomb_data[0] != 1 and self.gomb_data[1] != 2:
            self.puss = False

        elif True not in cells and self.gomb_data[1] != 1:
            self.puss = False

        elif self.gomb_data[0] == 2:
            if szeria_root[1] == 9:
                self.puss = True
            else:
                self.puss = False

        if self.puss is None and self.gomb_data[0] == 0:
            if szeria_root[1] == 1:
                self.puss = False
            else:
                self.puss = True

        if self.puss is None and self.gomb_data[1] == 2:
            self.puss = False

        elif self.puss is None:
            self.puss = True

        if self.puss:
            if self.gomb_data[1] == 0:
                self.time_color = 0

            elif True not in cells:
                self.time_color = 1

            else:
                self.time_color = 2

        else:
            self.time_limit = None

    def draw(self):
        if self.pos == (0, 0):
            make = True
        else:
            make = False

        modul_draw(self)

        if make:
            self.gomb = Button(self.pos[0] + 100*self.scaling, self.pos[1] + 39*self.scaling, self.colors[self.gomb_data[0]][0], self.scaling)

        Image(self.pos[0] + 56*self.scaling, self.pos[1] + 159*self.scaling, self.symbols[self.gomb_data[1]], self.scaling)

        allapot = self.gomb.button_draw(self.colors[self.gomb_data[0]][1], self.done)
        if not self.puss and allapot[1]:
            if self.time_limit is None:
                self.time_limit = moduls[6].szamlalo.current_seconds - 2

            if self.time_limit >= moduls[6].szamlalo.current_seconds:
                boom()

        if allapot[0]:
            if self.puss:
                if self.time_color == moduls[6].szamlalo.changing_ind:
                    self.done = allapot[0]

                else:
                    boom()

            else:
                self.done = allapot[0]

    def update(self):
        self.scaling = g_scale
        self.pos = (0, 0)


class Kerdes:
    def __init__(self, index:int, image:pygame.surface.Surface, pos:tuple=(0, 0), done:bool=False, scaling:float|int = 1) -> None:
        self.pos = pos
        self.scaling = scaling
        self.index = index
        self.image = image
        self.done = done

        self.betuk = ((il.a_gomb_img, il.a_gomb_action), (il.b_gomb_img, il.b_gomb_action), (il.c_gomb_img, il.c_gomb_action), (il.d_gomb_img, il.d_gomb_action))
        self.progress = (il.progress_0_img, il.progress_1_img, il.progress_2_img, il.progress_3_img, il.progress_4_img)
        self.kerdesek = (("Melyik szín, jelenik meg gyakran Szent Mártont ábrázoló képeken?",10),
                        ("Melyik a helyes válasz? ",18),
                        ("Melyik országnak szolgált katonaként Szent Márton?",13),
                        ("Milyen zöldséget szoktak libasülthöz adni?",13),
                        ("Mi Szent Márton egyik legismertebb tulajdonsága?",13),
                        ("Szent Márton minek a védõszentje?",13),
                        ("Melyik jelkép kapcsolódik Márton-naphoz a termények közül? ",10),
                        ("Mit adott Szent Márton a koldusnak?",13),
                        ("Melyik Szent Márton szülõvárosa?",13),
                        ("Mi készül hagyományosan libából Márton-napon?",13)
                        )
        #0: A; 1: B; 2: C; 3: D
        self.valaszok = (0, 3, 2, 0, 3, 1, 3, 2, 1, 2)
        self.current_kerdesek = []
        while len(self.current_kerdesek) < 4:
            rand_num = r.randint(0, len(self.kerdesek)-1)
            if rand_num not in self.current_kerdesek:
                self.current_kerdesek.append(rand_num)
        self.current_kerdes = 0

        a_gomb = None
        b_gomb = None
        c_gomb = None
        d_gomb = None
        self.gombok = [a_gomb, b_gomb, c_gomb, d_gomb]

    def draw(self):
        if self.pos == (0,0):
            make = True
        else:
            make = False

        modul_draw(self)

        if make:
            for i in range(len(self.gombok)):
                if i > 1:
                    half = 5*self.scaling

                else:
                    half = 0

                self.gombok[i] = Button(self.pos[0]+23*self.scaling+48*i*self.scaling+half, self.pos[1]+139, self.betuk[i][0], self.scaling)

        if self.done:
            for i in range(len(self.gombok)):
                if i > 1:
                    half = 5*self.scaling

                else:
                    half = 0
                
                Image(self.pos[0]+23*self.scaling+48*i*self.scaling+half, self.pos[1]+139*self.scaling, self.betuk[i][0], self.scaling)

            Image(self.pos[0]+22*self.scaling, self.pos[1]+198*self.scaling, self.progress[-1], self.scaling)
            text_draw("( =", self.pos[0]+78*self.scaling, self.pos[1]+32*self.scaling, (255,255,255), pygame.font.Font(family, 36*self.scaling))

        else:
            display_text(self.kerdesek[self.current_kerdesek[self.current_kerdes]][0], (self.pos[0]+37*self.scaling, self.pos[1]+32*self.scaling), self.pos[0]+190*self.scaling, pygame.font.Font(family, self.kerdesek[self.current_kerdesek[self.current_kerdes]][1]))
            Image(self.pos[0]+22*self.scaling, self.pos[1]+198*self.scaling, self.progress[self.current_kerdes], self.scaling)
            for i in range(len(self.gombok)):
                if self.gombok[i].button_draw(self.betuk[i][1])[0]:
                    if i == self.valaszok[self.current_kerdesek[self.current_kerdes]]:
                        if self.current_kerdes == 3:
                            self.done = True

                        else:
                            self.current_kerdes += 1

                    else:
                        boom()

    def update(self):
        self.scaling = g_scale
        self.pos = (0, 0)


class Jelszo:
    def __init__(self, index:int, image:pygame.surface.Surface, pos:tuple=(0, 0), done:bool=False, scaling:float|int = 1) -> None:
        self.pos = pos
        self.scaling = scaling
        self.index = index
        self.image = image
        self.done = done
        self.buffer_save = ""

        self.jelszo = f.password()

    def draw(self):
        if self.pos == (0,0):
            make = True
        else:
            make = False

        modul_draw(self)

        if make:
            self.rect = pygame.Rect(self.pos[0]+71*self.scaling, self.pos[1]+171*self.scaling, 82*self.scaling, 25*self.scaling)
            self.input = Input(self.rect.x, self.rect.y, 82*self.scaling, 25*self.scaling, 16*self.scaling, True)
            if self.buffer_save != "":
                self.input.buffer = self.buffer_save

        for i in range(len(self.jelszo[1][0])):
            for j in range(len(self.jelszo[1])):
                if i == 0 or i == 3:
                    plus = 0
                else:
                    plus = 2*self.scaling
                text_draw(self.jelszo[1][j][i], self.pos[0]+25*self.scaling+40*j*self.scaling+plus, self.pos[1]+15*self.scaling+34*i*self.scaling, (57, 57, 57), pygame.font.Font(family, 21*self.scaling))

        if self.done:
            pygame.draw.rect(screen, (57, 35, 0), self.rect)
            pygame.draw.rect(screen, (31, 19, 0), self.rect, 2)
        else:
            self.input.input_draw(5, -1, (57, 35, 0), (255, 255, 255), (31, 19, 0), (255,255,255), pygame.Rect(self.pos[0], self.pos[1], 244*self.scaling, 244*self.scaling))

        if self.input.value != "":
            if self.input.value.lower() == self.jelszo[0]:
                self.done = True

            else:
                boom()

    def update(self):
        self.scaling = g_scale
        self.pos = (0, 0)
        if self.input.buffer != "":
            self.buffer_save = self.input.buffer


class LibaMondja:
    def __init__(self, index:int, image:pygame.surface.Surface, pos:tuple=(0, 0), done:bool=False, scaling:float|int = 1) -> None:
        self.pos = pos
        self.scaling = scaling
        self.index = index
        self.image = image
        self.done = done

        # 0-3: allo; 4-7: fekvo
        # 0: kék; 1: piros; 2: sárga; 3: zöld
        self.szinek = ((il.allo_kek_img, il.allo_kek_img_action), (il.allo_piros_img, il.allo_piros_img_action), (il.allo_sarga_img, il.allo_sarga_img_action), (il.allo_zold_img, il.allo_zold_img_action), (il.fekvo_kek_img, il.fekvo_kek_img_action), (il.fekvo_piros_img, il.fekvo_piros_img_action), (il.fekvo_sarga_img, il.fekvo_sarga_img_action), (il.fekvo_zold_img, il.fekvo_zold_img_action))
        self.make = True
        self.voices = honking
        self.play = False
        self.round = 0

        self.pos_bonus = ((9, 9), (77, 9), (152, 77), (9, 152))
        self.buttons = []

    def draw(self):
        modul_draw(self)

        if self.make:
            self.limit = time
            self.round += 1
            self.honk = r.randint(1,4)
            self.start = moduls[6].szamlalo.current_seconds - 2
            channelhonk.pause()
            self.gombok = [None, None, None, None]
            self.buttons = []

            if spec_chart:
                if self.honk == 1:
                    if r.randint(0,1):
                        self.gombok[1] = 3

                    if r.randint(0,1):
                        self.gombok[3] = 3

                    else:
                        self.gombok[1 + 2*r.randint(0,1)] = 3

                elif self.honk == 2:
                    self.gombok[2] = 1

                elif self.honk == 3:
                    if r.randint(0,1):
                        self.gombok[0] = 0

                    if r.randint(0,1):
                        self.gombok[2] = 0

                    else:
                        self.gombok[2*r.randint(0,1)] = 0

                else:
                    self.gombok[r.randint(0,3)] = 2*r.randint(0,1)

            else:
                if self.honk == 2:
                    self.gombok[r.randint(0,3)] = 2

                elif self.honk == 3:
                    if r.randint(0,1):
                            self.gombok[1] = 3

                    if r.randint(0,1):
                        self.gombok[3] = 3

                    else:
                        self.gombok[1 + 2*r.randint(0,1)] = 3

                elif self.honk != 1:
                    self.gombok[3] = 1

            for i in range(len(self.gombok)):
                if self.gombok[i] == None:
                    self.gombok[i] = r.randint(0,3)


            for i in range(4):
                if i % 2 == 0:
                    bonus = 0

                else:
                    bonus = 4

                self.buttons.append(Button(self.pos[0]+self.pos_bonus[i][0]*self.scaling, self.pos[1]+self.pos_bonus[i][1]*self.scaling, self.szinek[self.gombok[i]+bonus][0], self.scaling))

            self.make = False

        if self.done:
            for i in range(len(self.buttons)):
                if i % 2 == 0:
                    plus = 0
                else:
                    plus = 4

                Image(self.buttons[i].rect.x, self.buttons[i].rect.y, self.szinek[self.gombok[i]+plus][0], self.scaling)
        
        else:
            if self.start == moduls[6].szamlalo.current_seconds:
                if not self.play:
                    self.start = moduls[6].szamlalo.current_seconds-(self.honk+2)
                    channelhonk.play(self.voices[self.honk-1])
                    self.play = True

            else:
                self.play = False

            for i in range(len(self.buttons)):
                if i % 2 == 0:
                    plus = 0
                else:
                    plus = 4

                if self.buttons[i].button_draw(self.szinek[self.gombok[i]+plus][1])[0]:
                    if spec_chart:
                        if self.honk == 1:
                            if i == 1 or i == 3:
                                if self.gombok[i] == 3:
                                    self.make = True

                        elif self.honk == 2:
                            if i == 2 and self.gombok[2] == 1:
                                self.make = True

                        elif self.honk == 3:
                            if i == 0 or i == 2:
                                if self.gombok[i] == 0:
                                    self.make = True

                        else:
                            if self.gombok[i] == 2 or self.gombok[i] == 0:
                                self.make = True

                    else:
                        if self.honk == 1:
                            if i == 0 or i == 2:
                                self.make = True

                        elif self.honk == 2:
                            if self.gombok[i] == 2:
                                self.make = True

                        elif self.honk == 3:
                            if i == 1 or i == 3:
                                if self.gombok[i] == 3:
                                    self.make = True

                        else:
                            if self.gombok[3] == 1:
                                self.make = True

                    if not self.make:
                        boom()

                    if self.round == 4:
                        self.done = True
                        self.make = False

    def update(self):
        self.scaling = g_scale
        self.pos = pos_coordinate[self.index]
        for i in range(4):
            if i % 2 == 0:
                bonus = 0

            else:
                bonus = 4

            self.buttons[i] = Button(self.pos[0]+self.pos_bonus[i][0]*self.scaling, self.pos[1]+self.pos_bonus[i][1]*self.scaling, self.szinek[self.gombok[i]+bonus][0], self.scaling)


class Idozito:
    def __init__(self, index:int, image:pygame.surface.Surface, pos:tuple=(0, 0), done:bool=True, scaling:float|int = 1) -> None:
        self.pos = pos
        self.scaling = scaling
        self.index = index
        self.image = image
        self.done = done

    def draw(self):
        if self.pos == (0,0):
            make = True
        else:
            make = False

        modul_draw(self)

        if make:
            self.szamlalo = Timer(self.pos[0]+55*self.scaling, self.pos[1]+113*self.scaling, 36*self.scaling, time)


        Image(self.pos[0], self.pos[1], self.image, self.scaling)

        color = changing_colors[self.szamlalo.changing_ind]
        back_color = changing_back_color[self.szamlalo.changing_ind]

        background = pygame.Rect(self.pos[0]+39*self.scaling, self.pos[1]+108*self.scaling, 146*self.scaling, 63*self.scaling)
        pygame.draw.rect(screen, back_color, background)
        self.szamlalo.timer_draw(color)

        cooldown = pygame.Rect(self.pos[0]+27*self.scaling, self.pos[1]+27*self.scaling, 40*(self.szamlalo.current_seconds%5)*self.scaling+10*self.scaling, 13*self.scaling)
        pygame.draw.rect(screen, color, cooldown)

    def update(self):
        self.scaling = g_scale
        self.pos = (0, 0)



def On_the_Bomb_sticker(self):
    self.sticker_buttons = []
    for i in range(len(self.current_sticker)):
        self.sticker_buttons.append(Button(self.pos_list[self.current_sticker[i][0]][0], self.pos_list[self.current_sticker[i][0]][1], self.current_sticker[i][1], self.scaling))

def On_the_Bomb_s_pos(scaling):
    pos_list = []
    for i in range(4):
        if i == 1 or i == 3:
            x_bonus = 399*scaling

        else:
            x_bonus = 0

        if i >= 2:
            y_bonus = 681*scaling

        else:
            y_bonus = 0

        pos_list.append((bomb_pos_x+225*scaling+x_bonus, bomb_pos_y+3*scaling+y_bonus))

    return pos_list

class On_the_Bomb:
    def __init__(self, cell, sticker, scaling:float|int = 1) -> None:
        self.scaling = scaling
        self.copy_cells = cell
        self.copy_stickers = sticker

        self.kijelolve = (il.szeriaszam_kijelolve, il.matrica_fel_kijelolve, il.matrica_le_kijelolve, il.matrica_le_kijelolve)

        self.pos_list = On_the_Bomb_s_pos(self.scaling)

        r_index = []
        for i in range(len(self.copy_stickers)):
            r_index.append(i+1)

        self.big_sticker = (il.nagy_szeria_matrica_img, il.nagy_feher_matrica_img, il.nagy_narancs_matrica_img, il.nagy_fekete_matrica_img)
        self.current_sticker= [(0, il.szeriaszam_img, 0)]

        for i in range(len(self.copy_stickers)):
            if self.copy_stickers[i]:
                rand_i = r.randint(0, len(r_index)-1)
                if r_index[rand_i] == 1:
                    image = il.matrica_fel_img
                else:
                    image = il.matrica_le_img

                self.current_sticker.append((r_index[rand_i], image, i+1))
                del r_index[rand_i]

        self.sticker_buttons = []
        On_the_Bomb_sticker(self)

        self.cells_img = (il.elem_bal_img, il.elem_jobb_img)

    def draw(self):
        global zoom_in, choose_sticker

        for i in range(len(self.sticker_buttons)):
            if self.sticker_buttons[i].pos_button_draw(self.kijelolve[self.current_sticker[i][0]]):
                zoom_in = True
                choose_sticker = i


        for i in range(len(self.copy_cells)):
            if self.copy_cells[i]:
                if i == 1 or i == 3:
                    y_bonus = 335*self.scaling

                else:
                    y_bonus = 0

                if i >= 2:
                    x_bonus = 1023*self.scaling

                else:
                    x_bonus = 0

                Image(bomb_pos_x*self.scaling+x_bonus, bomb_pos_y+130*self.scaling+y_bonus, self.cells_img[i//2], self.scaling)

    def update(self):
        self.scaling = g_scale

        self.pos_list = On_the_Bomb_s_pos(self.scaling)
        On_the_Bomb_sticker(self)

#Betöltések
explosion_sound = pygame.mixer.Sound("Assets/Hangok/robanas.mp3")
honk_1 = pygame.mixer.Sound("Assets/Hangok/1_hapog.mp3")
honk_2 = pygame.mixer.Sound("Assets/Hangok/2_hapog.mp3")
honk_3 = pygame.mixer.Sound("Assets/Hangok/3_hapog.mp3")
honk_4 = pygame.mixer.Sound("Assets/Hangok/4_hapog.mp3")
honking = (honk_1, honk_2, honk_3, honk_4)


def generate_bomb():
    # Változok

    global spec_chart, szeria_root, stickers, cells, properties, explosion

    explosion = False

    spec_chart = bool(r.randint(0, 1))
    szeria_root = f.szerianumber(spec_chart)
    # 0 fehér; 1 narancssárga; 2 fekete
    stickers = [bool(r.randint(0, 1)), bool(r.randint(0, 1)), bool(r.randint(0, 1))]
    # 0-1: balra; 2-3: jobbra
    cells = [bool(r.randint(0, 1)), bool(r.randint(0, 1)), bool(r.randint(0, 1)), bool(r.randint(0, 1))]

    properties = On_the_Bomb(cells, stickers)

    #0: SimaDrót; 1: KomplexKábel; 2: Gomb; 3: Jelszó; 4: Libamondja; 5: Kérdés; 6: Idözítő
    return(SimaDrot(None, il.s_drot_modul_img, scaling=g_scale), KomplexKabel(None, il.k_kabel_modul_img, scaling=g_scale), Gomb(None, il.gomb_modul_img, scaling=g_scale), Jelszo(None, il.jelszo_modul_img, scaling=g_scale), LibaMondja(None, il.liba_m_modul_img, scaling=g_scale), Kerdes(None, il.kerdes_modul_img, scaling=g_scale), Idozito(None, il.idozito_modul_img, scaling=g_scale))



def random_pos_modul(moduls:list, not_use:list): # a modulok szét szórása
    r_list = []
    for i in range(6):
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

def modul_draw(self): #kirajzolja a modult, figyelembe veszi hogy kész van-e?
    global modul_kesz, g_scale, pos_coordinate

    modul_kesz[self.index] = self.done

    if self.pos == (0, 0) and self.index is not None:
        self.pos = pos_coordinate[self.index]


    screen.blit(self.image, self.pos)
    change_image(self.pos[0] + 1, self.pos[1] + 1, il.jelek, g_scale, self.done)

# megcsinálja az eredmenyek mappát
try:
    os.mkdir("eredmenyek")
except Exception as e:
    print(f"hiba az eredmenyek mappa létrehozásánál: {e}")

def boom():
    global explosion
    channelhonk.pause()
    channelboom.play(explosion_sound)
    explosion = True
    end_game()

def check_done_moduls_num(): #Megnézi, hogy mennyi kész modul van.

    global modul_kesz

    j = 0
    for modul in modul_kesz:
        if modul:
            j += 1

    return j

def check_if_game_done(): #Ha az összes modul kész van akkor lefutatja a end_game-t.
    if check_done_moduls_num() != len(moduls)-len(not_use_m):
        return False

    channelhonk.pause()
    end_game()
    return True

def end_game(): #Ha a játék véget ér, akkor ez a függvény fut le. :return: None
    global game, running, menu, end_page, stickers, szeria_root, cells
    game = False
    running = False
    menu = False
    end_page = True

    for i in range(len(levels)):
        if levels[i] is True:
            szint = i + 1

    file = open(rf"eredmenyek/{csapat_input.value}_{szint}.txt", "w", encoding="UTF-8")
    # TODO: normális pontozás
    file.write(f"--------------\n{csapat_input.value}\n--------------\nIdő: {moduls[6].szamlalo.current_seconds}\nPontszám: {check_done_moduls_num()-1}\n")
    if explosion:
        file.write(f"Felrobbant.\n")
    file.write(f"--------------\n")

    file.write(f"Szériaszám: {szeria_root[0]}\n")

    bal = 0
    jobb = 0
    for i in range(len(cells)):
        if True == cells[i]:
            if i < 2:
                bal += 1

            else:
                jobb += 1
    file.write(f"Elemek: bal:{bal}; jobb:{jobb}\n")

    file.write("Matricák:\n")
    for i in range(len(stickers)):
        if True == stickers[i]:
            if i == 0:
                file.write("-fehér\n")

            elif i == 1:
                file.write("-narancssárga\n")

            else:
                file.write("-fekete\n")
    file.close()

scaled()

# Folyamat

while True:

    if game:
        screen.fill((120, 120, 120))
        if zoom_in:

            Image(0, 0 , il.background_img, screen_x)
            Image(bomb_pos_x+137*g_scale, bomb_pos_y+162*g_scale, properties.big_sticker[properties.current_sticker[choose_sticker][2]], g_scale)

            if properties.current_sticker[choose_sticker][2] == 0:
                text_draw(szeria_root[0], bomb_pos_x+254*g_scale, bomb_pos_y+340*g_scale, (255,255,255), pygame.font.Font(family, 100*g_scale))

            if len(properties.current_sticker) != 1:
                if left_button.pos_button_draw(il.left_kijelolve):
                    if choose_sticker - 1 == -1:
                        choose_sticker = len(properties.current_sticker)-1

                    else:
                        choose_sticker -= 1

                if right_button.pos_button_draw(il.right_kijelolve):
                    if choose_sticker + 1 == len(properties.current_sticker):
                        choose_sticker = 0

                    else:
                        choose_sticker += 1

            if back_button.puss_button_draw(il.back_le):
                zoom_in = False
                moduls[4].start = moduls[6].szamlalo.current_seconds - 1

        else:
            # 141, 25
            Image(bomb_pos_x+25*g_scale, bomb_pos_y+10*g_scale, il.bomb_img, g_scale)

            for i in range(len(moduls)):
                if (len(moduls)-1)-i not in not_use_m:
                    moduls[(len(moduls)-1)-i].draw()

            properties.draw()

            check_if_game_done()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if zoom_in:
                        zoom_in = False
                        moduls[4].start = moduls[6].szamlalo.current_seconds - 1
                    else:
                        game = False
                        menu = True

            elif event.type == pygame.VIDEORESIZE:
                scaled()

            if event.type == pygame.USEREVENT:
                moduls[6].szamlalo.current_seconds -= 1

        if moduls[6].szamlalo.current_seconds == 0:
            boom()


    elif start_page:
        screen.fill((30, 17, 34))
        Image(bomb_pos_x, bomb_pos_y, il.start_background_img, g_scale)

        csapat_input.input_draw(5, -2)

        if start_button.puss_button_draw(il.start_le):
            if csapat_input.buffer != "":

                moduls = generate_bomb()
                f.test_write(szeria_root[0], cells, stickers)

                modul_kesz = []
                for _ in range(len(moduls)):
                    modul_kesz.append(None)

                csapat_input.value = csapat_input.buffer
                start_page = False
                game = True
                running = True
                miss_write = False

                #0: SimaDrót; 1: KomplexKábel; 2: Gomb; 3: Jelszó; 4: Libamondja; 5: Kérdés; 6: Idözítő
                if levels[0]:
                    time = 480
                    not_use_m = [0, 3, 2]
                elif levels[1]:
                    time = 180
                    not_use_m = [1, 3, 5]
                elif levels[2]:
                    time = 300
                    not_use_m = [0]
                elif levels[3]:
                    time = 180
                    not_use_m = [4]

                random_pos_modul(moduls, not_use_m)

            else:
                miss_write = True

        if miss_write and csapat_input.buffer == "":
            text_draw("Nem adtad még meg az osztályt!", 450*g_scale, 180*g_scale, (255, 0, 0), pygame.font.Font(family, 20*g_scale))

        if lvl1_button.puss_button_draw(il.lvl1_le, levels[0]):
            levels = [True, False, False, False]

        if lvl2_button.puss_button_draw(il.lvl2_le, levels[1]):
            levels = [False, True, False, False]

        if lvl3_button.puss_button_draw(il.lvl3_le, levels[2]):
            levels = [False, False, True, False]

        if lvl4_button.puss_button_draw(il.lvl4_le, levels[3]):
            levels = [False, False, False, True]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    start_page = False
                    menu = True

            elif event.type == pygame.VIDEORESIZE:
                scaled()


    elif menu:
        screen.fill((30, 17, 34))
        Image(bomb_pos_x, bomb_pos_y, il.start_background_img, g_scale)
        Image(0, 0, il.background_img, screen_x)

        if quit_button.puss_button_draw(il.quit_le):
            break

        if resume_button.puss_button_draw(il.resume_le):
            menu = False

            if running:
                game = True
                moduls[4].start = moduls[6].szamlalo.current_seconds - 1
            else:
                start_page = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu = False
                    if running:
                        game = True
                    else:
                        start_page = True

            elif event.type == pygame.VIDEORESIZE:
                scaled()

            if running:
                if event.type == pygame.USEREVENT:
                    moduls[6].szamlalo.current_seconds -= 1

                if moduls[6].szamlalo.current_seconds == 0:
                    boom()


    elif end_page:
        screen.fill((30, 17, 34))
        Image(bomb_pos_x, bomb_pos_y, il.start_background_img, g_scale)
        Image(0, 0, il.background_img, screen_x, False)
        text_draw("Játék vége!", screen_x/2-120*g_scale, screen_y/2-200*g_scale)
        text_draw(f"Idõ: {moduls[6].szamlalo.current_seconds} másodperc",screen_x/2-180*g_scale, screen_y/2-100*g_scale)
        text_draw(f"Pontszám: {check_done_moduls_num()-1}", screen_x/2-120*g_scale, screen_y/2*g_scale)
        if explosion:
            text_draw("Felrobbantál!", screen_x/2-120*g_scale, screen_y/2+100*g_scale)

        if back_button.puss_button_draw(il.back_le):
            end_page = False
            start_page = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    end_page = False
                    start_page = True

            elif event.type == pygame.VIDEORESIZE:
                scaled()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.VIDEORESIZE:
            scaled()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()