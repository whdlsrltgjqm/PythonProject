import pygame
import sys
import random

# Pygame 초기화
pygame.init()

# 화면 크기 설정
GRID_SIZE = 9
CELL_SIZE = 60  # 기본 셀 크기
SCREEN_WIDTH = CELL_SIZE * GRID_SIZE
SCREEN_HEIGHT = CELL_SIZE * GRID_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("9x9 Grid Game")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# FPS 설정
clock = pygame.time.Clock()
FPS = 30

# 맵 정의
maps = {
    "Map 1": [
        "000000000",
        "011000110",
        "010000010",
        "000101000",
        "000000000",
        "000101000",
        "010000010",
        "011000110",
        "000000000"
    ],
    "Map 2": [
        "000000000",
        "011111110",
        "000000000",
        "011111110",
        "000000000",
        "011111110",
        "000000000",
        "011111110",
        "000000000"
    ],
    "Map 3": [
        "000000000",
        "000010000",
        "000010000",
        "000010000",
        "011111110",
        "000010000",
        "000010000",
        "000010000",
        "000000000"
    ]
}

# 플레이어 초기화
player1 = {"x": random.randint(0, GRID_SIZE - 1), "y": random.randint(0, GRID_SIZE - 1), "hp": 3, "range": 1, "powerups": 0, "attack_cooldown": 0, "hit_effect": 0, "attack_effect": []}
player2 = {"x": random.randint(0, GRID_SIZE - 1), "y": random.randint(0, GRID_SIZE - 1), "hp": 3, "range": 1, "powerups": 0, "attack_cooldown": 0, "hit_effect": 0, "attack_effect": []}

# 파워업 및 장애물
obstacles = []
powerups = []

def create_map(selected_map):
    global obstacles, powerups
    obstacles = []
    powerups = []
    for y, row in enumerate(maps[selected_map]):
        for x, cell in enumerate(row):
            if cell == "1":
                obstacles.append((x, y))
            elif cell == "0" and random.random() < 0.05:  # 5% 확률로 파워업 생성
                powerups.append((x, y))

def draw_grid(offset_x, offset_y):
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)

