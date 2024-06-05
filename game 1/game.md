# Snake Game Documentation

This document provides an overview and usage instructions for the `SnakeGame` class implemented in `snake_game.py`.

## Table of Contents

1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [Class Definitions](#class-definitions)
   - [Direction Enum](#direction-enum)
   - [Point Named Tuple](#point-named-tuple)
4. [SnakeGame Class](#snakegame-class)
   - [Initialization](#initialization)
   - [Methods](#methods)
     - [\_place_food](#_place_food)
     - [play_step](#play_step)
     - [\_is_collision](#_is_collision)
     - [\_update_ui](#_update_ui)
     - [\_move](#_move)
     - [askuser](#askuser)
5. [Usage](#usage)
6. [Controls](#controls)
7. [Running the Game](#running-the-game)

## Introduction

`snake_game.py` is a Python implementation of the classic Snake game using the Pygame library. The objective is to control a snake to eat food, growing longer with each piece consumed, while avoiding collisions with the walls and the snake's own body.

## Requirements

- Python 3.x
- Pygame library

To install Pygame, use:
```bash
pip install pygame
```

## Class Definitions

### Direction Enum

The `Direction` Enum defines the four possible movement directions for the snake:
- `RIGHT`: Movement to the right.
- `LEFT`: Movement to the left.
- `UP`: Movement upwards.
- `DOWN`: Movement downwards.

### Point Named Tuple

The `Point` named tuple represents coordinates on the game screen with `x` and `y` attributes.

## SnakeGame Class

The `SnakeGame` class contains all the logic and functionality for the Snake game.

### Initialization

```python
def __init__(self, w=1120, h=660):
```

- `w`: Width of the game window (default: 1120).
- `h`: Height of the game window (default: 660).

Initializes the game window, snake, food, and game variables.

### Methods

#### _place_food

```python
def _place_food(self, agent):
```

Places food at a random location on the game screen. Ensures the food does not appear on the snake's body.

#### play_step

```python
def play_step(self):
```

Executes one step of the game:
1. Collects user input.
2. Moves the snake.
3. Checks for collisions.
4. Places new food or moves the snake.
5. Updates the UI and clock.

Returns:
- `game_over` (bool): Indicates if the game is over.
- `score` (int): Current score of the game.

#### _is_collision

```python
def _is_collision(self):
```

Checks if the snake has collided with the walls or itself. Handles boundary wrapping if in "Free Use" mode.

Returns:
- `bool`: `True` if there is a collision, `False` otherwise.

#### _update_ui

```python
def _update_ui(self):
```

Updates the game display, drawing the snake, food, and game information.

#### _move

```python
def _move(self, direction):
```

Moves the snake's head in the specified direction and updates the position.

#### askuser

```python
def askuser(self):
```

Displays a prompt asking the user if they want to continue or end the game.

Returns:
- `bool`: `True` if the user wants to continue, `False` if they want to end the game.

## Usage

### Controls

- `Arrow Keys`: Move the snake in the respective direction.
- `Left Shift`: Increase snake speed.
- `Space`: Decrease snake speed.
- `Esc`: Exit the game.
- `0`: Toggle between "Survival" and "Free Use" modes.
- `H`: Toggle help information.

### Running the Game

To run the game, execute `snake_game.py`:

```bash
python snake_game.py
```

The game initializes and starts in an endless loop until the player decides to exit. Upon game over, the final score is displayed, and the player is prompted to continue or end the game. High scores are tracked and displayed.

---

This documentation covers the primary components and usage of the `SnakeGame` class in `snake_game.py`. For further details, refer to the comments within the code.