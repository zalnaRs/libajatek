import os
import random as r
from sys import exit
import pygame
import defs as f

# Állandok

changing_colors = [(255, 0, 0), (255, 135, 35), (235, 35, 200)]
changing_back_color = [(155, 0, 40), (210, 80, 25), (135, 35, 200)]

logo = pygame.image.load("logo_32x32.png")
pygame.display.set_icon(logo)
basic_x = 1048 # 1280
basic_y = 691 # 720

start_page = True
hiba = False
menu = False
game = False
explosion = False
end_page = False
running = False
scaling = False
scaling_index = None
szintek = [True, False, False, False]

pygame.init()
pygame.mixer.init()
channelhonk = pygame.mixer.Channel(0)
channelboom = pygame.mixer.Channel(1)
#info = pygame.display.Info() (.current_w, .current_h)
# (basic_x+232, basic_y+24)
screen = pygame.display.set_mode((basic_x, basic_y), pygame.RESIZABLE)
pygame.display.set_caption("Keep Honking and Nobody Explodes")
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)

def scaled(update:bool = True):
    global global_scaling, pos_order, screen_x, screen_y, bomb_pos_x, bomb_pos_y, running

    screen_x, screen_y = screen.get_size()

    if screen_x < basic_x:
        screen_x = basic_x
    if screen_y < basic_y:
        screen_y = basic_y

    scale_x = screen_x//basic_x
    scale_y = screen_y//basic_y

    if scale_x < scale_y:
        global_scaling = scale_x

    else:
        global_scaling = scale_y

    bomb_pos_x = (screen_x - basic_x*global_scaling)//2 # 116
    bomb_pos_y = (screen_y - basic_y*global_scaling)//2 # 12

    # ([197, 81], [528, 81], [859, 81], [197, 416], [528, 416], [859, 416])
    pos_order = ((bomb_pos_x+81*global_scaling, bomb_pos_y+66*global_scaling), (bomb_pos_x+412*global_scaling, bomb_pos_y+66*global_scaling), (bomb_pos_x+743*global_scaling, bomb_pos_y+66*global_scaling), (bomb_pos_x+81*global_scaling, bomb_pos_y+401*global_scaling), (bomb_pos_x+412*global_scaling, bomb_pos_y+401*global_scaling), (bomb_pos_x+743*global_scaling, bomb_pos_y+401*global_scaling))

    if update:
        global resume_button, quit_button, start_button, back_button, sz1_button, sz2_button, sz3_button, sz4_button, left_button, right_button, csapat_input

        resume_button = Button(bomb_pos_x+304*global_scaling, bomb_pos_y+228*global_scaling, resume_img, 10*global_scaling)
        quit_button = Button(bomb_pos_x+394*global_scaling, bomb_pos_y+378*global_scaling, quit_img, 10*global_scaling)
        start_button = Button(bomb_pos_x+363*global_scaling, bomb_pos_y+288*global_scaling, start_img, 10*global_scaling)
        back_button = Button(bomb_pos_x, bomb_pos_y+8*global_scaling, back_img, 5*global_scaling)
        sz1_button = Button(bomb_pos_x+46*global_scaling, bomb_pos_y+68*global_scaling, sz1_img, 5*global_scaling)
        sz2_button = Button(bomb_pos_x+44*global_scaling, bomb_pos_y+228*global_scaling, sz2_img, 5*global_scaling)
        sz3_button = Button(bomb_pos_x+44*global_scaling, bomb_pos_y+388*global_scaling, sz3_img, 5*global_scaling)
        sz4_button = Button(bomb_pos_x+44*global_scaling, bomb_pos_y+548*global_scaling, sz4_img, 5*global_scaling)
        left_button = Button(bomb_pos_x+5*global_scaling, bomb_pos_y+282*global_scaling, left_img, 4*global_scaling)
        right_button = Button(bomb_pos_x+basic_x-19*4*global_scaling, bomb_pos_y+286*global_scaling, right_img, 4*global_scaling)

        try:
            save = csapat_input.buffer
        except:
            save = ""

        csapat_input = Input(bomb_pos_x+384*global_scaling, bomb_pos_y+218*global_scaling, 200*global_scaling, 40*global_scaling, 28*global_scaling)
        csapat_input.buffer = save

        if running:
            global modulok, not_use_m, jellem


            jellem.pos_list = []
            for i in range(len(jellem.kijelolve)):
                if i == 1 or i == 3:
                    x_bonus = 399*jellem.scaling

                else:
                    x_bonus = 0

                if i >= 2:
                    y_bonus = 681*jellem.scaling

                else:
                    y_bonus = 0

                jellem.pos_list.append((bomb_pos_x+225*jellem.scaling+x_bonus, bomb_pos_y+3*jellem.scaling+y_bonus))

            jellem.matrica_buttons = []
            for i in range(len(jellem.current_matrica)):
                jellem.matrica_buttons.append(Button(jellem.pos_list[jellem.current_matrica[i][0]][0], jellem.pos_list[jellem.current_matrica[i][0]][1], jellem.current_matrica[i][1], jellem.scaling))


            for i in range(len(modulok)):
                if i not in not_use_m:
                    modulok[i].pos = pos_order[modulok[i].index]

                    #0: SimaDrót; 1: KomplexKábel; 2: Gomb; 3: Jelszó; 4: Libamondja; 5: Kérdés; 6: Idözítő

                    if i == 1:
                        for j in range(len(modulok[1].kabelek)):
                            modulok[1].num_kabel[j] = Button(modulok[1].pos[0] + 22*modulok[1].scaling + 28 * j*modulok[1].scaling, modulok[1].pos[1] + 23*modulok[1].scaling, modulok[1].num[modulok[1].kabelek[j][0]][0], modulok[1].scaling)

                    elif i == 2:
                        modulok[2].gomb = Button(modulok[2].pos[0] + 100*modulok[2].scaling, modulok[2].pos[1] + 39*modulok[2].scaling, modulok[2].colors[modulok[2].gomb_data[0]][0], modulok[2].scaling)

                    elif i == 3:
                        modulok[3].rect = pygame.Rect(modulok[3].pos[0]+71*modulok[3].scaling, modulok[3].pos[1]+171*modulok[3].scaling, 82*modulok[3].scaling, 25*modulok[3].scaling)
                        save = modulok[3].input.buffer
                        modulok[3].input = Input(modulok[3].rect.x, modulok[3].rect.y, 82*modulok[3].scaling, 25*modulok[3].scaling, 16*modulok[3].scaling, True)
                        modulok[3].input.buffer = save

                    elif i == 4:
                        modulok[4].buttons = []
                        for j in range(4):
                            if j % 2 == 0:
                                bonus = 0

                            else:
                                bonus = 4

                            modulok[4].buttons.append(Button(modulok[4].pos[0]+modulok[4].pos_bonus[j][0]*modulok[4].scaling, modulok[4].pos[1]+modulok[4].pos_bonus[j][1]*modulok[4].scaling, modulok[4].szinek[modulok[4].gombok[j]+bonus][0], modulok[4].scaling))

                    elif i == 5:
                        for j in range(len(modulok[5].gombok)):
                            if j > 1:
                                half = 5*modulok[5].scaling

                            else:
                                half = 0

                            modulok[5].gombok[j] = Button(modulok[5].pos[0]+23*modulok[5].scaling+48*j*modulok[5].scaling+half, modulok[5].pos[1]+139, modulok[5].betuk[j][0], modulok[5].scaling)

                    elif i == 6:
                        modulok[6].szamlalo = Timer(modulok[6].pos[0]+55*modulok[6].scaling, modulok[6].pos[1]+113*modulok[6].scaling, 36*modulok[6].scaling, modulok[6].szamlalo.current_seconds)

