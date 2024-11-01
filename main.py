import os
import random as r
from sys import exit
import pygame
import defs as f

# Állandok

pos_order = [(197, 81), (528, 81), (859, 81), (197, 416), (528, 416), (859, 416), ]
changing_colors = [(255, 0, 0), (255, 135, 35), (235, 35, 200)]

#logo = pygame.image.load("logo_128x128.png")
#pygame.display.set_icon(logo)
screen_x = 1280
screen_y = 720

# Változok

spec_chart = bool(r.randint(0, 1))
szeria_root = f.szerianumber(spec_chart)
# 0 piros; 1 narancssárga; 2 fekete
matricak = [bool(r.randint(0, 1)), bool(r.randint(0, 1)), bool(r.randint(0, 1))]
# 0-1: balra; 2-3: jobbra
elemek = [bool(r.randint(0, 1)), bool(r.randint(0, 1)), bool(r.randint(0, 1)), bool(r.randint(0, 1))]

time = 300
start_page = True
hiba = False
menu = False
game = False
explosion = False
end_page = False
running = False
scaling = False
szintek = [True, False, False, False]

pygame.init()
pygame.mixer.init()
#info = pygame.display.Info() (.current_w, .current_h)
screen = pygame.display.set_mode((screen_x, screen_y))
screen.fill((88, 88, 88))
pygame.display.set_caption("Keep Honking and Nobody Explodes")
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)


# Osztályok

class Image:
    def __init__(self, x: int, y: int, image: pygame.surface.Surface, scale: int = 1, delay: bool = False, trans: tuple[bool, int] = (False, 255)):
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
    def __init__(self, x: int, y: int, image: pygame.surface.Surface, scale: int = 1):
        width = image.get_width()
        height = image.get_height()
        self.scale = scale
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.click = False
        self.animate = 1

    def puss_button_draw(self, puss_data:tuple[int, int, pygame.surface.Surface, int], close:bool=None):
        action = False

        #egér helyzete:
        if close is not None and close:
            Image(puss_data[0], puss_data[1], puss_data[2], puss_data[3])

        else:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos) or self.click:
                if pygame.mouse.get_pressed()[0] == 1: #le van nyomva
                    self.click = True
                    Image(puss_data[0], puss_data[1], puss_data[2], puss_data[3])#mit jelenítsen meg helyete
                        

                elif pygame.mouse.get_pressed()[0] == 0 and self.click:
                    self.click = False
                    action = True
                    if close is not None:
                        close = True
                        self.click = True

            if not self.click:
                screen.blit(self.image, (self.rect.x, self.rect.y))
            
            if close is not None and close:
                Image(puss_data[0], puss_data[1], puss_data[2], puss_data[3])
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

    def simple_button_draw(self):
        action = False

        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))
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

                if running and event.type == pygame.USEREVENT:
                    ido.szamlalo.current_seconds -= 1

        if self.active:
            color = active_color
        else:
            color = passive_color

        pygame.draw.rect(screen, background, self.rect)
        pygame.draw.rect(screen, color, self.rect, 2)
        text_draw(self.buffer, self.rect.x + plus_x, self.rect.y + plus_y, text_color, pygame.font.Font("Grand9K Pixel.ttf", self.text_size))

        return self.value


