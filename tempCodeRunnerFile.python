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

# Function to create new flags
def create_flags():
    new_flags = []
    for i in range(6):
        flag_x = random.randint(30, WINDOW_WIDTH - 30)
        flag_y = random.randint(30, PLAYING_AREA - 30)
        new_flags.append(Flag(flag_x, flag_y, FLAG_COLORS[i]))
    return new_flags

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
            flag_points = [(self.x, self.y - 30), (self.x + 20, self.y - 20), (self.x, self.y - 10)]
            pygame.draw.polygon(screen, self.color, flag_points)
    
    def check_capture(self, player_x, player_y, player_radius):
        if not self.captured:
            distance = ((player_x - self.x) ** 2 + (player_y - self.y) ** 2) ** 0.5
            if distance < player_radius + 10:
                self.captured = True
                return True
        return False

# Function to reset the game
def reset_game():
    global circle_x, circle_y, flags, score, start_time, game_over
    circle_x = WINDOW_WIDTH // 2
    circle_y = PLAYING_AREA // 2
    flags = create_flags()
    score = 0
    start_time = pygame.time.get_ticks()
    game_over = False

# Circle properties
circle_radius = 20
circle_x = WINDOW_WIDTH // 2
circle_y = PLAYING_AREA // 2
circle_speed = 5

# Create initial flags
flags = create_flags()

# Game variables
score = 0
font = pygame.font.SysFont(None, 36)
large_font = pygame.font.SysFont(None, 72)
start_time = pygame.time.get_ticks()
game_duration = 60000  # 60 seconds in milliseconds
game_over = False

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
    
    # Check for reset key
    if keys[pygame.K_r] and game_over:
        reset_game()
    
    # Clear the screen
    screen.fill(BLACK)
    
    if not game_over:
        # Move the circle based on arrow key presses
        if keys[pygame.K_LEFT] and circle_x - circle_speed > circle_radius:
            circle_x -= circle_speed
        if keys[pygame.K_RIGHT] and circle_x + circle_speed < WINDOW_WIDTH - circle_radius:
            circle_x += circle_speed
        if keys[pygame.K_UP] and circle_y - circle_speed > circle_radius:
            circle_y -= circle_speed
        if keys[pygame.K_DOWN] and circle_y + circle_speed < PLAYING_AREA - circle_radius:
            circle_y += circle_speed
        
        # Check time remaining
        current_time = pygame.time.get_ticks()
        time_left = max(0, game_duration - (current_time - start_time))
        if time_left == 0:
            game_over = True
        
        # Check for flag captures
        flags_captured = 0
        for flag in flags:
            if flag.check_capture(circle_x, circle_y, circle_radius):
                score += 50
            if flag.captured:
                flags_captured += 1
        
        # Check if all flags are captured - generate new flags
        if flags_captured == 6:
            flags = create_flags()
        
        # Draw the flags
        for flag in flags:
            flag.draw()
        
        # Draw the circle
        pygame.draw.circle(screen, RED, (circle_x, circle_y), circle_radius)
        
        # Draw score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (20, PLAYING_AREA + 20))
        
        # Draw timer
        timer_text = font.render(f"Time: {time_left // 1000}s", True, (255, 255, 255))
        screen.blit(timer_text, (WINDOW_WIDTH - 120, PLAYING_AREA + 20))
    else:
        # Draw game over banner
        game_over_text = large_font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 150, PLAYING_AREA // 2 - 50))
        
        # Draw final score
        final_score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
        screen.blit(final_score_text, (WINDOW_WIDTH // 2 - 80, PLAYING_AREA // 2 + 20))
        
        # Draw reset instruction
        reset_text = font.render("Press 'R' to play again", True, (255, 255, 255))
        screen.blit(reset_text, (WINDOW_WIDTH // 2 - 120, PLAYING_AREA // 2 + 60))
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
sys.exit()
