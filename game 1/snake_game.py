import pygame
import random
from enum import Enum
from collections import namedtuple

# Initialize Pygame
pygame.init()

# Fonts for displaying text on screen
font1 = pygame.font.SysFont('arial', 25)
font2 = pygame.font.SysFont('arial', 14)
font = pygame.font.SysFont('arial', 50)

# Enum for defining snake direction
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

# Named tuple to represent a point in the game
Point = namedtuple('Point', 'x, y')

# RGB colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
RED2 = (180, 0, 0)
GREEN1 = (0, 115, 255)
GREEN2 = (0, 200, 255)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

# Game settings
BLOCK_SIZE = 10
BLOCK_SIZE_MINI = 6
SPEED = 12

class SnakeGame:
    def __init__(self, w=1120, h=660):
        """Initialize the game with default width and height."""
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        # Initial snake direction
        self.direction = Direction.RIGHT
        
        # Initial snake position and body
        self.head = Point(w / 2, h / 2)
        self.snake = [self.head, 
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]
        self.score = 0
        
        # Place the first food item
        self.food = None
        self._place_food(self)
        
        # Initial game settings
        self.SPEED = 20
        self.survival = True 
        self.help = False
        
    def _place_food(self, agent):
        """Place food at a random location on the screen, ensuring it doesn't appear on the snake."""
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE 
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in agent.snake:
            self._place_food()
        
    def play_step(self):
        """Play one step of the game."""
        # 1. Collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN
                elif event.key == pygame.K_LSHIFT:
                    self.SPEED += 20
                elif event.key == pygame.K_SPACE:
                    self.SPEED -= 10
                    if self.SPEED <= 0:
                        self.SPEED = 10
                elif event.key == pygame.K_ESCAPE:
                    return True, self.score
                elif event.key == pygame.K_0:
                    self.survival = not self.survival
                elif event.key == pygame.K_h:
                    self.help = not self.help
        
        # 2. Move the snake
        self._move(self.direction)
        self.snake.insert(0, self.head)
        
        # 3. Check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
            
        # 4. Place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food(self)
        else:
            self.snake.pop()
    
        # 5. Update UI and clock
        self._update_ui()
        self.clock.tick(self.SPEED)
        
        # 6. Return game over and score
        return game_over, self.score
    
    def _is_collision(self):
        """Check if the snake has collided with the boundaries or itself."""
        if self.survival:
            # Check for collision with boundaries
            if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
                return True
            # Check for collision with itself
            if self.head in self.snake[1:]:
                return True
        else:
            # Handle boundary wrapping
            if self.head.x > self.w - BLOCK_SIZE:
                self.head = Point(0, self.head.y)
            if self.head.y > self.h - BLOCK_SIZE:
                self.head = Point(self.head.x, 0)
            if self.head.x < 0:
                self.head = Point(self.w - BLOCK_SIZE, self.head.y)
            if self.head.y < 0:
                self.head = Point(self.head.x, self.h - BLOCK_SIZE)
        
        return False
        
    def _update_ui(self):
        """Update the game UI."""
        self.display.fill(BLACK)
        
        for pt in self.snake:
            if pt == self.head:
                pygame.draw.rect(self.display, GREEN1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(self.display, GREEN2, pygame.Rect(pt.x + 2, pt.y + 2, BLOCK_SIZE_MINI, BLOCK_SIZE_MINI))
            else:
                pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))

        pygame.draw.rect(self.display, RED2, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x + 2, self.food.y + 2, BLOCK_SIZE_MINI, BLOCK_SIZE_MINI))
        pygame.draw.rect(self.display, RED2, pygame.Rect(self.food.x + 4, self.food.y + 4, BLOCK_SIZE_MINI - 4, BLOCK_SIZE_MINI - 4))

        text1 = font1.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text1, [5, 5])

        text2 = font2.render("Press h for Help", True, WHITE)
        self.display.blit(text2, [5, 30])
        if self.survival:
            mode = font2.render("Survival", True, WHITE)
        else:
            mode = font2.render("Free Use", True, WHITE)
        self.display.blit(mode, [5, 45])

        if self.help:
            help_text = font1.render("Shift - Speed Increase | Space - Speed Decrease", True, BLUE2)
            self.display.blit(help_text, (5, self.h - 30))
            mode2 = font2.render("Press 0 for changing mode", True, WHITE)
            self.display.blit(mode2, [5, self.h - 50])
        
        pygame.display.flip()
        
    def _move(self, direction):
        """Move the snake in the specified direction."""
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        self.head = Point(x, y)
    
    def askuser(self):
        """Prompt the user to continue or end the game."""
        text1 = font.render("y for continue / n for end", True, WHITE)
        self.display.blit(text1, [self.w // 2 - 270, self.h // 2])
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        return True
                    if event.key == pygame.K_n:
                        return False

if __name__ == '__main__':
    while True:
        game = SnakeGame()
        
        # Game loop
        while True:
            game_over, score = game.play_step()
            
            if game_over:
                break

        print('\nFinal Score', score, "\n")

        # High score management
        try:
            with open("score") as f:
                high_score = int(f.readline())
        except FileNotFoundError:
            high_score = 0

        if score >= high_score:
            print("Made a new high score!!!")
            with open("score", "w") as f:
                f.write(str(score))
        else:
            print("Highest score is", high_score)

        if game.askuser():
            continue
        else:
            break

    pygame.quit()
