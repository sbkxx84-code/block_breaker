import pygame
import sys
import random

# Window settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (232, 76, 61)
GREEN = (84, 153, 199)
BLUE = (52, 152, 219)
YELLOW = (241, 196, 15)
PURPLE = (155, 89, 182)

# Paddle settings
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_SPEED = 7

# Ball settings
BALL_RADIUS = 10
BALL_SPEED = 5

# Brick settings
BRICK_ROWS = 5
BRICK_COLUMNS = 10
BRICK_WIDTH = 70
BRICK_HEIGHT = 25
BRICK_MARGIN = 10
BRICK_TOP_OFFSET = 60


def create_bricks():
    bricks = []
    colors = [RED, GREEN, BLUE, YELLOW, PURPLE]
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLUMNS):
            x = BRICK_MARGIN + col * (BRICK_WIDTH + BRICK_MARGIN)
            y = BRICK_TOP_OFFSET + row * (BRICK_HEIGHT + BRICK_MARGIN)
            rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
            bricks.append((rect, colors[row % len(colors)]))
    return bricks


def draw_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ブロック崩し")
    clock = pygame.time.Clock()

    paddle = pygame.Rect((SCREEN_WIDTH - PADDLE_WIDTH) // 2,
                         SCREEN_HEIGHT - 50,
                         PADDLE_WIDTH,
                         PADDLE_HEIGHT)

    ball = pygame.Rect(
        SCREEN_WIDTH // 2 - BALL_RADIUS,
        SCREEN_HEIGHT // 2 - BALL_RADIUS,
        BALL_RADIUS * 2,
        BALL_RADIUS * 2,
    )
    ball_vel = [BALL_SPEED * random.choice([-1, 1]), -BALL_SPEED]

    bricks = create_bricks()
    score = 0
    running = True
    game_over = False
    win = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            paddle.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            paddle.x += PADDLE_SPEED

        paddle.x = max(0, min(SCREEN_WIDTH - PADDLE_WIDTH, paddle.x))

        if not game_over and not win:
            ball.x += ball_vel[0]
            ball.y += ball_vel[1]

            if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
                ball_vel[0] = -ball_vel[0]
            if ball.top <= 0:
                ball_vel[1] = -ball_vel[1]

            if ball.colliderect(paddle) and ball_vel[1] > 0:
                ball_vel[1] = -BALL_SPEED
                offset = (ball.centerx - paddle.centerx) / (PADDLE_WIDTH / 2)
                ball_vel[0] = BALL_SPEED * offset

            hit_index = ball.collidelist([brick[0] for brick in bricks])
            if hit_index != -1:
                hit_brick, _ = bricks.pop(hit_index)
                score += 100

                if abs(ball.bottom - hit_brick.top) < BALL_SPEED and ball_vel[1] > 0:
                    ball_vel[1] = -ball_vel[1]
                elif abs(ball.top - hit_brick.bottom) < BALL_SPEED and ball_vel[1] < 0:
                    ball_vel[1] = -ball_vel[1]
                else:
                    ball_vel[0] = -ball_vel[0]

            if ball.bottom >= SCREEN_HEIGHT:
                game_over = True

            if not bricks:
                win = True

        screen.fill(BLACK)

        pygame.draw.rect(screen, WHITE, paddle)
        pygame.draw.ellipse(screen, YELLOW, ball)

        for rect, color in bricks:
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)

        draw_text(screen, f"スコア: {score}", 30, 20, 10)

        if game_over:
            draw_text(screen, "ゲームオーバー", 60, SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 - 30, RED)
            draw_text(screen, "Rキーで再挑戦", 30, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40, WHITE)
            if keys[pygame.K_r]:
                bricks = create_bricks()
                score = 0
                ball.x = SCREEN_WIDTH // 2 - BALL_RADIUS
                ball.y = SCREEN_HEIGHT // 2 - BALL_RADIUS
                ball_vel = [BALL_SPEED * random.choice([-1, 1]), -BALL_SPEED]
                game_over = False

        if win:
            draw_text(screen, "完全クリア！", 60, SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 - 30, GREEN)
            draw_text(screen, "Rキーで再挑戦", 30, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40, WHITE)
            if keys[pygame.K_r]:
                bricks = create_bricks()
                score = 0
                ball.x = SCREEN_WIDTH // 2 - BALL_RADIUS
                ball.y = SCREEN_HEIGHT // 2 - BALL_RADIUS
                ball_vel = [BALL_SPEED * random.choice([-1, 1]), -BALL_SPEED]
                win = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
