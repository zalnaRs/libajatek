import pygame
import defs as f
from sys import exit
import random as r


#Állandok

pos_order = [(197, 81), (528, 81), (859, 81),
        (197, 416), (528, 416), (859, 416),
        ]
changing_colors = [(255, 0, 0), (255, 135, 35), (235, 35, 200)]

screen_x = 1280
screen_y = 720


#Változok

spec_chart = bool(r.randint(0,1))
szeria_root = f.szerianumber(spec_chart)
#0 fehér; 1 narancssárga; 2 fekete
matricak = [bool(r.randint(0,1)), bool(r.randint(0,1)), bool(r.randint(0,1))]
#0-1: balra; 2-3: jobbra
elemek = [bool(r.randint(0,1)), bool(r.randint(0,1)), bool(r.randint(0,1)), bool(r.randint(0,1))]


start_page = True
menu = False
game = False
running = False
scaling = False


pygame.init()
screen = pygame.display.set_mode((screen_x,screen_y))
screen.fill((88,88,88))
pygame.display.set_caption("Keep Honking and Nobody Explodes")
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)


#Osztályok

class Image:
    def __init__(self, x:int, y:int, image:pygame.surface.Surface, scale:int=1, delay:bool=False, trans:tuple[bool, int]=(False, 255)):
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
    def __init__(self, x:int, y:int, image:pygame.surface.Surface, scale:int=1):
        width = image.get_width()
        height = image.get_height()
        self.scale = scale
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.click = False
        self.animate = 1

    def puss_button_draw(self, puss_data:tuple[int, int, pygame.surface.Surface, int]):
        action = False

        #egér helyzete:
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) or self.click:
            if pygame.mouse.get_pressed()[0] == 1: #le van nyomva
                self.click = True
                Image(puss_data[0], puss_data[1], puss_data[2], puss_data[3])#mit jelenítsen meg helyete
                    

            elif pygame.mouse.get_pressed()[0] == 0 and self.click:
                self.click = False
                action = True

        if not self.click:
            screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

    def cable_draw(self, action:bool, images:tuple[pygame.surface.Surface]):

        if action:
            if self.animate < len(images)-1:
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

        if close is not None and not close:

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
    def __init__(self, x:int, y:int, w:int, h:int):
        self.rect = pygame.Rect(x, y, w, h)
        self.text_x = x + 10
        self.text_y = y - (h //20)*(h //20)
        self.text_size = h - (10+h//30)
        self.max = w // self.text_size
        self.input_text = ""
        self.active = False
        self.puffer = ""

    def input_draw(self, background=(20,20,20), active_color=(255,255,255), passive_color=(88,88,88), text_color=(255,255,255)):

        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
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
                    # sortörést nem fogadunk el.
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        self.active = False

                    #    self.puffer = self.input_text
                    #    self.input_text = ""

                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[0:-1]
                    elif len(self.input_text) < self.max:
                        self.input_text += event.unicode

        if self.active:
            color = active_color
        else:
            color = passive_color

        pygame.draw.rect(screen, background, self.rect)
        pygame.draw.rect(screen, color, self.rect, 2)
        text_draw(self.input_text, self.text_x, self.text_y, text_color, pygame.font.Font("Grand9K Pixel.ttf", self.text_size))

        return self.puffer



class Timer:
    def __init__(self, x:int, y:int, time:int=300) -> None:
        self.x = x
        self.y = y
        self.current_seconds = time
        self.changing_ind = 0

    def timer_draw(self, color:tuple[int, int, int]=(255, 255, 255)):
        display_minutes = self.current_seconds // 60
        display_seconds = self.current_seconds % 60

        self.changing_ind = (self.current_seconds // 5)% 3

        text_draw(f"{display_minutes:02}:{display_seconds:02}", self.x, self.y, color)

def change_image(x:int, y:int, images:tuple[pygame.surface.Surface], scale:int=1, close:bool = None):
    pos = pygame.mouse.get_pos()

    alap = Image(x, y, images[0], scale)

    if close is not None and len(images) > 2 and close:
        Image(x, y, images[2], scale)

    elif alap.rect.collidepoint(pos):
        Image(x, y, images[1], scale)



class SimaDrot:
    def __init__(self, index:int, image:pygame.surface.Surface) -> None:
        self.pos = None
        self.index = index
        self.image = image
        self.done = False

        self.colors = ((fekete_drot_img, fekete_drot_action), (kek_drot_img, kek_drot_action), (piros_drot_img, piros_drot_action), (sarga_drot_img, sarga_drot_action))
        self.drotok = f.generate_drotok()
        self.animate_button = None

    def drotok_draw(self):
        modul_draw(self)
        for i in range(len(self.drotok)):
            if i < 3:
                half = 0
            else:
                half = 6
            
            if self.done and self.drotok[i] is not None:
                if self.drotok[i][1]:
                    if self.animate_button is None:
                        self.animate_button = Button(self.pos[0]+35, self.pos[1]+34+28*i+half, self.colors[self.drotok[i][0]][0])
                    self.animate_button.cable_draw(self.drotok[i][1],self.colors[self.drotok[i][0]][1])

                else:
                    Image(self.pos[0]+35, self.pos[1]+34+28*i+half, self.colors[self.drotok[i][0]][0])

            elif self.drotok[i] is not None:
                self.done = Button(self.pos[0]+35, self.pos[1]+34+28*i+half, self.colors[self.drotok[i][0]][0]).cable_draw(self.drotok[i][1],self.colors[self.drotok[i][0]][1])
                self.drotok[i][1] = self.done



class KomplexKabel:
    def __init__(self, index:int, image:pygame.surface.Surface) -> None:
        self.index = index
        self.pos = (0,0)
        self.image = image
        self.done = False

        self.num = ((kabel_1_img, kabel_1_action),(kabel_2_img, kabel_2_action), (kabel_3_img, kabel_3_action), (kabel_4_img, kabel_4_action))
        self.kabelek = []
        for _ in range(6):
            self.kabelek.append([r.randint(0, 3), False])


        self.first = 5
        self.second = 4
        self.third = 3
        self.fourth = 2
        self.fifth = 1
        self.sixth = 0
        self.num_kabel = [
        self.sixth,
        self.fifth,
        self.fourth,
        self.third,
        self.second,
        self.first,
        ]

        self.cut_them = []
        self.feher = None

        #sárga lap
        if szeria_root[1] == 5:
            self.cut_them.append(self.second)

        else:
            if True in elemek:
                self.feher = 1

            self.cut_them.append(self.sixth)

        #zöld lap
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

        #fehér 4. oldal
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


    def kabelek_draw(self):
        if self.pos == (0,0):
            make = True
        else:
            make = False

        modul_draw(self)

        if make:
            for i in range(len(self.kabelek)):
                self.num_kabel[i] = Button(self.pos[0]+22+28*i, self.pos[1]+23, self.num[self.kabelek[i][0]][0])


        for i in range(len(self.kabelek)):
            if self.done:
                if self.kabelek[i][1]:

                    for j in range(len(self.kabelek)):
                        if self.kabelek[j][1]:
                            self.num_kabel[i].cable_draw(self.kabelek[i][1],self.num[self.kabelek[i][0]][1])

                else:
                    Image(self.pos[0]+22+28*i, self.pos[1]+23, self.num[self.kabelek[i][0]][0])

            else:
                self.kabelek[i][1] = self.num_kabel[i].cable_draw(self.kabelek[i][1],self.num[self.kabelek[i][0]][1])
                
                if self.kabelek[i][1]:
                    if i in self.cut_them:
                        
                        c = 0
                        for j in range(len(self.kabelek)):
                            if self.kabelek[j][1]:
                                c += 1

                        if c == len(self.cut_them):
                            self.done = True

                    else:
                        print("boom")
                        # csak a teszt miat van a következő 7 sor
                        c = 0
                        for j in range(len(self.kabelek)):
                            if self.kabelek[j][1]:
                                c += 1

                        if c == len(self.cut_them):
                            self.done = True

class Gomb:
    def __init__(self, index:int, image:pygame.surface.Surface) -> None:
        self.pos = (0,0)
        self.index = index
        self.image = image
        self.done = False

        self.colors = ((kek_gomb_img, kek_gomb_action), (piros_gomb_img, piros_gomb_action), (zold_gomb_img, zold_gomb_action))
        self.symbols = (lud_szimbolum, talp_szimbolum, tojas_szimbolum)
        self.gomb_data = (r.randint(0,2), r.randint(0,2))

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


    def gomb_draw(self):
        if self.pos == (0,0):
            make = True
        else:
            make = False

        modul_draw(self)

        if make:
            self.gomb = Button(self.pos[0]+100, self.pos[1]+39, self.colors[self.gomb_data[0]][0])

        Image(self.pos[0]+56, self.pos[1]+159, self.symbols[self.gomb_data[1]])

        allapot = self.gomb.button_draw(self.colors[self.gomb_data[0]][1], self.done)
        if not self.puss and allapot[1]:
            if self.time_limit is None:
                self.time_limit = visszaszamlalo.current_seconds - 2

            if self.time_limit >= visszaszamlalo.current_seconds:
                print("boom")

        if allapot[0]:
            if self.puss:
                if self.time_color == visszaszamlalo.changing_ind:
                    self.done = allapot[0]

                else:
                    print("boom")

            else:
                self.done = allapot[0]


#Szöveg

font = pygame.font.Font("Grand9K Pixel.ttf", 36) #õ -> ő

def text_draw(text, x, y, text_color=(255,255,255), style=font):
    img = style.render(text, True, text_color)
    screen.blit(img,(x,y))

#Betöltés

back_img = pygame.image.load("Backs/background.png").convert_alpha()
start_back_img = pygame.image.load("Backs/start.png").convert_alpha()


resume_img = pygame.image.load("Buttons/resume_button.png").convert_alpha()
resume_le = (430,250,pygame.image.load("Buttons/resume_button_le.png").convert_alpha(),10)
quit_img = pygame.image.load("Buttons/quit_button.png").convert_alpha()
quit_le = (520,400,pygame.image.load("Buttons/quit_button_le.png").convert_alpha(),10)
start_img = pygame.image.load("Buttons/start_button.png").convert_alpha()
start_le = (489,310,pygame.image.load("Buttons/start_button_le.png").convert_alpha(),10)

resume_button = Button(420,240, resume_img, 10)
quit_button = Button(510,390, quit_img, 10)
start_button = Button(479,300, start_img, 10)


bomba_img = pygame.image.load("Backs/bomba_alap.png").convert_alpha()

sima_drot_modul_img = pygame.image.load("nat_drotok/drot_nat_224x224.png").convert_alpha()

fekete_drot_img = pygame.image.load("nat_drotok/fekete/fekete_alap.png").convert_alpha()
fekete_drot_action = (pygame.image.load("nat_drotok/fekete/fekete_kijelolve.png").convert_alpha(), pygame.image.load("nat_drotok/fekete/fekete_vagas.png").convert_alpha(), pygame.image.load("nat_drotok/fekete/fekete_kesz.png").convert_alpha())
kek_drot_img = pygame.image.load("nat_drotok/kek/kek_alap.png").convert_alpha()
kek_drot_action = (pygame.image.load("nat_drotok/kek/kek_kijelolve.png").convert_alpha(), pygame.image.load("nat_drotok/kek/kek_vagas.png").convert_alpha(), pygame.image.load("nat_drotok/kek/kek_kesz.png").convert_alpha())
piros_drot_img = pygame.image.load("nat_drotok/piros/piros_alap.png").convert_alpha()
piros_drot_action = (pygame.image.load("nat_drotok/piros/piros_kijelolve.png").convert_alpha(), pygame.image.load("nat_drotok/piros/piros_vagas.png").convert_alpha(), pygame.image.load("nat_drotok/piros/piros_kesz.png").convert_alpha())
sarga_drot_img = pygame.image.load("nat_drotok/sarga/sarga_alap.png").convert_alpha()
sarga_drot_action = (pygame.image.load("nat_drotok/sarga/sarga_kijelolve.png").convert_alpha(), pygame.image.load("nat_drotok/sarga/sarga_vagas.png").convert_alpha(), pygame.image.load("nat_drotok/sarga/sarga_kesz.png").convert_alpha())

komplex_kabel_modul_img = pygame.image.load("kom_kabel/kabel_kom_224x224.png").convert_alpha()

kabel_1_img = pygame.image.load("kom_kabel/1_kabel/1_alap.png").convert_alpha()
kabel_1_action = (pygame.image.load("kom_kabel/1_kabel/1_kijelolve.png").convert_alpha(), pygame.image.load("kom_kabel/1_kabel/1_vagas.png").convert_alpha(), pygame.image.load("kom_kabel/1_kabel/1_kesz.png").convert_alpha())
kabel_2_img = pygame.image.load("kom_kabel/2_kabel/2_alap.png").convert_alpha()
kabel_2_action = (pygame.image.load("kom_kabel/2_kabel/2_kijelolve.png").convert_alpha(), pygame.image.load("kom_kabel/2_kabel/2_vagas.png").convert_alpha(), pygame.image.load("kom_kabel/2_kabel/2_kesz.png").convert_alpha())
kabel_3_img = pygame.image.load("kom_kabel/3_kabel/3_alap.png").convert_alpha()
kabel_3_action = (pygame.image.load("kom_kabel/3_kabel/3_kijelolve.png").convert_alpha(), pygame.image.load("kom_kabel/3_kabel/3_vagas.png").convert_alpha(), pygame.image.load("kom_kabel/3_kabel/3_kesz.png").convert_alpha())
kabel_4_img = pygame.image.load("kom_kabel/4_kabel/4_alap.png").convert_alpha()
kabel_4_action = (pygame.image.load("kom_kabel/4_kabel/4_kijelolve.png").convert_alpha(), pygame.image.load("kom_kabel/4_kabel/4_vagas.png").convert_alpha(), pygame.image.load("kom_kabel/4_kabel/4_kesz.png").convert_alpha())

gomb_modul_img = pygame.image.load("gomb_modul/gomb_alap_224x224.png").convert_alpha()

kek_gomb_img = pygame.image.load("gomb_modul/kek/kek_sima.png").convert_alpha()
kek_gomb_action = (pygame.image.load("gomb_modul/kek/kek_kijelol.png").convert_alpha(), pygame.image.load("gomb_modul/kek/kek_benyomva.png").convert_alpha(), pygame.image.load("gomb_modul/kek/kek_kesz.png").convert_alpha())
piros_gomb_img = pygame.image.load("gomb_modul/piros/piros_sima.png").convert_alpha()
piros_gomb_action = (pygame.image.load("gomb_modul/piros/piros_kijelol.png").convert_alpha(), pygame.image.load("gomb_modul/piros/piros_benyomva.png").convert_alpha(), pygame.image.load("gomb_modul/piros/piros_kesz.png").convert_alpha())
zold_gomb_img = pygame.image.load("gomb_modul/zold/zold_sima.png").convert_alpha()
zold_gomb_action = (pygame.image.load("gomb_modul/zold/zold_kijelol.png").convert_alpha(), pygame.image.load("gomb_modul/zold/zold_benyomva.png").convert_alpha(), pygame.image.load("gomb_modul/zold/zold_kesz.png").convert_alpha())

lud_szimbolum = pygame.image.load("gomb_modul/szimbolumok/minta_lud.png").convert_alpha()
talp_szimbolum = pygame.image.load("gomb_modul/szimbolumok/minta_talp.png").convert_alpha()
tojas_szimbolum = pygame.image.load("gomb_modul/szimbolumok/minta_tojas.png").convert_alpha()


jel_alap = pygame.image.load("Jelzok/alap_keret.png").convert_alpha()
jel_kijel = pygame.image.load("Jelzok/kijelol_keret.png").convert_alpha()
#jel_kat = pygame.image.load("Jelzok/kat_keret.png").convert_alpha()
jel_kesz = pygame.image.load("Jelzok/kesz_keret.png").convert_alpha()

jelek = (jel_alap, jel_kijel, jel_kesz)


explosion_sound = pygame.mixer.Sound("Hangok/explosion.mp3")
honk_1 = pygame.mixer.Sound("Hangok/honk_1.mp3")
honk_2 = pygame.mixer.Sound("Hangok/honk_2.mp3")
honk_3 = pygame.mixer.Sound("Hangok/honk_3.mp3")
honking = (honk_1, honk_2, honk_3)
#honk_1.play()


osztaly_input = Input(500, 230, 200, 40)
visszaszamlalo = Timer(10, 25)

#összes modul hivatkozása
s_d = SimaDrot(None, sima_drot_modul_img)
k_k = KomplexKabel(None, komplex_kabel_modul_img)
j = SimaDrot(None, sima_drot_modul_img)
l = SimaDrot(None, sima_drot_modul_img)
g = Gomb(None, gomb_modul_img)
ker = SimaDrot(None, sima_drot_modul_img)
ido = SimaDrot(None, sima_drot_modul_img)
modulok = [s_d, k_k, j, l, g, ker, ido]
not_use_m = [ido]

#a modulok szét szórása
r_list = []
for i in range(6):
    r_list.append(i)

for i in range(len(modulok)):
    if modulok[i] not in not_use_m:
        rand_index = r.randint(0, len(r_list)-1)
        modulok[i].index = r_list[rand_index]
        del r_list[rand_index]

modul_kesz = []
for i in range(6):
    modul_kesz.append(None)



def modul_draw(self, p_order=None, jel = jelek, m_kesz=None):
    if p_order is None:
        p_order = pos_order
    if m_kesz is None:
        m_kesz = modul_kesz
    m_kesz[self.index] = self.done
    if self.index is not None:
        self.pos = p_order[self.index]

    screen.blit(self.image, self.pos)
    change_image(self.pos[0]+1, self.pos[1]+1, jel, 1, self.done)



#Folyamat

while True:

    if game:
        screen.fill((88,88,88))
        Image(141,25, bomba_img)
        s_d.drotok_draw()
        k_k.kabelek_draw()
        g.gomb_draw()
        visszaszamlalo.timer_draw(changing_colors[visszaszamlalo.changing_ind])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game = False
                    menu = True

            if event.type == pygame.USEREVENT:
                visszaszamlalo.current_seconds -= 1


    elif start_page:
        Image(0,0,start_back_img)

        osztaly_input.input_draw()

        if start_button.puss_button_draw(start_le):
            if osztaly_input.input_text != "":
                osztaly_input.puffer = osztaly_input.input_text
                osztaly_input.input_text = ""

            start_page = False
            game = True
            running = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    start_page = False
                    menu = True


    elif menu:
        back = Image(0,0,back_img,screen_x, False, (True, 50))

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
                visszaszamlalo.current_seconds -= 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()