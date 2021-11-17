import random
import pygame
import sys

pygame.init()

# colours
AQUA = (0, 255, 255)
BANANA = (227, 207, 87)
CORAL = (255, 127, 80)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 183, 235)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
INDIGO = (75, 0, 130)
PURPLE = (255, 255, 0)
VIOLET = (134, 1, 175)
ORANGE = (255, 165, 0)
PINK = (255, 200, 200)
GREY = (127, 127, 127)

# settings (can be changed)
WIDTH, HEIGHT = 1000, 600
FPS = 60

# makes screen and caption
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# rotors and reflectors for choosing later
ROTOR1 = [24, 6, 21, 20, 0, 22, 17, 15, 14, 13, 4,
          19, 11, 23, 18, 2, 5, 16, 3, 10, 12, 8, 25, 9, 1, 7]
ROTOR2 = [8, 20, 23, 10, 25, 21, 14, 0, 4, 13, 15,
          22, 1, 12, 24, 6, 11, 17, 19, 7, 18, 2, 3, 5, 9, 16]
ROTOR3 = [8, 15, 24, 18, 3, 11, 5, 4, 12, 1, 17, 2,
          7, 23, 25, 20, 9, 0, 10, 19, 13, 6, 14, 21, 22, 16]
ROTOR4 = [19, 17, 16, 20, 13, 1, 4, 12, 15, 14, 21, 3,
          11, 8, 2, 22, 25, 7, 6, 24, 5, 23, 0, 9, 10, 18]
ROTOR5 = [25, 24, 15, 0, 16, 11, 23, 14, 10, 18,
          22, 20, 3, 7, 21, 19, 9, 2, 12, 13, 5, 8, 6, 4, 17, 1]

REFLECTOR = {
    1: 11,
    11: 1,
    25: 16,
    16: 25,
    4: 24,
    24: 4,
    18: 22,
    22: 18,
    15: 17,
    17: 15,
    3: 7,
    7: 3,
    13: 20,
    20: 13,
    0: 21,
    21: 0,
    2: 5,
    5: 2,
    14: 23,
    23: 14,
    6: 19,
    19: 6,
    8: 12,
    12: 8,
    10: 9,
    9: 10
}

REFLECTOR2 = {
    4: 3,
    3: 4,
    7: 19,
    19: 7,
    21: 15,
    15: 21,
    1: 23,
    23: 1,
    12: 6,
    6: 12,
    5: 25,
    25: 5,
    18: 8,
    8: 18,
    9: 13,
    13: 9,
    24: 20,
    20: 24,
    16: 0,
    0: 16,
    10: 2,
    2: 10,
    14: 22,
    22: 14,
    17: 11,
    11: 17
}

# puts rotors and reflectors into a list to be used easily later
ROTORS = [ROTOR1, ROTOR2, ROTOR3, ROTOR4, ROTOR5]
REFLECTORS = [REFLECTOR, REFLECTOR2]


