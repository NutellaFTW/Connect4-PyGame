import random
import sys

import pygame as pg

pg.init()

current_map = 0


class Map:

    def __init__(self):
        self.step = 10
        self.point_rectangles = []
        self.track_objects = []
        self.box_width = 50
        self.box_amount = 30
        self.players = [Player(1, random.randint(1, window_manager.WIDTH - 1),
                        random.randint(1, window_manager.HEIGHT - Controls.BOX_HEIGHT)),
                        Player(2, random.randint(1, window_manager.WIDTH - 1),
                               random.randint(1, window_manager.HEIGHT - Controls.BOX_HEIGHT))]

    def generate_map(self):
        self.calculate_points()
        self.generate_track()

    def calculate_points(self):
        for x in range(window_manager.WIDTH):
            for y in range(window_manager.HEIGHT - controls.BOX_HEIGHT):
                if x % self.step == 0 and y %  self.step == 0:
                    self.point_rectangles.append((x, y))

    def draw_buffered_points(self):
        for point in self.point_rectangles:
            pg.draw.rect(window_manager.display, (255, 255, 255), pg.Rect(point[0], point[1], 1, 1))

    def generate_track(self):
        for i in range(self.box_amount):
            color = (255, 0, 0)
            if i == self.box_amount - 1:
                color = (0, 255, 0)
            if i == self.box_amount - 2:
                color = (0, 0, 255)
            rectangle = pg.Rect(random.randint(0, window_manager.WIDTH / 10) * 10,
                                random.randint(0, (window_manager.HEIGHT - controls.BOX_HEIGHT) / 10) * 10,
                                self.box_width, self.box_width)
            for appended in self.track_objects:
                overlapping = appended[1]
                while overlapping.left <= rectangle.left <= overlapping.left + overlapping.width or (
                        overlapping.top <= rectangle.top <= overlapping.top + overlapping.height) or (
                        rectangle.top + rectangle.height >= window_manager.HEIGHT - controls.BOX_HEIGHT):
                    rectangle = pg.Rect(random.randint(0, window_manager.WIDTH / 10) * 10,
                                        random.randint(0, (window_manager.HEIGHT - controls.BOX_HEIGHT) / 10) * 10,
                                        self.box_width, self.box_width)
            self.track_objects.append((color, rectangle))

    def draw_track(self):
        for rectangle in self.track_objects:
            pg.draw.rect(window_manager.display, rectangle[0], rectangle[1])

    @staticmethod
    def draw_current_map():
        maps[current_map].draw_buffered_points()
        maps[current_map].draw_track()

    @staticmethod
    def swap_map(new_map):
        global current_map
        current_map = new_map


class Player:

    def __init__(self, _id, left, top):
        self.id = _id
        if _id == 1:
            self.color = (206, 120, 54)
        else:
            self.color = (142, 81, 133)
        self.left = left
        self.top = top
        self.width = 10
        self.generated = False

    def generate_player(self):
        if not self.generated:
            point = tuple(window_manager.display.get_at((self.left + 1, self.top + 1))[:3])
            while point != (255, 255, 255):
                point = tuple(window_manager.display.get_at((self.left, self.top))[:3])
                self.left = random.randint(1, window_manager.WIDTH - 1)
                self.top = random.randint(1, window_manager.HEIGHT - Controls.BOX_HEIGHT)
            self.generated = True

    def draw_player(self):
        pg.draw.rect(window_manager.display, self.color, (self.left - 1, self.top - 1, self.width, self.width))


