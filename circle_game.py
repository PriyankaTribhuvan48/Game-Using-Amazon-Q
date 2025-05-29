import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Set up display dimensions
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 800
PLAYING_AREA = 600

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
FLAG_COLORS = [
    (255, 255, 0),    # Yellow
    (0, 255, 0),      # Green
    (0, 0, 255),      # Blue
    (255, 0, 255),    # Magenta
    (0, 255, 255),    # Cyan
    (255, 165, 0)     # Orange
]

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Circle Movement Game")

# Circle properties
circle_radius = 20
circle_x = WINDOW_WIDTH // 2
circle_y = PLAYING_AREA // 2
circle_speed = 5

# Flag properties
class Flag:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.captured = False
    
    def draw(self):
        if not self.captured:
            # Draw flag pole (brown)
            pygame.draw.line(screen, BROWN, (self.x, self.y), (self.x, self.y - 30), 3)
            
            # Draw triangular flag
            flag_points = [
                (self.x, self.y - 30),
                (self.x + 20, self.y - 20),
                (self.x, self.y - 10)
            ]
            pygame.draw.polygon(screen, self.color, flag_points)
    
    def check_capture(self, player_x, player_y, player_radius):
        if not self.captured:
            # Check if player circle overlaps with flag
            distance = ((player_x - self.x) ** 2 + (player_y - self.y) ** 2) ** 0.5
            if distance < player_radius + 10:  # 10 is an approximate flag hitbox radius
                self.captured = True
                return True
        return False

# Create flags at random positions
flags = []
for i in range(6):
    valid_position = False
    while not valid_position:
        flag_x = random.randint(30, WINDOW_WIDTH - 30)
        flag_y = random.randint(30, PLAYING_AREA - 30)
        
        # Check if position is far enough from other flags and player start position
        valid_position = True
        for flag in flags:
            if ((flag_x - flag.x) ** 2 + (flag_y - flag.y) ** 2) ** 0.5 < 60:
                valid_position = False
                break
        
        # Check distance from player start position
        if ((flag_x - circle_x) ** 2 + (flag_y - circle_y) ** 2) ** 0.5 < 100:
            valid_position = False
    
    flags.append(Flag(flag_x, flag_y, FLAG_COLORS[i]))

# Game variables
score = 0
font = pygame.font.SysFont(None, 36)

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
    
    # Check for flag captures
    flags_captured = 0
    for flag in flags:
        if flag.check_capture(circle_x, circle_y, circle_radius):
            score += 50
        if flag.captured:
            flags_captured += 1
    
    # Check if all flags are captured (game over)
    if flags_captured == 6:
        game_over_text = font.render("Game Over! All flags captured!", True, (255, 255, 255))
        screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 180, PLAYING_AREA + 50))
        pygame.display.flip()
        pygame.time.wait(3000)  # Wait 3 seconds before quitting
        running = False
    
    # Clear the screen
    screen.fill(BLACK)
    
    # Draw the flags
    for flag in flags:
        flag.draw()
    
    # Draw the circle
    pygame.draw.circle(screen, RED, (circle_x, circle_y), circle_radius)
    
    # Draw score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, PLAYING_AREA + 20))
    
    # Draw flags remaining
    flags_text = font.render(f"Flags Remaining: {6 - flags_captured}", True, (255, 255, 255))
    screen.blit(flags_text, (20, PLAYING_AREA + 60))
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
sys.exit()
