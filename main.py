import pygame
import sys
from game import run_game  # game.py의 run_game 함수 임포트

# Pygame 초기화
pygame.init()

# 화면 크기 및 설정
resolutions = [(800, 600), (1280, 720), (1920, 1080)]
current_resolution_index = 0
screen_width, screen_height = resolutions[current_resolution_index]
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cross game")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 102, 255)
RED = (255, 0, 0)

# 글꼴 설정
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

# 상태 변수
current_index = 0

def create_buttons():
    global start_buttons, start_button_texts, how_to_play_buttons, how_to_play_button_texts, next_button, prev_button, exit_button, next_button_text, prev_button_text, exit_button_text, mode_buttons, mode_button_texts, map_buttons, map_button_texts, end_buttons, end_button_texts

    # 버튼 텍스트와 위치 정의
    start_buttons = {
        "Start": pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 100, 200, 60),
        "How to Play": pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 60),
        "Option": pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 100, 200, 60)
    }
    start_button_texts = {
        "Start": button_font.render("Start", True, WHITE),
        "How to Play": button_font.render("How to Play", True, WHITE),
        "Option": button_font.render("Option", True, WHITE)
    }

    # 버튼 설정
    how_to_play_buttons = {
        "Next": pygame.Rect(screen_width - 150, screen_height - 100, 100, 50),
        "Prev": pygame.Rect(50, screen_height - 100, 100, 50),
        "Exit": pygame.Rect(screen_width // 2 - 50, screen_height - 100, 100, 50)
    }
    how_to_play_button_texts = {
        "Next": button_font.render("Next", True, WHITE),
        "Prev": button_font.render("Prev", True, WHITE),
        "Exit": button_font.render("Exit", True, WHITE)
    }

    # 해상도 옵션 버튼
    next_button = pygame.Rect(screen_width - 150, screen_height - 100, 100, 50)
    prev_button = pygame.Rect(50, screen_height - 100, 100, 50)
    exit_button = pygame.Rect(screen_width // 2 - 50, screen_height - 100, 100, 50)
    next_button_text = button_font.render("Next", True, WHITE)
    prev_button_text = button_font.render("Prev", True, WHITE)
    exit_button_text = button_font.render("Exit", True, WHITE)

    # 게임 모드 및 맵 선택 버튼
    mode_buttons = {
        "PvP": pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 100, 200, 60),
        "PvE": pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 60)
    }
    mode_button_texts = {
        "PvP": button_font.render("PvP", True, WHITE),
        "PvE": button_font.render("PvE", True, WHITE)
    }

    map_buttons = {
        "Map 1": pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 100, 200, 60),
        "Map 2": pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 60),
        "Map 3": pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 100, 200, 60)
    }
    map_button_texts = {
        "Map 1": button_font.render("Map 1", True, WHITE),
        "Map 2": button_font.render("Map 2", True, WHITE),
        "Map 3": button_font.render("Map 3", True, WHITE)
    }

    # 엔딩 화면 버튼
    end_buttons = {
        "Retry": pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 60),
        "Title": pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 100, 200, 60)
    }
    end_button_texts = {
        "Retry": button_font.render("Retry", True, WHITE),
        "Title": button_font.render("Title", True, WHITE)
    }

create_buttons()

