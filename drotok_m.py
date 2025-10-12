import pygame
import common as c
#Image, Button, Timer, Input, modul_draw, boom, g_scale, cells, stickers, szeria_root, spec_chart, properties, explosion
import defs as f
import img_load as il

class SimaDrot:
    def __init__(self, index: int, image: pygame.surface.Surface, pos:tuple=(0, 0), done:bool=False, scaling:float|int = 1) -> None:
        self.pos = pos
        self.scaling = scaling
        self.index = index
        self.image = image
        self.done = done
        self.mistake = False

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
                if c.szeria_root[1] == 3:
                    self.correct = 3

                elif c.szeria_root[1] % 2 == 0 and c.stickers[2]:
                    self.correct = 2

                elif c.szeria_root[1] % 2 == 1:
                    self.correct = 3

                elif c.stickers[1]:
                    self.correct = 1

                else:
                    if c.szeria_root[1] / 2 + 7 == 8:
                        self.correct = 0

                    elif c.szeria_root[1] / 2 + 7 == 9:
                        self.correct = 2

                    elif c.szeria_root[1] / 2 + 7 == 10:
                        self.correct = 3

                    else:
                        self.correct = 1

        if not sarga and self.drotok_color[2] == 0 and c.cells[2:4] == [True, True]:
            self.correct = 0

        elif f.count(self.drotok_color, 1) == 2 and f.count(self.drotok_color, 2) == 0:
            self.correct = 1

        elif f.count(self.drotok_color, 2) == 1:
            self.correct = 3

        elif f.count(self.drotok_color, 0) == 0:
            if c.szeria_root[1] == 6:
                self.correct = 0

            elif True in c.cells[0:2] and True not in c.cells[2:4]:
                self.correct = 1

            else:
                self.correct = 3

        elif self.drotok_color[0] == 3 and c.stickers[1]:
            self.correct = 3

        elif not c.stickers[2]:
            self.correct = 0

        else:
            self.correct = 2

    def draw(self, timer = None):
        c.modul_draw(self)
        count = 0
        for i in range(len(self.drotok)):
            if i < 3:
                half = 0
            else:
                half = 6*self.scaling

            if self.drotok[i] is not None and self.done:
                if self.drotok[i][1]:
                    if self.animate_button is None:
                        self.animate_button = c.Button(self.pos[0] + 35*self.scaling, self.pos[1] + 34*self.scaling + 28 * i*self.scaling + half, self.colors[self.drotok[i][0]][0], self.scaling)
                    self.animate_button.cable_draw(self.drotok[i][1], self.colors[self.drotok[i][0]][1])

                else:
                    c.Image(self.pos[0] + 35*self.scaling, self.pos[1] + 34*self.scaling + 28 * i*self.scaling + half, self.colors[self.drotok[i][0]][0], self.scaling)

            elif self.drotok[i] is not None:
                self.drotok[i][1] = c.Button(self.pos[0] + 35*self.scaling, self.pos[1] + 34*self.scaling + 28 * i*self.scaling + half, self.colors[self.drotok[i][0]][0]).cable_draw(self.drotok[i][1], self.colors[self.drotok[i][0]][1])
                if self.drotok[i][1]:
                    if i - count == self.correct:
                        self.done = self.drotok[i][1]

                    else:
                        self.mistake = True

            else:
                count += 1

    def update(self):
        self.scaling = c.g_scale
        self.pos = (0, 0)