import os, pygame
from sys import exit
import Moduls.common as c

"""
FONTOS!! generate_bomb():
szeria_root[0: szeriaszám (str); 1: digital root]
cells[0-1: balra; 2-3: jobbra]
stickers[0: fehér; 1: narancssárga; 2: fekete]
modul = 0:Idözítő; 1: Gomb; 2: Kérdés; 3: SimaDrót; 4: KomplexKábel; 5: Jelszó; 6: Libamondja
Ezeket a On_the_Bomb (= properties) jeleníti meg és teszi interaktálhatóvá.
"""

#Változók

miss_write = False      #El fogadható-e a csapat/osztály név
running = False         #Játték épp fut-e vagy sem
levels = [True, False, False, False] #Melyik szint aktív éppen (vagyis melyik fog elindulni)


def test_write(sz_root, elemek, matricak):
    print("Szériaszám: "+sz_root[0])

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


# megcsinálja az eredmenyek mappát
try:
    os.mkdir("eredmenyek")
except Exception as e:
    print(f"hiba az eredmenyek mappa létrehozásánál: {e}")


c.scaled()

import Moduls.img_load as il


class StartPage:
    def __init__(self, background: tuple[int,int,int] = (30, 17, 34), scaling: float|int = 1):
        self.back_color = background
        self.scaling = scaling
        self.active = True
        self.make = True

    def draw(self):
        global moduls, properties, all_updatable_object, running ,miss_write, levels, explosion

        if self.make:
            
            try:
                save = self.csapat_input.buffer
            except:
                save = ""

            self.csapat_input = c.Input(c.bomb_pos_x+384*self.scaling, c.bomb_pos_y+218*self.scaling, 200*self.scaling, 40*self.scaling, 28*self.scaling, all_updatable_object)
            self.csapat_input.buffer = save

            self.start_button = c.Button(c.bomb_pos_x+363*self.scaling, c.bomb_pos_y+288*self.scaling, il.start_img, 10*self.scaling)
            self.lvl1_button = c.Button(c.bomb_pos_x+46*self.scaling, c.bomb_pos_y+68*self.scaling, il.lvl1_img, 5*self.scaling)
            self.lvl2_button = c.Button(c.bomb_pos_x+44*self.scaling, c.bomb_pos_y+228*self.scaling, il.lvl2_img, 5*self.scaling)
            self.lvl3_button = c.Button(c.bomb_pos_x+44*self.scaling, c.bomb_pos_y+388*self.scaling, il.lvl3_img, 5*self.scaling)
            self.lvl4_button = c.Button(c.bomb_pos_x+44*self.scaling, c.bomb_pos_y+548*self.scaling, il.lvl4_img, 5*self.scaling)

            self.make = False

        c.screen.fill(self.back_color)
        c.Image(c.bomb_pos_x, c.bomb_pos_y, il.start_background_img, self.scaling)

        self.csapat_input.input_draw(running, plus_x = 5, plus_y = -2)

        if self.start_button.puss_button_draw(il.start_le):
            if self.csapat_input.buffer != "":

                c.generate_bomb()

                self.csapat_input.value = self.csapat_input.buffer
                self.active = False
                g_page.active = True
                running = True
                miss_write = False

                
                #0:Idözítő; 1: Gomb; 2: Kérdés; 3: SimaDrót; 4: KomplexKábel; 5: Jelszó; 6: Libamondja
                if levels[0]:
                    time = 480
                    create_moduls = [0, 1, 1, 2, 3]
                elif levels[1]:
                    time = 480
                    create_moduls = [0, 3, 3, 2, 5]
                elif levels[2]:
                    time = 480
                    create_moduls = [0, 2, 4, 5, 5, 6]
                elif levels[3]:
                    time = 480
                    create_moduls = [0, 2, 3, 4, 4, 6]

                explosion = False


                import importlib
                import random
                
                moduls = []
                modul_name = ("Idozito", "Gomb", "Kerdes", "SimaDrot", "KomplexKabel", "Jelszo", "LibaMondja")


                r_list = []
                for i in range(6): #mivel csak hat hely van a bonbán
                    r_list.append(i)

                for i in create_moduls:
                    modul = importlib.import_module(f"Moduls.{modul_name[i]}")
                    rand_index = random.randint(0, len(r_list) - 1)
                    moduls.append(modul.Panel(index = r_list[rand_index],scaling = c.g_scale))
                    del r_list[rand_index]


                from Moduls.on_the_bomb import On_the_Bomb

                properties = On_the_Bomb(c.cells, c.stickers)


                moduls[0].time = time

                test_write(c.szeria_root[0], c.cells, c.stickers)


                for modul in moduls:
                    all_updatable_object.append(modul)

                    if modul.id == "jelszo":
                        modul.update_list = all_updatable_object

                    if modul.id == "lib_mondja":
                        sti_page.lib_mon = modul

            else:
                miss_write = True

        if miss_write and self.csapat_input.buffer == "":
            c.text_draw("Nem adtad még meg az osztályt!", 450*self.scaling, 180*self.scaling, (255, 0, 0), pygame.font.Font(c.family, 20*self.scaling))

        if self.lvl1_button.puss_button_draw(il.lvl1_le, levels[0]):
            levels = [True, False, False, False]

        if self.lvl2_button.puss_button_draw(il.lvl2_le, levels[1]):
            levels = [False, True, False, False]

        if self.lvl3_button.puss_button_draw(il.lvl3_le, levels[2]):
            levels = [False, False, True, False]

        if self.lvl4_button.puss_button_draw(il.lvl4_le, levels[3]):
            levels = [False, False, False, True]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.active = False
                    m_page.active = True

            elif event.type == pygame.VIDEORESIZE:
                c.scaled(all_updatable_object)

    def update(self):
        self.scaling = c.g_scale
        self.make = True