scaled(False)

# Osztályok

class Image:
    def __init__(self, x: int, y: int, image: pygame.surface.Surface, scale: float|int = 1, delay: bool = False, trans: tuple[bool, int] = (False, 255)):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        if trans[0]:
            self.image.set_alpha(trans[1])
        if not delay:
            screen.blit(self.image, (self.rect.x, self.rect.y))

    def delay_draw(self):
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
                    modulok[6].szamlalo.current_seconds -= 1

        if self.active:
            color = active_color
        else:
            color = passive_color

        pygame.draw.rect(screen, background, self.rect)
        pygame.draw.rect(screen, color, self.rect, 2)
        text_draw(self.buffer, self.rect.x + plus_x, self.rect.y + plus_y, text_color, pygame.font.Font("Grand9K Pixel.ttf", self.text_size))

        return self.value


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


def change_image(x: int, y: int, images: tuple[pygame.surface.Surface], scale: float|int = 1, close: bool = None):
    pos = pygame.mouse.get_pos()

    alap = Image(x, y, images[0], scale)

    if close is not None and len(images) > 2 and close:
        Image(x, y, images[2], scale)

    elif alap.rect.collidepoint(pos):
        Image(x, y, images[1], scale)


class SimaDrot:
    def __init__(self, index: int, image: pygame.surface.Surface, pos:tuple=(0, 0), done:bool=False, scaling:float|int = 1) -> None:
        self.pos = pos
        self.scaling = scaling
        self.index = index
        self.image = image
        self.done = done

        self.colors = (
        (fekete_drot_img, fekete_drot_action), (kek_drot_img, kek_drot_action), (piros_drot_img, piros_drot_action),
        (sarga_drot_img, sarga_drot_action))
        self.drotok = f.generate_drotok()
        self.animate_button = None

        self.drotok_color = []

        for i in range(len(self.drotok)):
            if self.drotok[i] is not None:
                self.drotok_color.append(self.drotok[i][0])

        if f.count(self.drotok_color, 2) >= 2:
            if szeria_root[1] == 3:
                self.correct = 3

            elif szeria_root[1] % 2 == 0 and matricak[2]:
                self.correct = 2

            elif szeria_root[1] % 2 == 1:
                self.correct = 3

            elif matricak[2]:
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

        elif self.drotok_color[2] == 0 and elemek[2:4] == [True, True]:
            self.correct = 0

        elif f.count(self.drotok_color, 1) == 2 and f.count(self.drotok_color, 2) == 0:
            self.correct = 1

        elif f.count(self.drotok_color, 2) == 1:
            self.correct = 3

        elif f.count(self.drotok_color, 0) == 0:
            if szeria_root[1] == 6:
                self.correct = 0

            elif elemek[0:2] == [True, True]:
                self.correct = 1

            else:
                self.correct = 3

        elif self.drotok_color[0] == 3 and matricak[1]:
            self.correct = 3

        elif True not in matricak:
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


