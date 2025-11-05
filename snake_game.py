"""
Snake Game with theme worlds
"""

import pygame
import random
import sys
from enum import Enum

# Starting Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
HEADER_HEIGHT = 50
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = (WINDOW_HEIGHT - HEADER_HEIGHT) // GRID_SIZE
FPS = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Theme:
    """ Base class for theme worlds """
    def __init__(self, name, bg_color, snake_color, food_color, accent_color):
        self.name = name
        self.bg_color = bg_color
        self.snake_color = snake_color
        self.food_color = food_color
        self.accent_color = accent_color
        self.description = ""

# Defining all the theme worlds
class MarioTheme(Theme):
    def __init__(self):
        super().__init__(
            name="Super Mario World",
            bg_color=(92, 148, 252),  # Blue sky
            snake_color=(248, 56, 0),  # Red
            food_color=(252, 188, 16),  # Coin-yellow
            accent_color=(0, 168, 0)   # Green tubes
        )
        self.description = "It's-a me, Snake-io!"

class ZeldaTheme(Theme):
    def __init__(self):
        super().__init__(
            name="Hyrule Kingdom",
            bg_color=(34, 139, 34),    # Green
            snake_color=(30, 144, 255), # Blue
            food_color=(255, 215, 0),   # Gold
            accent_color=(139, 69, 19)  # Brown
        )
        self.description = "It's dangerous to go alone!"

class StitchTheme(Theme):
    def __init__(self):
        super().__init__(
            name="Ohana Island",
            bg_color=(135, 206, 250),  # Tropical blue
            snake_color=(65, 105, 225), # Stitch-blue
            food_color=(255, 182, 193), # Pink
            accent_color=(255, 140, 0)  # Tropical orange
        )
        self.description = "Ohana means family!"

class HelloKittyTheme(Theme):
    def __init__(self):
        super().__init__(
            name="Kawaii Paradise",
            bg_color=(255, 192, 203),  # Pink
            snake_color=(255, 105, 180), # Hot pink
            food_color=(255, 20, 147),  # Dark pink
            accent_color=(255, 105, 180) # Hot pink
        )
        self.description = "Kawaii desu ne~!"
        self.background_image = None

    def load_background(self, window_width, window_height):
        """ Load and scale the background image """
        try:
            import os
            bg_path = os.path.join(os.path.expanduser("~"), "Pictures", "Hackathon", "hellokittybackground.jpg")
            if os.path.exists(bg_path):
                self.background_image = pygame.image.load(bg_path)
                self.background_image = pygame.transform.scale(self.background_image, (window_width, window_height))
        except Exception as e:
            print(f"Could not load background image: {e}")
            self.background_image = None

class RetroTheme(Theme):
    def __init__(self):
        super().__init__(
            name="Retro Classic",
            bg_color=(0, 0, 0), # Black
            snake_color=(0, 255, 0), # Neon green
            food_color=(255, 0, 0), # Red
            accent_color=(255, 255, 0) # Yellow
        )
        self.description = "Old school vibes!"

class Snake:
    """ Snake-klassen for handeling the snakes logic """
    def __init__(self):
        self.reset()

    def reset(self):
        """ Reset the snake to start position """
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = Direction.RIGHT
        self.grow = False

    def move(self):
        """ Move the snake """
        head_x, head_y = self.body[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)

        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, new_direction):
        """ Change direction """
        if (self.direction == Direction.UP and new_direction != Direction.DOWN) or \
        (self.direction == Direction.DOWN and new_direction != Direction.UP) or \
        (self.direction == Direction.LEFT and new_direction != Direction.RIGHT) or \
        (self.direction == Direction.RIGHT and new_direction != Direction.LEFT):
            self.direction = new_direction

    def check_collision(self):
        """ Check if the snake is colliding with itself or the wall """
        head_x, head_y = self.body[0]

        # Wall-collision
        if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
            return True

        # Self-collision
        if self.body[0] in self.body[1:]:
            return True

        return False

    def eat_food(self, food_pos):
        """ Check if the snake eats food """
        if self.body[0] == food_pos:
            self.grow = True
            return True
        return False

class Food:
    """Base class for food (coins, mushrooms, and special items)"""
    def __init__(self, food_type="coin"):
        self.food_type = food_type  # "coin", "mushroom", "bow", "hellokitty"
        self.type = food_type  # Alias for compatibility

        # Set points based on food type
        if food_type == "coin":
            self.points = 1
        elif food_type == "mushroom":
            self.points = 2
        elif food_type == "bow":
            self.points = 1
        elif food_type == "hellokitty":
            self.points = 1
        else:
            self.points = 1  # Default

        self.position = self.generate_position()

    def generate_position(self, snake_body=None, obstacles=None):
        """Generate a random position for food"""
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            obstacle_positions = [obs.position for obs in obstacles] if obstacles else []
            if (snake_body is None or pos not in snake_body) and pos not in obstacle_positions:
                self.position = pos
                return pos

class Goomba:
    """Goomba class for Mario theme obstacles"""
    def __init__(self, position=None, can_move=False):
        if position is None:
            self.position = self.generate_position()
        else:
            self.position = position
        self.animation_frame = 0
        self.animation_speed = 10
        self.animation_counter = 0
        self.can_move = can_move
        self.move_counter = 0
        self.move_speed = 15  # How many frames between each movement
        self.direction = random.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])

    def generate_position(self, snake_body=None, food_pos=None, other_goombas=None):
        """Generate a random position for Goomba"""
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if snake_body is None or pos not in snake_body:
                if food_pos is None or pos != food_pos:
                    if other_goombas is None or pos not in other_goombas:
                        self.position = pos
                        return pos

    def update_animation(self):
        """Update animation for Goomba"""
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.animation_frame = (self.animation_frame + 1) % 2

    def move(self, snake_body, food_pos, other_goombas):
        """Move Goomba if it can move"""
        if not self.can_move:
            return

        self.move_counter += 1
        if self.move_counter >= self.move_speed:
            self.move_counter = 0

            # Try to move in current direction
            x, y = self.position
            dx, dy = self.direction.value
            new_pos = (x + dx, y + dy)

            # Check if new position is valid
            if (0 <= new_pos[0] < GRID_WIDTH and
                0 <= new_pos[1] < GRID_HEIGHT and
                new_pos not in snake_body and
                new_pos != food_pos and
                new_pos not in other_goombas):
                self.position = new_pos
            else:
                # Change direction if we collide
                self.direction = random.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])

