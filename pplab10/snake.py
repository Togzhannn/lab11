import pygame 
import random
from color import *
from database import *  # Импортируем все, включая get_user и create_user

pygame.init()
init_db()  # Инициализация базы данных и создание таблиц

username = input("User name: ")
user = get_user(username)  # Получаем пользователя по имени

if not user:
    user_id = create_user(username)  # Создаем нового пользователя, если его нет
else:
    user_id = user[0]  # Получаем ID пользователя из базы

progress = get_user_progress(user_id)  # Получаем прогресс (счёт, уровень) пользователя

WIDTH = 600
HEIGHT = 600
CELL = 30  
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Инициализация экрана
pygame.display.set_caption("Snake Game")
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)

def draw_grid():
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx, self.dy = 1, 0 
        self.score = 0
        self.level = 1

    def move(self):
        head = self.body[0]
        new_head = Point(head.x + self.dx, head.y + self.dy)
        if new_head.x < 0 or new_head.x >= WIDTH // CELL or new_head.y < 0 or new_head.y >= HEIGHT // CELL:
            return False
        if new_head in self.body:
            return False
        self.body.insert(0, new_head)
        self.body.pop()
        return True

    def draw(self):
        for i, segment in enumerate(self.body):
            color = colorRED if i == 0 else colorYELLOW
            pygame.draw.rect(screen, color, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_collision(self, food):
        if self.body[0] == food.pos:
            self.body.append(Point(self.body[-1].x, self.body[-1].y))  
            self.score += 1
            if self.score % 3 == 0:
                self.level += 1
            food.generate_random_pos(self)
            return True
        return False

class Food:
    def __init__(self):
        self.pos = Point(0, 0)
        self.generate_random_pos(None)  

    def generate_random_pos(self, snake):
        while True:
            x = random.randint(0, WIDTH // CELL - 1)
            y = random.randint(0, HEIGHT // CELL - 1)
            new_pos = Point(x, y)
            if snake is None or new_pos not in snake.body:
                self.pos = new_pos
                break

    def draw(self):
        pygame.draw.rect(screen, colorGREEN, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

snake = Snake()
if progress:
    snake.score, snake.level = progress
    print(f"Прогресс загружен: Счёт = {snake.score}, Уровень = {snake.level}")
else:
    print("Новый пользователь. Удачи!")
print("Загрузка прогресса завершена!")

food = Food()
FPS = 4  
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(colorBLACK)
    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake.dx == 0:
                snake.dx, snake.dy = 1, 0
            elif event.key == pygame.K_LEFT and snake.dx == 0:
                snake.dx, snake.dy = -1, 0
            elif event.key == pygame.K_DOWN and snake.dy == 0:
                snake.dx, snake.dy = 0, 1
            elif event.key == pygame.K_UP and snake.dy == 0:
                snake.dx, snake.dy = 0, -1         
            elif event.key == pygame.K_p:
                save_progress(user_id, snake.score, snake.level)
                paused = True
                while paused:
                    for pause_event in pygame.event.get():
                        if pause_event.type == pygame.KEYDOWN and pause_event.key == pygame.K_p:
                            paused = False      

    if not snake.move():
        running = False  

    snake.check_collision(food)
    snake.draw()
    food.draw()

    score_text = font.render(f"Score: {snake.score}", True, colorWHITE)
    level_text = font.render(f"Level: {snake.level}", True, colorWHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    pygame.display.flip()
    clock.tick(FPS + snake.level)  

# Сохранение перед выходом
save_progress(user_id, snake.score, snake.level)

# Конец игры
screen.fill(colorBLACK)
game_over_text = game_over_font.render("GAME OVER", True, colorRED)
text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
screen.blit(game_over_text, text_rect)

final_score_text = font.render(f"Final Score: {snake.score}", True, colorWHITE)
score_rect = final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
screen.blit(final_score_text, score_rect)

final_level_text = font.render(f"Final Level: {snake.level}", True, colorWHITE)
level_rect = final_level_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
screen.blit(final_level_text, level_rect)

pygame.display.flip()
clock.tick(FPS + snake.level)
pygame.time.delay(3000) 
pygame.quit()
