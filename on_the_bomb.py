import pygame
import random as r
import img_load as il
import common as c

def On_the_Bomb_sticker(self):
    self.sticker_buttons = []
    for i in range(len(self.current_sticker)):
        self.sticker_buttons.append(c.Button(self.pos_list[self.current_sticker[i][0]][0], self.pos_list[self.current_sticker[i][0]][1], self.current_sticker[i][1], self.scaling))

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

        pos_list.append((c.bomb_pos_x+225*scaling+x_bonus, c.bomb_pos_y+3*scaling+y_bonus))

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

    def draw(self, sticker_page, game_page):
        for i in range(len(self.sticker_buttons)):
            if self.sticker_buttons[i].pos_button_draw(self.kijelolve[self.current_sticker[i][0]]):
                sticker_page.active = True
                sticker_page.choose_sticker = i
                game_page.active = False


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

                c.Image(c.bomb_pos_x*self.scaling+x_bonus, c.bomb_pos_y+130*self.scaling+y_bonus, self.cells_img[i//2], self.scaling)

    def update(self):
        self.scaling = c.g_scale

        self.pos_list = On_the_Bomb_s_pos(self.scaling)
        On_the_Bomb_sticker(self)