class KomplexKabel:
    def __init__(self, index: int, image: pygame.surface.Surface, pos:tuple=(0, 0), done:bool=False, scaling:float|int = 1) -> None:
        self.pos = pos
        self.scaling = scaling
        self.index = index
        self.image = image
        self.done = done

        self.num = ((kabel_1_img, kabel_1_action), (kabel_2_img, kabel_2_action), (kabel_3_img, kabel_3_action),
                    (kabel_4_img, kabel_4_action))
        self.kabelek = []
        for _ in range(6):
            self.kabelek.append([r.randint(0, 3), False])

        self.first = 5
        self.second = 4
        self.third = 3
        self.fourth = 2
        self.fifth = 1
        self.sixth = 0
        self.num_kabel = [self.sixth, self.fifth, self.fourth, self.third, self.second, self.first]

        self.cut_them = []
        self.feher = None

        # sárga lap
        if szeria_root[1] == 5:
            self.cut_them.append(self.second)

        else:
            if True in elemek:
                self.feher = 1

            self.cut_them.append(self.sixth)

        # zöld lap
        if szeria_root[1] == 3 or szeria_root[1] == 9:
            self.cut_them.append(self.fourth)

        elif szeria_root[1] == 4:
            self.cut_them.append(self.third)

        elif matricak[2] or szeria_root[1] == 8:
            self.cut_them.append(self.third)

        else:
            if True not in elemek:
                self.feher = 4

            if True not in matricak:
                self.cut_them.append(self.third)

            else:
                self.cut_them.append(self.fourth)

        # fehér 4. oldal
        if self.feher == 1:
            if szeria_root[1] > 7:
                self.cut_them.append(self.first)

            elif matricak[0]:
                self.cut_them.append(self.first)

            elif szeria_root[1] < 5:
                self.cut_them.append(self.fifth)

            else:
                self.feher = 4

        if self.feher == 4:
            if szeria_root[1] < 5:
                current_root = szeria_root[1] + 5

            else:
                current_root = szeria_root[1]

            if current_root == 5:
                self.cut_them.append(self.first)

            elif current_root == 6:
                self.cut_them.append(self.fifth)

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


class Gomb:
    def __init__(self, index: int, image: pygame.surface.Surface, pos:tuple=(0, 0), done:bool=False, scaling:float|int = 1) -> None:
        self.pos = pos
        self.scaling = scaling
        self.index = index
        self.image = image
        self.done = done

        self.colors = ((kek_gomb_img, kek_gomb_action), (piros_gomb_img, piros_gomb_action), (zold_gomb_img, zold_gomb_action))
        self.symbols = (lud_szimbolum, talp_szimbolum, tojas_szimbolum)
        self.gomb_data = (r.randint(0, 2), r.randint(0, 2))

        self.puss = None
        if self.gomb_data[0] == 0 and f.count(elemek[0:2], True) > 0:
            self.puss = True

        elif spec_chart and self.gomb_data[0] != 1 and self.gomb_data[1] != 2:
            self.puss = False

        elif True not in elemek and self.gomb_data[1] != 1:
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

            elif True not in elemek:
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
                self.time_limit = modulok[6].szamlalo.current_seconds - 2

            if self.time_limit >= modulok[6].szamlalo.current_seconds:
                boom()

        if allapot[0]:
            if self.puss:
                if self.time_color == modulok[6].szamlalo.changing_ind:
                    self.done = allapot[0]

                else:
                    boom()

            else:
                self.done = allapot[0]