class Button:

    def __init__(self, txt: str, x: int, y: int, func, parameter, colour: tuple, size: int, centre=True) -> None:
        """Button with text and function
        will display text at x, y and automatically create a hitbox
        """
        self.txt = txt
        self.font = pygame.font.SysFont("optima", size)
        self.font_size = self.font.size(self.txt)

        # centres text if centre
        if centre:
            self.x = x - (self.font_size[0] // 2)
            self.y = y - (self.font_size[1] // 2)
        else:
            self.x = x
            self.y = y

        self.rect = pygame.Rect(
            self.x, self.y, self.font_size[0], self.font_size[1])
        self.colour = colour

        self.func = func
        self.parameter = parameter

    def draw(self):
        pygame.draw.rect(WIN, BANANA, self.rect,
                         4)  # box
        draw_txt = self.font.render(self.txt, 1, self.colour)
        WIN.blit(draw_txt, (self.x, self.y))  # text

    def executeFunction(self):
        if self.parameter != None:
            self.func(self.parameter)
        else:
            self.func()


def drawEnigma(fill_colour: tuple, *args) -> None:
    """fills screen with fill_colour and then
    iterates through args and executes each item's draw() function
    """
    if fill_colour:
        WIN.fill(fill_colour)

    for item in args:
        item.draw()


class SelectRotor:

    def __init__(self, rotor: list, x: int, name: str) -> None:
        self.rotor = rotor
        self.x = x
        self.name = name
        self.rect = pygame.Rect(x, 15, 150, HEIGHT - 95)
        self.glow = False
        self.rotor_buttons = self.makeRotorButtons()

    def draw(self) -> None:
        font = pygame.font.SysFont("optima", 30)

        if self.glow:
            pygame.draw.rect(WIN, YELLOW, self.rect)

        pygame.draw.rect(WIN, BLACK, self.rect, 2)

        for n, rotor in enumerate(self.rotor):
            if n == 0:
                draw_n = font.render(str(rotor), 1, GREEN)
            else:
                draw_n = font.render(str(rotor), 1, BLUE)

            size = font.size(str(rotor))

            WIN.blit(draw_n, (self.x + 75 - (size[0] // 2), (n + 1) *
                     (HEIGHT - 100) // len(self.rotor)))

        for button in self.rotor_buttons:
            button.draw()

    def makeRotorButtons(self) -> list:
        size = 50
        buttons = []

        buttons.append(
            Button("<", self.x + 50, 550, self.rotateRotor, False, BLUE, size, True))
        buttons.append(
            Button(">", self.x + 100, 550, self.rotateRotor, True, BLUE, size, True))

        return buttons

    def rotateRotor(self, forward: bool) -> None:
        if forward:
            self.rotor = self.rotor[len(
                self.rotor)-1:] + self.rotor[:len(self.rotor)-1]
        else:
            self.rotor = self.rotor[1:] + self.rotor[:1]


def makeSelectRotors() -> list:
    select_rotors = []

    for n, rotor in enumerate(ROTORS):
        select_rotors.append(SelectRotor(
            rotor, 150 * n, f"ROTOR {str(n + 1)}"))

    return select_rotors


def drawSelectedRotors(selected_rotors: list) -> None:
    font = pygame.font.SysFont("optima", 20)

    draw_selected_txt = font.render("SELECTED ROTORS:", 1, RED)
    selected_txt_size = font.size("SELECTED ROTORS:")

    WIN.blit(draw_selected_txt, (875 - (selected_txt_size[0] // 2), 100))

    if selected_rotors:
        for n, rotor in enumerate(selected_rotors):
            draw_rotor_txt = font.render(rotor.name, 1, RED)
            rotor_txt_size = font.size(rotor.name)

            WIN.blit(draw_rotor_txt,
                     (875 - (rotor_txt_size[0] // 2), 100 + (n + 1) * 50))


def chooseRotors() -> list:
    rotors = makeSelectRotors()
    run = True
    selected_rotors = []
    pygame.display.set_caption("Choose Rotors")
    clock = pygame.time.Clock()

    while len(selected_rotors) < 3 and run:
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                for rotor in rotors:
                    if rotor.rect.collidepoint(pos) and rotor not in selected_rotors:
                        selected_rotors.append(rotor)

                    for button in rotor.rotor_buttons:
                        if button.rect.collidepoint(pos):
                            button.executeFunction()

        for rotor in rotors:
            if rotor.rect.collidepoint(pos):
                rotor.glow = True
            else:
                rotor.glow = False

        WIN.fill(WHITE)
        drawSelectedRotors(selected_rotors)
        drawEnigma(None, *rotors)
        pygame.display.flip()

        clock.tick(FPS)

    if not run:
        pygame.quit()
        sys.exit()

    pygame.display.flip()
    pygame.time.delay(200)

    out_rotors = []
    for rotor in selected_rotors:
        out_rotors.append(rotor.rotor)

    return out_rotors


class SelectReflector:

    def __init__(self, reflector: dict, x: int, name: str) -> None:
        self.reflector = reflector
        self.x = x
        self.name = name
        self.rect = pygame.Rect(x, 15, 500, HEIGHT - 95)
        self.glow = False

    def draw(self):
        font = pygame.font.SysFont("optima", 30)

        if self.glow:
            pygame.draw.rect(WIN, YELLOW, self.rect)
        pygame.draw.rect(WIN, BLACK, self.rect, 2)

        for i, n in enumerate(self.reflector):
            draw_n = font.render(f"{n} : {self.reflector[n]}", 1, GREEN)

            size = font.size(f"{n} : {self.reflector[n]}")
            WIN.blit(draw_n, (self.x + 250 - (size[0] // 2), (i + 1) *
                     (HEIGHT - 100) // len(self.reflector)))


def makeSelectReflectors() -> list:
    select_reflectors = []

    for n, reflector in enumerate(REFLECTORS):
        select_reflectors.append(SelectReflector(
            reflector, 500 * n, f"reflector {str(n + 1)}"))

    return select_reflectors


def chooseReflector() -> dict:
    reflectors = makeSelectReflectors()
    run = True
    selected_reflector = None
    pygame.display.set_caption("Choose Reflector")
    clock = pygame.time.Clock()

    while not selected_reflector and run:
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                for reflector in reflectors:
                    if reflector.rect.collidepoint(pos):
                        selected_reflector = reflector

        for reflector in reflectors:
            if reflector.rect.collidepoint(pos):
                reflector.glow = True
            else:
                reflector.glow = False

        drawEnigma(WHITE, *reflectors)
        pygame.display.flip()
        clock.tick(FPS)

    if not run:
        pygame.quit()
        sys.exit()

    return selected_reflector.reflector


class PlugboardLetter:

    def __init__(self, letter: str, x: int, y: int) -> None:
        self.letter = letter
        self.linked_letter = None

        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 80, 80)

        self.font = pygame.font.SysFont("optima", 80)
        self.txt = self.font.render(letter, 1, AQUA)
        self.size = self.font.size(letter)

        self.clicked = False

    def link(self, link_letter: int) -> None:
        self.linked_letter = link_letter
        link_letter.linked_letter = self

    def draw(self):
        if not self.clicked:
            pygame.draw.rect(WIN, RED, self.rect)
        elif self.clicked and not self.linked_letter:
            pygame.draw.rect(WIN, GREEN, self.rect)
        else:
            pygame.draw.rect(WIN, GREY, self.rect)

        WIN.blit(self.txt, (self.x + 40 - (self.size[0] // 2),
                            self.y + 40 - (self.size[1] // 2)))

        if self.linked_letter:
            linked_size = self.font.size(self.linked_letter.letter)
            WIN.blit(self.linked_letter.txt, (self.x + 40 - (linked_size[0] // 2),
                                              self.y + 110 - (linked_size[1] // 2)))

        pygame.draw.rect(WIN, BLACK, self.rect, 2)


def makePlugboardKeys() -> list:
    keys = []
    rows = [
        "abcdefghi",
        "jklmnopqr",
        "stuvwxyz"
    ]

    for i, row in enumerate(rows):
        for n, letter in enumerate(row):
            keys.append(PlugboardLetter(letter, 100 + (n * 90),
                                        50 + (150 * i)))

    return keys


def configurePlugboard() -> dict:
    plugboard = {}
    keys = makePlugboardKeys()
    current_key = None
    run = True
    pygame.display.set_caption("Configure Plugboard")
    clock = pygame.time.Clock()
    done = False

    finish_button = Button("Done", 900, 550, None, None, BLUE, 100)

    while len(plugboard) < 20 and not done and run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if finish_button.rect.collidepoint(pos):
                    done = True

                if not current_key:
                    for key in keys:
                        if key.rect.collidepoint(pos) and not key.linked_letter:
                            current_key = key
                            key.clicked = True
                else:
                    for key in keys:
                        if key.rect.collidepoint(pos) and not key.linked_letter:
                            key.link(current_key)
                            key.clicked = True
                            current_key = None

                            plugboard[ord(key.letter) -
                                      97] = ord(key.linked_letter.letter) - 97
                            plugboard[ord(key.linked_letter.letter) -
                                      97] = ord(key.letter) - 97

        drawEnigma(WHITE, *keys, finish_button)
        pygame.display.flip()
        clock.tick(FPS)

    if not run:
        pygame.quit()
        sys.exit()

    return plugboard


class Key:

    def __init__(self, letter: str, x: int, y: int) -> None:
        self.letter = letter
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 40, 40)

        self.font = pygame.font.SysFont("optima", 40)
        self.txt = self.font.render(letter, 1, AQUA)
        self.size = self.font.size(letter)

        self.pressed = False

    def draw(self):
        if self.pressed:
            pygame.draw.rect(WIN, GREEN, self.rect)
        else:
            pygame.draw.rect(WIN, RED, self.rect)

        WIN.blit(self.txt, (self.x + 20 - (self.size[0] // 2),
                            self.y + 20 - (self.size[1] // 2)))

        pygame.draw.rect(WIN, BLACK, self.rect, 2)


def makeKeys() -> list:
    in_keys = []

    rows = [
        "qwertyuiop",
        "asdfghjkl",
        "zxcvbnm"
    ]

    for i, row in enumerate(rows):
        for n, letter in enumerate(row):
            in_keys.append(Key(letter, 300 + (i * 30) + (n * 40),
                               300 + (i * 100)))

    return in_keys


def makeLines(txt: str) -> list:
    lines = []

    if len(txt) > 120:
        lines.append(txt[:40])
        lines.append(txt[40:80])
        lines.append(txt[80:120])
        lines.append(txt[120:])
    elif len(txt) > 80:
        lines.append(txt[:40])
        lines.append(txt[40:80])
        lines.append(txt[80:])
    elif len(txt) > 40:
        lines.append(txt[:40])
        lines.append(txt[40:])
    else:
        lines.append(txt)

    return lines


def drawText(txt: str) -> None:
    lines = makeLines(txt)

    if lines:
        for n, line in enumerate(lines):

            formatted_txt = f":{line}:"

            font = pygame.font.SysFont("optima", 50)
            size = font.size(formatted_txt)

            x = 500 - (size[0] // 2)
            y = 80 + (n * 50) - (size[1] // 2)

            draw_txt = font.render(formatted_txt, 1, BLUE)
            WIN.blit(draw_txt, (x, y))


def getKeyboardInput() -> str:
    txt = ""
    keys = makeKeys()
    run = True
    pygame.display.set_caption("Get Keyboard Input")
    clock = pygame.time.Clock()
    done = False

    backspace_timer = 0
    backspace_cooldown = 100

    alphabet = "abcdefghijklmnopqrstuvwxyz"

    finish_button = Button("Done", 900, 550, None, None, BLUE, 50)

    while not done and run:
        pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if finish_button.rect.collidepoint(pos):
                    done = True

            if pressed[pygame.K_BACKSPACE] and backspace_timer <= 0 and txt:
                txt = txt[:len(txt)-1]
                backspace_timer = backspace_cooldown

            if event.type == pygame.KEYDOWN and len(txt) < 160:
                if pygame.key.name(event.key) in alphabet:
                    for key in keys:
                        if key.letter == pygame.key.name(event.key):
                            key.pressed = True
                            if pressed[pygame.K_LSHIFT]:
                                txt += key.letter.upper()
                            else:
                                txt += key.letter

                if event.key == pygame.K_SPACE:
                    txt += " "

            if event.type == pygame.KEYUP:
                if pygame.key.name(event.key) in alphabet:
                    for key in keys:
                        if key.letter == pygame.key.name(event.key):
                            key.pressed = False

        drawEnigma(WHITE, *keys, finish_button)
        drawText(txt)
        pygame.display.flip()

        eta = clock.tick(FPS)

        if backspace_timer > 0:
            backspace_timer -= eta

    if not run:
        pygame.quit()
        sys.exit()

    return txt.strip()


class Textbox:

    def __init__(self, x: int, y: int, width: int, height: int, text: str) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

        self.text = text
        self.font = pygame.font.SysFont("optima", 40)

    def draw(self):
        pygame.draw.rect(WIN, BLUE, self.rect, 10, 2)
        lines = makeLines(self.text)

        if lines:
            for n, line in enumerate(lines):

                formatted_text = line

                size = self.font.size(formatted_text)

                draw_text = self.font.render(formatted_text, 1, BLUE)
                WIN.blit(draw_text, ((self.x + self.width // 2 - size[0] // 2,
                                      (40 * n) + self.y + size[1] // 2)))


def makeTextboxes(text: str) -> object:
    textbox_in = Textbox(100, 0, 800, 180, text)
    textbox_out = Textbox(100, 420, 800, 180, "")
    return textbox_in, textbox_out


def rotateRotor(rotor1: list, rotor2: list, rotor3: list,
                o_rotor1: list, o_rotor2: list, o_rotor3: list) -> list:
    rotor1 = rotor1[len(rotor1)-1:] + rotor1[:len(rotor1)-1]
    if rotor1 == o_rotor1:
        rotor2 = rotor2[len(rotor2)-1:] + rotor2[:len(rotor2)-1]
        if rotor2 == o_rotor2:
            rotor3 = rotor3[len(rotor3)-1:] + rotor3[:len(rotor3)-1]

    return rotor1, rotor2, rotor3


def plugboardConvert(letter: str, plugboard: dict) -> str:
    conv_n = 0

    if letter.islower():
        conv_n = 97
    elif letter.isupper():
        conv_n = 65
    else:
        raise Exception("The enigma machine only processes letters")

    if (ord(letter) - conv_n) in plugboard:
        out_letter = chr(plugboard[ord(letter) - conv_n] + conv_n)
    else:
        out_letter = letter

    return out_letter


def processLetter(letter: str, conv_n: int, rotor1: list, rotor2: list, rotor3: list,
                  o_rotor1: list, o_rotor2: list, o_rotor3: list) -> str:
    if letter.islower():
        conv_n = 97
    elif letter.isupper():
        conv_n = 65

    rotor1, rotor2, rotor3 = rotateRotor(rotor1, rotor2, rotor3,
                                         o_rotor1, o_rotor2, o_rotor3)

    # index passes through rotors 3 2 1 then reflects and passes back through rotors 1 2 3
    return chr(
        rotor3.index(
            rotor2.index(
                rotor1.index(
                    REFLECTOR[
                        rotor1[
                            rotor2[
                                rotor3[
                                    ord(letter) - conv_n
                                ]]]
                    ]
                )))
        + conv_n), rotor1, rotor2, rotor3


def enigma(rotors: list, letter: str, plugboard: dict,
           o_rotor1: list, o_rotor2: list, o_rotor3: list) -> str:
    rotor1 = rotors[0]
    rotor2 = rotors[1]
    rotor3 = rotors[2]

    letter = plugboardConvert(letter, plugboard)

    conv_n = 0

    if letter.islower():
        conv_n = 97
    elif letter.isupper():
        conv_n = 65
    else:
        raise Exception("The enigma machine only processes letters")

    out_letter, rotor1, rotor2, rotor3 = processLetter(letter, conv_n,
                                                       rotor1, rotor2, rotor3, o_rotor1, o_rotor2, o_rotor3)

    out_letter = plugboardConvert(out_letter, plugboard)

    n_rotors = [rotor1, rotor2, rotor3]

    return out_letter, n_rotors


def getRotorNs(rotors: list) -> list:
    rotor_n_list = []

    for rotor in rotors:
        rotor_list = [rotor[len(rotor)-1], rotor[0], rotor[1]]
        rotor_n_list.append(rotor_list)

    return rotor_n_list


def drawRotors(rotors: list) -> None:
    font = pygame.font.SysFont("optima", 70)

    rotor_n_list = getRotorNs(rotors)

    for n, rotor in enumerate(rotor_n_list):

        for i, number in enumerate(rotor):
            if i == 1:
                draw_txt = font.render(str(number), 1, YELLOW)
            else:
                draw_txt = font.render(str(number), 1, GREEN)

            size = font.size(str(number))

            WIN.blit(draw_txt, (200 + (300 * n) - (size[0] // 2),
                                220 + (80 * i) - (size[1] // 2)))

    pygame.display.flip()


def visualiseEnigma(rotors: list, reflector: dict, plugboard: dict, text: str) -> str:
    run = True
    pygame.display.set_caption("Visualise Enigma")
    clock = pygame.time.Clock()
    done = False

    o_rotor1 = rotors[0]
    o_rotor2 = rotors[1]
    o_rotor3 = rotors[2]
    rotor1 = o_rotor1.copy()
    rotor2 = o_rotor2.copy()
    rotor3 = o_rotor3.copy()
    n_rotors = [rotor1, rotor2, rotor3]

    enigma_cooldown = 0
    enigma_gap = 200

    textbox_in, textbox_out = makeTextboxes(text)

    while not done and run and len(textbox_in.text) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        eta = clock.tick(FPS)
        enigma_cooldown -= eta

        if enigma_cooldown <= 0:
            enigma_cooldown = enigma_gap
            in_letter = textbox_in.text[0]
            textbox_in.text = textbox_in.text[1:]

            if in_letter == " ":
                out_letter = " "
            else:
                out_letter, n_rotors = enigma(
                    n_rotors, in_letter, plugboard, o_rotor1, o_rotor2, o_rotor3)

            textbox_out.text += out_letter

        drawEnigma(BLACK, textbox_in, textbox_out)
        drawRotors(n_rotors)

    if not run:
        print("program was terminated abruptly during the visualisation process")
        pygame.quit()
        sys.exit()

    pygame.time.delay(500)

    return textbox_out.text


def main():
    rotors = chooseRotors()
    reflector = chooseReflector()
    plugboard = configurePlugboard()
    text = getKeyboardInput()
    out_text = visualiseEnigma(rotors, reflector, plugboard, text)
    pygame.quit()
    return out_text


if __name__ == "__main__":
    print(main())