def draw_players(offset_x, offset_y):
    if player1["hit_effect"] > 0:
        pygame.draw.rect(screen, YELLOW, (offset_x + player1["x"] * CELL_SIZE, offset_y + player1["y"] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    else:
        pygame.draw.rect(screen, BLUE, (offset_x + player1["x"] * CELL_SIZE, offset_y + player1["y"] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    if player2["hit_effect"] > 0:
        pygame.draw.rect(screen, YELLOW, (offset_x + player2["x"] * CELL_SIZE, offset_y + player2["y"] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    else:
        pygame.draw.rect(screen, RED, (offset_x + player2["x"] * CELL_SIZE, offset_y + player2["y"] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_obstacles(offset_x, offset_y):
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLACK, (offset_x + obstacle[0] * CELL_SIZE, offset_y + obstacle[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_powerups(offset_x, offset_y):
    for powerup in powerups:
        pygame.draw.rect(screen, GREEN, (offset_x + powerup[0] * CELL_SIZE, offset_y + powerup[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_hp():
    pygame.draw.rect(screen, WHITE, (10, SCREEN_HEIGHT - 40, 200, 20))
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - 210, SCREEN_HEIGHT - 40, 200, 20))

    pygame.draw.rect(screen, BLUE, (10, SCREEN_HEIGHT - 40, player1["hp"] * 66, 20))
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH - 210, SCREEN_HEIGHT - 40, player2["hp"] * 66, 20))

def draw_powerup_count():
    powerup_text1 = pygame.font.Font(None, 36).render(f"Powerups: {player1['powerups']}", True, BLUE)
    powerup_text2 = pygame.font.Font(None, 36).render(f"Powerups: {player2['powerups']}", True, RED)
    screen.blit(powerup_text1, (10, SCREEN_HEIGHT - 80))
    screen.blit(powerup_text2, (SCREEN_WIDTH - 210, SCREEN_HEIGHT - 80))

def draw_cooldown():
    cooldown_text1 = pygame.font.Font(None, 36).render(f"Cooldown: {player1['attack_cooldown'] / FPS:.2f}", True, BLUE)
    cooldown_text2 = pygame.font.Font(None, 36).render(f"Cooldown: {player2['attack_cooldown'] / FPS:.2f}", True, RED)
    screen.blit(cooldown_text1, (10, SCREEN_HEIGHT - 120))
    screen.blit(cooldown_text2, (SCREEN_WIDTH - 210, SCREEN_HEIGHT - 120))

def move_player(player, keys, key_pressed, up, down, left, right):
    if keys[up] and not key_pressed[up] and player["y"] > 0 and (player["x"], player["y"] - 1) not in obstacles:
        player["y"] -= 1
        key_pressed[up] = True
    elif keys[down] and not key_pressed[down] and player["y"] < GRID_SIZE - 1 and (player["x"], player["y"] + 1) not in obstacles:
        player["y"] += 1
        key_pressed[down] = True
    elif keys[left] and not key_pressed[left] and player["x"] > 0 and (player["x"] - 1, player["y"]) not in obstacles:
        player["x"] -= 1
        key_pressed[left] = True
    elif keys[right] and not key_pressed[right] and player["x"] < GRID_SIZE - 1 and (player["x"] + 1, player["y"]) not in obstacles:
        player["x"] += 1
        key_pressed[right] = True

def attack(player, target, keys, key_pressed, attack_key):
    if keys[attack_key] and not key_pressed[attack_key] and player["attack_cooldown"] == 0:
        effect_positions = []
        for i in range(1, player["range"] + 1):
            if player["y"] - i >= 0 and (player["x"], player["y"] - i) not in obstacles:
                effect_positions.append((player["x"], player["y"] - i))
            else:
                break
        for i in range(1, player["range"] + 1):
            if player["y"] + i < GRID_SIZE and (player["x"], player["y"] + i) not in obstacles:
                effect_positions.append((player["x"], player["y"] + i))
            else:
                break
        for i in range(1, player["range"] + 1):
            if player["x"] - i >= 0 and (player["x"] - i, player["y"]) not in obstacles:
                effect_positions.append((player["x"] - i, player["y"]))
            else:
                break
        for i in range(1, player["range"] + 1):
            if player["x"] + i < GRID_SIZE and (player["x"] + i, player["y"]) not in obstacles:
                effect_positions.append((player["x"] + i, player["y"]))
            else:
                break

        player["attack_effect"] = effect_positions

        for pos in effect_positions:
            if pos == (target["x"], target["y"]):
                target["hp"] -= 1
                target["hit_effect"] = FPS  # 피격 모션 잔존 기간 설정

        player["attack_cooldown"] = FPS * 2  # 쿨타임 설정

        key_pressed[attack_key] = True

# 파워업 효과: 공격 범위 증가
def check_powerups(player):
    if (player["x"], player["y"]) in powerups:
        player["range"] += 1
        player["powerups"] += 1
        powerups.remove((player["x"], player["y"]))

# 게임 종료 조건 확인
def check_game_over():
    if player1["hp"] <= 0:
        return "Player 2"
    if player2["hp"] <= 0:
        return "Player 1"
    return None

# 게임 종료 화면
def draw_end_screen(winner):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render(winner, True, WHITE)
    screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)))

    button_font = pygame.font.Font(None, 50)
    retry_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 60)
    title_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 60)
    retry_text = button_font.render("Retry", True, WHITE)
    title_text = button_font.render("Title", True, WHITE)

    pygame.draw.rect(screen, BLUE, retry_button, width=3)
    screen.blit(retry_text, retry_text.get_rect(center=retry_button.center))

    pygame.draw.rect(screen, BLUE, title_button, width=3)
    screen.blit(title_text, title_text.get_rect(center=title_button.center))

    pygame.display.flip()

    return retry_button, title_button

# 게임 실행
def run_game(selected_map, screen_width, screen_height, mode):
    global screen, CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, player1, player2
    SCREEN_WIDTH = screen_width
    SCREEN_HEIGHT = screen_height
    CELL_SIZE = min(SCREEN_WIDTH // GRID_SIZE, SCREEN_HEIGHT // GRID_SIZE)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    create_map(selected_map)
    
    offset_x = (SCREEN_WIDTH - GRID_SIZE * CELL_SIZE) // 2
    offset_y = (SCREEN_HEIGHT - GRID_SIZE * CELL_SIZE) // 2

    # 플레이어 초기화
    player1 = {"x": random.randint(0, GRID_SIZE - 1), "y": random.randint(0, GRID_SIZE - 1), "hp": 3, "range": 1, "powerups": 0, "attack_cooldown": 0, "hit_effect": 0, "attack_effect": []}
    player2 = {"x": random.randint(0, GRID_SIZE - 1), "y": random.randint(0, GRID_SIZE - 1), "hp": 3, "range": 1, "powerups": 0, "attack_cooldown": 0, "hit_effect": 0, "attack_effect": []}

    # 키 입력 상태 초기화
    key_pressed = {key: False for key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_f, pygame.K_KP0]}
    
    # AI 쿨다운 초기화
    ai_move_cooldown = 0
    ai_attack_cooldown = 0

    # 메인 게임 루프
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key in key_pressed:
                    key_pressed[event.key] = False

        keys = pygame.key.get_pressed()

        # 플레이어 이동 및 공격
        move_player(player1, keys, key_pressed, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)
        
        if mode == "PvP":
            move_player(player2, keys, key_pressed, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
            attack(player2, player1, keys, key_pressed, pygame.K_KP0)
        elif mode == "PvE":
            if ai_move_cooldown == 0:
                ai_move_player(player2)
                ai_move_cooldown = FPS  # 1초 대기
            if ai_attack_cooldown == 0:
                ai_attack(player2, player1)
                ai_attack_cooldown = FPS * 2  # 2초 대기

        attack(player1, player2, keys, key_pressed, pygame.K_f)

        # 파워업 체크
        check_powerups(player1)
        check_powerups(player2)

        # 공격 쿨타임 및 효과 감소
        if player1["attack_cooldown"] > 0:
            player1["attack_cooldown"] -= 1
        if player2["attack_cooldown"] > 0:
            player2["attack_cooldown"] -= 1

        if player1["hit_effect"] > 0:
            player1["hit_effect"] -= 1
        if player2["hit_effect"] > 0:
            player2["hit_effect"] -= 1

        if ai_move_cooldown > 0:
            ai_move_cooldown -= 1
        if ai_attack_cooldown > 0:
            ai_attack_cooldown -= 1

        # 화면 그리기
        screen.fill(WHITE)
        draw_grid(offset_x, offset_y)
        draw_obstacles(offset_x, offset_y)
        draw_powerups(offset_x, offset_y)

        # 공격 모션 그리기
        for pos in player1["attack_effect"]:
            pygame.draw.rect(screen, ORANGE, (offset_x + pos[0] * CELL_SIZE, offset_y + pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        for pos in player2["attack_effect"]:
            pygame.draw.rect(screen, ORANGE, (offset_x + pos[0] * CELL_SIZE, offset_y + pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        draw_players(offset_x, offset_y)
        draw_hp()
        draw_powerup_count()
        draw_cooldown()

        pygame.display.flip()
        clock.tick(FPS)

        # 공격 모션 초기화
        if player1["attack_cooldown"] <= FPS * 1.5:  # 공격 모션을 더 길게 유지
            player1["attack_effect"] = []
        if player2["attack_cooldown"] <= FPS * 1.5:  # 공격 모션을 더 길게 유지
            player2["attack_effect"] = []

        # 게임 종료 조건 확인
        winner = check_game_over()
        if winner:
            return winner

def ai_move_player(player):
    # 간단한 AI 동작: 플레이어 1을 향해 이동
    if player["x"] < player1["x"] and (player["x"] + 1, player["y"]) not in obstacles:
        player["x"] += 1
    elif player["x"] > player1["x"] and (player["x"] - 1, player["y"]) not in obstacles:
        player["x"] -= 1
    elif player["y"] < player1["y"] and (player["x"], player["y"] + 1) not in obstacles:
        player["y"] += 1
    elif player["y"] > player1["y"] and (player["x"], player["y"] - 1) not in obstacles:
        player["y"] -= 1

def ai_attack(player, target):
    # 간단한 AI 공격: 플레이어 1이 공격 범위 내에 있으면 공격
    if player["attack_cooldown"] == 0:
        effect_positions = []
        for i in range(1, player["range"] + 1):
            if player["y"] - i >= 0 and (player["x"], player["y"] - i) not in obstacles:
                effect_positions.append((player["x"], player["y"] - i))
            else:
                break
        for i in range(1, player["range"] + 1):
            if player["y"] + i < GRID_SIZE and (player["x"], player["y"] + i) not in obstacles:
                effect_positions.append((player["x"], player["y"] + i))
            else:
                break
        for i in range(1, player["range"] + 1):
            if player["x"] - i >= 0 and (player["x"] - i, player["y"]) not in obstacles:
                effect_positions.append((player["x"] - i, player["y"]))
            else:
                break
        for i in range(1, player["range"] + 1):
            if player["x"] + i < GRID_SIZE and (player["x"] + i, player["y"]) not in obstacles:
                effect_positions.append((player["x"] + i, player["y"]))
            else:
                break

        player["attack_effect"] = effect_positions

        for pos in effect_positions:
            if pos == (target["x"], target["y"]):
                target["hp"] -= 1
                target["hit_effect"] = FPS  # 피격 모션 잔존 기간 설정

        player["attack_cooldown"] = FPS * 2  # 쿨타임 설정 (예: 2초)

if __name__ == "__main__":
    selected_map = "Map 1"  # 기본 맵 설정
    while True:
        result = run_game(selected_map, SCREEN_WIDTH, SCREEN_HEIGHT, "PvP")
        if result == "title":
            break
