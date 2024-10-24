import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game states
MENU = 'menu'
PLAYING = 'playing'
GAME_OVER = 'game_over'

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("LollMS Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()
        self.game_state = MENU
        self.level = 1
        self.speed = 10

    def reset_game(self):
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.food = self.spawn_food()
        self.score = 0
        
    def spawn_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
            if food not in self.snake:
                return food

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.game_state == MENU:
                    if event.key == pygame.K_RETURN:
                        self.game_state = PLAYING
                elif self.game_state == PLAYING:
                    if event.key == pygame.K_UP and self.direction != (0, 1):
                        self.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                        self.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                        self.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                        self.direction = (1, 0)
                elif self.game_state == GAME_OVER:
                    if event.key == pygame.K_RETURN:
                        self.reset_game()
                        self.game_state = PLAYING
                        self.level = 1
                        self.speed = 10
        return True

    def update(self):
        if self.game_state != PLAYING:
            return

        # Move snake
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        # Check for collisions
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
            new_head in self.snake):
            self.game_state = GAME_OVER
            return

        self.snake.insert(0, new_head)

        # Check for food
        if new_head == self.food:
            self.score += 1
            self.food = self.spawn_food()
            # Level up every 5 points
            if self.score % 5 == 0:
                self.level += 1
                self.speed += 2
        else:
            self.snake.pop()

    def draw(self):
        self.screen.fill(BLACK)

        if self.game_state == MENU:
            self.draw_menu()
        elif self.game_state == PLAYING:
            self.draw_game()
        elif self.game_state == GAME_OVER:
            self.draw_game_over()

        pygame.display.flip()

    def draw_menu(self):
        title = self.font.render("LollMS Snake Game", True, WHITE)
        start_text = self.font.render("Press ENTER to Start", True, WHITE)
        self.screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, WINDOW_HEIGHT//3))
        self.screen.blit(start_text, (WINDOW_WIDTH//2 - start_text.get_width()//2, WINDOW_HEIGHT//2))

    def draw_game(self):
        # Draw snake
        for segment in self.snake:
            pygame.draw.rect(self.screen, GREEN,
                           (segment[0]*GRID_SIZE, segment[1]*GRID_SIZE, GRID_SIZE-2, GRID_SIZE-2))

        # Draw food
        pygame.draw.rect(self.screen, RED,
                        (self.food[0]*GRID_SIZE, self.food[1]*GRID_SIZE, GRID_SIZE-2, GRID_SIZE-2))

        # Draw score and level
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 50))

    def draw_game_over(self):
        game_over_text = self.font.render("Game Over!", True, WHITE)
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        restart_text = self.font.render("Press ENTER to Restart", True, WHITE)
        
        self.screen.blit(game_over_text, (WINDOW_WIDTH//2 - game_over_text.get_width()//2, WINDOW_HEIGHT//3))
        self.screen.blit(score_text, (WINDOW_WIDTH//2 - score_text.get_width()//2, WINDOW_HEIGHT//2))
        self.screen.blit(restart_text, (WINDOW_WIDTH//2 - restart_text.get_width()//2, WINDOW_HEIGHT//2 + 50))

    def run(self):
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(self.speed)

def main():
    game = SnakeGame()
    game.run()

if __name__ == "__main__":
    main()