class Kerdes:
    def __init__(self, index:int, image:pygame.surface.Surface, pos:tuple=(0, 0), done:bool=False, scaling:float|int = 1) -> None:
        self.pos = pos
        self.scaling = scaling
        self.index = index
        self.image = image
        self.done = done

        self.betuk = ((a_gomb_img, a_gomb_action), (b_gomb_img, b_gomb_action), (c_gomb_img, c_gomb_action), (d_gomb_img, d_gomb_action))
        self.progress = (progress_0_img, progress_1_img, progress_2_img, progress_3_img, progress_4_img)
        self.kerdesek = (("Melyik szín, jelenik meg gyakran Szent Mártont ábrázoló képeken?",10),
                        ("Melyik a helyes válasz? ",18),
                        ("Melyik országnak szolgált katonaként Szent Márton?",13),
                        ("Milyen zöldséget szoktak libasülthöz adni?",13),
                        ("Mi Szent Márton egyik legismertebb tulajdonsága?",13),
                        ("Szent Mártont minek a védõszentje?",13),
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


class Jelszo:
    def __init__(self, index:int, image:pygame.surface.Surface, pos:tuple=(0, 0), done:bool=False, scaling:float|int = 1) -> None:
        self.pos = pos
        self.scaling = scaling
        self.index = index
        self.image = image
        self.done = done

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


class LibaMondja:
    def __init__(self, index:int, image:pygame.surface.Surface, pos:tuple=(0, 0), done:bool=False, scaling:float|int = 1) -> None:
        self.pos = pos
        self.scaling = scaling
        self.index = index
        self.image = image
        self.done = done

        # 0-3: allo; 4-7: fekvo
        # 0: kék; 1: piros; 2: sárga; 3: zöld
        self.szinek = ((allo_kek_img, allo_kek_img_action), (allo_piros_img, allo_piros_img_action), (allo_sarga_img, allo_sarga_img_action), (allo_zold_img, allo_zold_img_action), (fekvo_kek_img, fekvo_kek_img_action), (fekvo_piros_img, fekvo_piros_img_action), (fekvo_sarga_img, fekvo_sarga_img_action), (fekvo_zold_img, fekvo_zold_img_action))
        self.make = True
        self.voices = honking
        self.play = False
        self.round = 0

    def draw(self):
        modul_draw(self)

        if self.make:
            self.limit = time
            self.round += 1
            self.honk = r.randint(1,4)
            self.start = modulok[6].szamlalo.current_seconds - 2
            channelhonk.pause()
            self.gombok = [None, None, None, None]

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

            self.pos_bonus = ((9, 9), (77, 9), (152, 77), (9, 152))
            self.buttons = []
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
            if self.start == modulok[6].szamlalo.current_seconds:
                if not self.play:
                    self.start = modulok[6].szamlalo.current_seconds-(self.honk+2)
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

        if self.szamlalo.current_seconds == 0:
            boom()


class Egyebek:
    def __init__(self, elem, matrica, scaling:float|int = 1) -> None:
        self.scaling = scaling
        self.elemek = elem
        self.matricak = matrica

        self.kijelolve = (szeriaszam_kijelolve, matrica_fel_kijelolve, matrica_le_kijelolve, matrica_le_kijelolve)

        self.pos_list = []
        for i in range(len(self.kijelolve)):
            if i == 1 or i == 3:
                x_bonus = 399*self.scaling

            else:
                x_bonus = 0

            if i >= 2:
                y_bonus = 681*self.scaling

            else:
                y_bonus = 0

            self.pos_list.append((bomb_pos_x+225*self.scaling+x_bonus, bomb_pos_y+3*self.scaling+y_bonus))

        r_index = []
        for i in range(len(self.matricak)):
            r_index.append(i+1)

        self.nagy_matricak = (nagy_szeria_matrica_img, nagy_feher_matrica_img, nagy_narancs_matrica_img, nagy_fekete_matrica_img)
        self.current_matrica= [(0, szeriaszam_img, 0)]

        for i in range(len(self.matricak)):
            if self.matricak[i]:
                rand_i = r.randint(0, len(r_index)-1)
                if r_index[rand_i] == 1:
                    image = matrica_fel_img
                else:
                    image = matrica_le_img

                self.current_matrica.append((r_index[rand_i], image, i+1))
                del r_index[rand_i]

        self.matrica_buttons = []
        for i in range(len(self.current_matrica)):
            self.matrica_buttons.append(Button(self.pos_list[self.current_matrica[i][0]][0], self.pos_list[self.current_matrica[i][0]][1], self.current_matrica[i][1], self.scaling))

        self.elemek_img = (elem_bal_img, elem_jobb_img)

    def draw(self):
        global scaling, scaling_index

        for i in range(len(self.matrica_buttons)):
            if self.matrica_buttons[i].pos_button_draw(self.kijelolve[self.current_matrica[i][0]]):
                scaling = True
                scaling_index = i


        for i in range(len(self.elemek)):
            if self.elemek[i]:
                if i == 1 or i == 3:
                    y_bonus = 335*self.scaling

                else:
                    y_bonus = 0

                if i >= 2:
                    x_bonus = 1023*self.scaling

                else:
                    x_bonus = 0

                Image(bomb_pos_x*self.scaling+x_bonus, bomb_pos_y+130*self.scaling+y_bonus, self.elemek_img[i//2], self.scaling)


# Betöltés

background_img = pygame.image.load("Backs/background.png").convert_alpha()
start_background_img = pygame.image.load("Backs/start.png").convert_alpha()

resume_img = pygame.image.load("Buttons/resume_button.png").convert_alpha()
resume_le = pygame.image.load("Buttons/resume_button_le.png").convert_alpha()
quit_img = pygame.image.load("Buttons/quit_button.png").convert_alpha()
quit_le = pygame.image.load("Buttons/quit_button_le.png").convert_alpha()
start_img = pygame.image.load("Buttons/start_button.png").convert_alpha()
start_le = pygame.image.load("Buttons/start_button_le.png").convert_alpha()
back_img = pygame.image.load("Buttons/back_button.png").convert_alpha()
back_le = pygame.image.load("Buttons/back_button_le.png").convert_alpha()
sz1_img = pygame.image.load("Buttons/1_button.png").convert_alpha()
sz1_le = pygame.image.load("Buttons/1_button_le.png").convert_alpha()
sz2_img = pygame.image.load("Buttons/2_button.png").convert_alpha()
sz2_le = pygame.image.load("Buttons/2_button_le.png").convert_alpha()
sz3_img = pygame.image.load("Buttons/3_button.png").convert_alpha()
sz3_le = pygame.image.load("Buttons/3_button_le.png").convert_alpha()
sz4_img = pygame.image.load("Buttons/4_button.png").convert_alpha()
sz4_le = pygame.image.load("Buttons/4_button_le.png").convert_alpha()
left_img = pygame.image.load("Buttons/balra.png").convert_alpha()
left_kijelolve = pygame.image.load("Buttons/balra_kijelolve.png").convert_alpha()
right_img = pygame.image.load("Buttons/jobbra.png").convert_alpha()
right_kijelolve = pygame.image.load("Buttons/jobbra_kijelolve.png").convert_alpha()

bomba_img = pygame.image.load("Backs/bomba_alap.png").convert_alpha()

sima_drot_modul_img = pygame.image.load("nat_drotok/drot_nat_224x224.png").convert_alpha()

fekete_drot_img = pygame.image.load("nat_drotok/fekete/fekete_alap.png").convert_alpha()
fekete_drot_action = (pygame.image.load("nat_drotok/fekete/fekete_kijelolve.png").convert_alpha(),
                      pygame.image.load("nat_drotok/fekete/fekete_vagas.png").convert_alpha(),
                      pygame.image.load("nat_drotok/fekete/fekete_kesz.png").convert_alpha())
kek_drot_img = pygame.image.load("nat_drotok/kek/kek_alap.png").convert_alpha()
kek_drot_action = (pygame.image.load("nat_drotok/kek/kek_kijelolve.png").convert_alpha(),
                   pygame.image.load("nat_drotok/kek/kek_vagas.png").convert_alpha(),
                   pygame.image.load("nat_drotok/kek/kek_kesz.png").convert_alpha())
piros_drot_img = pygame.image.load("nat_drotok/piros/piros_alap.png").convert_alpha()
piros_drot_action = (pygame.image.load("nat_drotok/piros/piros_kijelolve.png").convert_alpha(),
                     pygame.image.load("nat_drotok/piros/piros_vagas.png").convert_alpha(),
                     pygame.image.load("nat_drotok/piros/piros_kesz.png").convert_alpha())
sarga_drot_img = pygame.image.load("nat_drotok/sarga/sarga_alap.png").convert_alpha()
sarga_drot_action = (pygame.image.load("nat_drotok/sarga/sarga_kijelolve.png").convert_alpha(),
                     pygame.image.load("nat_drotok/sarga/sarga_vagas.png").convert_alpha(),
                     pygame.image.load("nat_drotok/sarga/sarga_kesz.png").convert_alpha())

komplex_kabel_modul_img = pygame.image.load("kom_kabel/kabel_kom_224x224.png").convert_alpha()

kabel_1_img = pygame.image.load("kom_kabel/1_kabel/1_alap.png").convert_alpha()
kabel_1_action = (pygame.image.load("kom_kabel/1_kabel/1_kijelolve.png").convert_alpha(),
                  pygame.image.load("kom_kabel/1_kabel/1_vagas.png").convert_alpha(),
                  pygame.image.load("kom_kabel/1_kabel/1_kesz.png").convert_alpha())
kabel_2_img = pygame.image.load("kom_kabel/2_kabel/2_alap.png").convert_alpha()
kabel_2_action = (pygame.image.load("kom_kabel/2_kabel/2_kijelolve.png").convert_alpha(),
                  pygame.image.load("kom_kabel/2_kabel/2_vagas.png").convert_alpha(),
                  pygame.image.load("kom_kabel/2_kabel/2_kesz.png").convert_alpha())
kabel_3_img = pygame.image.load("kom_kabel/3_kabel/3_alap.png").convert_alpha()
kabel_3_action = (pygame.image.load("kom_kabel/3_kabel/3_kijelolve.png").convert_alpha(),
                  pygame.image.load("kom_kabel/3_kabel/3_vagas.png").convert_alpha(),
                  pygame.image.load("kom_kabel/3_kabel/3_kesz.png").convert_alpha())
kabel_4_img = pygame.image.load("kom_kabel/4_kabel/4_alap.png").convert_alpha()
kabel_4_action = (pygame.image.load("kom_kabel/4_kabel/4_kijelolve.png").convert_alpha(),
                  pygame.image.load("kom_kabel/4_kabel/4_vagas.png").convert_alpha(),
                  pygame.image.load("kom_kabel/4_kabel/4_kesz.png").convert_alpha())

gomb_modul_img = pygame.image.load("gomb_modul/gomb_alap_224x224.png").convert_alpha()

kek_gomb_img = pygame.image.load("gomb_modul/kek/kek_sima.png").convert_alpha()
kek_gomb_action = (pygame.image.load("gomb_modul/kek/kek_kijelol.png").convert_alpha(),
                   pygame.image.load("gomb_modul/kek/kek_benyomva.png").convert_alpha(),
                   pygame.image.load("gomb_modul/kek/kek_kesz.png").convert_alpha())
piros_gomb_img = pygame.image.load("gomb_modul/piros/piros_sima.png").convert_alpha()
piros_gomb_action = (pygame.image.load("gomb_modul/piros/piros_kijelol.png").convert_alpha(),
                     pygame.image.load("gomb_modul/piros/piros_benyomva.png").convert_alpha(),
                     pygame.image.load("gomb_modul/piros/piros_kesz.png").convert_alpha())
zold_gomb_img = pygame.image.load("gomb_modul/zold/zold_sima.png").convert_alpha()
zold_gomb_action = (pygame.image.load("gomb_modul/zold/zold_kijelol.png").convert_alpha(),
                    pygame.image.load("gomb_modul/zold/zold_benyomva.png").convert_alpha(),
                    pygame.image.load("gomb_modul/zold/zold_kesz.png").convert_alpha())

lud_szimbolum = pygame.image.load("gomb_modul/szimbolumok/minta_lud.png").convert_alpha()
talp_szimbolum = pygame.image.load("gomb_modul/szimbolumok/minta_talp.png").convert_alpha()
tojas_szimbolum = pygame.image.load("gomb_modul/szimbolumok/minta_tojas.png").convert_alpha()

kerdes_modul_img = pygame.image.load("kerdesek/kerdesek_panel.png").convert_alpha()

a_gomb_img = pygame.image.load("kerdesek/A/a_alap.png").convert_alpha()
a_gomb_action = (pygame.image.load("kerdesek/A/a_kijelol.png").convert_alpha(), pygame.image.load("kerdesek/A/a_benyom.png").convert_alpha())
b_gomb_img = pygame.image.load("kerdesek/B/b_alap.png").convert_alpha()
b_gomb_action = (pygame.image.load("kerdesek/B/b_kijelol.png").convert_alpha(), pygame.image.load("kerdesek/B/b_benyom.png").convert_alpha())
c_gomb_img = pygame.image.load("kerdesek/C/c_alap.png").convert_alpha()
c_gomb_action = (pygame.image.load("kerdesek/C/c_kijelol.png").convert_alpha(), pygame.image.load("kerdesek/C/c_benyom.png").convert_alpha())
d_gomb_img = pygame.image.load("kerdesek/D/d_alap.png").convert_alpha()
d_gomb_action = (pygame.image.load("kerdesek/D/d_kijelol.png").convert_alpha(), pygame.image.load("kerdesek/D/d_benyom.png").convert_alpha())

progress_0_img = pygame.image.load("kerdesek/allapot/progress_0.png").convert_alpha()
progress_1_img = pygame.image.load("kerdesek/allapot/progress_1.png").convert_alpha()
progress_2_img = pygame.image.load("kerdesek/allapot/progress_2.png").convert_alpha()
progress_3_img = pygame.image.load("kerdesek/allapot/progress_3.png").convert_alpha()
progress_4_img = pygame.image.load("kerdesek/allapot/progress_4.png").convert_alpha()

jelszo_modul_img = pygame.image.load("jelszo/jelszo_modul.png").convert_alpha()

lud_mondja_modul_img = pygame.image.load("simon/szines.png").convert_alpha()

allo_kek_img = pygame.image.load("simon/allo/alap_kek_allo.png").convert_alpha()
allo_kek_img_action = (pygame.image.load("simon/allo/kijelolt_kek_allo.png").convert_alpha(), pygame.image.load("simon/allo/benyom_kek_allo.png").convert_alpha())
allo_piros_img = pygame.image.load("simon/allo/alap_piros_allo.png").convert_alpha()
allo_piros_img_action = (pygame.image.load("simon/allo/kijelolt_piros_allo.png").convert_alpha(), pygame.image.load("simon/allo/benyom_piros_allo.png").convert_alpha())
allo_sarga_img = pygame.image.load("simon/allo/alap_sarga_allo.png").convert_alpha()
allo_sarga_img_action = (pygame.image.load("simon/allo/kijelolt_sarga_allo.png").convert_alpha(), pygame.image.load("simon/allo/benyom_sarga_allo.png").convert_alpha())
allo_zold_img = pygame.image.load("simon/allo/alap_zold_allo.png").convert_alpha()
allo_zold_img_action = (pygame.image.load("simon/allo/kijelolt_zold_allo.png").convert_alpha(), pygame.image.load("simon/allo/benyom_zold_allo.png").convert_alpha())

fekvo_kek_img = pygame.image.load("simon/fekvo/alap_kek_fekvo.png").convert_alpha()
fekvo_kek_img_action = (pygame.image.load("simon/fekvo/kijelolt_kek_fekvo.png").convert_alpha(), pygame.image.load("simon/fekvo/benyom_kek_fekvo.png").convert_alpha())
fekvo_piros_img = pygame.image.load("simon/fekvo/alap_piros_fekvo.png").convert_alpha()
fekvo_piros_img_action = (pygame.image.load("simon/fekvo/kijelolt_piros_fekvo.png").convert_alpha(), pygame.image.load("simon/fekvo/benyom_piros_fekvo.png").convert_alpha())
fekvo_sarga_img = pygame.image.load("simon/fekvo/alap_sarga_fekvo.png").convert_alpha()
fekvo_sarga_img_action = (pygame.image.load("simon/fekvo/kijelolt_sarga_fekvo.png").convert_alpha(), pygame.image.load("simon/fekvo/benyom_sarga_fekvo.png").convert_alpha())
fekvo_zold_img = pygame.image.load("simon/fekvo/alap_zold_fekvo.png").convert_alpha()
fekvo_zold_img_action = (pygame.image.load("simon/fekvo/kijelolt_zold_fekvo.png").convert_alpha(), pygame.image.load("simon/fekvo/benyom_zold_fekvo.png").convert_alpha())

visszaszamlalo_img = pygame.image.load("idozito/idozito.png").convert_alpha()

szeriaszam_img = pygame.image.load("egyeb/matricak_alap/szeria_alap.png").convert_alpha()
szeriaszam_kijelolve = pygame.image.load("egyeb/matricak_alap/szeria_alap_kijelolve.png").convert_alpha()

nagy_szeria_matrica_img = pygame.image.load("egyeb/matricak_nagyitva/szeria_nagyitva.png").convert_alpha()

matrica_fel_img = pygame.image.load("egyeb/matricak_alap/matrica_fel.png").convert_alpha()
matrica_fel_kijelolve = pygame.image.load("egyeb/matricak_alap/matrica_fel_kijelolve.png").convert_alpha()
matrica_le_img = pygame.image.load("egyeb/matricak_alap/matrica_le.png").convert_alpha()
matrica_le_kijelolve = pygame.image.load("egyeb/matricak_alap/matrica_le_kijelolve.png").convert_alpha()

nagy_feher_matrica_img = pygame.image.load("egyeb/matricak_nagyitva/feher.png").convert_alpha()
nagy_fekete_matrica_img = pygame.image.load("egyeb/matricak_nagyitva/fekete.png").convert_alpha()
nagy_narancs_matrica_img = pygame.image.load("egyeb/matricak_nagyitva/narancs.png").convert_alpha()

elem_jobb_img = pygame.image.load("egyeb/elemek/elem_jobb.png").convert_alpha()
elem_bal_img = pygame.image.load("egyeb/elemek/elem_bal.png").convert_alpha()

jel_alap = pygame.image.load("Jelzok/alap_keret.png").convert_alpha()
jel_kijel = pygame.image.load("Jelzok/kijelol_keret.png").convert_alpha()
# jel_kat = pygame.image.load("Jelzok/kat_keret.png").convert_alpha()
jel_kesz = pygame.image.load("Jelzok/kesz_keret.png").convert_alpha()

jelek = (jel_alap, jel_kijel, jel_kesz)

explosion_sound = pygame.mixer.Sound("Hangok/explosion.mp3")
honk_1 = pygame.mixer.Sound("Hangok/1_honking.mp3")
honk_2 = pygame.mixer.Sound("Hangok/2_honking.mp3")
honk_3 = pygame.mixer.Sound("Hangok/3_honking.mp3")
honk_4 = pygame.mixer.Sound("Hangok/4_honking.mp3")
honking = (honk_1, honk_2, honk_3, honk_4)
# honk_1.play()


def generate_bomb():
    # Változok

    global spec_chart, szeria_root, matricak, elemek, jellem

    spec_chart = bool(r.randint(0, 1))
    szeria_root = f.szerianumber(spec_chart)
    # 0 fehér; 1 narancssárga; 2 fekete
    matricak = [bool(r.randint(0, 1)), bool(r.randint(0, 1)), bool(r.randint(0, 1))]
    # 0-1: balra; 2-3: jobbra
    elemek = [bool(r.randint(0, 1)), bool(r.randint(0, 1)), bool(r.randint(0, 1)), bool(r.randint(0, 1))]

    jellem = Egyebek(elemek, matricak)

    #0: SimaDrót; 1: KomplexKábel; 2: Gomb; 3: Jelszó; 4: Libamondja; 5: Kérdés; 6: Idözítő
    return(SimaDrot(None, sima_drot_modul_img, scaling=global_scaling), KomplexKabel(None, komplex_kabel_modul_img, scaling=global_scaling), Gomb(None, gomb_modul_img, scaling=global_scaling), Jelszo(None, jelszo_modul_img, scaling=global_scaling), LibaMondja(None, lud_mondja_modul_img, scaling=global_scaling), Kerdes(None, kerdes_modul_img, scaling=global_scaling), Idozito(None, visszaszamlalo_img, scaling=global_scaling))


def test_write():
    print("Szériaszám: "+szeria_root[0])

    bal = 0
    jobb = 0
    for i in range(len(elemek)):
        if True == elemek[i]:
            if i < 2:
                bal += 1

            else:
                jobb += 1
    print(f"Elemek: bal:{bal}; jobb:{jobb}")

    print("Matricák:")
    for i in range(len(matricak)):
        if True == matricak[i]:
            if i == 0:
                print("-fehér")

            elif i == 1:
                print("-narancssárga")

            else:
                print("-fekete")

# a modulok szét szórása
def random_pos_modul(modulok:list, not_use:list):
    r_list = []
    for i in range(6):
        r_list.append(i)

    for i in range(len(modulok)):
        if i not in not_use:
            rand_index = r.randint(0, len(r_list) - 1)
            modulok[i].index = r_list[rand_index]
            del r_list[rand_index]


def modul_draw(self):
    """
    kirajzolja a modult, figyelembe veszi hogy kész van-e?
    """
    global modul_kesz, global_scaling, pos_order, jelek

    modul_kesz[self.index] = self.done

    if self.index is not None:
        self.pos = pos_order[self.index]


    screen.blit(self.image, self.pos)
    change_image(self.pos[0] + 1, self.pos[1] + 1, jelek, global_scaling, self.done)

# Szöveg

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

def check_kesz_modulok_szama():
    """
    Megnézi, hogy mennyi kész modul van.
    """

    global modul_kesz

    j = 0
    for modul in modul_kesz:
        if modul:
            j += 1

    return j

def check_if_game_done():
    """
    Ha az összes modul kész van akkor lefutatja a end_game-t.
    """
    if check_kesz_modulok_szama() != len(modulok)-len(not_use_m):
        return False

    channelhonk.pause()
    end_game()
    return True

def end_game():
    """
    Ha a játék véget ér, akkor ez a függvény fut le.
    :return: None
    """
    global game, running, menu, end_page, matricak, szeria_root, elemek
    game = False
    running = False
    menu = False
    end_page = True

    for i in range(len(szintek)):
        if szintek[i] is True:
            szint = i + 1

    file = open(rf"eredmenyek/{csapat_input.value}_{szint}.txt", "w", encoding="UTF-8")
    # TODO: normális pontozás
    file.write(f"--------------\n{csapat_input.value}\n--------------\nIdő: {modulok[6].szamlalo.current_seconds}\nPontszám: {check_kesz_modulok_szama()-1}\n")
    if explosion:
        file.write(f"Felrobbant.\n")
    file.write(f"--------------\n")

    file.write(f"Szériaszám: {szeria_root[0]}\n")

    bal = 0
    jobb = 0
    for i in range(len(elemek)):
        if True == elemek[i]:
            if i < 2:
                bal += 1

            else:
                jobb += 1
    file.write(f"Elemek: bal:{bal}; jobb:{jobb}\n")

    file.write("Matricák:\n")
    for i in range(len(matricak)):
        if True == matricak[i]:
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
        if scaling:

            Image(0, 0 , background_img, screen_x)
            Image(bomb_pos_x+137*global_scaling, bomb_pos_y+162*global_scaling, jellem.nagy_matricak[jellem.current_matrica[scaling_index][2]], global_scaling)

            if jellem.current_matrica[scaling_index][2] == 0:
                text_draw(szeria_root[0], bomb_pos_x+254*global_scaling, bomb_pos_y+340*global_scaling, (255,255,255), pygame.font.Font(family, 100*global_scaling))

            if len(jellem.current_matrica) != 1:
                if left_button.pos_button_draw(left_kijelolve):
                    if scaling_index - 1 == -1:
                        scaling_index = len(jellem.current_matrica)-1

                    else:
                        scaling_index -= 1

                if right_button.pos_button_draw(right_kijelolve):
                    if scaling_index + 1 == len(jellem.current_matrica):
                        scaling_index = 0

                    else:
                        scaling_index += 1

            if back_button.puss_button_draw(back_le):
                scaling = False
                modulok[4].start = modulok[6].szamlalo.current_seconds - 1

        else:
            # 141, 25
            Image(bomb_pos_x+25*global_scaling, bomb_pos_y+10*global_scaling, bomba_img, global_scaling)

            for i in range(len(modulok)):
                if (len(modulok)-1)-i not in not_use_m:
                    modulok[(len(modulok)-1)-i].draw()

            jellem.draw()

            check_if_game_done()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if scaling:
                        scaling = False
                        modulok[4].start = modulok[6].szamlalo.current_seconds - 1
                    else:
                        game = False
                        menu = True

            elif event.type == pygame.VIDEORESIZE:
                scaled()

            if event.type == pygame.USEREVENT:
                modulok[6].szamlalo.current_seconds -= 1


    elif start_page:
        screen.fill((30, 17, 34))
        Image(bomb_pos_x, bomb_pos_y, start_background_img, global_scaling)

        csapat_input.input_draw(5, -2)

        if start_button.puss_button_draw(start_le):
            if csapat_input.buffer != "":

                modulok = generate_bomb()
                test_write()

                modul_kesz = []
                for _ in range(len(modulok)):
                    modul_kesz.append(None)

                csapat_input.value = csapat_input.buffer
                start_page = False
                game = True
                running = True
                hiba = False

                #0: SimaDrót; 1: KomplexKábel; 2: Gomb; 3: Jelszó; 4: Libamondja; 5: Kérdés; 6: Idözítő
                if szintek[0]:
                    time = 480
                    not_use_m = [0, 3, 2]
                elif szintek[1]:
                    time = 180
                    not_use_m = [1, 3, 5]
                elif szintek[2]:
                    time = 300
                    not_use_m = [0]
                elif szintek[3]:
                    time = 180
                    not_use_m = [4]

                random_pos_modul(modulok, not_use_m)

            else:
                hiba = True

        if hiba and csapat_input.buffer == "":
            text_draw("Nem adtad még meg az osztályt!", 450*global_scaling, 180*global_scaling, (255, 0, 0), pygame.font.Font(family, 20*global_scaling))

        if sz1_button.puss_button_draw(sz1_le, szintek[0]):
            szintek = [True, False, False, False]

        if sz2_button.puss_button_draw(sz2_le, szintek[1]):
            szintek = [False, True, False, False]

        if sz3_button.puss_button_draw(sz3_le, szintek[2]):
            szintek = [False, False, True, False]

        if sz4_button.puss_button_draw(sz4_le, szintek[3]):
            szintek = [False, False, False, True]

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
        Image(bomb_pos_x, bomb_pos_y, start_background_img, global_scaling)
        Image(0, 0, background_img, screen_x)

        if quit_button.puss_button_draw(quit_le):
            break

        if resume_button.puss_button_draw(resume_le):
            menu = False

            if running:
                game = True
                modulok[4].start = modulok[6].szamlalo.current_seconds - 1
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

            if running and event.type == pygame.USEREVENT:
                modulok[6].szamlalo.current_seconds -= 1


    elif end_page:
        screen.fill((30, 17, 34))
        Image(bomb_pos_x, bomb_pos_y, start_background_img, global_scaling)
        Image(0, 0, background_img, screen_x, False)
        text_draw("Játék vége!", screen_x/2-120*global_scaling, screen_y/2-200*global_scaling)
        text_draw(f"Idõ: {modulok[6].szamlalo.current_seconds} másodperc",screen_x/2-180*global_scaling, screen_y/2-100*global_scaling)
        text_draw(f"Pontszám: {check_kesz_modulok_szama()-1}", screen_x/2-120*global_scaling, screen_y/2*global_scaling)
        if explosion:
            text_draw("Felrobbantál!", screen_x/2-120*global_scaling, screen_y/2+100*global_scaling)

        if back_button.puss_button_draw(back_le):
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
