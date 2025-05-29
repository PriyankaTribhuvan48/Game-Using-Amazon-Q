import pygame
import sys

# Initialize pygame
pygame.init()

# Set up display dimensions
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 800
PLAYING_AREA = 600

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Circle Movement Game")

# Circle properties
circle_radius = 20
circle_x = WINDOW_WIDTH // 2
circle_y = PLAYING_AREA // 2
circle_speed = 5

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Get keyboard input
    keys = pygame.key.get_pressed()
    
    # Move the circle based on arrow key presses
    if keys[pygame.K_LEFT] and circle_x - circle_speed > circle_radius:
        circle_x -= circle_speed
    if keys[pygame.K_RIGHT] and circle_x + circle_speed < WINDOW_WIDTH - circle_radius:
        circle_x += circle_speed
    if keys[pygame.K_UP] and circle_y - circle_speed > circle_radius:
        circle_y -= circle_speed
    if keys[pygame.K_DOWN] and circle_y + circle_speed < PLAYING_AREA - circle_radius:
        circle_y += circle_speed
    
    # Clear the screen
    screen.fill(BLACK)
    
    # Draw the circle
    pygame.draw.circle(screen, RED, (circle_x, circle_y), circle_radius)
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
sys.exit()
