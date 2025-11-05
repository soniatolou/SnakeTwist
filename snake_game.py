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
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
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
            snake_color=(255, 255, 255), # White
            food_color=(255, 20, 147),  # Dark pink
            accent_color=(255, 105, 180) # Hot pink
        )
        self.description = "Kawaii desu ne~!"

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
    """ Food class to handle the position of the food """
    def __init__(self):
        self.position = self.generate_position()

    def generate_position(self, snake_body=None):
        """ Generates a random position for food """
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if snake_body is None or pos not in snake_body:
                self.position = pos
                return pos

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

        self.current_theme = None
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_state = "menu"  # menu, playing, game_over

    def draw_text(self, text, pos, font=None, color=WHITE):
        """ Draws text on the screen """
        if font is None:
            font = self.font
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=pos)
        self.screen.blit(text_surface, text_rect)

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

    def draw_game(self):
        """ Draws the game """
        # Background
        self.screen.fill(self.current_theme.bg_color)

        # Draw snake with gradient effect
        for i, (x, y) in enumerate(self.snake.body):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 2, GRID_SIZE - 2)

            # Head i lighter
            if i == 0:
                color = self.current_theme.snake_color
                pygame.draw.rect(self.screen, color, rect, border_radius=5)
                # Draw eyes
                eye_color = BLACK if self.current_theme.name != "Kawaii Paradise" else self.current_theme.food_color
                pygame.draw.circle(self.screen, eye_color, (x * GRID_SIZE + 5, y * GRID_SIZE + 5), 2)
                pygame.draw.circle(self.screen, eye_color, (x * GRID_SIZE + GRID_SIZE - 7, y * GRID_SIZE + 5), 2)
            else:
                # The body gets darker further back
                factor = max(0.5, 1 - (i * 0.02))
                color = tuple(int(c * factor) for c in self.current_theme.snake_color)
                pygame.draw.rect(self.screen, color, rect, border_radius=3)

        # Draw food as a circle
        food_x, food_y = self.food.position
        food_rect = pygame.Rect(food_x * GRID_SIZE, food_y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.circle(self.screen, self.current_theme.food_color, food_rect.center, GRID_SIZE // 2)

        # Draw score
        score_text = self.small_font.render(f"Score: {self.score}", True, self.current_theme.accent_color)
        score_bg = pygame.Rect(10, 10, score_text.get_width() + 20, score_text.get_height() + 10)
        pygame.draw.rect(self.screen, BLACK, score_bg, border_radius=5)
        pygame.draw.rect(self.screen, self.current_theme.accent_color, score_bg, 2, border_radius=5)
        self.screen.blit(score_text, (20, 15))

        # Draw theme names
        theme_text = self.small_font.render(self.current_theme.name, True, self.current_theme.accent_color)
        theme_bg = pygame.Rect(WINDOW_WIDTH - theme_text.get_width() - 30, 10,
                            theme_text.get_width() + 20, theme_text.get_height() + 10)
        pygame.draw.rect(self.screen, BLACK, theme_bg, border_radius=5)
        pygame.draw.rect(self.screen, self.current_theme.accent_color, theme_bg, 2, border_radius=5)
        self.screen.blit(theme_text, (WINDOW_WIDTH - theme_text.get_width() - 20, 15))

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
        self.food.generate_position(self.snake.body)
        self.score = 0

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
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.snake.change_direction(Direction.UP)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.snake.change_direction(Direction.DOWN)
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.snake.change_direction(Direction.LEFT)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.snake.change_direction(Direction.RIGHT)
            elif event.key == pygame.K_ESCAPE:
                self.game_state = "menu"

    def handle_game_over_input(self, event):
        """ Handles inputs on the game over-screen"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.reset_game()
                self.game_state = "playing"
            elif event.key == pygame.K_ESCAPE:
                self.game_state = "menu"

    def update(self):
        """ Updating game logic """
        if self.game_state == "playing":
            self.snake.move()

            # Checks collisions
            if self.snake.check_collision():
                self.game_state = "game_over"
                return

            # Checks if the snake eats food
            if self.snake.eat_food(self.food.position):
                self.score += 10
                self.food.generate_position(self.snake.body)

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