class Controls:

    BOX_HEIGHT = 150

    @staticmethod
    def control_button_down(player, x, y):

        player = str(player)

        if x == 1:
            print(player + " clicked right")
        elif x == -1:
            print(player + " clicked left")

        if y == 1:
            print(player + " clicked up")
        elif y == -1:
            print(player + " clicked down")


    @staticmethod
    def control_loop():

        pg.draw.rect(window_manager.display, (0, 0, 0), pg.Rect(0, window_manager.HEIGHT - 150, window_manager.WIDTH,
                                                                window_manager.HEIGHT - Controls.BOX_HEIGHT))

        pg.draw.rect(window_manager.display, (255, 255, 255),
                     pg.Rect(0, window_manager.HEIGHT - Controls.BOX_HEIGHT, window_manager.WIDTH, 5))
        pg.draw.rect(window_manager.display, (255, 255, 255),
                     pg.Rect(0, window_manager.HEIGHT - 5, window_manager.WIDTH, 5))
        pg.draw.rect(window_manager.display, (255, 255, 255), pg.Rect(0, window_manager.HEIGHT - Controls.BOX_HEIGHT, 5,
                                                                      window_manager.HEIGHT - Controls.BOX_HEIGHT))
        pg.draw.rect(window_manager.display, (255, 255, 255),
                     pg.Rect(window_manager.WIDTH - 5, window_manager.HEIGHT - Controls.BOX_HEIGHT, 5,
                             window_manager.HEIGHT - Controls.BOX_HEIGHT))
        pg.draw.rect(window_manager.display, (255, 255, 255),
                     pg.Rect(window_manager.WIDTH / 2, window_manager.HEIGHT - Controls.BOX_HEIGHT, 5,
                             window_manager.HEIGHT - Controls.BOX_HEIGHT))

        # Player 1 Buttons

        Utils.draw_button("Wingdings 3.ttf", 75, "f", window_manager.WIDTH / 2 - 375, window_manager.HEIGHT - 115, 75,
                          75, (255, 255, 255), (200, 200, 200), lambda: Controls.control_button_down(1, -1, 0))
        Utils.draw_button("Wingdings 3.ttf", 75, "g", window_manager.WIDTH / 2 - 225, window_manager.HEIGHT - 115, 75,
                          75, (255, 255, 255), (200, 200, 200), lambda: Controls.control_button_down(1, 1, 0))
        Utils.draw_button("Wingdings 3.ttf", 75, "i", window_manager.WIDTH / 2 - 300, window_manager.HEIGHT - 75, 75,
                          55, (255, 255, 255), (200, 200, 200), lambda: Controls.control_button_down(1, 0, -1))
        Utils.draw_button("Wingdings 3.ttf", 75, "h", window_manager.WIDTH / 2 - 300, window_manager.HEIGHT - 130, 75,
                          55, (255, 255, 255), (200, 200, 200), lambda: Controls.control_button_down(1, 0, 1))

        # Player 2 Buttons

        Utils.draw_button("Wingdings 3.ttf", 75, "f", window_manager.WIDTH - 375, window_manager.HEIGHT - 115, 75,
                          75, (255, 255, 255), (200, 200, 200), lambda: Controls.control_button_down(2, -1, 0))
        Utils.draw_button("Wingdings 3.ttf", 75, "g", window_manager.WIDTH - 225, window_manager.HEIGHT - 115, 75,
                          75, (255, 255, 255), (200, 200, 200), lambda: Controls.control_button_down(2, 1, 0))
        Utils.draw_button("Wingdings 3.ttf", 75, "i", window_manager.WIDTH - 300, window_manager.HEIGHT - 75, 75,
                          55, (255, 255, 255), (200, 200, 200), lambda: Controls.control_button_down(2, 0, -1))
        Utils.draw_button("Wingdings 3.ttf", 75, "h", window_manager.WIDTH - 300, window_manager.HEIGHT - 130, 75,
                          55, (255, 255, 255), (200, 200, 200), lambda: Controls.control_button_down(2, 0, 1))


class Utils:

    @staticmethod
    def draw_button(font, font_size, msg, left, top, width, height, inactive, hovered, action=None):

        mouse = pg.mouse.get_pos()

        clicked = pg.mouse.get_pressed()

        color = inactive

        if left + width > mouse[0] > left and top + height > mouse[1] > top:
            color = hovered
            if clicked[0] == 1 and action is not None:
                action()

        pg.draw.rect(window_manager.display, color, (left, top, width, height))

        text = pg.font.Font(font, font_size)

        text_surface = text.render(msg, True, (0, 0, 0))
        text_rectangle = text_surface.get_rect()

        text_rectangle.center = (left + (width / 2), top + (height / 2))

        window_manager.display.blit(text_surface, text_rectangle)


class Window:

    WIDTH, HEIGHT = 1200, 700

    RUNNING = False

    FPS = 60

    display = pg.display.set_mode((WIDTH, HEIGHT))

    pg.display.set_caption("pygame is such a burger thumb")

    clock = pg.time.Clock()

    def __init__(self):
        self.display.fill((0, 0, 0))

    def start_loop(self):

        self.RUNNING = True

        loop = 0

        while self.RUNNING:

            self.display.fill((0, 0, 0))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.RUNNING = False
                    pg.quit()
                    sys.exit()

            Map.draw_current_map()

            controls.control_loop()

            if loop == 2:
                for _map in maps:
                    for player in _map.players:
                        player.generate_player()

            for player in maps[current_map].players:
                player.draw_player()

            loop += 1

            self.clock.tick(self.FPS)
            pg.display.update()


window_manager = Window()

maps = [Map(), Map(), Map(), Map(), Map()]

controls = Controls()

for map_list in maps:
    map_list.generate_map()

window_manager.start_loop()
