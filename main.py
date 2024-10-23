import pygame

pygame.init()
# TODO: ezt a kettőt fixálni
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("PRO LIBA JÁTÉK")
clock = pygame.time.Clock()
running = True
dt = 0

center = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

pygame.font.init()
# TODO: töltsunk be egy saját betütipust
font = pygame.font.SysFont('Montserrat', 18)

class Button:
    def __init__(self, x, y, width, height, text='', font_size=36, font_color=(0, 0, 0), button_color=(200, 200, 200), hover_color=(150, 150, 150)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.button_color = button_color
        self.hover_color = hover_color
        self.clicked = False
        self.font = pygame.font.Font(None, font_size)

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.button_color, self.rect)

        text_surface = self.font.render(self.text, True, self.font_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self):
        """ Ellenőrzi, hogy rákattintottak-e a gombra """
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if self.rect.collidepoint(mouse_pos) and mouse_click[0]:  # Bal egérgomb (0 index)
            return True
        return False


def draw_text_with_word_wrap(screen, text, font, color, x, y, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "

    if current_line:
        lines.append(current_line)

    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        screen.blit(text_surface, (x, y + i * font.get_height()))

class Module:
    def __init__(self, x, y, kerdes, tipus, valaszok, megoldas):
        self.valaszok = valaszok
        self.renderRect = pygame.Rect(x, y, 320, 320)
        self.tipus = tipus
        self.megoldas = megoldas
        self.kerdes = kerdes
    def draw(self):
        pygame.draw.rect(screen, (0, 0, 0), self.renderRect)

        draw_text_with_word_wrap(screen, self.kerdes, font, (255,255,255),self.renderRect.right/2, self.renderRect.bottom/2-20, 300)

        #gombok
        x = self.renderRect.x
        for i, valasz in enumerate(self.valaszok):
            # egymás alá helyezés
            y = self.renderRect.bottom-50
            if i >= 2:
                if i == 2:
                    x=0
                y=self.renderRect.bottom-100
            btn = Button(x,y, 160, 50, valasz)
            btn.draw()
            x += btn.rect.width

modules = [Module(0, 0, "A Márton naphoz milyen felvonulás kapcsolódik?", "tobb", ["lámpás", "zsiroskenyer", "valami2", "valami3"], "lámpás")]

jelenlegimodule = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    modules[jelenlegimodule].draw()

    keys = pygame.key.get_pressed()

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()