class Obstacle:
    """ Obstacle class for moving obstacles in themed worlds """
    def __init__(self, obstacle_type, color):
        self.type = obstacle_type  # "palm", "surfboard", "kuromi", or "rupee"
        self.color = color
        self.position = self.generate_position()
        self.direction = random.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])
        self.move_counter = 0
        # Kuromi moves faster than palm trees, rupees move at medium speed
        if obstacle_type == "kuromi":
            self.move_delay = 2
        elif obstacle_type == "rupee":
            self.move_delay = 4
        else:
            self.move_delay = 3

    def generate_position(self):
        """ Generate random position for obstacle """
        return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def move(self):
        """ Move the obstacle """
        self.move_counter += 1
        if self.move_counter >= self.move_delay:
            self.move_counter = 0

            x, y = self.position
            dx, dy = self.direction.value
            new_x = x + dx
            new_y = y + dy

            # Bounce off walls
            if new_x < 0 or new_x >= GRID_WIDTH:
                self.direction = Direction.LEFT if self.direction == Direction.RIGHT else Direction.RIGHT
                new_x = x
            if new_y < 0 or new_y >= GRID_HEIGHT:
                self.direction = Direction.UP if self.direction == Direction.DOWN else Direction.DOWN
                new_y = y

            self.position = (new_x, new_y)

    def draw(self, screen):
        """ Draw the obstacle """
        x, y = self.position
        screen_x = x * GRID_SIZE
        screen_y = y * GRID_SIZE + HEADER_HEIGHT
        rect = pygame.Rect(screen_x, screen_y, GRID_SIZE, GRID_SIZE)

        if self.type == "palm":
            # Draw palm tree (brown trunk + green fronds)
            trunk_color = (139, 69, 19)
            leaf_color = (34, 139, 34)
            dark_leaf_color = (0, 128, 0)

            # Trunk (curved/segmented for tropical look)
            trunk_rect = pygame.Rect(screen_x + 7, screen_y + 8, 6, 12)
            pygame.draw.rect(screen, trunk_color, trunk_rect)
            # Trunk segments
            pygame.draw.line(screen, (101, 50, 15), (screen_x + 7, screen_y + 11), (screen_x + 13, screen_y + 11), 1)
            pygame.draw.line(screen, (101, 50, 15), (screen_x + 7, screen_y + 15), (screen_x + 13, screen_y + 15), 1)

            # Palm fronds (5-6 leaves radiating from center)
            center_x = screen_x + 10
            center_y = screen_y + 6

            # Top frond
            pygame.draw.line(screen, leaf_color, (center_x, center_y), (center_x, center_y - 6), 3)
            pygame.draw.line(screen, dark_leaf_color, (center_x, center_y), (center_x, center_y - 6), 1)

            # Top-left frond
            pygame.draw.line(screen, leaf_color, (center_x, center_y), (center_x - 5, center_y - 4), 3)
            pygame.draw.line(screen, dark_leaf_color, (center_x, center_y), (center_x - 5, center_y - 4), 1)

            # Top-right frond
            pygame.draw.line(screen, leaf_color, (center_x, center_y), (center_x + 5, center_y - 4), 3)
            pygame.draw.line(screen, dark_leaf_color, (center_x, center_y), (center_x + 5, center_y - 4), 1)

            # Left frond
            pygame.draw.line(screen, leaf_color, (center_x, center_y), (center_x - 7, center_y), 3)
            pygame.draw.line(screen, dark_leaf_color, (center_x, center_y), (center_x - 7, center_y), 1)

            # Right frond
            pygame.draw.line(screen, leaf_color, (center_x, center_y), (center_x + 7, center_y), 3)
            pygame.draw.line(screen, dark_leaf_color, (center_x, center_y), (center_x + 7, center_y), 1)

            # Bottom-left frond
            pygame.draw.line(screen, leaf_color, (center_x, center_y), (center_x - 5, center_y + 3), 3)
            pygame.draw.line(screen, dark_leaf_color, (center_x, center_y), (center_x - 5, center_y + 3), 1)

            # Bottom-right frond
            pygame.draw.line(screen, leaf_color, (center_x, center_y), (center_x + 5, center_y + 3), 3)
            pygame.draw.line(screen, dark_leaf_color, (center_x, center_y), (center_x + 5, center_y + 3), 1)

        elif self.type == "surfboard":
            # Draw surfboard (elongated oval)
            board_color = (255, 69, 0)  # Orange-red
            stripe_color = (255, 255, 255)

            # Main board
            pygame.draw.ellipse(screen, board_color, rect)
            # Stripe
            stripe_rect = pygame.Rect(screen_x + 2, screen_y + GRID_SIZE//2 - 1,
                                     GRID_SIZE - 4, 2)
            pygame.draw.rect(screen, stripe_color, stripe_rect)

        elif self.type == "kuromi":
            # Draw Kuromi (black/purple character with devil tail and pink skull)
            kuromi_black = (50, 50, 50)
            kuromi_purple = (138, 43, 226)
            pink = (255, 105, 180)

            # Body (black circle)
            pygame.draw.circle(screen, kuromi_black, rect.center, GRID_SIZE // 2 - 1)

            # Eyes (white with black pupils)
            eye_left = (screen_x + 6, screen_y + 8)
            eye_right = (screen_x + 14, screen_y + 8)
            pygame.draw.circle(screen, (255, 255, 255), eye_left, 2)
            pygame.draw.circle(screen, (255, 255, 255), eye_right, 2)
            pygame.draw.circle(screen, BLACK, eye_left, 1)
            pygame.draw.circle(screen, BLACK, eye_right, 1)

            # Devil ears (purple triangles)
            ear_left_points = [
                (screen_x + 3, screen_y + 2),
                (screen_x, screen_y - 3),
                (screen_x + 6, screen_y + 2)
            ]
            ear_right_points = [
                (screen_x + 14, screen_y + 2),
                (screen_x + 20, screen_y - 3),
                (screen_x + 17, screen_y + 2)
            ]
            pygame.draw.polygon(screen, kuromi_purple, ear_left_points)
            pygame.draw.polygon(screen, kuromi_purple, ear_right_points)

            # Pink skull mark on forehead
            pygame.draw.circle(screen, pink, (screen_x + 10, screen_y + 4), 2)

        elif self.type == "rupee":
            # Draw rupee (diamond-shaped gem from Zelda)
            center_x = screen_x + GRID_SIZE // 2
            center_y = screen_y + GRID_SIZE // 2

            # Diamond points
            rupee_points = [
                (center_x, center_y - 8),      # Top
                (center_x + 6, center_y),      # Right
                (center_x, center_y + 8),      # Bottom
                (center_x - 6, center_y)       # Left
            ]

            # Draw filled rupee
            pygame.draw.polygon(screen, self.color, rupee_points)

            # Add highlight (lighter color on top-left)
            highlight_color = tuple(min(255, c + 50) for c in self.color)
            highlight_points = [
                (center_x, center_y - 8),
                (center_x - 3, center_y - 4),
                (center_x, center_y)
            ]
            pygame.draw.polygon(screen, highlight_color, highlight_points)

            # Draw outline
            dark_color = tuple(max(0, c - 50) for c in self.color)
            pygame.draw.polygon(screen, dark_color, rupee_points, 2)

class Game:
    """ Main class for the game """
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake - Theme worlds")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # All avaliable themes
        self.themes = [
            MarioTheme(),
            ZeldaTheme(),
            StitchTheme(),
            HelloKittyTheme(),
            RetroTheme()
        ]

        # Load background images for themes that have them
        for theme in self.themes:
            if hasattr(theme, 'load_background'):
                theme.load_background(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.current_theme = None
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.food_collected = 0
        self.goombas = []
        self.game_state = "menu"  # menu, playing, game_over
        self.paused = False
        self.obstacles = []
        self.obstacle_spawn_counter = 0
        self.obstacle_spawn_rate = 50  # Spawn obstacle every 50 frames (approx 5 seconds)


    def grid_to_screen(self, grid_x, grid_y):
        """ Convert grid coordinates to screen coordinates (accounting for header) """
        return (grid_x * GRID_SIZE, grid_y * GRID_SIZE + HEADER_HEIGHT)

    def draw_text(self, text, pos, font=None, color=WHITE):
        """ Draws text on the screen """
        if font is None:
            font = self.font
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=pos)
        self.screen.blit(text_surface, text_rect)

    def draw_header(self):
        """ Draw header bar with score and theme name """
        # Draw header background
        header_rect = pygame.Rect(0, 0, WINDOW_WIDTH, HEADER_HEIGHT)
        pygame.draw.rect(self.screen, BLACK, header_rect)
        pygame.draw.line(self.screen, self.current_theme.accent_color,
                        (0, HEADER_HEIGHT), (WINDOW_WIDTH, HEADER_HEIGHT), 3)

        # Draw score on the left
        score_text = self.small_font.render(f"Score: {self.score}", True, self.current_theme.accent_color)
        self.screen.blit(score_text, (20, 15))

        # Draw theme name in the center
        theme_text = self.small_font.render(self.current_theme.name, True, self.current_theme.accent_color)
        theme_rect = theme_text.get_rect(center=(WINDOW_WIDTH // 2, HEADER_HEIGHT // 2))
        self.screen.blit(theme_text, theme_rect)

        # Draw pause hint on the right
        pause_text = self.small_font.render("Press P to pause", True, WHITE)
        self.screen.blit(pause_text, (WINDOW_WIDTH - pause_text.get_width() - 20, 15))

    def draw_triforce(self, x, y, size):
        """ Draw a Triforce symbol for Zelda theme """
        gold = (255, 215, 0)
        dark_gold = (218, 165, 32)

        # Top triangle
        top_triangle = [
            (x, y - size),
            (x - size, y),
            (x + size, y)
        ]
        # Bottom-left triangle
        left_triangle = [
            (x - size, y),
            (x - 2*size, y + size),
            (x, y + size)
        ]
        # Bottom-right triangle
        right_triangle = [
            (x + size, y),
            (x, y + size),
            (x + 2*size, y + size)
        ]

        pygame.draw.polygon(self.screen, gold, top_triangle)
        pygame.draw.polygon(self.screen, gold, left_triangle)
        pygame.draw.polygon(self.screen, gold, right_triangle)

        # Draw outlines
        pygame.draw.polygon(self.screen, dark_gold, top_triangle, 2)
        pygame.draw.polygon(self.screen, dark_gold, left_triangle, 2)
        pygame.draw.polygon(self.screen, dark_gold, right_triangle, 2)

    def draw_hyrule_grass(self, grid_x, grid_y):
        """ Draw grass patch for Zelda theme """
        grass_green = (0, 128, 0)
        dark_green = (0, 100, 0)

        x, y = self.grid_to_screen(grid_x, grid_y)

        # Draw grass blades
        for i in range(3):
            offset_x = i * 6
            blade_points = [
                (x + offset_x, y + GRID_SIZE),
                (x + offset_x + 2, y + GRID_SIZE - 8),
                (x + offset_x + 4, y + GRID_SIZE)
            ]
            pygame.draw.polygon(self.screen, grass_green if i % 2 == 0 else dark_green, blade_points)

    def draw_master_sword(self, grid_x, grid_y):
        """ Draw Master Sword as food for Zelda theme """
        screen_x, screen_y = self.grid_to_screen(grid_x, grid_y)
        x = screen_x + GRID_SIZE // 2
        y = screen_y + GRID_SIZE // 2

        # Blade (blue-silver)
        blade_color = (192, 192, 220)
        blade_rect = pygame.Rect(x - 2, y - 8, 4, 10)
        pygame.draw.rect(self.screen, blade_color, blade_rect)

        # Blade tip (triangle)
        tip_points = [
            (x, y - 10),
            (x - 2, y - 8),
            (x + 2, y - 8)
        ]
        pygame.draw.polygon(self.screen, blade_color, tip_points)

        # Guard (gold)
        guard_color = (255, 215, 0)
        guard_rect = pygame.Rect(x - 5, y + 2, 10, 2)
        pygame.draw.rect(self.screen, guard_color, guard_rect)

        # Handle (blue)
        handle_color = (30, 144, 255)
        handle_rect = pygame.Rect(x - 1, y + 4, 2, 5)
        pygame.draw.rect(self.screen, handle_color, handle_rect)

        # Pommel (gold)
        pygame.draw.circle(self.screen, guard_color, (x, y + 10), 2)

    def draw_pixelated_mario_mushroom(self, x, y, size=30):
        """ Draw a pixelated Mario mushroom decoration """
        mushroom_red = (255, 0, 0)
        mushroom_white = (255, 255, 255)
        mushroom_beige = (245, 222, 179)
        pixel_size = size // 6

        # Mushroom cap pattern (pixelated)
        # Row 1 (top)
        pygame.draw.rect(self.screen, mushroom_red, (x + pixel_size * 2, y, pixel_size * 2, pixel_size))

        # Row 2
        pygame.draw.rect(self.screen, mushroom_red, (x + pixel_size, y + pixel_size, pixel_size, pixel_size))
        pygame.draw.rect(self.screen, mushroom_white, (x + pixel_size * 2, y + pixel_size, pixel_size, pixel_size))
        pygame.draw.rect(self.screen, mushroom_red, (x + pixel_size * 3, y + pixel_size, pixel_size * 2, pixel_size))

        # Row 3
        pygame.draw.rect(self.screen, mushroom_red, (x, y + pixel_size * 2, pixel_size, pixel_size))
        pygame.draw.rect(self.screen, mushroom_white, (x + pixel_size, y + pixel_size * 2, pixel_size, pixel_size))
        pygame.draw.rect(self.screen, mushroom_red, (x + pixel_size * 2, y + pixel_size * 2, pixel_size, pixel_size))
        pygame.draw.rect(self.screen, mushroom_white, (x + pixel_size * 3, y + pixel_size * 2, pixel_size, pixel_size))
        pygame.draw.rect(self.screen, mushroom_red, (x + pixel_size * 4, y + pixel_size * 2, pixel_size * 2, pixel_size))

        # Row 4 (stem starts)
        pygame.draw.rect(self.screen, mushroom_red, (x, y + pixel_size * 3, pixel_size, pixel_size))
        pygame.draw.rect(self.screen, mushroom_beige, (x + pixel_size, y + pixel_size * 3, pixel_size * 4, pixel_size))
        pygame.draw.rect(self.screen, mushroom_red, (x + pixel_size * 5, y + pixel_size * 3, pixel_size, pixel_size))

        # Row 5 (stem)
        pygame.draw.rect(self.screen, mushroom_beige, (x + pixel_size * 2, y + pixel_size * 4, pixel_size * 2, pixel_size))

        # Row 6 (stem bottom)
        pygame.draw.rect(self.screen, mushroom_beige, (x + pixel_size * 2, y + pixel_size * 5, pixel_size * 2, pixel_size))

    def draw_pixelated_stitch(self, x, y, size=30):
        """ Draw a pixelated Stitch decoration """
        stitch_blue = (65, 105, 225)
        dark_blue = (30, 60, 150)
        pixel_size = size // 6

        # Body pattern (pixelated)
        # Row 1 (ears)
        pygame.draw.rect(self.screen, dark_blue, (x, y, pixel_size, pixel_size))
        pygame.draw.rect(self.screen, dark_blue, (x + pixel_size * 5, y, pixel_size, pixel_size))

        # Row 2 (head top)
        pygame.draw.rect(self.screen, dark_blue, (x, y + pixel_size, pixel_size, pixel_size))
        pygame.draw.rect(self.screen, stitch_blue, (x + pixel_size, y + pixel_size, pixel_size * 4, pixel_size))
        pygame.draw.rect(self.screen, dark_blue, (x + pixel_size * 5, y + pixel_size, pixel_size, pixel_size))

        # Row 3 (eyes)
        pygame.draw.rect(self.screen, stitch_blue, (x + pixel_size, y + pixel_size * 2, pixel_size, pixel_size))
        pygame.draw.rect(self.screen, BLACK, (x + pixel_size * 2, y + pixel_size * 2, pixel_size, pixel_size))
        pygame.draw.rect(self.screen, stitch_blue, (x + pixel_size * 3, y + pixel_size * 2, pixel_size, pixel_size))
        pygame.draw.rect(self.screen, BLACK, (x + pixel_size * 4, y + pixel_size * 2, pixel_size, pixel_size))
        pygame.draw.rect(self.screen, stitch_blue, (x + pixel_size * 5, y + pixel_size * 2, pixel_size, pixel_size))

        # Row 4 (face area - no nose, more realistic)
        pygame.draw.rect(self.screen, stitch_blue, (x + pixel_size, y + pixel_size * 3, pixel_size * 5, pixel_size))

        # Row 5 (body)
        pygame.draw.rect(self.screen, stitch_blue, (x + pixel_size, y + pixel_size * 4, pixel_size * 4, pixel_size))

        # Row 6 (body bottom)
        pygame.draw.rect(self.screen, stitch_blue, (x + pixel_size * 2, y + pixel_size * 5, pixel_size * 2, pixel_size))

    def draw_menu(self):
        """ Draws the theme world-menu """
        self.screen.fill((30, 30, 50))

        # Title
        title = self.font.render("SNAKE - CHOOSE YOUR WORLD", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)

        # Drawing every theme
        start_y = 120
        spacing = 80

        for i, theme in enumerate(self.themes):
            y_pos = start_y + i * spacing

            # Draw a colored box for the theme
            box_rect = pygame.Rect(150, y_pos - 25, 500, 60)
            pygame.draw.rect(self.screen, theme.accent_color, box_rect, 3)

            # Draw the theme name
            name_text = self.small_font.render(f"{i+1}. {theme.name}", True, theme.accent_color)
            self.screen.blit(name_text, (170, y_pos - 15))

            # Draw description
            desc_text = self.small_font.render(theme.description, True, WHITE)
            self.screen.blit(desc_text, (170, y_pos + 10))

        # Instructions
        instr = self.small_font.render("Press 1 to 5 to choose world", True, WHITE)
        instr_rect = instr.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))
        self.screen.blit(instr, instr_rect)

    def draw_coin(self, position, color):
        """Rita ett mynt"""
        x, y = position
        screen_x, screen_y = self.grid_to_screen(x, y)
        center_x = screen_x + GRID_SIZE // 2
        center_y = screen_y + GRID_SIZE // 2

        # Guldmynt med cirkel
        pygame.draw.circle(self.screen, color, (center_x, center_y), GRID_SIZE // 2 - 2)
        # Inre cirkel (detalj)
        darker_color = tuple(max(0, c - 40) for c in color)
        pygame.draw.circle(self.screen, darker_color, (center_x, center_y), GRID_SIZE // 3, 2)

    def draw_mushroom(self, position, color):
        """Rita en svamp (mushroom)"""
        x, y = position
        base_x, base_y = self.grid_to_screen(x, y)

        # Svamphatt (röd med vita prickar för Mario-tema)
        mushroom_red = (255, 0, 0) if self.current_theme.name == "Super Mario World" else color
        mushroom_white = (255, 255, 255)
        mushroom_beige = (245, 222, 179)

        # Hatt (övre delen)
        hat_rect = pygame.Rect(base_x + 2, base_y + 2, GRID_SIZE - 4, GRID_SIZE // 2)
        pygame.draw.ellipse(self.screen, mushroom_red, hat_rect)

        # Vita prickar på hatten
        pygame.draw.circle(self.screen, mushroom_white, (base_x + GRID_SIZE // 2, base_y + 6), 2)
        pygame.draw.circle(self.screen, mushroom_white, (base_x + 5, base_y + 8), 1)
        pygame.draw.circle(self.screen, mushroom_white, (base_x + GRID_SIZE - 5, base_y + 8), 1)

        # Stam (nedre delen)
        stem_rect = pygame.Rect(base_x + GRID_SIZE // 3, base_y + GRID_SIZE // 2, GRID_SIZE // 3, GRID_SIZE // 2 - 2)
        pygame.draw.rect(self.screen, mushroom_beige, stem_rect, border_radius=2)

    def draw_goomba(self, goomba):
        """Rita en Goomba"""
        x, y = goomba.position
        base_x, base_y = self.grid_to_screen(x, y)

        # Goomba kropp (brun svamp-form)
        goomba_brown = (139, 69, 19)
        goomba_dark = (101, 50, 15)

        # Kropp
        body_rect = pygame.Rect(base_x + 2, base_y + 8, GRID_SIZE - 4, GRID_SIZE - 10)
        pygame.draw.ellipse(self.screen, goomba_brown, body_rect)

        # Fötter (animerade)
        foot_offset = 2 if goomba.animation_frame == 0 else -2
        pygame.draw.rect(self.screen, goomba_dark,
                        (base_x + 3 + foot_offset, base_y + GRID_SIZE - 4, 5, 3))
        pygame.draw.rect(self.screen, goomba_dark,
                        (base_x + GRID_SIZE - 8 - foot_offset, base_y + GRID_SIZE - 4, 5, 3))

        # Ögon (arga)
        eye_white = WHITE
        eye_black = BLACK
        # Vänster öga
        pygame.draw.circle(self.screen, eye_white, (base_x + 6, base_y + 10), 3)
        pygame.draw.circle(self.screen, eye_black, (base_x + 7, base_y + 10), 2)
        # Höger öga
        pygame.draw.circle(self.screen, eye_white, (base_x + GRID_SIZE - 6, base_y + 10), 3)
        pygame.draw.circle(self.screen, eye_black, (base_x + GRID_SIZE - 7, base_y + 10), 2)

        # Ögonbryn (arga)
        pygame.draw.line(self.screen, goomba_dark,
                        (base_x + 4, base_y + 8), (base_x + 8, base_y + 9), 2)
        pygame.draw.line(self.screen, goomba_dark,
                        (base_x + GRID_SIZE - 4, base_y + 8), (base_x + GRID_SIZE - 8, base_y + 9), 2)

    def draw_game(self):
        """ Draws the game """
        # Background - fill game area only (below header)
        game_area_rect = pygame.Rect(0, HEADER_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT - HEADER_HEIGHT)
        if (hasattr(self.current_theme, 'background_image') and
            self.current_theme.background_image is not None):
            # Draw background image if available - crop to game area
            self.screen.fill(BLACK)  # Fill entire screen first
            self.screen.blit(self.current_theme.background_image, (0, HEADER_HEIGHT),
                           (0, HEADER_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT - HEADER_HEIGHT))
        else:
            # Fill entire screen first with black, then game area with theme color
            self.screen.fill(BLACK)
            pygame.draw.rect(self.screen, self.current_theme.bg_color, game_area_rect)

        # Draw themed background decorations
        if self.current_theme.name == "Super Mario World":
            # Draw pixelated Mario mushrooms in corners (below header) - bigger size
            self.draw_pixelated_mario_mushroom(15, HEADER_HEIGHT + 15, 50)
            self.draw_pixelated_mario_mushroom(WINDOW_WIDTH - 65, HEADER_HEIGHT + 15, 50)
            self.draw_pixelated_mario_mushroom(15, WINDOW_HEIGHT - 65, 50)
            self.draw_pixelated_mario_mushroom(WINDOW_WIDTH - 65, WINDOW_HEIGHT - 65, 50)

        elif self.current_theme.name == "Ohana Island":
            # Draw pixelated Stitch in corners (below header) - bigger size
            self.draw_pixelated_stitch(15, HEADER_HEIGHT + 15, 50)
            self.draw_pixelated_stitch(WINDOW_WIDTH - 65, HEADER_HEIGHT + 15, 50)
            self.draw_pixelated_stitch(15, WINDOW_HEIGHT - 65, 50)
            self.draw_pixelated_stitch(WINDOW_WIDTH - 65, WINDOW_HEIGHT - 65, 50)

        elif self.current_theme.name == "Hyrule Kingdom":
            # Draw Triforce symbols in corners (below header)
            self.draw_triforce(50, HEADER_HEIGHT + 50, 15)
            self.draw_triforce(WINDOW_WIDTH - 50, HEADER_HEIGHT + 50, 15)
            self.draw_triforce(50, WINDOW_HEIGHT - 50, 15)
            self.draw_triforce(WINDOW_WIDTH - 50, WINDOW_HEIGHT - 50, 15)

            # Draw grass patches around the map
            grass_positions = [(5, 10), (15, 8), (25, 12), (35, 9), (10, 25), (30, 22),
                              (5, 20), (20, 5), (38, 15), (2, 28)]
            for gx, gy in grass_positions:
                self.draw_hyrule_grass(gx, gy)

        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        # Draw Goombas (Mario theme)
        if self.current_theme and self.current_theme.name == "Super Mario World":
            for goomba in self.goombas:
                self.draw_goomba(goomba)
                goomba.update_animation()

                # Move Goomba
                other_goomba_positions = [g.position for g in self.goombas if g != goomba]
                goomba.move(self.snake.body, self.food.position, other_goomba_positions)

        # Draw snake with gradient effect
        for i, (x, y) in enumerate(self.snake.body):
            screen_x, screen_y = self.grid_to_screen(x, y)
            rect = pygame.Rect(screen_x, screen_y, GRID_SIZE - 2, GRID_SIZE - 2)

            # Head i lighter
            if i == 0:
                color = self.current_theme.snake_color
                pygame.draw.rect(self.screen, color, rect, border_radius=5)
                # Draw eyes
                eye_color = BLACK if self.current_theme.name != "Kawaii Paradise" else self.current_theme.food_color
                pygame.draw.circle(self.screen, eye_color, (screen_x + 5, screen_y + 5), 2)
                pygame.draw.circle(self.screen, eye_color, (screen_x + GRID_SIZE - 7, screen_y + 5), 2)
            else:
                # The body gets darker further back
                factor = max(0.5, 1 - (i * 0.02))
                color = tuple(int(c * factor) for c in self.current_theme.snake_color)
                pygame.draw.rect(self.screen, color, rect, border_radius=3)

        # Draw food (themed based on world)
        food_x, food_y = self.food.position
        food_screen_x, food_screen_y = self.grid_to_screen(food_x, food_y)
        food_rect = pygame.Rect(food_screen_x, food_screen_y, GRID_SIZE, GRID_SIZE)

        if self.current_theme.name == "Hyrule Kingdom":
            # Draw Master Sword for Zelda theme
            self.draw_master_sword(food_x, food_y)

        elif self.current_theme.name == "Ohana Island":
            # Draw Stitch (blue alien with big ears)
            stitch_blue = (65, 105, 225)
            dark_blue = (30, 60, 150)

            # Body (main circle)
            pygame.draw.circle(self.screen, stitch_blue, food_rect.center, GRID_SIZE // 2 - 1)

            # Big black eyes
            eye_left = (food_screen_x + 5, food_screen_y + 8)
            eye_right = (food_screen_x + 15, food_screen_y + 8)
            pygame.draw.circle(self.screen, BLACK, eye_left, 3)
            pygame.draw.circle(self.screen, BLACK, eye_right, 3)

            # Ears (dark blue triangles on top)
            ear_left_points = [
                (food_screen_x + 3, food_screen_y + 2),
                (food_screen_x, food_screen_y - 3),
                (food_screen_x + 6, food_screen_y + 2)
            ]
            ear_right_points = [
                (food_screen_x + 14, food_screen_y + 2),
                (food_screen_x + 20, food_screen_y - 3),
                (food_screen_x + 17, food_screen_y + 2)
            ]
            pygame.draw.polygon(self.screen, dark_blue, ear_left_points)
            pygame.draw.polygon(self.screen, dark_blue, ear_right_points)

            # Nose (small pink)
            pygame.draw.circle(self.screen, self.current_theme.food_color,
                             (food_screen_x + 10, food_screen_y + 12), 2)

        elif self.current_theme.name == "Kawaii Paradise":
            if self.food.type == "bow":
                # Draw pink bow (1 point)
                pink = (255, 105, 180)
                dark_pink = (255, 20, 147)

                # Bow center
                pygame.draw.circle(self.screen, dark_pink, food_rect.center, 3)

                # Bow left side
                left_bow = [
                    (food_screen_x + 4, food_screen_y + 10),
                    (food_screen_x + 2, food_screen_y + 6),
                    (food_screen_x + 8, food_screen_y + 10)
                ]
                pygame.draw.polygon(self.screen, pink, left_bow)

                # Bow right side
                right_bow = [
                    (food_screen_x + 12, food_screen_y + 10),
                    (food_screen_x + 18, food_screen_y + 6),
                    (food_screen_x + 16, food_screen_y + 10)
                ]
                pygame.draw.polygon(self.screen, pink, right_bow)

            elif self.food.type == "hellokitty":
                # Draw Hello Kitty (2 points)
                white = (255, 255, 255)
                pink = (255, 105, 180)
                yellow = (255, 215, 0)

                # Black outline circle
                pygame.draw.circle(self.screen, BLACK, food_rect.center, GRID_SIZE // 2, 2)

                # Head (white circle)
                pygame.draw.circle(self.screen, white, food_rect.center, GRID_SIZE // 2 - 1)

                # Black eyes
                eye_left = (food_screen_x + 6, food_screen_y + 9)
                eye_right = (food_screen_x + 14, food_screen_y + 9)
                pygame.draw.circle(self.screen, BLACK, eye_left, 2)
                pygame.draw.circle(self.screen, BLACK, eye_right, 2)

                # Yellow nose
                pygame.draw.circle(self.screen, yellow,
                                 (food_screen_x + 10, food_screen_y + 12), 2)

                # Ears (white triangles on top)
                ear_left_points = [
                    (food_screen_x + 3, food_screen_y + 4),
                    (food_screen_x + 1, food_screen_y),
                    (food_screen_x + 6, food_screen_y + 4)
                ]
                ear_right_points = [
                    (food_screen_x + 14, food_screen_y + 4),
                    (food_screen_x + 19, food_screen_y),
                    (food_screen_x + 17, food_screen_y + 4)
                ]
                pygame.draw.polygon(self.screen, white, ear_left_points)
                pygame.draw.polygon(self.screen, white, ear_right_points)

                # Pink bow on left ear
                bow_center = (food_screen_x + 3, food_screen_y + 2)
                pygame.draw.circle(self.screen, pink, bow_center, 3)

        else:
            # Draw coin or mushroom for other themes
            if self.food.food_type == "coin":
                self.draw_coin(self.food.position, self.current_theme.food_color)
            else:  # mushroom
                self.draw_mushroom(self.food.position, self.current_theme.food_color)

        # Draw header with score and theme name
        self.draw_header()

    def draw_paused(self):
        """ Draws the paused screen """
        # Draw the game in the background
        self.draw_game()

        # Dark overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # Paused text
        self.draw_text("PAUSED", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40), color=self.current_theme.accent_color)

        # Instructions
        self.draw_text("Press P to continue", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10),
                    font=self.small_font, color=WHITE)

        self.draw_text("Press ESC to return to menu", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40),
                    font=self.small_font, color=WHITE)

    def draw_game_over(self):
        """ Draws the game over-screen """
        # Draw the game in the background
        self.draw_game()

        # Dark overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # Game Over text
        self.draw_text("GAME OVER!", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60), color=self.current_theme.food_color)

        # Final score
        self.draw_text(f"Final Score: {self.score}", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2),
                    font=self.small_font, color=WHITE)

        # Instructions
        self.draw_text("Press SPACE to play again", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40),
                    font=self.small_font, color=self.current_theme.accent_color)

        self.draw_text("Press ESC to choose a new world", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 70),
                    font=self.small_font, color=self.current_theme.accent_color)

    def reset_game(self):
        """ Resets the game """
        self.snake.reset()
        self.obstacles = []
        self.obstacle_spawn_counter = 0
        self.spawn_food()
        self.score = 0
        self.food_collected = 0
        self.goombas = []
        self.paused = False

    def spawn_food(self):
        """ Spawn food based on current theme """
        if self.current_theme and self.current_theme.name == "Kawaii Paradise":
            # 70% chance for bow (10 points), 30% chance for Hello Kitty (10 points)
            if random.random() < 0.7:
                self.food = Food(food_type="bow")
            else:
                self.food = Food(food_type="hellokitty")
        elif self.current_theme and self.current_theme.name == "Retro Classic":
            # Only coins for Retro Classic Snake (no mushrooms)
            self.food = Food(food_type="coin")
        else:
            # Coin/mushroom system for other themes (70% coin=1pt, 30% mushroom=2pt)
            food_type = "coin" if random.random() < 0.7 else "mushroom"
            self.food = Food(food_type=food_type)

        self.food.generate_position(self.snake.body, self.obstacles)

    def spawn_obstacle(self):
        """ Spawn a random obstacle for themed worlds """
        if self.current_theme and self.current_theme.name == "Ohana Island":
            obstacle_type = "palm"  # Only palm trees
            obstacle = Obstacle(obstacle_type, self.current_theme.accent_color)

            # Make sure obstacle doesn't spawn on snake or food
            attempts = 0
            while attempts < 10:
                if (obstacle.position not in self.snake.body and
                    obstacle.position != self.food.position):
                    self.obstacles.append(obstacle)
                    break
                obstacle.position = obstacle.generate_position()
                attempts += 1

            # Limit number of obstacles
            if len(self.obstacles) > 5:
                self.obstacles.pop(0)

        elif self.current_theme and self.current_theme.name == "Kawaii Paradise":
            obstacle_type = "kuromi"  # Only Kuromi
            obstacle = Obstacle(obstacle_type, self.current_theme.accent_color)

            # Make sure obstacle doesn't spawn on snake or food
            attempts = 0
            while attempts < 10:
                if (obstacle.position not in self.snake.body and
                    obstacle.position != self.food.position):
                    self.obstacles.append(obstacle)
                    break
                obstacle.position = obstacle.generate_position()
                attempts += 1

            # Gradually increase max Kuromis based on food collected
            # Start with 1, then add 1 more every 5 food items collected (max 5 Kuromis)
            max_kuromis = min(5, 1 + (self.food_collected // 5))
            if len(self.obstacles) > max_kuromis:
                self.obstacles.pop(0)

        elif self.current_theme and self.current_theme.name == "Hyrule Kingdom":
            # Spawn rupees with different colors (green, blue, red, gold)
            rupee_colors = [
                (0, 255, 0),      # Green rupee
                (0, 0, 255),      # Blue rupee
                (255, 0, 0),      # Red rupee
                (255, 215, 0)     # Gold rupee
            ]
            obstacle_type = "rupee"
            rupee_color = random.choice(rupee_colors)
            obstacle = Obstacle(obstacle_type, rupee_color)

            # Make sure obstacle doesn't spawn on snake or food
            attempts = 0
            while attempts < 10:
                if (obstacle.position not in self.snake.body and
                    obstacle.position != self.food.position):
                    self.obstacles.append(obstacle)
                    break
                obstacle.position = obstacle.generate_position()
                attempts += 1

            # Limit number of obstacles to 6 for Zelda world
            if len(self.obstacles) > 6:
                self.obstacles.pop(0)

    def check_obstacle_collision(self):
        """ Check if snake collides with any obstacle """
        head = self.snake.body[0]
        for obstacle in self.obstacles:
            if head == obstacle.position:
                return True
        return False

    def handle_menu_input(self, event):
        """ Handles input in the menu """
        if event.type == pygame.KEYDOWN:
            if pygame.K_1 <= event.key <= pygame.K_5:
                theme_index = event.key - pygame.K_1
                if theme_index < len(self.themes):
                    self.current_theme = self.themes[theme_index]
                    self.game_state = "playing"
                    self.reset_game()

    def handle_game_input(self, event):
        """ Handles input during the game """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                # Toggle pause
                self.paused = not self.paused
            elif event.key == pygame.K_ESCAPE:
                if self.paused:
                    # Return to menu when paused
                    self.game_state = "menu"
                    self.paused = False
                else:
                    # Allow ESC to pause as well
                    self.paused = True
            elif not self.paused:
                # Only allow movement when not paused
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.snake.change_direction(Direction.UP)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.snake.change_direction(Direction.DOWN)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.snake.change_direction(Direction.LEFT)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.snake.change_direction(Direction.RIGHT)

    def handle_game_over_input(self, event):
        """ Handles inputs on the game over-screen"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.reset_game()
                self.game_state = "playing"
            elif event.key == pygame.K_ESCAPE:
                self.game_state = "menu"

    def spawn_goomba(self):
        """Skapa en ny Goomba på en säker plats"""
        goomba_positions = [g.position for g in self.goombas]

        # Goombas börjar röra sig efter 15 block (5 + 3 + 3 + 3 + 3 = 17, så efter 4:e Goomban)
        can_move = self.food_collected >= 15

        new_goomba = Goomba(can_move=can_move)
        new_goomba.generate_position(self.snake.body, self.food.position, goomba_positions)
        self.goombas.append(new_goomba)

        # Aktivera rörelse för alla Goombas när tröskeln nås
        if can_move:
            for goomba in self.goombas:
                goomba.can_move = True

    def update(self):
        """ Updating game logic """
        if self.game_state == "playing" and not self.paused:
            self.snake.move()

            # Move obstacles
            for obstacle in self.obstacles:
                obstacle.move()

            # Spawn obstacles for themed worlds
            if self.current_theme and (self.current_theme.name == "Ohana Island" or
                                       self.current_theme.name == "Kawaii Paradise" or
                                       self.current_theme.name == "Hyrule Kingdom"):
                self.obstacle_spawn_counter += 1
                # Spawn rate depends on theme
                spawn_rate = self.obstacle_spawn_rate
                if self.current_theme.name == "Kawaii Paradise" and len(self.obstacles) == 0:
                    # Spawn Kuromi immediately if none exists
                    self.spawn_obstacle()
                elif self.obstacle_spawn_counter >= spawn_rate:
                    self.spawn_obstacle()
                    self.obstacle_spawn_counter = 0

            # Checks collisions with walls and self
            if self.snake.check_collision():
                self.game_state = "game_over"
                return

            # Check collisions with obstacles (Stitch theme)
            if self.check_obstacle_collision():
                self.game_state = "game_over"
                return

            # Check Goomba collisions (Mario theme)
            if self.current_theme and self.current_theme.name == "Super Mario World":
                for goomba in self.goombas:
                    if self.snake.body[0] == goomba.position:
                        self.game_state = "game_over"
                        return

            # Check if the snake eats food
            if self.snake.eat_food(self.food.position):
                # Add points based on food type
                self.score += self.food.points
                self.food_collected += 1

                # Spawn Goomba (Mario theme only)
                # First at 5 blocks, then every 3rd (at 8, 11, 14, 17, etc.)
                if self.current_theme and self.current_theme.name == "Super Mario World":
                    if self.food_collected == 5 or (self.food_collected > 5 and (self.food_collected - 5) % 3 == 0):
                        self.spawn_goomba()

                # Spawn new food
                self.spawn_food()

    def run(self):
        """ Main game loop """
        running = True

        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.game_state == "menu":
                    self.handle_menu_input(event)
                elif self.game_state == "playing":
                    self.handle_game_input(event)
                elif self.game_state == "game_over":
                    self.handle_game_over_input(event)

            # Updating game logic
            self.update()

            # Draw everything
            if self.game_state == "menu":
                self.draw_menu()
            elif self.game_state == "playing":
                if self.paused:
                    self.draw_paused()
                else:
                    self.draw_game()
            elif self.game_state == "game_over":
                self.draw_game_over()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
