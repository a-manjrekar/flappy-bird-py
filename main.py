import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
BIRD_SIZE = 30
PIPE_WIDTH, PIPE_HEIGHT = 50, 300
FPS = 60
GRAVITY = 1
JUMP_VELOCITY = -15

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Create the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load bird image
bird_image = pygame.Surface((BIRD_SIZE, BIRD_SIZE), pygame.SRCALPHA)
pygame.draw.circle(bird_image, RED, (BIRD_SIZE // 2, BIRD_SIZE // 2), BIRD_SIZE // 2)

# Load pipe image
pipe_image = pygame.Surface((PIPE_WIDTH, PIPE_HEIGHT), pygame.SRCALPHA)
pipe_rect = pygame.draw.rect(pipe_image, GREEN, (0, 0, PIPE_WIDTH, PIPE_HEIGHT))

clock = pygame.time.Clock()

# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_image
        self.rect = self.image.get_rect(center=(100, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        # Keep the bird on the screen
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0

    def jump(self):
        self.velocity = JUMP_VELOCITY

# Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pipe_image
        self.rect = self.image.get_rect(topleft=(x, random.randint(150, HEIGHT - 150)))

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.rect.left = WIDTH
            self.rect.top = random.randint(150, HEIGHT - 150)

# Create sprites group
all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()

# Create bird
bird = Bird()
all_sprites.add(bird)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()

    # Update
    all_sprites.update()

    # Check for collisions
    hits = pygame.sprite.spritecollide(bird, pipes, False)
    if hits:
        running = False

    # Generate pipes
    if random.randint(1, 75) == 1:
        new_pipe = Pipe(WIDTH)
        pipes.add(new_pipe)
        all_sprites.add(new_pipe)

    # Draw
    window.fill(WHITE)
    all_sprites.draw(window)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
