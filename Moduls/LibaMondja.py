import pygame
import random as r
import Moduls.img_load as il
import Moduls.common as c

class Panel:
    def __init__(self, index:int = None, image:pygame.surface.Surface = il.lib_mondja_modul_img, pos:tuple=(0, 0), done:bool=False, scaling:float|int = 1) -> None:
        self.id = "lib_mondja"
        self.pos = pos
        self.scaling = scaling
        self.index = index
        self.image = image
        self.done = done
        self.mistake = False

        honk_1 = pygame.mixer.Sound("Assets/Hangok/1_hapog.mp3")
        honk_2 = pygame.mixer.Sound("Assets/Hangok/2_hapog.mp3")
        honk_3 = pygame.mixer.Sound("Assets/Hangok/3_hapog.mp3")
        honk_4 = pygame.mixer.Sound("Assets/Hangok/4_hapog.mp3")
        honking = (honk_1, honk_2, honk_3, honk_4)

        # 0-3: allo; 4-7: fekvo
        # 0: kék; 1: piros; 2: sárga; 3: zöld
        self.szinek = ((il.allo_kek_img, il.allo_kek_img_action),
                       (il.allo_piros_img, il.allo_piros_img_action),
                       (il.allo_sarga_img, il.allo_sarga_img_action),
                       (il.allo_zold_img, il.allo_zold_img_action),
                       (il.fekvo_kek_img, il.fekvo_kek_img_action),
                       (il.fekvo_piros_img, il.fekvo_piros_img_action),
                       (il.fekvo_sarga_img, il.fekvo_sarga_img_action),
                       (il.fekvo_zold_img, il.fekvo_zold_img_action))
        self.make = True
        self.voices = honking
        self.played = True
        self.round = 0

        self.pos_bonus = ((9, 9), (77, 9), (152, 77), (9, 152))
        self.buttons = []

    def draw(self, timer):
        c.modul_draw(self)

        if self.make:
            self.limit = timer.time
            self.round += 1
            self.honk = r.randint(1,4)
            self.start = timer.szamlalo.current_seconds - 2
            c.channelhonk.pause()
            self.gombok = [None, None, None, None]
            self.buttons = []

            if c.spec_chart:
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

                self.buttons.append(c.Button(self.pos[0]+self.pos_bonus[i][0]*self.scaling, self.pos[1]+self.pos_bonus[i][1]*self.scaling, self.szinek[self.gombok[i]+bonus][0], self.scaling))

            self.make = False

        if self.done:
            for i in range(len(self.buttons)):
                if i % 2 == 0:
                    plus = 0
                else:
                    plus = 4

                c.Image(self.buttons[i].rect.x, self.buttons[i].rect.y, self.szinek[self.gombok[i]+plus][0], self.scaling)
        
        else:
            if self.start >= timer.szamlalo.current_seconds:
                if not self.played:
                    self.start = timer.szamlalo.current_seconds-(self.honk+2)
                    c.channelhonk.play(self.voices[self.honk-1])
                    self.played = True

            else:
                self.played = False

            for i in range(len(self.buttons)):
                if i % 2 == 0:
                    plus = 0
                else:
                    plus = 4

                if self.buttons[i].button_draw(self.szinek[self.gombok[i]+plus][1])[0]:
                    if c.spec_chart:
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
                        self.mistake = True

                    if self.round == 4:
                        self.done = True
                        self.make = False

    def make_sound(self, timer):
        if self.start >= timer.szamlalo.current_seconds:
            if not self.played:
                self.start = timer.szamlalo.current_seconds-(self.honk+2)
                c.channelhonk.play(self.voices[self.honk-1])
                self.played = True

    def update(self):
        self.scaling = c.g_scale
        self.pos = c.pos_coordinate[self.index]
        for i in range(4):
            if i % 2 == 0:
                bonus = 0

            else:
                bonus = 4

            self.buttons[i] = c.Button(self.pos[0]+self.pos_bonus[i][0]*self.scaling, self.pos[1]+self.pos_bonus[i][1]*self.scaling, self.szinek[self.gombok[i]+bonus][0], self.scaling)

