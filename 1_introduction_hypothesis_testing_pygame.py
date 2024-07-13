import pygame
import sys
import random
import math
from scipy import stats

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1800, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hypothesis Testing Adventure")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
GRAY = (200, 200, 200)

# Fonts
FONT_SMALL = pygame.font.Font(None, 24)
FONT_MEDIUM = pygame.font.Font(None, 32)
FONT_LARGE = pygame.font.Font(None, 48)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2

# Game variables
game_state = MENU
score = 0
level = 1
time_left = 60
last_time = pygame.time.get_ticks()

# Hypothesis testing variables
null_hypothesis = 0.5
alternative_hypothesis = 0.55
sample_size = 100
significance_level = 0.05
critical_value = stats.norm.ppf(1 - significance_level)

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # Add border
        text_surface = FONT_MEDIUM.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Create buttons
reject_button = Button(WIDTH // 4 - 150, HEIGHT - 80, 300, 60, "Reject H₀", RED, WHITE)
fail_to_reject_button = Button(3 * WIDTH // 4 - 150, HEIGHT - 80, 300, 60, "Fail to Reject H₀", BLUE, WHITE)

# Helper functions
def draw_normal_distribution(mean, std_dev, critical_value, test_statistic):
    plot_width, plot_height = 1400, 500
    plot_x, plot_y = (WIDTH - plot_width) // 2, 100
    
    x = [i for i in range(plot_width)]
    y = [plot_height - 400 * stats.norm.pdf((i - plot_width/2) / 100, mean, std_dev) for i in x]
    
    # Draw background
    pygame.draw.rect(screen, WHITE, (plot_x, plot_y, plot_width, plot_height))
    pygame.draw.rect(screen, BLACK, (plot_x, plot_y, plot_width, plot_height), 2)
    
    # Draw normal distribution curve
    scaled_y = [plot_y + y_val for y_val in y]
    pygame.draw.lines(screen, BLACK, False, list(zip([plot_x + x_val for x_val in x], scaled_y)), 2)
    
    # Draw critical value line
    cv_x = int(plot_x + plot_width/2 + critical_value * 100)
    pygame.draw.line(screen, RED, (cv_x, plot_y), (cv_x, plot_y + plot_height), 2)
    
    # Draw test statistic line
    ts_x = int(plot_x + plot_width/2 + test_statistic * 100)
    pygame.draw.line(screen, GREEN, (ts_x, plot_y), (ts_x, plot_y + plot_height), 2)
    
    # Shade rejection region (constrained within the plot)
    rejection_points = [(max(cv_x, plot_x), plot_y + plot_height)]
    for x, y in zip(x[cv_x-plot_x:], scaled_y[cv_x-plot_x:]):
        if plot_x <= x + plot_x <= plot_x + plot_width:
            rejection_points.append((x + plot_x, max(y, plot_y)))
    rejection_points.append((plot_x + plot_width, plot_y + plot_height))
    
    if len(rejection_points) > 2:
        pygame.draw.polygon(screen, (*RED, 64), rejection_points)


def generate_sample():
    return random.choices([0, 1], k=sample_size, weights=[1-alternative_hypothesis, alternative_hypothesis])

def calculate_test_statistic(sample):
    sample_mean = sum(sample) / len(sample)
    standard_error = math.sqrt(null_hypothesis * (1 - null_hypothesis) / sample_size)
    return (sample_mean - null_hypothesis) / standard_error

def calculate_p_value(test_statistic):
    return 1 - stats.norm.cdf(test_statistic)

# Initialize test_statistic and p_value
sample = generate_sample()
test_statistic = calculate_test_statistic(sample)
p_value = calculate_p_value(test_statistic)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == MENU:
                game_state = PLAYING
                score = 0
                level = 1
                time_left = 60
                last_time = pygame.time.get_ticks()
                sample = generate_sample()
                test_statistic = calculate_test_statistic(sample)
                p_value = calculate_p_value(test_statistic)
            elif game_state == PLAYING:
                if reject_button.is_clicked(event.pos) or fail_to_reject_button.is_clicked(event.pos):
                    correct_decision = (test_statistic > critical_value and reject_button.is_clicked(event.pos)) or \
                                       (test_statistic <= critical_value and fail_to_reject_button.is_clicked(event.pos))
                    if correct_decision:
                        score += 1
                    level += 1
                    sample = generate_sample()
                    test_statistic = calculate_test_statistic(sample)
                    p_value = calculate_p_value(test_statistic)
            elif game_state == GAME_OVER:
                game_state = MENU

    screen.fill(LIGHT_BLUE)

    if game_state == MENU:
        # Draw a game-like background
        for i in range(0, WIDTH, 50):
            for j in range(0, HEIGHT, 50):
                pygame.draw.rect(screen, GRAY, (i, j, 25, 25))
        
        title = FONT_LARGE.render("Hypothesis Testing Adventure", True, BLUE)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(title, title_rect)
        
        instructions = FONT_MEDIUM.render("Click anywhere to start", True, BLACK)
        instructions_rect = instructions.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(instructions, instructions_rect)

    elif game_state == PLAYING:
        # Update time
        current_time = pygame.time.get_ticks()
        time_left -= (current_time - last_time) / 1000
        last_time = current_time

        if time_left <= 0:
            game_state = GAME_OVER

        # Draw normal distribution
        draw_normal_distribution(0, 1, critical_value, test_statistic)

        # Draw buttons
        reject_button.draw(screen)
        fail_to_reject_button.draw(screen)

        # Draw game info
        pygame.draw.rect(screen, WHITE, (10, 10, 200, 100))
        pygame.draw.rect(screen, BLACK, (10, 10, 200, 100), 2)
        level_text = FONT_MEDIUM.render(f"Level: {level}", True, BLACK)
        screen.blit(level_text, (20, 20))
        score_text = FONT_MEDIUM.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (20, 50))
        time_text = FONT_MEDIUM.render(f"Time: {int(time_left)}s", True, BLACK)
        screen.blit(time_text, (20, 80))

        # Draw statistics
        pygame.draw.rect(screen, WHITE, (WIDTH - 410, 10, 400, 130))
        pygame.draw.rect(screen, BLACK, (WIDTH - 410, 10, 400, 130), 2)
        stats_text = FONT_SMALL.render(f"H₀: p = {null_hypothesis:.2f}, Hₐ: p > {null_hypothesis:.2f}", True, BLACK)
        screen.blit(stats_text, (WIDTH - 400, 20))
        sample_text = FONT_SMALL.render(f"Sample Size: {sample_size}", True, BLACK)
        screen.blit(sample_text, (WIDTH - 400, 45))
        alpha_text = FONT_SMALL.render(f"Significance Level (α): {significance_level:.2f}", True, BLACK)
        screen.blit(alpha_text, (WIDTH - 400, 70))
        cv_text = FONT_SMALL.render(f"Critical Value: {critical_value:.2f}", True, RED)
        screen.blit(cv_text, (WIDTH - 400, 95))
        ts_text = FONT_SMALL.render(f"Test Statistic: {test_statistic:.2f}", True, GREEN)
        screen.blit(ts_text, (WIDTH - 400, 120))

        # Draw p-value
        p_value_text = FONT_MEDIUM.render(f"p-value: {p_value:.4f}", True, BLUE)
        p_value_rect = p_value_text.get_rect(center=(WIDTH // 2, HEIGHT - 150))
        screen.blit(p_value_text, p_value_rect)

    elif game_state == GAME_OVER:
        # Draw a game-like background
        for i in range(0, WIDTH, 50):
            for j in range(0, HEIGHT, 50):
                pygame.draw.rect(screen, GRAY, (i, j, 25, 25))
        
        game_over_text = FONT_LARGE.render("Game Over", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(game_over_text, game_over_rect)

        final_score_text = FONT_MEDIUM.render(f"Final Score: {score}", True, BLACK)
        final_score_rect = final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(final_score_text, final_score_rect)

        restart_text = FONT_MEDIUM.render("Click anywhere to restart", True, BLACK)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, 2 * HEIGHT // 3))
        screen.blit(restart_text, restart_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()