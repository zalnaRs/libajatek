import pygame
import common as c

class Idozito:
    def __init__(self, index:int, image:pygame.surface.Surface, pos:tuple=(0, 0), done:bool=True, scaling:float|int = 1) -> None:
        self.pos = pos
        self.scaling = scaling
        self.index = index
        self.image = image
        self.done = done
        self.mistake = False

        self.time = None

        self.changing_colors = [(255, 0, 0), (255, 135, 35), (235, 35, 200)]
        self.changing_back_color = [(155, 0, 40), (210, 80, 25), (135, 35, 200)]

    def draw(self, **timer):
        if self.pos == (0,0):
            make = True
        else:
            make = False

        c.modul_draw(self)

        if make:
            self.szamlalo = c.Timer(self.pos[0]+55*self.scaling, self.pos[1]+113*self.scaling, 36*self.scaling, self.time)


        c.Image(self.pos[0], self.pos[1], self.image, self.scaling)

        color = self.changing_colors[self.szamlalo.changing_ind]
        back_color = self.changing_back_color[self.szamlalo.changing_ind]

        background = pygame.Rect(self.pos[0]+39*self.scaling, self.pos[1]+108*self.scaling, 146*self.scaling, 63*self.scaling)
        pygame.draw.rect(c.screen, back_color, background)
        self.szamlalo.timer_draw(color)

        cooldown = pygame.Rect(self.pos[0]+27*self.scaling, self.pos[1]+27*self.scaling, 40*(self.szamlalo.current_seconds%5)*self.scaling+10*self.scaling, 13*self.scaling)
        pygame.draw.rect(c.screen, color, cooldown)

    def update(self):
        self.scaling = c.g_scale
        self.pos = (0, 0)

