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
font = pygame.font.Font(None, 18)
big_font = pygame.font.Font(None, 24)


class Button:
    def __init__(self, x, y, width, height, text='', font_size=36, font_color=(0, 0, 0), button_color=(200, 200, 200),
                 hover_color=(150, 150, 150)):
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
    def __init__(self, kerdes, tipus, valaszok, megoldas, rectX, rectY):
        self.valaszok = valaszok
        self.renderRect = pygame.Rect(rectX, rectY, 320, 320)
        self.tipus = tipus
        self.megoldas = megoldas
        self.kerdes = kerdes
        self.kivalasztott = ""

    def draw(self):
        pygame.draw.rect(screen, (0, 0, 0), self.renderRect)

        draw_text_with_word_wrap(screen, self.kerdes, big_font, (255, 255, 255),
                                 self.renderRect.centerx / 2 - 20 + self.renderRect.x / 2, self.renderRect.centery - 80,
                                 240)

        # gombok
        x = self.renderRect.x
        for i, valasz in enumerate(self.valaszok):
            # egymás alá helyezés
            y = self.renderRect.bottom - 50
            if i >= 2:
                if i == 2:
                    x = self.renderRect.x
                y = self.renderRect.bottom - 100
            button_color = (200, 200, 200)
            if self.kivalasztott == valasz:
                button_color = (46, 194, 126)
            btn = Button(x, y, 160, 50, valasz, 36, (0, 0, 0), button_color)
            btn.draw()
            if btn.is_clicked():
                self.kivalasztott = valasz
            x += btn.rect.width


# modules = [Module("", "tobb", ["lámpás", "zsiroskenyer", "valami2", "valami3"], "lámpás", 0),
#     Module("A Márton naphoz milyen felvonulás kapcsol2222ódik?", "tobb",
#            ["lámpás", "zsiroskenyer", "valami2", "valami3"], "lámpás", 320),
#     Module("A Márton naphoz milyen felvonulás kapcsol2222ód123123ik?", "tobb", ["1231", "123123", "123", "valami3"],
#            "1231", 640)]

modules = []

y = 0
x = 0

for i, module in enumerate([{"kerdes": "A Márton naphoz milyen felvonulás kapcsolódik?", "tipus": "tobb",
                             "valaszok": ["lampás", "zsiroskenyer", "valami2", "valami3"], "megoldas": "lampas"},
                            {"kerdes": "A Márton213123123 naphoz milyen felvonulás kapcsolódik?", "tipus": "tobb",
                             "valaszok": ["lampás", "zsiroskenyer", "valami2", "valami3"], "megoldas": "lampas"},
                            {"kerdes": "A Márton naphoz milyen felvonulás kapcsolódik?", "tipus": "tobb",
                             "valaszok": ["lam2222pás", "22222", "213123123", "123123"], "megoldas": "123123"},
                            {"kerdes": "A Márton qqqq milyen felvonulás kapcsolódik?", "tipus": "tobb",
                             "valaszok": ["11111", "22222", "211113123123", "123123"], "megoldas": "123123"},
                            {"kerdes": "A Márton nwwwwwaphoz milyen felvonulás kapcsolódik?", "tipus": "tobb",
                             "valaszok": ["asdasda", "2qwewe2222", "213q123123", "123123"], "megoldas": "123123"}]):
    if i == 4:
        y = 320
        x -= 1280
    if i != 0:
        x += 320
    modules.append(Module(module["kerdes"], module["tipus"], module["valaszok"], module["megoldas"], x, y))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    for module in modules[:]:
        module.draw()

    keys = pygame.key.get_pressed()

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()
