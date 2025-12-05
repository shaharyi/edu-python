import pygame
import random
import sys

# ---------- Linked List Node ----------

class Node:
    def __init__(self, value, next=None):
        self.value = value  # (x, y) position in grid
        self.next = next    # next Node in the snake body


# ---------- Snake Class Using Linked List ----------

class Snake:
    def __init__(self, start_pos):
        # Start with a single-segment snake
        self.head = Node(start_pos)
        self.grow_segments = 0  # how many segments left to grow

    def get_head_pos(self):
        return self.head.value

    def contains(self, pos):
        """Check if any segment has the given position."""
        current = self.head
        while current is not None:
            if current.value == pos:
                return True
            current = current.next
        return False

    def get_positions(self):
        """Return a list of all segment positions (for drawing)."""
        positions = []
        current = self.head
        while current is not None:
            positions.append(current.value)
            current = current.next
        return positions

    def length(self):
        """Optional helper for debugging/understanding."""
        count = 0
        current = self.head
        while current is not None:
            count += 1
            current = current.next
        return count

    def move_to(self, new_head_pos, grow=False):
        """
        Move snake so that:
        - new_head_pos becomes the new head position
        - if grow is False: remove tail (same length)
        - if grow is True: keep tail (length + 1)
        """
        # Add new head node in front of current head
        new_head = Node(new_head_pos, self.head)
        self.head = new_head

        if grow:
            return  # don't remove tail

        # Remove tail from singly linked list
        # We must stop at the node *before* the tail
        # Edge case: if only one node, do nothing (but this won't happen
        #            right after adding a new head; length >= 2 here).
        current = self.head
        if current.next is None:
            # length == 1, nothing to remove
            return

        while current.next.next is not None:
            current = current.next

        # current.next is the tail, cut it off
        current.next = None


# ---------- Game Setup ----------

pygame.init()

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20

WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake with Linked List (value, next)")

clock = pygame.time.Clock()
FONT = pygame.font.SysFont("consolas", 24)

# Colors (R, G, B)
COLOR_BG = (0, 0, 0)
COLOR_SNAKE = (0, 200, 0)
COLOR_FOOD = (200, 0, 0)
COLOR_TEXT = (255, 255, 255)


def random_food_position(snake):
    """Return a random position not occupied by the snake."""
    while True:
        pos = (random.randrange(0, GRID_WIDTH),
               random.randrange(0, GRID_HEIGHT))
        if not snake.contains(pos):
            return pos


def draw_cell(pos, color):
    x, y = pos
    pygame.draw.rect(
        screen,
        color,
        (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    )


def main():
    def reset():
        start_pos = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        snake = Snake(start_pos)
        direction = (1, 0)
        food_pos = random_food_position(snake)
        score = 0
        return snake, direction, food_pos, score

    snake, direction, food_pos, score = reset()

    running = True
    game_over = False

    while running:
        clock.tick(10)

        # ---------- Handle Events ----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if game_over:
                    # ------ NEW FEATURE ------
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:
                        # Restart the entire game
                        snake, direction, food_pos, score = reset()
                        game_over = False
                    continue

                # ----- Movement -----
                dx, dy = direction
                if event.key == pygame.K_UP:
                    if dy != 1:
                        direction = (0, -1)
                elif event.key == pygame.K_DOWN:
                    if dy != -1:
                        direction = (0, 1)
                elif event.key == pygame.K_LEFT:
                    if dx != 1:
                        direction = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    if dx != -1:
                        direction = (1, 0)

        # ---------- Drawing Game Over ----------
        if game_over:
            screen.fill(COLOR_BG)
            game_over_text = FONT.render("Game Over!", True, COLOR_TEXT)
            score_text = FONT.render(f"Score: {score}", True, COLOR_TEXT)
            hint_text = FONT.render("Press R to Restart | ESC to Quit", True, COLOR_TEXT)

            screen.blit(game_over_text,
                        (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 60))
            screen.blit(score_text,
                        (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 20))
            screen.blit(hint_text,
                        (WIDTH // 2 - hint_text.get_width() // 2, HEIGHT // 2 + 20))

            pygame.display.flip()
            continue

        # ---------- Game Logic ----------
        head_x, head_y = snake.get_head_pos()
        dx, dy = direction
        new_head_pos = (head_x + dx, head_y + dy)

        # Wall or self collision
        x, y = new_head_pos
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT or snake.contains(new_head_pos):
            game_over = True
        else:
            ate_food = (new_head_pos == food_pos)
            snake.move_to(new_head_pos, grow=ate_food)

            if ate_food:
                score += 1
                food_pos = random_food_position(snake)

        # ---------- Drawing ----------
        screen.fill(COLOR_BG)

        # Food
        draw_cell(food_pos, COLOR_FOOD)

        # Snake
        for pos in snake.get_positions():
            draw_cell(pos, COLOR_SNAKE)

        # Draw score
        score_surf = FONT.render(f"Score: {score}", True, COLOR_TEXT)
        screen.blit(score_surf, (10, 10))
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