class MenuPage:
    def __init__(self, background: tuple[int,int,int] = (30, 17, 34), scaling: float|int = 1):
        self.back_color = background
        self.scaling = scaling
        self.active = False
        self.make = True

    def draw(self):
        if self.make:
            self.resume_button = c.Button(c.bomb_pos_x+304*c.g_scale, c.bomb_pos_y+228*c.g_scale, il.resume_img, 10*c.g_scale)
            self.quit_button = c.Button(c.bomb_pos_x+394*c.g_scale, c.bomb_pos_y+378*c.g_scale, il.quit_img, 10*c.g_scale)

            self.make = False

        c.screen.fill(self.back_color)
        c.Image(c.bomb_pos_x, c.bomb_pos_y, il.start_background_img, c.g_scale)
        c.Image(0, 0, il.background_img, c.screen_x)

        if self.quit_button.puss_button_draw(il.quit_le):
            pygame.quit()

        if self.resume_button.puss_button_draw(il.resume_le):
            self.active = False

            if running:
                g_page.active = True
                for modul in moduls:
                    if modul.id == "lib_modja":
                        modul.start = moduls[0].szamlalo.current_seconds - 1
            else:
                sta_page.active = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.active = False
                    if running:
                        g_page.active = True
                    else:
                        sta_page.active = True

            elif event.type == pygame.VIDEORESIZE:
                c.scaled(all_updatable_object)

            if running:
                if event.type == pygame.USEREVENT:
                    moduls[0].szamlalo.current_seconds -= 1

                if moduls[0].szamlalo.current_seconds == 0:
                    boom()
    
    def update(self):
        self.scaling = c.g_scale
        self.make = True


