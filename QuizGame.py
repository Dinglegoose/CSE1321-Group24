import pygame, sys
from pygame.locals import *

# Initializes Pygame
pygame.init()

# Screen settings
resolution = (800, 600)
screen = pygame.display.set_mode(resolution)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
BLUE = (70, 130, 180)
GREEN = (70, 180, 130)

# Game Font
font = pygame.font.Font(None, 36)

# Function to create text surfaces
def create_text_surface(text, color=WHITE):
    return font.render(text, True, color)

# Load questions and answers from a file
def load_questions():
    with open("questions.txt", "r") as file:
        lines = file.readlines()
    questions = []
    for line in lines:
        question, answer = line.strip().split(',')
        questions.append({"question": question, "answer": answer})
    return questions

# Load instructions from a file
def load_instructions():
    with open("instructions.txt", "r") as file:
        instructions = file.readlines()
    return [line.strip() for line in instructions]

# Load high score from a file
def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0

# Save high score to a file
def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

# Function to display text on a surface
def display_text(text, pos, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

# Initialize game variables
instructions = load_instructions()
questions = load_questions()
score = 0
current_question = 0
user_input = ""
game_over = False
gameStart = True  # Start with the intro screen
high_score = load_high_score()  # Load the high score at the start

# Surface definitions
background_surface = pygame.Surface(resolution)
background_surface.fill(BLACK)

header_surface = pygame.Surface((800, 50))
header_surface.fill(GRAY)

score_panel = pygame.Surface((140, 110))
score_panel.fill(GREEN)

instructions_panel = pygame.Surface((600, 230))
instructions_panel.fill(BLUE)

question_panel = pygame.Surface((600, 200))
question_panel.fill(GRAY)

answer_panel = pygame.Surface((600, 50))
answer_panel.fill(BLUE)

footer_panel = pygame.Surface((800, 50))
footer_panel.fill(GRAY)

game_over_surface = create_text_surface("Game Over! Press ESC to quit.", WHITE)

# Clock for FPS control
clock = pygame.time.Clock()

# Main gameplay loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif gameStart and event.key == pygame.K_RETURN:
                # Start the game after intro
                gameStart = False
            elif not gameStart and not game_over:
                if event.key == pygame.K_RETURN:
                    # Process the answer
                    if user_input.lower() == questions[current_question]["answer"].lower():
                        score += 1
                    current_question += 1
                    user_input = ""
                    if current_question >= len(questions):
                        game_over = True
                        # Update high score if current score is greater
                        if score > high_score:
                            high_score = score
                            save_high_score(high_score)
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

    # Clear the screen
    screen.blit(background_surface, (0, 0))

    if gameStart:
        # Display the game start screen with instructions
        screen.blit(header_surface, (0, 0))
        screen.blit(instructions_panel, (100, 170))
        screen.blit(footer_panel, (0, 550))

        y_offset = 200
        for line in instructions:
            line_text = create_text_surface(line)
            screen.blit(line_text, (110, y_offset))
            y_offset += 30

        high_score_text = create_text_surface(f"High Score: {high_score}", WHITE)
        screen.blit(high_score_text, (610, 100))
        display_text("Press Enter to start...", (50, y_offset + 80))
    elif not game_over:
        # Main game screen
        screen.blit(header_surface, (0, 0))
        screen.blit(score_panel, (600, 50))
        screen.blit(question_panel, (100, 200))
        screen.blit(answer_panel, (100, 400))
        screen.blit(footer_panel, (0, 550))

        # Update score and question displays
        score_text = create_text_surface(f"Score: {score}")
        question_text = create_text_surface(questions[current_question]["question"])
        answer_text = create_text_surface(f"Your Answer: {user_input}")

        # Display score, question, and answer
        screen.blit(score_text, (610, 100))
        screen.blit(question_text, (110, 210))
        screen.blit(answer_text, (110, 410))
    else:
        # Game over screen
        screen.blit(game_over_surface, (200, 200))
        final_score_text = create_text_surface(f"Final Score: {score}", WHITE)
        high_score_text = create_text_surface(f"High Score: {high_score}", WHITE)
        screen.blit(final_score_text, (300, 350))
        screen.blit(high_score_text, (300, 400))

    # Update the display
    pygame.display.flip()
    clock.tick(60)
