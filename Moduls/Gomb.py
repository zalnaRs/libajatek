import pygame
import random as r
import Moduls.img_load as il
import Moduls.common as c
import Moduls.defs as f

class Panel:
    def __init__(self, index: int = None, image: pygame.surface.Surface = il.gomb_modul_img, pos:tuple=(0, 0), done:bool=False, scaling:float|int = 1) -> None:
        self.id = "Gomb"
        self.pos = pos
        self.scaling = scaling
        self.index = index
        self.image = image
        self.done = done
        self.mistake = False

        self.colors = ((il.kek_gomb_img, il.kek_gomb_action), (il.piros_gomb_img, il.piros_gomb_action), (il.zold_gomb_img, il.zold_gomb_action))
        self.symbols = (il.lud_szimbolum, il.talp_szimbolum, il.tojas_szimbolum)
        self.gomb_data = (r.randint(0, 2), r.randint(0, 2)) #self.gomb_data[0][0:kék; 1:piros; 2:zöld]

        self.puss = None
        if self.gomb_data[0] == 0 and f.count(c.cells[0:2], True) > 0:
            self.puss = True

        elif c.spec_chart and self.gomb_data[1] != 2:
            self.puss = False

        elif True not in c.cells and self.gomb_data[1] == 1:
            self.puss = False

        elif self.gomb_data[0] == 2:
            if c.szeria_root[1] == 7:
                self.puss = True
            else:
                self.puss = False

        elif self.gomb_data[0] == 0:
            if c.szeria_root[1] == 1:
                self.puss = False
            else:
                self.puss = True

        elif self.gomb_data[1] == 2:
            self.puss = False

        elif self.puss is None:
            self.puss = True

        if self.puss:
            if self.gomb_data[1] == 0:
                self.time_color = 0

            elif f.count(c.cells, True) == 2:
                self.time_color = 1

            else:
                self.time_color = 2

        else:
            self.time_limit = None

    def draw(self, timer):
        if self.pos == (0, 0):
            make = True
        else:
            make = False

        c.modul_draw(self)

        if make:
            self.gomb = c.Button(self.pos[0] + 100*self.scaling, self.pos[1] + 39*self.scaling, self.colors[self.gomb_data[0]][0], self.scaling)

        c.Image(self.pos[0] + 56*self.scaling, self.pos[1] + 159*self.scaling, self.symbols[self.gomb_data[1]], self.scaling)

        allapot = self.gomb.button_draw(self.colors[self.gomb_data[0]][1], self.done)
        if not self.puss and allapot[1]:
            if self.time_limit is None:
                self.time_limit = timer.szamlalo.current_seconds - 2

            if self.time_limit >= timer.szamlalo.current_seconds:
                self.mistake = True

        if allapot[0]:
            if self.puss:
                if self.time_color == timer.szamlalo.changing_ind:
                    self.done = allapot[0]

                else:
                    self.mistake = True

            else:
                self.done = allapot[0]

    def update(self):
        self.scaling = c.g_scale
        self.pos = (0, 0)