class GamePage:
    def __init__(self, background: tuple[int,int,int] = (120, 120, 120), scaling: float|int = 1):
        self.back_color = background
        self.scaling = scaling
        self.active = False

    def draw(self):
        c.screen.fill(self.back_color)
        c.Image(c.bomb_pos_x+25*c.g_scale, c.bomb_pos_y+10*c.g_scale, il.bomb_img, c.g_scale)

        for i in range(len(moduls)):
            moduls[i].draw(timer = moduls[0])

        properties.draw(sti_page, g_page)

        check_if_game_done()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    g_page.active = False
                    m_page.active = True

            elif event.type == pygame.VIDEORESIZE:
                c.scaled(all_updatable_object)

            if event.type == pygame.USEREVENT:
                moduls[0].szamlalo.current_seconds -= 1

        if moduls[0].szamlalo.current_seconds == 0:
            boom()

    def update(self):
        self.scaling = c.g_scale


class StickerPage:
    def __init__(self, background: tuple[int,int,int] = (120, 120, 120), scaling: float|int = 1):
        self.back_color = background
        self.scaling = scaling
        self.active = False
        self.make = True
        self.choose_sticker = None
        self.lib_mon = None

    def draw(self):
        if self.make:
            self.left_button = c.Button(c.bomb_pos_x+5*c.g_scale, c.bomb_pos_y+282*c.g_scale, il.left_img, 4*c.g_scale)
            self.right_button = c.Button(c.bomb_pos_x+c.basic_x-19*4*c.g_scale-5*c.g_scale, c.bomb_pos_y+286*c.g_scale, il.right_img, 4*c.g_scale)
            self.back_button = c.Button(c.bomb_pos_x+5*c.g_scale, c.bomb_pos_y+8*c.g_scale, il.back_img, 5*c.g_scale)
            self.make = False

        c.screen.fill(self.back_color)
        c.Image(0, 0 , il.background_img, c.screen_x)
        c.Image(c.bomb_pos_x+137*c.g_scale, c.bomb_pos_y+162*c.g_scale, properties.big_sticker[properties.current_sticker[self.choose_sticker][2]], c.g_scale)

        if properties.current_sticker[self.choose_sticker][2] == 0:
            c.text_draw(c.szeria_root[0], c.bomb_pos_x+254*c.g_scale, c.bomb_pos_y+340*c.g_scale, (255,255,255), pygame.font.Font(c.family, 100*c.g_scale))

        if len(properties.current_sticker) != 1:
            if self.left_button.pos_button_draw(il.left_kijelolve):
                if self.choose_sticker - 1 == -1:
                    self.choose_sticker = len(properties.current_sticker)-1

                else:
                    self.choose_sticker -= 1

            if self.right_button.pos_button_draw(il.right_kijelolve):
                if self.choose_sticker + 1 == len(properties.current_sticker):
                    self.choose_sticker = 0

                else:
                    self.choose_sticker += 1

        if self.back_button.puss_button_draw(il.back_le):
            sti_page.active = False
            g_page.active = True
            for modul in moduls:
                if modul.id == "lib_modja":
                    modul.start = moduls[0].szamlalo.current_seconds - 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sti_page.active = False
                    g_page.active = True
                    for modul in moduls:
                        if modul.id == "lib_modja":
                            modul.start = moduls[0].szamlalo.current_seconds - 1

            elif event.type == pygame.VIDEORESIZE:
                c.scaled(all_updatable_object)

            if event.type == pygame.USEREVENT:
                moduls[0].szamlalo.current_seconds -= 1

        if moduls[0].szamlalo.current_seconds == 0:
            boom()

        if self.lib_mon != None:
            self.lib_mon.make_sound(moduls[0])

    def update(self):
        self.scaling = c.g_scale
        self.make = True


