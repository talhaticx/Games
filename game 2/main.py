import pygame
import random

# Initialize Pygame and its font module
pygame.init()
pygame.font.init()

# Screen dimensions
w, h = 700, 500

# Radius of the objects (rock, paper, scissors)
RADIUS = 12

# Number of objects of each type
N = 80

# Speed of the objects
SPEED = 1

# Set up display window
display = pygame.display.set_mode((w, h))
pygame.display.set_caption('Rock Paper Scissors Simulation')

# Load font for displaying text
font = pygame.font.SysFont(None, 36)

# Load images for the objects and scale them to fit within the RADIUS
rock_image = pygame.image.load("pics/Rock.png")
scissors_image = pygame.image.load("pics/Scissors.png")
paper_image = pygame.image.load("pics/Paper.png")

rock_image = pygame.transform.scale(rock_image, (2 * RADIUS, 2 * RADIUS))
scissors_image = pygame.transform.scale(scissors_image, (2 * RADIUS, 2 * RADIUS))
paper_image = pygame.transform.scale(paper_image, (2 * RADIUS, 2 * RADIUS))

class Obj:
    def __init__(self, type, x, y):
        """
        Initialize an object with a specific type, position, random color, and random speed.

        Parameters:
        type (str): The type of the object ('r' for rock, 's' for scissors, 'p' for paper)
        x (int): The initial x-coordinate of the object
        y (int): The initial y-coordinate of the object
        """
        self.type = type
        self.pos_x = x
        self.pos_y = y
        self.color = (tuple(random.randint(0, 255) for _ in range(3)))
        self.x_s = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
        self.y_s = random.choice([-1, 1]) * random.uniform(0.5, 1.5)

    def _move(self):
        """
        Move the object, update its speed randomly, and ensure it stays within the screen boundaries.
        """
        # Randomly adjust speed with a small probability
        if random.random() < 0.1:
            self.x_s += random.uniform(-0.2, 0.2)
            self.y_s += random.uniform(-0.2, 0.2)

        # Normalize speed to maintain constant speed
        speed = (self.x_s ** 2 + self.y_s ** 2) ** 0.5
        self.x_s = (self.x_s / speed) * SPEED
        self.y_s = (self.y_s / speed) * SPEED

        # Update position based on speed
        self.pos_x += self.x_s
        self.pos_y += self.y_s

        # Ensure the object stays within the horizontal boundaries
        if self.pos_x + RADIUS > w:
            self.pos_x = w - RADIUS
            self.x_s = -abs(self.x_s) * random.uniform(1.0, 1.2)
        elif self.pos_x - RADIUS < 0:
            self.pos_x = RADIUS
            self.x_s = abs(self.x_s) * random.uniform(1.0, 1.2)

        # Ensure the object stays within the vertical boundaries
        if self.pos_y + RADIUS > h:
            self.pos_y = h - RADIUS
            self.y_s = -abs(self.y_s) * random.uniform(1.0, 1.2)
        elif self.pos_y - RADIUS < 0:
            self.pos_y = RADIUS
            self.y_s = abs(self.y_s) * random.uniform(1.0, 1.2)

    def check_collision(self, other):
        """
        Check if the current object has collided with another object.

        Parameters:
        other (Obj): Another object to check for collision.

        Returns:
        bool: True if the objects have collided, False otherwise.
        """
        distance = ((self.pos_x - other.pos_x) ** 2 + (self.pos_y - other.pos_y) ** 2) ** 0.5
        return distance < 2 * RADIUS

    def resolve_collision(self, other):
        """
        Resolve the collision between this object and another object based on their types.

        Parameters:
        other (Obj): Another object to resolve collision with.
        """
        if self.type == other.type:
            return  # No change if the same type
        elif (self.type == 'r' and other.type == 's') or (self.type == 's' and other.type == 'p') or (self.type == 'p' and other.type == 'r'):
            other.type = self.type  # This object wins
        else:
            self.type = other.type  # The other object wins

def count_types(objs):
    """
    Count the number of each type of object in the simulation.

    Parameters:
    objs (list): List of objects in the simulation.

    Returns:
    dict: Dictionary with counts of each type of object.
    """
    counts = {'r': 0, 's': 0, 'p': 0}
    for obj in objs:
        counts[obj.type] += 1
    return counts

# List to store all objects
objs = []

# Initialize rocks in the bottom-left corner of the screen
for i in range(N):
    obj_type = 'r'
    obj_instance = Obj(obj_type, random.randint(0, 50), random.randint(450, 500))
    objs.append(obj_instance)

# Initialize scissors in the top-center of the screen
for i in range(N):
    obj_type = 's'
    obj_instance = Obj(obj_type, random.randint(325, 375), random.randint(0, 50))
    objs.append(obj_instance)

# Initialize papers in the bottom-right corner of the screen
for i in range(N):
    obj_type = 'p'
    obj_instance = Obj(obj_type, random.randint(650, 700), random.randint(450, 500))
    objs.append(obj_instance)

# Clock to control the frame rate
clock = pygame.time.Clock()

# Main game loop
while True:
    # Event handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            quit()

    # Clear the screen
    display.fill((40, 40, 40))

    # Draw and move each object
    for i, obj_instance in enumerate(objs):
        if obj_instance.type == 'r':
            display.blit(rock_image, (obj_instance.pos_x - RADIUS, obj_instance.pos_y - RADIUS))
        elif obj_instance.type == 's':
            display.blit(scissors_image, (obj_instance.pos_x - RADIUS, obj_instance.pos_y - RADIUS))
        elif obj_instance.type == 'p':
            display.blit(paper_image, (obj_instance.pos_x - RADIUS, obj_instance.pos_y - RADIUS))

        obj_instance._move()

    # Check and resolve collisions between objects
    for i in range(len(objs)):
        for j in range(i + 1, len(objs)):
            if objs[i].check_collision(objs[j]):
                objs[i].resolve_collision(objs[j])

    # Count the number of each type of object
    counts = count_types(objs)
    stats_text = f"Rocks: {counts['r']}  Scissors: {counts['s']}  Papers: {counts['p']}"
    stats_surf = font.render(stats_text, True, (255, 255, 255))
    display.blit(stats_surf, (10, 10))

    # Check for a winner
    if counts['r'] > 0 and counts['s'] == 0 and counts['p'] == 0:
        win_text = "Rock wins!"
    elif counts['s'] > 0 and counts['r'] == 0 and counts['p'] == 0:
        win_text = "Scissors win!"
    elif counts['p'] > 0 and counts['r'] == 0 and counts['s'] == 0:
        win_text = "Paper wins!"
    else:
        win_text = ""

    # Display the winning message
    if win_text:
        win_surf = font.render(win_text, True, (255, 255, 255))
        display.blit(win_surf, (w // 2 - win_surf.get_width() // 2, h // 2 - win_surf.get_height() // 2))

    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate at 60 frames per second
    clock.tick(60)
