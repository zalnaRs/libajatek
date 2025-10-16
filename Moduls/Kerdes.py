import pygame
import random as r
import Moduls.img_load as il
import Moduls.common as c

class Panel:
    def __init__(self, index:int = None, image:pygame.surface.Surface = il.kerdes_modul_img, pos:tuple=(0, 0), done:bool=False, scaling:float|int = 1) -> None:
        self.id = "Kerdes"
        self.pos = pos
        self.scaling = scaling
        self.index = index
        self.image = image
        self.done = done
        self.mistake = False

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

    def draw(self, timer = None):
        if self.pos == (0,0):
            make = True
        else:
            make = False

        c.modul_draw(self)

        if make:
            for i in range(len(self.gombok)):
                if i > 1:
                    half = 5*self.scaling

                else:
                    half = 0

                self.gombok[i] = c.Button(self.pos[0]+23*self.scaling+48*i*self.scaling+half, self.pos[1]+139, self.betuk[i][0], self.scaling)

        if self.done:
            for i in range(len(self.gombok)):
                if i > 1:
                    half = 5*self.scaling

                else:
                    half = 0
                
                c.Image(self.pos[0]+23*self.scaling+48*i*self.scaling+half, self.pos[1]+139*self.scaling, self.betuk[i][0], self.scaling)

            c.Image(self.pos[0]+22*self.scaling, self.pos[1]+198*self.scaling, self.progress[-1], self.scaling)
            c.text_draw("( =", self.pos[0]+78*self.scaling, self.pos[1]+32*self.scaling, (255,255,255), pygame.font.Font(c.family, 36*self.scaling))

        else:
            c.display_text(self.kerdesek[self.current_kerdesek[self.current_kerdes]][0], (self.pos[0]+37*self.scaling, self.pos[1]+32*self.scaling), self.pos[0]+190*self.scaling, pygame.font.Font(c.family, self.kerdesek[self.current_kerdesek[self.current_kerdes]][1]))
            c.Image(self.pos[0]+22*self.scaling, self.pos[1]+198*self.scaling, self.progress[self.current_kerdes], self.scaling)
            for i in range(len(self.gombok)):
                if self.gombok[i].button_draw(self.betuk[i][1])[0]:
                    if i == self.valaszok[self.current_kerdesek[self.current_kerdes]]:
                        if self.current_kerdes == 3:
                            self.done = True

                        else:
                            self.current_kerdes += 1

                    else:
                        self.mistake = True

    def update(self):
        self.scaling = c.g_scale
        self.pos = (0, 0)