class Timer:
    def __init__(self, x: int, y: int, time: int = 300) -> None:
        self.x = x
        self.y = y
        self.current_seconds = time
        self.changing_ind = 0

    def timer_draw(self, color: tuple[int, int, int] = (255, 255, 255)):
        display_minutes = self.current_seconds // 60
        display_seconds = self.current_seconds % 60

        self.changing_ind = (self.current_seconds // 5) % 3

        text_draw(f"{display_minutes:02}:{display_seconds:02}", self.x, self.y, color)


def change_image(x: int, y: int, images: tuple[pygame.surface.Surface], scale: int = 1, close: bool = None):
    pos = pygame.mouse.get_pos()

    alap = Image(x, y, images[0], scale)

    if close is not None and len(images) > 2 and close:
        Image(x, y, images[2], scale)

    elif alap.rect.collidepoint(pos):
        Image(x, y, images[1], scale)


class SimaDrot:
    def __init__(self, index: int, image: pygame.surface.Surface) -> None:
        self.pos = None
        self.index = index
        self.image = image
        self.done = False

        self.colors = (
        (fekete_drot_img, fekete_drot_action), (kek_drot_img, kek_drot_action), (piros_drot_img, piros_drot_action),
        (sarga_drot_img, sarga_drot_action))
        self.drotok = f.generate_drotok()
        self.animate_button = None

        self.drotok_color = []

        for i in range(len(self.drotok)):
            if self.drotok[i] is not None:
                self.drotok_color.append(self.drotok[i][0])

        if f.count(self.drotok, [2, False]) >= 2:
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

        elif f.count(self.drotok, [1, False]) == 2 and f.count(self.drotok, [2, False]) == 0:
            self.correct = 1

        elif f.count(self.drotok, [2, False]) == 1:
            self.correct = 3

        elif f.count(self.drotok, [0, False]) == 0:
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
                half = 6

            if self.drotok[i] is not None and self.done:
                if self.drotok[i][1]:
                    if self.animate_button is None:
                        self.animate_button = Button(self.pos[0] + 35, self.pos[1] + 34 + 28 * i + half, self.colors[self.drotok[i][0]][0])
                    self.animate_button.cable_draw(self.drotok[i][1], self.colors[self.drotok[i][0]][1])

                else:
                    Image(self.pos[0] + 35, self.pos[1] + 34 + 28 * i + half, self.colors[self.drotok[i][0]][0])

            elif self.drotok[i] is not None:
                self.drotok[i][1] = Button(self.pos[0] + 35, self.pos[1] + 34 + 28 * i + half, self.colors[self.drotok[i][0]][0]).cable_draw(self.drotok[i][1], self.colors[self.drotok[i][0]][1])
                if self.drotok[i][1]:
                    if i - c == self.correct:
                        self.done = self.drotok[i][1]

                    else:
                        boom()
                        # csak a teszt miat van a következő sor
                        self.done = True

            else:
                c += 1


class KomplexKabel:
    def __init__(self, index: int, image: pygame.surface.Surface) -> None:
        self.index = index
        self.pos = (0, 0)
        self.image = image
        self.done = False

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
        self.num_kabel = [self.sixth, self.fifth, self.fourth, self.third, self.second, self.first, ]

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
                self.feher = 4

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
                self.num_kabel[i] = Button(self.pos[0] + 22 + 28 * i, self.pos[1] + 23, self.num[self.kabelek[i][0]][0])

        for i in range(len(self.kabelek)):
            if self.done:
                if self.kabelek[i][1]:

                    for j in range(len(self.kabelek)):
                        if self.kabelek[j][1]:
                            self.num_kabel[i].cable_draw(self.kabelek[i][1], self.num[self.kabelek[i][0]][1])

                else:
                    Image(self.pos[0] + 22 + 28 * i, self.pos[1] + 23, self.num[self.kabelek[i][0]][0])

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
                        # csak a teszt miat van a következő 7 sor
                        c = 0
                        for j in range(len(self.kabelek)):
                            if self.kabelek[j][1]:
                                c += 1

                        if c == len(self.cut_them):
                            self.done = True


class Gomb:
    def __init__(self, index: int, image: pygame.surface.Surface) -> None:
        self.pos = (0, 0)
        self.index = index
        self.image = image
        self.done = False

        self.colors = (
        (kek_gomb_img, kek_gomb_action), (piros_gomb_img, piros_gomb_action), (zold_gomb_img, zold_gomb_action))
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
            self.gomb = Button(self.pos[0] + 100, self.pos[1] + 39, self.colors[self.gomb_data[0]][0])

        Image(self.pos[0] + 56, self.pos[1] + 159, self.symbols[self.gomb_data[1]])

        allapot = self.gomb.button_draw(self.colors[self.gomb_data[0]][1], self.done)
        if not self.puss and allapot[1]:
            if self.time_limit is None:
                self.time_limit = ido.szamlalo.current_seconds - 2

            if self.time_limit >= ido.szamlalo.current_seconds:
                boom()

        if allapot[0]:
            if self.puss:
                if self.time_color == ido.szamlalo.changing_ind:
                    self.done = allapot[0]

                else:
                    boom()

            else:
                self.done = allapot[0]


class Kerdes:
    def __init__(self, index:int, image:pygame.surface.Surface) -> None:
        self.pos = (0,0)
        self.index = index
        self.image = image
        self.done = False

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
                    half = 5

                else:
                    half = 0

                self.gombok[i] = Button(self.pos[0]+23+48*i+half, self.pos[1]+139, self.betuk[i][0])

        if self.done:
            for i in range(len(self.gombok)):
                if i > 1:
                    half = 5

                else:
                    half = 0
                
                Image(self.pos[0]+23+48*i+half, self.pos[1]+139, self.betuk[i][0])

            Image(self.pos[0]+22, self.pos[1]+198, self.progress[-1])
            text_draw("( =", self.pos[0]+78, self.pos[1]+32, (255,255,255), pygame.font.Font(family, 36))

        else:
            display_text(self.kerdesek[self.current_kerdesek[self.current_kerdes]][0], (self.pos[0]+37, self.pos[1]+32), self.pos[0]+190, pygame.font.Font(family, self.kerdesek[self.current_kerdesek[self.current_kerdes]][1]))
            Image(self.pos[0]+22, self.pos[1]+198, self.progress[self.current_kerdes])
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
    def __init__(self, index:int, image:pygame.surface.Surface) -> None:
        self.pos = (0,0)
        self.index = index
        self.image = image
        self.done = False

        self.jelszo = f.password()

    def draw(self):
        if self.pos == (0,0):
            make = True
        else:
            make = False

        modul_draw(self)

        if make:
            self.rect = pygame.Rect(self.pos[0]+71, self.pos[1]+171, 82, 25)
            self.input = Input(self.rect.x, self.rect.y, 82, 25, 16, True)

        for i in range(len(self.jelszo[1][0])):
            for j in range(len(self.jelszo[1])):
                if i == 0 or i == 3:
                    plus = 0
                else:
                    plus = 2
                text_draw(self.jelszo[1][j][i], self.pos[0]+25+40*j+plus, self.pos[1]+15+34*i, (57, 57, 57), pygame.font.Font(family, 21))

        if self.done:
            pygame.draw.rect(screen, (57, 35, 0), self.rect)
            pygame.draw.rect(screen, (31, 19, 0), self.rect, 2)
        else:
            self.input.input_draw(5, -1, (57, 35, 0), (255, 255, 255), (31, 19, 0), (255,255,255), pygame.Rect(self.pos[0], self.pos[1], 244, 244))

        if self.input.value != "":
            if self.input.value.lower() == self.jelszo[0]:
                self.done = True

            else:
                boom()


class LibaMondja:
    def __init__(self, index:int, image:pygame.surface.Surface) -> None:
        self.pos = (0,0)
        self.index = index
        self.image = image
        self.done = False

        # 0-3: allo; 4-7: fekvo
        # 0: kék; 1: piros; 2: sárga; 3: zöld
        self.szinek = ((allo_kek_img, allo_kek_img_action), (allo_piros_img, allo_piros_img_action), (allo_sarga_img, allo_sarga_img_action), (allo_zold_img, allo_zold_img_action), (fekvo_kek_img, fekvo_kek_img_action), (fekvo_piros_img, fekvo_piros_img_action), (fekvo_sarga_img, fekvo_sarga_img_action), (fekvo_zold_img, fekvo_zold_img_action))
        self.make = True
        self.voices = honking
        self.play = False
        self.limit = time
        self.round = 0

    def draw(self):
        modul_draw(self)

        if self.make:
            self.round += 1
            self.honk = r.randint(1,4)
            self.limit = ido.szamlalo.current_seconds - 2
            pygame.mixer.pause()
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

            button_1 = Button(self.pos[0]+9, self.pos[1]+9, self.szinek[self.gombok[0]][0])
            button_2 = Button(self.pos[0]+77, self.pos[1]+9, self.szinek[self.gombok[1]+4][0])
            button_3 = Button(self.pos[0]+152, self.pos[1]+77, self.szinek[self.gombok[2]][0])
            button_4 = Button(self.pos[0]+9, self.pos[1]+152, self.szinek[self.gombok[3]+4][0])
            self.buttons = [button_1, button_2, button_3, button_4]
            self.make = False

        if self.done:
            for i in range(len(self.buttons)):
                if i % 2 == 0:
                    plus = 0
                else:
                    plus = 4

                Image(self.buttons[i].rect.x, self.buttons[i].rect.y, self.szinek[self.gombok[i]+plus][0])
        
        else:
            if self.limit > ido.szamlalo.current_seconds:
                if ido.szamlalo.current_seconds % (self.honk+2) == 0:
                    if not self.play:
                        self.voices[self.honk-1].play()
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
    def __init__(self, index:int, image:pygame.surface.Surface) -> None:
        self.pos = (0,0)
        self.index = index
        self.image = image
        self.done = True
        self.szamlalo = Timer(self.pos[0], self.pos[1] , time)

    def draw(self):
        if self.pos == (0,0):
            make = True
        else:
            make = False

        modul_draw(self)

        if make:
            self.szamlalo = Timer(self.pos[0]+55, self.pos[1]+113, time)


        Image(self.pos[0], self.pos[1], self.image)

        self.szamlalo.timer_draw(changing_colors[self.szamlalo.changing_ind])

        cooldown = pygame.Rect(self.pos[0]+27, self.pos[1]+27, 40*(self.szamlalo.current_seconds%5)+10, 13)
        pygame.draw.rect(screen, changing_colors[self.szamlalo.changing_ind], cooldown)

        if self.szamlalo.current_seconds == 0:
            boom()



# Betöltés

back_img = pygame.image.load("Backs/background.png").convert_alpha()
start_back_img = pygame.image.load("Backs/start.png").convert_alpha()

resume_img = pygame.image.load("Buttons/resume_button.png").convert_alpha()
resume_le = (430, 250, pygame.image.load("Buttons/resume_button_le.png").convert_alpha(), 10)
quit_img = pygame.image.load("Buttons/quit_button.png").convert_alpha()
quit_le = (520, 400, pygame.image.load("Buttons/quit_button_le.png").convert_alpha(), 10)
start_img = pygame.image.load("Buttons/start_button.png").convert_alpha()
start_le = (489, 310, pygame.image.load("Buttons/start_button_le.png").convert_alpha(), 10)
sz1_img = pygame.image.load("Buttons/1_button.png").convert_alpha()
sz1_le = (167,85, pygame.image.load("Buttons/1_button_le.png").convert_alpha(), 5)
sz2_img = pygame.image.load("Buttons/2_button.png").convert_alpha()
sz2_le = (165,245, pygame.image.load("Buttons/2_button_le.png").convert_alpha(), 5)
sz3_img = pygame.image.load("Buttons/3_button.png").convert_alpha()
sz3_le = (165,405, pygame.image.load("Buttons/3_button_le.png").convert_alpha(), 5)
sz4_img = pygame.image.load("Buttons/4_button.png").convert_alpha()
sz4_le = (165,565, pygame.image.load("Buttons/4_button_le.png").convert_alpha(), 5)

resume_button = Button(420, 240, resume_img, 10)
quit_button = Button(510, 390, quit_img, 10)
start_button = Button(479, 300, start_img, 10)
sz1_button = Button(162,80, sz1_img, 5)
sz2_button = Button(160,240, sz2_img, 5)
sz3_button = Button(160,400, sz3_img, 5)
sz4_button = Button(160,560, sz4_img, 5)

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


csapat_input = Input(500, 230, 200, 40, 28)

# összes modul hivatkozása
s_d = SimaDrot(None, sima_drot_modul_img)
k_k = KomplexKabel(None, komplex_kabel_modul_img)
j = Jelszo(None, jelszo_modul_img)
l = LibaMondja(None, lud_mondja_modul_img)
g = Gomb(None, gomb_modul_img)
ker = Kerdes(None, kerdes_modul_img)
ido = Idozito(None, visszaszamlalo_img)
modulok = [s_d, k_k, j, l, g, ker, ido]

modul_kesz = []
for _ in range(6):
    modul_kesz.append(None)

# a modulok szét szórása
def random_pos_modul(modulok:list, not_use:list):
    r_list = []
    for i in range(6):
        r_list.append(i)

    for i in range(len(modulok)):
        if modulok[i] not in not_use:
            rand_index = r.randint(0, len(r_list) - 1)
            modulok[i].index = r_list[rand_index]
            del r_list[rand_index]


def modul_draw(self, p_order=pos_order, jel=jelek, m_kesz=modul_kesz):
    """
    kirajzolja a modult, figyelembe veszi hogy kész van-e?
    """

    m_kesz[self.index] = self.done

    if self.index is not None:
        self.pos = p_order[self.index]


    screen.blit(self.image, self.pos)
    change_image(self.pos[0] + 1, self.pos[1] + 1, jel, 1, self.done)

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
    pygame.mixer.pause()
    explosion_sound.play()
    print("boom")
    explosion = True
    # end_game()

def check_kesz_modulok_szama():
    """
    Megnézi, hogy mennyi kész modul van.
    """
    j = 0
    for modul in modul_kesz[:]:
        if modul:
            j += 1

    return j

def check_if_game_done():
    """
    Ha az összes modul kész van akkor lefutatja a end_game-t.
    """
    if check_kesz_modulok_szama() != len(modulok)-len(not_use_m):
        return False

    end_game()
    return True

def end_game():
    """
    Ha a játék véget ér, akkor ez a függvény fut le.
    :return: None
    """
    global game, running, menu, end_page
    game = False
    running = False
    menu = False
    end_page = True

    for i in range(len(szintek)):
        if szintek[i] is True:
            szint = i + 1

    file = open(rf"eredmenyek/{csapat_input.value}_{szint}.txt", "w")
    # TODO: normális pontozás
    file.write(f"--------------\n{csapat_input.value}\n--------------\nIdő: {ido.szamlalo.current_seconds}\nPontszám: {check_kesz_modulok_szama()-1}\n--------------")
    file.close()

# Folyamat

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
            print("-piros")

        elif i == 1:
            print("-narancssárga")

        else:
            print("-fekete")

while True:

    if game:
        screen.fill((88, 88, 88))
        Image(141, 25, bomba_img)

        for i in range(len(modulok)):
            if modulok[i] not in not_use_m:
                modulok[i].draw()

        check_if_game_done()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game = False
                    menu = True

            if event.type == pygame.USEREVENT:
                ido.szamlalo.current_seconds -= 1


    elif start_page:
        Image(0, 0, start_back_img)

        csapat_input.input_draw(5, -2)

        if start_button.puss_button_draw(start_le):
            if csapat_input.buffer != "":
                csapat_input.value = csapat_input.buffer
                csapat_input.buffer = ""

            start_page = False
            game = True
            running = True
            hiba = False

            if szintek[0]:
                not_use_m = [s_d, j, g]
            elif szintek[1]:
                time = 180
                not_use_m = [k_k, j, ker]
            elif szintek[2]:
                not_use_m = [s_d]
            elif szintek[3]:
                time = 180
                not_use_m = [l]

            random_pos_modul(modulok, not_use_m)

            """
            if osztaly_input.value != "":
                start_page = False
                game = True
                running = True
                hiba = False

            else:
                hiba = True
            """

        if hiba and csapat_input.buffer == "":
            text_draw("Nem adtad még meg az osztályt!", 450, 180, (255, 0, 0), pygame.font.Font(font, 20))

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


    elif menu:
        Image(0,0,start_back_img)
        Image(0, 0, back_img, screen_x, False)

        if quit_button.puss_button_draw(quit_le):
            break

        if resume_button.puss_button_draw(resume_le):
            menu = False

            if running:
                game = True
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

            if event.type == pygame.USEREVENT:
                ido.szamlalo.current_seconds -= 1

    elif end_page:
        if running:
            explosion_sound.play()
            running = False

        Image(0,0,start_back_img)
        Image(0, 0, back_img, screen_x, False)
        text_draw("Játék vége!", screen_x/2-120, screen_y/2-200)
        text_draw(f"Idõ: {ido.szamlalo.current_seconds} másodperc",screen_x/2-180, screen_y/2-100)
        text_draw(f"Pontszám: {check_kesz_modulok_szama()-1}", screen_x/2-120, screen_y/2)
        if explosion:
            text_draw("Felrobbantál!", screen_x/2-120, screen_y/2+100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                # itt szerintem egy scriptel ujra inditjuk a játékot tehát ez nem kell ide
                # end_page = False
                # start_page = True
                pygame.quit()
                exit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
