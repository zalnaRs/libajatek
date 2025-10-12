import pygame
import random as r
import img_load as il
import common as c

class KomplexKabel:
    def __init__(self, index: int, image: pygame.surface.Surface, pos:tuple=(0, 0), done:bool=False, scaling:float|int = 1) -> None:
        self.pos = pos
        self.scaling = scaling
        self.index = index
        self.image = image
        self.done = done
        self.mistake = False

        self.num = ((il.kabel_1_img, il.kabel_1_action), (il.kabel_2_img, il.kabel_2_action), (il.kabel_3_img, il.kabel_3_action),
                    (il.kabel_4_img, il.kabel_4_action))
        self.kabelek = []
        for _ in range(6):
            self.kabelek.append([r.randint(0, 3), False])

        self.num_kabel = [0, 1, 2, 3, 4, 5]

        self.cut_them = []
        self.feher = None

        # sárga lap
        if c.szeria_root[1] == 5:
            self.cut_them.append(4)

        else:
            if True in c.cells:
                self.feher = 1

            self.cut_them.append(0)

        # zöld lap
        if c.szeria_root[1] == 3 or c.szeria_root[1] == 9:
            self.cut_them.append(2)

        elif c.szeria_root[1] == 4:
            self.cut_them.append(3)

        elif c.stickers[2] or c.szeria_root[1] == 8:
            self.cut_them.append(3)

        else:
            if True not in c.cells:
                self.feher = 4

            if not c.stickers[0]:
                self.cut_them.append(3)

            else:
                self.cut_them.append(2)

        # fehér 4. oldal
        if self.feher == 1:
            if c.szeria_root[1] > 7:
                self.cut_them.append(5)

            elif c.stickers[0]:
                self.cut_them.append(5)

            elif c.szeria_root[1] < 5:
                self.cut_them.append(1)

            else:
                self.feher = 4

        if self.feher == 4:
            if c.szeria_root[1] < 5:
                current_root = c.szeria_root[1] + 5

            else:
                current_root = c.szeria_root[1]

            if current_root == 5:
                self.cut_them.append(5)

            elif current_root == 6:
                self.cut_them.append(1)

    def draw(self, timer = None):
        if self.pos == (0, 0):
            make = True
        else:
            make = False

        c.modul_draw(self)

        if make:
            for i in range(len(self.kabelek)):
                self.num_kabel[i] = c.Button(self.pos[0] + 22*self.scaling + 28 * i*self.scaling, self.pos[1] + 23*self.scaling, self.num[self.kabelek[i][0]][0], self.scaling)

        for i in range(len(self.kabelek)):
            if self.done:
                if self.kabelek[i][1]:

                    for j in range(len(self.kabelek)):
                        if self.kabelek[j][1]:
                            self.num_kabel[i].cable_draw(self.kabelek[i][1], self.num[self.kabelek[i][0]][1])

                else:
                    c.Image(self.pos[0] + 22*self.scaling + 28 * i*self.scaling, self.pos[1] + 23*self.scaling, self.num[self.kabelek[i][0]][0], self.scaling)

            else:
                self.kabelek[i][1] = self.num_kabel[i].cable_draw(self.kabelek[i][1], self.num[self.kabelek[i][0]][1])

                if self.kabelek[i][1]:
                    if i in self.cut_them:

                        count = 0
                        for j in range(len(self.kabelek)):
                            if self.kabelek[j][1]:
                                count += 1

                        if count == len(self.cut_them):
                            self.done = True

                    else:
                        self.mistake = True

    def update(self):
        self.scaling = c.g_scale
        self.pos = (0, 0)
