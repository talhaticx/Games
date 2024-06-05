# Rock Paper Scissors Simulation Documentation

This document provides an overview and usage instructions for the Rock Paper Scissors Simulation implemented in `main.py`.

## Table of Contents

1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [Class Definitions](#class-definitions)
   - [Obj Class](#obj-class)
4. [Functions](#functions)
   - [count_types](#count_types)
5. [Simulation Setup](#simulation-setup)
6. [Game Loop](#game-loop)
7. [Usage](#usage)

## Introduction

`main.py` simulates a dynamic version of the Rock Paper Scissors game where multiple objects of three types (Rock, Paper, Scissors) move around on the screen, collide, and change types based on the traditional rules of the game. The simulation continues until one type dominates.

## Requirements

- Python 3.x
- Pygame library

To install Pygame, use:
```bash
pip install pygame
```

## Class Definitions

### Obj Class

The `Obj` class represents an object in the simulation with attributes and methods for movement and collision handling.

#### Initialization

```python
class Obj:
    def __init__(self, type, x, y):
        self.type = type
        self.pos_x = x
        self.pos_y = y
        self.color = (tuple(random.randint(0, 255) for i in range(3)))
        self.x_s = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
        self.y_s = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
```
- `type`: The type of the object ('r' for rock, 's' for scissors, 'p' for paper).
- `x`, `y`: Initial position of the object.

#### Methods

##### _move

```python
def _move(self):
```

Moves the object, updates its position, and ensures it stays within the screen boundaries.

##### check_collision

```python
def check_collision(self, other):
```

Checks if the current object has collided with another object.

##### resolve_collision

```python
def resolve_collision(self, other):
```

Resolves the collision based on the types of the two colliding objects according to the Rock Paper Scissors rules.

## Functions

### count_types

```python
def count_types(objs):
```

Counts the number of each type of object in the simulation.

## Simulation Setup

The simulation initializes a Pygame display window, loads images for the different object types, and creates a list of objects of each type positioned randomly.

```python
pygame.init()
w, h = 700, 500
display = pygame.display.set_mode((w, h))
pygame.display.set_caption('Rock Paper Scissors Simulation')

font = pygame.font.SysFont(None, 36)

rock_image = pygame.image.load("pics/Rock.png")
scissors_image = pygame.image.load("pics/Scissors.png")
paper_image = pygame.image.load("pics/Paper.png")

rock_image = pygame.transform.scale(rock_image, (2 * RADIUS, 2 * RADIUS))
scissors_image = pygame.transform.scale(scissors_image, (2 * RADIUS, 2 * RADIUS))
paper_image = pygame.transform.scale(paper_image, (2 * RADIUS, 2 * RADIUS))

objs = []

for i in range(N):
    obj_type = 'r'
    obj_instance = Obj(obj_type, random.randint(0, 50), random.randint(450, 500))
    objs.append(obj_instance)

for i in range(N):
    obj_type = 's'
    obj_instance = Obj(obj_type, random.randint(325, 375), random.randint(0, 50))
    objs.append(obj_instance)

for i in range(N):
    obj_type = 'p'
    obj_instance = Obj(obj_type, random.randint(650, 700), random.randint(450, 500))
    objs.append(obj_instance)

clock = pygame.time.Clock()
```

## Game Loop

The main game loop handles events, updates object positions, checks for collisions, and updates the display.

```python
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            quit()

    display.fill((40, 40, 40))

    for i, obj_instance in enumerate(objs):
        if obj_instance.type == 'r':
            display.blit(rock_image, (obj_instance.pos_x - RADIUS, obj_instance.pos_y - RADIUS))
        elif obj_instance.type == 's':
            display.blit(scissors_image, (obj_instance.pos_x - RADIUS, obj_instance.pos_y - RADIUS))
        elif obj_instance.type == 'p':
            display.blit(paper_image, (obj_instance.pos_x - RADIUS, obj_instance.pos_y - RADIUS))

        obj_instance._move()

    for i in range(len(objs)):
        for j in range(i + 1, len(objs)):
            if objs[i].check_collision(objs[j]):
                objs[i].resolve_collision(objs[j])

    counts = count_types(objs)
    stats_text = f"Rocks: {counts['r']}  Scissors: {counts['s']}  Papers: {counts['p']}"
    stats_surf = font.render(stats_text, True, (255, 255, 255))
    display.blit(stats_surf, (10, 10))

    if counts['r'] > 0 and counts['s'] == 0 and counts['p'] == 0:
        win_text = "Rock wins!"
    elif counts['s'] > 0 and counts['r'] == 0 and counts['p'] == 0:
        win_text = "Scissors win!"
    elif counts['p'] > 0 and counts['r'] == 0 and counts['s'] == 0:
        win_text = "Paper wins!"
    else:
        win_text = ""

    if win_text:
        win_surf = font.render(win_text, True, (255, 255, 255))
        display.blit(win_surf, (w // 2 - win_surf.get_width() // 2, h // 2 - win_surf.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)
```

## Usage

To run the simulation, execute `main.py`:

```bash
python main.py
```

The simulation window will display objects moving and colliding based on the rules of Rock Paper Scissors. The simulation will continue until one type dominates, displaying the winner.

This documentation covers the primary components and usage of the Rock Paper Scissors Simulation in `main.py`. For further details, refer to the comments within the code.