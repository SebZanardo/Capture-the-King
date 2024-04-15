import pygame
import random
from sys import exit

pygame.init()

screen = pygame.display.set_mode((1240, 700))
screen_rect = screen.get_rect()
clock = pygame.time.Clock()

# Initialise map stuff
rest_surf = pygame.image.load("Graphics/Fire_Symbol.png").convert_alpha()
fight_surf = pygame.image.load("Graphics/Fight_Symbol.png").convert_alpha()
map_bg_surf = pygame.image.load("Graphics/map_bg.png").convert_alpha()
empty_surface = pygame.image.load("Graphics/Empty.png").convert_alpha()
shop_surf = pygame.image.load("Graphics/Shop_Symbol_Single1.png").convert_alpha()
boss_surf = pygame.image.load("Graphics/Boss_Symbol.png").convert_alpha()


class Node:

    path = None
    eventtype = None
    surf = None
    rect = None
    pos = (0, 0)

    def __init__(self, rect):
        self.rect = rect
        self.pos = (rect.x, rect.y)

    def get_surf(self):
        global rest_surf, fight_surf, map_bg_surf, empty_surface, shop_surf
        if self.eventtype == 'Shop':
            self.surf = shop_surf
        elif self.eventtype == 'Fight':
            self.surf = fight_surf
        elif self.eventtype == 'rest_surf':
            self.surf = rest_surf
        elif self.eventtype == 'Boss':
            self.surf = boss_surf
        else:
            self.surf = empty_surface


    # Define floors
num_floors = 15
events_per_floor = 7

Floors = []
floor_height = 64
item_width = 64

for number in range(0, num_floors):
    Floors.append([])
a = 0
for floor in Floors:
    for event in range(0, events_per_floor):
        rect_top = (64 * (num_floors - a))
        rect_left = item_width * event
        new_rect = pygame.rect.Rect((rect_left, rect_top), (item_width, floor_height))
        new_node = Node(new_rect)
        floor.append(new_node)
        if event == (events_per_floor - 1):
            a += 1

# Creating the paths.
available_positions = [0, 1, 2, 3, 4, 5, 6]
new_list = available_positions
num_paths = 3
Paths = []
for path in range(0, num_paths):
    Paths.append([])
b = 0
for num in range(0, num_floors):
    for path in Paths:
        if num == 0:
            path_pos = new_list.pop(random.choice(range(0, len(new_list))))
            path.append(path_pos)
            # Choosing a path by selecting a range within the previous event position (+ or - 1).
            # If the range is too high or low I adjust the range and select again.
        elif num > 0:
            path_range = random.choice(range(path[num - 1] - 1, path[num - 1] + 2))
            if path_range < 0:
                path_range = random.choice(range(path[num - 1], path[num - 1] + 3))
                print(f"Num: {num}")
            elif path_range >= len(new_list) - 1:
                path_range = random.choice(range(path[num - 1] - 3, path[num - 1] - 1))
            print(f"final: {num, path_range, len(new_list)}")
            path_pos = new_list.pop(path_range)
            path.append(path_pos)
        b += 1
        if b > 2:
            new_list = [0, 1, 2, 3, 4, 5, 6]
            b = 0
possible_events = ['Shop', 'Fight', 'Boss']

# Setting path in the node object. Setting event in the node object.
for number in range(0, num_floors):
    for path in Paths:
        index = path[number]
        # Conditions for certain floors containing only one type of event
        if number == 0:
            Floors[number][index].eventtype = 'Fight'
        elif number == 7:
            Floors[number][index].eventtype = 'Shop'
        elif number == num_floors - 1:
            Floors[number][index].eventtype = 'Boss'
        else:
            Floors[number][index].eventtype = random.choice(possible_events)
        Floors[number][index].path = Paths.index(path)

#List of nodes for easy access
# Nodes by floor are in Floors list
node_list_singles = []
for floor in Floors:
    for event in range(0, events_per_floor):
        node_list_singles.append(event)

# Game Loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    for floor in Floors:
        for node in floor:
            node.get_surf()
            screen.blit(node.surf, node.pos)

# Drawing Paths
    for path in range(0, num_paths):
        for floor in Floors:
            for node in floor:
                if node.path == path:
                    floor_index = Floors.index(floor)
                    pos1 = node.rect.center
                    if floor_index < len(Floors) - 1:
                        for node2 in Floors[floor_index + 1]:
                            if node2.path == node.path:
                                pos2 = node2.rect.center
                    pygame.draw.line(screen, 'White', pos1, pos2,)

    pygame.display.update()
    clock.tick(60)
