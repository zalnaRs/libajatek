import pygame
import Moduls.common as c
import Moduls.defs as f
import Moduls.img_load as il

class Panel:
    def __init__(self, index:int = None, image:pygame.surface.Surface = il.jelszo_modul_img, pos:tuple=(0, 0), done:bool=False, scaling:float|int = 1) -> None:
        self.id = "Jelszo"
        self.pos = pos
        self.scaling = scaling
        self.index = index
        self.image = image
        self.done = done
        self.buffer_save = ""
        self.mistake = False

        self.jelszo = f.password()
        self.update_list = None

    def draw(self, timer):
        if self.pos == (0,0):
            make = True
        else:
            make = False

        c.modul_draw(self)

        if make:
            self.rect = pygame.Rect(self.pos[0]+71*self.scaling, self.pos[1]+171*self.scaling, 82*self.scaling, 25*self.scaling)
            self.input = c.Input(self.rect.x, self.rect.y, 82*self.scaling, 25*self.scaling, 16*self.scaling, self.update_list, True)
            if self.buffer_save != "":
                self.input.buffer = self.buffer_save

        for i in range(len(self.jelszo[1][0])):
            for j in range(len(self.jelszo[1])):
                if i == 0 or i == 3:
                    plus = 0
                else:
                    plus = 2*self.scaling
                c.text_draw(self.jelszo[1][j][i], self.pos[0]+25*self.scaling+40*j*self.scaling+plus, self.pos[1]+15*self.scaling+34*i*self.scaling, (57, 57, 57), pygame.font.Font(c.family, 21*self.scaling))

        if self.done:
            pygame.draw.rect(c.screen, (57, 35, 0), self.rect)
            pygame.draw.rect(c.screen, (31, 19, 0), self.rect, 2)
        else:
            self.input.input_draw(True, timer, 5, -1, (57, 35, 0), (255, 255, 255), (31, 19, 0), (255,255,255), pygame.Rect(self.pos[0], self.pos[1], 244*self.scaling, 244*self.scaling))

        if self.input.value != "":
            if self.input.value.lower() == self.jelszo[0]:
                self.done = True

            else:
                self.mistake = True

    def update(self):
        self.scaling = c.g_scale
        self.pos = (0, 0)
        if self.input.buffer != "":
            self.buffer_save = self.input.buffer