class EndPage:
    def __init__(self, background: tuple[int,int,int] = (30, 17, 34), scaling: float|int = 1):
        self.back_color = background
        self.scaling = scaling
        self.active = False
        self.make = True
    
    def draw(self):
        if self.make:
            self.back_button = c.Button(c.bomb_pos_x+5*c.g_scale, c.bomb_pos_y+8*c.g_scale, il.back_img, 5*c.g_scale)
            self.make = False
        
        c.screen.fill(self.back_color)
        c.Image(c.bomb_pos_x, c.bomb_pos_y, il.start_background_img, c.g_scale)
        c.Image(0, 0, il.background_img, c.screen_x, False)
        c.text_draw("Játék vége!", c.screen_x/2-120*c.g_scale, c.screen_y/2-200*c.g_scale)
        c.text_draw(f"Idõ: {moduls[0].szamlalo.current_seconds} másodperc",c.screen_x/2-180*c.g_scale, c.screen_y/2-100*c.g_scale)
        c.text_draw(f"Pontszám: {check_done_moduls_num()-1}", c.screen_x/2-120*c.g_scale, c.screen_y/2*c.g_scale)
        if explosion:
            c.text_draw("Felrobbantál!", c.screen_x/2-120*c.g_scale, c.screen_y/2+100*c.g_scale)

        if self.back_button.puss_button_draw(il.back_le):
            self.active = False
            sta_page.active = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.active = False
                    sta_page.active = True

            elif event.type == pygame.VIDEORESIZE:
                c.scaled(all_updatable_object)

    def update(self):
        self.scaling = c.g_scale
        self.make = True


#Betöltés
explosion_sound = pygame.mixer.Sound("Assets/Hangok/robanas.mp3")

def boom():
    global explosion
    c.channelhonk.pause()
    c.channelboom.play(explosion_sound)
    explosion = True
    end_game()


def check_done_moduls_num(): #Megnézi, hogy mennyi kész modul van.

    j = 0
    for modul in moduls:
        if modul.done == True:
            j += 1

    return j


def check_if_game_done(): #Ha az összes modul kész van akkor lefutatja a end_game-t.
    for i in range(len(moduls)):
        if moduls[i].mistake == True:
            boom()

    if check_done_moduls_num() != len(moduls):
        return False

    c.channelhonk.pause()
    end_game()
    return True


def end_game(): #Ha a játék véget ér, akkor ez a függvény fut le. :return: None
    global running
    g_page.active = False
    running = False
    m_page.active = False
    e_page.active = True

    for i in range(len(levels)):
        if levels[i] is True:
            szint = i + 1

    file = open(rf"eredmenyek/{sta_page.csapat_input.value}_{szint}.txt", "w", encoding="UTF-8")
    # TODO: normális pontozás
    file.write(f"--------------\n{sta_page.csapat_input.value}\n--------------\nIdő: {moduls[0].szamlalo.current_seconds}\nPontszám: {check_done_moduls_num()-1}\n")
    if explosion:
        file.write(f"Felrobbant.\n")
    file.write(f"--------------\n")

    file.write(f"Szériaszám: {c.szeria_root[0]}\n")

    bal = 0
    jobb = 0
    for i in range(len(c.cells)):
        if True == c.cells[i]:
            if i < 2:
                bal += 1

            else:
                jobb += 1
    file.write(f"Elemek: bal:{bal}; jobb:{jobb}\n")

    file.write("Matricák:\n")
    for i in range(len(c.stickers)):
        if True == c.stickers[i]:
            if i == 0:
                file.write("-fehér\n")

            elif i == 1:
                file.write("-narancssárga\n")

            else:
                file.write("-fekete\n")
    file.close()

sta_page = StartPage()
m_page = MenuPage()
e_page = EndPage()
g_page = GamePage()
sti_page = StickerPage()

pages = [sta_page, m_page, e_page, g_page, sti_page]

all_updatable_object = []

for p in pages:
    all_updatable_object.append(p)


# Folyamat

while True:

    for page in pages:
        if page.active == True:
            page.draw()

    """if g_page.active:
        g_page.draw()
    elif sti_page.active:
        sti_page.draw()
    elif m_page.active:
        m_page.draw()
    elif sta_page.active:
        sta_page.draw()
    elif e_page.active:
        e_page.draw()"""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.VIDEORESIZE:
            c.scaled(all_updatable_object)

    pygame.display.flip()
    c.clock.tick(60)

pygame.quit()