# 메인 루프
def title_screen():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 창 닫기 이벤트
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button_name, rect in start_buttons.items():
                    if rect.collidepoint(event.pos):  # 버튼 클릭 확인
                        if button_name == "Start":
                            return "start"  # 게임 모드 선택 화면 전환
                        elif button_name == "How to Play":
                            return "how_to_play"  # 설명 화면 전환
                        elif button_name == "Option":
                            return "option"  # 옵션 화면 전환

        # 화면 채우기
        screen.fill(BLACK)

        # 제목 표시
        title_text = font.render("Cross game", True, WHITE)
        screen.blit(title_text, title_text.get_rect(center=(screen_width // 2, 150)))

        # 버튼 그리기
        for button_name, rect in start_buttons.items():
            pygame.draw.rect(screen, BLUE, rect, width=3)  # 버튼 그리기
            screen.blit(start_button_texts[button_name], start_button_texts[button_name].get_rect(center=rect.center))

        # 화면 업데이트
        pygame.display.flip()

# 게임 설명 화면
def how_to_play_screen():
    instructions = [
        [
            "Game Objective:",
            "Defeat opponent by reducing their HP to 0.",
            "Collect power-ups to increase your attack range.",
            "Avoid obstacles and strategically attack your opponent."
        ],
        [
            "Controls:",
            "Player 1 (Blue):",
            "  - Move: W, A, S, D",
            "  - Attack: F",
            "Player 2 (Red) in PvP mode:",
            "  - Move: Arrow Keys",
            "  - Attack: Numpad 0",
            "Player 2 (Red) in PvE mode:",
            "  - Controlled by AI"
        ],
        [
            "Power-ups and Gimmicks:",
            "Power-ups:",
            "  - Green squares that increase your attack range.",
            "Obstacles:",
            "  - Black squares that block movement and attacks.",
            "Strategy:",
            "  - Use obstacles to your advantage.",
            "  - Collect power-ups to gain an edge over your opponent."
        ]
    ]
    current_index = 0
    running = True

    # 화면 크기에 비례하는 폰트 크기 계산
    base_font_size = 30  # 글자 크기 증가
    font_size = int(base_font_size * (screen_width / 800))
    dynamic_font = pygame.font.Font(None, font_size)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 창 닫기 이벤트
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if how_to_play_buttons["Next"].collidepoint(event.pos) and current_index < len(instructions) - 1:
                    current_index += 1
                elif how_to_play_buttons["Prev"].collidepoint(event.pos) and current_index > 0:
                    current_index -= 1
                elif how_to_play_buttons["Exit"].collidepoint(event.pos):
                    running = False

        # 화면 채우기
        screen.fill(BLACK)

        # 텍스트 표시
        for i, line in enumerate(instructions[current_index]):
            instruction_text = dynamic_font.render(line, True, WHITE)
            screen.blit(instruction_text, (50, 50 + i * (font_size + 10)))

        # 버튼 그리기
        if current_index < len(instructions) - 1:
            pygame.draw.rect(screen, BLUE, how_to_play_buttons["Next"], width=3)
            screen.blit(how_to_play_button_texts["Next"], how_to_play_button_texts["Next"].get_rect(center=how_to_play_buttons["Next"].center))

        if current_index > 0:
            pygame.draw.rect(screen, BLUE, how_to_play_buttons["Prev"], width=3)
            screen.blit(how_to_play_button_texts["Prev"], how_to_play_button_texts["Prev"].get_rect(center=how_to_play_buttons["Prev"].center))

        pygame.draw.rect(screen, RED, how_to_play_buttons["Exit"], width=3)
        screen.blit(how_to_play_button_texts["Exit"], how_to_play_button_texts["Exit"].get_rect(center=how_to_play_buttons["Exit"].center))

        # 화면 업데이트
        pygame.display.flip()

def option_screen():
    global screen_width, screen_height, screen, current_resolution_index
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 창 닫기 이벤트
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if next_button.collidepoint(event.pos):
                    current_resolution_index = (current_resolution_index + 1) % len(resolutions)
                    screen_width, screen_height = resolutions[current_resolution_index]
                    screen = pygame.display.set_mode((screen_width, screen_height))
                    create_buttons()  # 버튼 위치 및 크기 업데이트
                elif prev_button.collidepoint(event.pos):
                    current_resolution_index = (current_resolution_index - 1) % len(resolutions)
                    screen_width, screen_height = resolutions[current_resolution_index]
                    screen = pygame.display.set_mode((screen_width, screen_height))
                    create_buttons()  # 버튼 위치 및 크기 업데이트
                elif exit_button.collidepoint(event.pos):
                    running = False

        # 화면 채우기
        screen.fill(BLACK)

        # 해상도 표시
        resolution_text = button_font.render(f"Resolution: {screen_width}x{screen_height}", True, WHITE)
        screen.blit(resolution_text, resolution_text.get_rect(center=(screen_width // 2, 150)))

        # 버튼 그리기
        pygame.draw.rect(screen, BLUE, next_button, width=3)
        screen.blit(next_button_text, next_button_text.get_rect(center=next_button.center))

        pygame.draw.rect(screen, BLUE, prev_button, width=3)
        screen.blit(prev_button_text, prev_button_text.get_rect(center=prev_button.center))

        pygame.draw.rect(screen, RED, exit_button, width=3)
        screen.blit(exit_button_text, exit_button_text.get_rect(center=exit_button.center))

        # 화면 업데이트
        pygame.display.flip()

def mode_selection_screen():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 창 닫기 이벤트
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button_name, rect in mode_buttons.items():
                    if rect.collidepoint(event.pos):  # 버튼 클릭 확인
                        print(f"{button_name} mode selected!")  # 디버그용
                        return button_name  # 게임 모드 선택

        # 화면 채우기
        screen.fill(BLACK)

        # 제목 표시
        mode_text = font.render("Select Game Mode", True, WHITE)
        screen.blit(mode_text, mode_text.get_rect(center=(screen_width // 2, 150)))

        # 버튼 그리기 (테두리만)
        for button_name, rect in mode_buttons.items():
            pygame.draw.rect(screen, BLUE, rect, width=3)  # 버튼 테두리만 그리기
            screen.blit(mode_button_texts[button_name], mode_button_texts[button_name].get_rect(center=rect.center))

        # 화면 업데이트
        pygame.display.flip()

def map_selection_screen():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 창 닫기 이벤트
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button_name, rect in map_buttons.items():
                    if rect.collidepoint(event.pos):  # 버튼 클릭 확인
                        print(f"{button_name} selected!")  # 디버그용
                        return button_name  # 맵 선택

        # 화면 채우기
        screen.fill(BLACK)

        # 제목 표시
        map_text = font.render("Select Map", True, WHITE)
        screen.blit(map_text, map_text.get_rect(center=(screen_width // 2, 150)))

        # 버튼 그리기 (테두리만)
        for button_name, rect in map_buttons.items():
            pygame.draw.rect(screen, BLUE, rect, width=3)  # 버튼 테두리만 그리기
            screen.blit(map_button_texts[button_name], map_button_texts[button_name].get_rect(center=rect.center))

        # 화면 업데이트
        pygame.display.flip()

def end_screen(winner):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 창 닫기 이벤트
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button_name, rect in end_buttons.items():
                    if rect.collidepoint(event.pos):  # 버튼 클릭 확인
                        print(f"{button_name} button clicked!")  # 디버그용
                        running = False
                        return button_name.lower()  # "retry" 또는 "title" 반환

        # 화면 채우기
        screen.fill(BLACK)

        # 승리자 표시
        winner_text = font.render(f"{winner} Wins!", True, WHITE)
        screen.blit(winner_text, winner_text.get_rect(center=(screen_width // 2, 150)))

        # 버튼 그리기
        for button_name, rect in end_buttons.items():
            pygame.draw.rect(screen, BLUE, rect, width=3)  # 버튼 그리기
            screen.blit(end_button_texts[button_name], end_button_texts[button_name].get_rect(center=rect.center))

        # 화면 업데이트
        pygame.display.flip()

# 메인 루프
if __name__ == "__main__":
    create_buttons()

    while True:
        result = title_screen()
        if result == "start":
            print("Starting the game...")
            mode = mode_selection_screen()
            if mode:
                selected_map = map_selection_screen()
                if selected_map:
                    while True:
                        winner = run_game(selected_map, screen_width, screen_height, mode)  # 게임 실행
                        end_result = end_screen(winner)
                        if end_result == "retry":
                            continue
                        elif end_result == "title":
                            break
            continue  # 타이틀 화면으로 돌아가기 위해 루프 계속
        elif result == "how_to_play":
            how_to_play_screen()
        elif result == "option":
            option_screen()

