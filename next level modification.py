import pygame
import sys
import random
import math
import os

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
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)
GOLD = (255, 215, 0)
GREEN = (0, 128, 0)
PURPLE = (128, 0, 128)
FLAG_COLORS = [
    (255, 255, 0),    # Yellow
    (0, 255, 0),      # Green
    (0, 0, 255),      # Blue
    (255, 0, 255),    # Magenta
    (0, 255, 255),    # Cyan
    (255, 165, 0)     # Orange
]

# Background colors for different levels
BACKGROUND_COLORS = [
    (0, 0, 30),      # Dark blue
    (30, 0, 30),     # Dark purple
    (30, 30, 0),     # Dark yellow
    (0, 30, 0),      # Dark green
    (30, 0, 0),      # Dark red
]

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flag Catcher Game")

# Background elements
class Background:
    def __init__(self, level=1):
        self.stars = []
        self.offset_x = 0
        self.offset_y = 0
        self.color = BACKGROUND_COLORS[(level - 1) % len(BACKGROUND_COLORS)]
        self.generate_stars(50)
        self.transition = False
        self.transition_progress = 0
        self.next_color = None
    
    def generate_stars(self, count):
        self.stars = []
        for _ in range(count):
            self.stars.append({
                'x': random.randint(0, WINDOW_WIDTH),
                'y': random.randint(0, PLAYING_AREA),
                'size': random.randint(1, 3),
                'brightness': random.randint(100, 255),
                'speed': random.uniform(0.2, 1.0)
            })
    
    def start_transition(self, next_level):
        self.transition = True
        self.transition_progress = 0
        self.next_color = BACKGROUND_COLORS[(next_level - 1) % len(BACKGROUND_COLORS)]
    
    def update(self):
        # Move stars for parallax effect
        self.offset_x = (self.offset_x + 0.5) % WINDOW_WIDTH
        
        # Update transition if active
        if self.transition:
            self.transition_progress += 0.02
            if self.transition_progress >= 1:
                self.color = self.next_color
                self.transition = False
    
    def draw(self):
        # Draw background color
        if self.transition:
            # Blend between colors during transition
            r = int(self.color[0] * (1 - self.transition_progress) + self.next_color[0] * self.transition_progress)
            g = int(self.color[1] * (1 - self.transition_progress) + self.next_color[1] * self.transition_progress)
            b = int(self.color[2] * (1 - self.transition_progress) + self.next_color[2] * self.transition_progress)
            screen.fill((r, g, b))
        else:
            screen.fill(self.color)
        
        # Draw moving stars
        for star in self.stars:
            # Calculate position with parallax effect
            x = (star['x'] - self.offset_x * star['speed']) % WINDOW_WIDTH
            y = star['y']
            
            # Make stars twinkle
            brightness = star['brightness'] + random.randint(-20, 20)
            brightness = max(100, min(255, brightness))
            pygame.draw.circle(screen, (brightness, brightness, brightness), 
                              (int(x), int(y)), star['size'])

# Flag properties
class Flag:
    def __init__(self, x, y, color, points=50, speed_multiplier=1.0):
        self.x = x
        self.y = y
        self.color = color
        self.captured = False
        self.speed_x = random.uniform(-1.5, 1.5) * speed_multiplier
        self.speed_y = random.uniform(-1.5, 1.5) * speed_multiplier
        self.points = points
        self.special = points > 50
        self.angle = 0
        self.wave_speed = random.uniform(0.05, 0.1)
    
    def draw(self):
        if not self.captured:
            # Draw flag pole (brown)
            pygame.draw.line(screen, BROWN, (self.x, self.y), (self.x, self.y - 30), 3)
            
            # Animate flag waving
            self.angle += self.wave_speed
            wave = math.sin(self.angle) * 3
            
            # Draw triangular flag with wave effect
            flag_points = [
                (self.x, self.y - 30),
                (self.x + 20 + wave, self.y - 20),
                (self.x, self.y - 10)
            ]
            pygame.draw.polygon(screen, self.color, flag_points)
            
            # Draw special indicator for bonus flags
            if self.special:
                pygame.draw.circle(screen, GOLD, (self.x + 10, self.y - 20), 5)
    
    def move(self):
        if not self.captured:
            # Move the flag
            self.x += self.speed_x
            self.y += self.speed_y
            
            # Bounce off walls
            if self.x < 20 or self.x > WINDOW_WIDTH - 20:
                self.speed_x *= -1
            if self.y < 40 or self.y > PLAYING_AREA - 10:
                self.speed_y *= -1
    
    def check_capture(self, player_x, player_y, player_radius):
        if not self.captured:
            distance = ((player_x - self.x) ** 2 + (player_y - self.y) ** 2) ** 0.5
            if distance < player_radius + 10:
                self.captured = True
                return True
        return False

# Butterfly net class
class ButterflyNet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 25
        self.handle_length = 40
        self.animation_frame = 0
        self.animation_speed = 0.2
        self.power_up = False
        self.power_up_time = 0
    
    def draw(self):
        # Draw the net handle (brown)
        pygame.draw.line(screen, BROWN, (self.x, self.y), 
                         (self.x, self.y + self.handle_length), 5)
        
        # Draw the net rim (white or gold if powered up)
        rim_color = GOLD if self.power_up else WHITE
        pygame.draw.circle(screen, rim_color, (self.x, self.y), self.radius, 3)
        
        # Draw the net mesh (light blue with animation)
        self.animation_frame += self.animation_speed
        wave_offset = math.sin(self.animation_frame) * 3
        
        # Draw mesh lines
        mesh_color = LIGHT_BLUE
        if self.power_up:
            mesh_color = (200, 200, 100)  # Golden mesh when powered up
            
        for i in range(0, 360, 30):
            angle = math.radians(i)
            end_x = self.x + (self.radius - 5) * math.cos(angle)
            end_y = self.y + (self.radius - 5) * math.sin(angle) + wave_offset
            pygame.draw.line(screen, mesh_color, (self.x, self.y), (end_x, end_y), 1)
        
        # Draw inner circles for mesh effect
        pygame.draw.circle(screen, mesh_color, (self.x, self.y + wave_offset // 2), self.radius * 0.7, 1)
        pygame.draw.circle(screen, mesh_color, (self.x, self.y + wave_offset // 3), self.radius * 0.4, 1)

# Particle effect for captures
class CaptureEffect:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.particles = []
        self.lifetime = 30
        
        # Create particles
        for _ in range(10):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(1, 3)
            self.particles.append({
                'x': self.x,
                'y': self.y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'size': random.randint(2, 5)
            })
    
    def update(self):
        self.lifetime -= 1
        for p in self.particles:
            p['x'] += p['dx']
            p['y'] += p['dy']
            p['size'] *= 0.95
    
    def draw(self):
        for p in self.particles:
            pygame.draw.circle(screen, self.color, (int(p['x']), int(p['y'])), int(p['size']))
    
    def is_finished(self):
        return self.lifetime <= 0

# Obstacle class with movement
class Obstacle:
    def __init__(self, x, y, width, height, level=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = GRAY
        self.speed_x = random.uniform(-1, 1) * (0.5 + level * 0.2)
        self.speed_y = random.uniform(-1, 1) * (0.5 + level * 0.2)
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
    def move(self):
        # Move the obstacle
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Bounce off walls
        if self.x < 0 or self.x + self.width > WINDOW_WIDTH:
            self.speed_x *= -1
        if self.y < 0 or self.y + self.height > PLAYING_AREA:
            self.speed_y *= -1
    
    def check_collision(self, player_x, player_y, player_radius):
        # Check if player collides with obstacle
        closest_x = max(self.x, min(player_x, self.x + self.width))
        closest_y = max(self.y, min(player_y, self.y + self.height))
        
        distance = ((player_x - closest_x) ** 2 + (player_y - closest_y) ** 2) ** 0.5
        return distance < player_radius

# Function to create new flags
def create_flags(level=1):
    new_flags = []
    for i in range(6):
        flag_x = random.randint(30, WINDOW_WIDTH - 30)
        flag_y = random.randint(30, PLAYING_AREA - 30)
        
        # Add chance for bonus flags in higher levels
        if level > 1 and random.random() < 0.2:
            points = 100
            speed_mult = 1.5
        else:
            points = 50
            speed_mult = 1.0 + (level - 1) * 0.2  # Increase speed with level
            
        new_flags.append(Flag(flag_x, flag_y, FLAG_COLORS[i % len(FLAG_COLORS)], points, speed_mult))
    return new_flags

# Function to create obstacles with level-based difficulty
def create_obstacles(level):
    obstacles = []
    if level >= 2:  # Start adding obstacles from level 2
        num_obstacles = min(level, 5)  # Max 5 obstacles
        for _ in range(num_obstacles):
            width = random.randint(30, 60)
            height = random.randint(30, 60)
            x = random.randint(50, WINDOW_WIDTH - width - 50)
            y = random.randint(50, PLAYING_AREA - height - 50)
            obstacles.append(Obstacle(x, y, width, height, level))
    return obstacles

# Function to reset the game
def reset_game():
    global player_x, player_y, flags, score, start_time, game_over, level, effects, obstacles, background
    player_x = WINDOW_WIDTH // 2
    player_y = PLAYING_AREA // 2
    level = 1
    flags = create_flags(level)
    obstacles = []
    score = 0
    start_time = pygame.time.get_ticks()
    game_over = False
    effects = []
    background = Background(level)

# Create background
background = Background()

# Player properties
player_x = WINDOW_WIDTH // 2
player_y = PLAYING_AREA // 2
player_speed = 5
player_radius = 25  # Capture radius

# Create butterfly net
net = ButterflyNet(player_x, player_y)

# Create initial flags and obstacles
flags = create_flags(1)
obstacles = []

# Game variables
score = 0
level = 1
high_score = 0
font = pygame.font.SysFont(None, 36)
large_font = pygame.font.SysFont(None, 72)
start_time = pygame.time.get_ticks()
game_duration = 60000  # 60 seconds in milliseconds
game_over = False
effects = []  # List to store visual effects

# Power-up variables
power_up_active = False
power_up_timer = 0
power_up_duration = 5000  # 5 seconds

# Game loop
clock = pygame.time.Clock()
running = True
paused = False
current_time = 0
pause_start_time = 0

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Pause game with P key
            if event.key == pygame.K_p and not game_over:
                paused = not paused
                if paused:
                    pause_start_time = pygame.time.get_ticks()
                else:
                    # Adjust start time to account for pause
                    pause_duration = pygame.time.get_ticks() - pause_start_time
                    start_time += pause_duration
    
    # Skip updates if paused
    if paused:
        # Draw pause screen
        pause_text = large_font.render("PAUSED", True, WHITE)
        screen.blit(pause_text, (WINDOW_WIDTH // 2 - 100, PLAYING_AREA // 2 - 50))
        pygame.display.flip()
        clock.tick(10)  # Lower frame rate while paused
        continue
    
    # Get keyboard input
    keys = pygame.key.get_pressed()
    
    # Check for reset key
    if keys[pygame.K_r] and game_over:
        reset_game()
    
    # Update background
    background.update()
    
    # Draw background
    background.draw()
    
    # Draw separator line
    pygame.draw.line(screen, GRAY, (0, PLAYING_AREA), (WINDOW_WIDTH, PLAYING_AREA), 2)
    
    if not game_over:
        # Store previous position
        prev_x, prev_y = player_x, player_y
        
        # Move the player based on arrow key presses
        if keys[pygame.K_LEFT] and player_x - player_speed > player_radius:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x + player_speed < WINDOW_WIDTH - player_radius:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y - player_speed > player_radius:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y + player_speed < PLAYING_AREA - player_radius:
            player_y += player_speed
        
        # Check collision with obstacles
        collision = False
        for obstacle in obstacles:
            if obstacle.check_collision(player_x, player_y, player_radius):
                collision = True
                break
        
        # Revert position if collision detected
        if collision:
            player_x, player_y = prev_x, prev_y
        
        # Move obstacles
        for obstacle in obstacles:
            obstacle.move()
        
        # Update net position
        net.x = player_x
        net.y = player_y
        
        # Check time remaining
        current_time = pygame.time.get_ticks()
        time_left = max(0, game_duration - (current_time - start_time))
        if time_left == 0:
            game_over = True
            if score > high_score:
                high_score = score
        
        # Check power-up status
        if power_up_active:
            if current_time - power_up_timer > power_up_duration:
                power_up_active = False
                net.power_up = False
                player_speed = 5  # Reset speed
            else:
                # Draw power-up timer
                power_up_left = power_up_duration - (current_time - power_up_timer)
                pygame.draw.rect(screen, GOLD, (WINDOW_WIDTH // 2 - 50, 10, 
                                              int(100 * power_up_left / power_up_duration), 10))
        
        # Draw obstacles
        for obstacle in obstacles:
            obstacle.draw()
        
        # Move and check for flag captures
        flags_captured = 0
        for flag in flags:
            flag.move()  # Move the flags
            if flag.check_capture(player_x, player_y, player_radius):
                score += flag.points
                
                # Create capture effect
                effects.append(CaptureEffect(flag.x, flag.y, flag.color))
                
                # Chance for power-up on special flag capture
                if flag.special and random.random() < 0.5:
                    power_up_active = True
                    power_up_timer = current_time
                    net.power_up = True
                    player_speed = 8  # Speed boost
            
            if flag.captured:
                flags_captured += 1
        
        # Update and draw effects
        for effect in effects[:]:
            effect.update()
            effect.draw()
            if effect.is_finished():
                effects.remove(effect)
        
        # Check if all flags are captured - generate new flags and level up
        if flags_captured == 6:
            level += 1
            # Increase difficulty with level
            flags = create_flags(level)
            
            # Start background transition to next level
            background.start_transition(level)
            
            # Add obstacles at every level starting from level 2
            obstacles = create_obstacles(level)
        
        # Draw the flags
        for flag in flags:
            flag.draw()
        
        # Draw the butterfly net
        net.draw()
        
        # Draw level indicator
        level_text = font.render(f"Level: {level}", True, GREEN)
        screen.blit(level_text, (WINDOW_WIDTH // 2 - 40, 10))
        
        # Draw score at the bottom
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (50, PLAYING_AREA + (WINDOW_HEIGHT - PLAYING_AREA) // 2))
        
        # Draw timer at the bottom
        timer_text = font.render(f"Time: {time_left // 1000}s", True, WHITE)
        screen.blit(timer_text, (WINDOW_WIDTH - 150, PLAYING_AREA + (WINDOW_HEIGHT - PLAYING_AREA) // 2))
        
        # Draw flags remaining
        flags_text = font.render(f"Flags: {6 - flags_captured}", True, WHITE)
        screen.blit(flags_text, (WINDOW_WIDTH // 2 - 40, PLAYING_AREA + (WINDOW_HEIGHT - PLAYING_AREA) // 2))
        
        # Draw controls hint
        if level == 1 and time_left > 55000:  # Show only at the beginning
            hint_text = font.render("Arrow keys to move, P to pause", True, (150, 150, 150))
            screen.blit(hint_text, (WINDOW_WIDTH // 2 - 150, PLAYING_AREA - 30))
    else:
        # Draw game over banner
        game_over_text = large_font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 150, PLAYING_AREA // 2 - 100))
        
        # Draw final score
        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(final_score_text, (WINDOW_WIDTH // 2 - 80, PLAYING_AREA // 2 - 20))
        
        # Draw high score
        high_score_text = font.render(f"High Score: {high_score}", True, GOLD)
        screen.blit(high_score_text, (WINDOW_WIDTH // 2 - 80, PLAYING_AREA // 2 + 20))
        
        # Draw level reached
        level_text = font.render(f"Level Reached: {level}", True, GREEN)
        screen.blit(level_text, (WINDOW_WIDTH // 2 - 80, PLAYING_AREA // 2 + 60))
        
        # Draw reset instruction
        reset_text = font.render("Press 'R' to play again", True, WHITE)
        screen.blit(reset_text, (WINDOW_WIDTH // 2 - 120, PLAYING_AREA // 2 + 100))
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
sys.exit()
