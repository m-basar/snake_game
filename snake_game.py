import pygame
import time
import random
import sys

# Initialize pygame
pygame.init()

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Set display dimensions
display_width = 600
display_height = 400

# Set up the display
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Simple Snake Game')

# Set the clock
clock = pygame.time.Clock()

# Set snake block size and speed
snake_block = 10
initial_snake_speed = 8  # Starting speed (slow)
snake_speed = initial_snake_speed
speed_increment = 1      # How much to increase speed
speed_milestone = 5      # Increase speed every 5 food items

# Font styles
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def display_score(score):
    """Display the current score on the screen"""
    value = score_font.render("Score: " + str(score), True, black)
    game_display.blit(value, [0, 0])
    
    # Also display current speed
    speed_text = font_style.render(f"Speed: {snake_speed}", True, blue)
    game_display.blit(speed_text, [0, 40])

def draw_snake(snake_block, snake_list):
    """Draw the snake on the screen"""
    for x in snake_list:
        pygame.draw.rect(game_display, green, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    """Display a message on the screen"""
    mesg = font_style.render(msg, True, color)
    mesg_rect = mesg.get_rect(center=(display_width/2, display_height/2))
    game_display.blit(mesg, mesg_rect)
    
def legend_message():
    """Display a legend message with dramatic effect"""
    overlay = pygame.Surface((display_width, display_height))
    overlay.set_alpha(180)  # Semi-transparent overlay
    overlay.fill(black)
    game_display.blit(overlay, (0, 0))
    
    # Create large gold text
    legend_font = pygame.font.SysFont("impact", 60)
    legend_text = legend_font.render("YOU ARE A LEGEND!", True, (255, 215, 0))  # Gold color
    text_rect = legend_text.get_rect(center=(display_width/2, display_height/2 - 30))
    
    # Draw a glow effect (multiple layers of the same text with decreasing alpha)
    for offset in range(10, 0, -2):
        glow_text = legend_font.render("YOU ARE A LEGEND!", True, (255, 215, 0, 20))
        glow_rect = glow_text.get_rect(center=(display_width/2, display_height/2 - 30))
        glow_rect.x += offset
        glow_rect.y += offset
        game_display.blit(glow_text, glow_rect)
    
    game_display.blit(legend_text, text_rect)
    
    # Add subtitle
    subtitle_font = pygame.font.SysFont("arial", 25)
    subtitle = subtitle_font.render("Press SPACE to play again or ESC to quit", True, white)
    sub_rect = subtitle.get_rect(center=(display_width/2, display_height/2 + 50))
    game_display.blit(subtitle, sub_rect)

def game_loop():
    """Main game loop"""
    global snake_speed  # Make speed variable global so we can modify it
    
    game_over = False
    game_close = False
    legend_status = False
    
    # Reset speed at the start of each game
    snake_speed = initial_snake_speed
    
    # Starting position of the snake - make sure it's aligned to grid
    x1 = round(display_width / 2 / snake_block) * snake_block
    y1 = round(display_height / 2 / snake_block) * snake_block

    # Change in position - start moving right to make game more engaging
    x1_change = snake_block
    y1_change = 0

    # Snake body
    snake_list = []
    snake_length = 1

    # Generate first food position
    foodx = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block
    
    # Track food eaten for speed increases
    food_count = 0
    
    # Calculate maximum possible snake length
    max_possible_length = (display_width // snake_block) * (display_height // snake_block)
    legend_threshold = int(max_possible_length * 0.7)  # 70% of maximum possible length
    
    # Print instructions to console
    print("Snake Game Started!")
    print("Use arrow keys to control the snake.")
    print("Every 5 food items, the speed will increase!")
    print("Fill the screen to become a LEGEND!")

    while not game_over:

        while game_close:
            # Game over screen
            game_display.fill(white)
            
            if legend_status:
                # Show legend screen with dramatic effect
                legend_message()
            else:
                # Regular game over message
                message("Game Over! Press SPACE to Play Again or ESC to Quit", red)
                
            display_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_SPACE:
                        game_loop()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:  # Prevent 180-degree turns
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0
                # Add escape key to quit
                elif event.key == pygame.K_ESCAPE:
                    game_over = True
                    pygame.quit()
                    sys.exit()

        # Check if snake hits boundary
        if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
            game_close = True

        # Update snake position
        x1 += x1_change
        y1 += y1_change
        
        # Fill the display
        game_display.fill(white)
        
        # Draw the food
        pygame.draw.rect(game_display, red, [foodx, foody, snake_block, snake_block])
        
        # Update snake
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        
        # Remove extra snake segments
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check if snake hits itself
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        # Draw snake and score
        draw_snake(snake_block, snake_list)
        display_score(snake_length - 1)

        # Update display
        pygame.display.update()

        # Check if snake eats food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block
            snake_length += 1
            food_count += 1
            
            # Check if we should increase speed (every 5 foods)
            if food_count % speed_milestone == 0:
                snake_speed += speed_increment
                print(f"Speed increased to {snake_speed}!")
            
            # Check if snake has reached legend status (filled most of the screen)
            if snake_length > legend_threshold:
                legend_status = True
                game_close = True

        # Set the game speed
        clock.tick(snake_speed)

    # Quit pygame
    pygame.quit()
    sys.exit()

# Start the game
if __name__ == "__main__":
    print("Starting Snake Game...")
    print("Controls: Arrow keys to move, ESC to quit")
    try:
        game_loop()
    except Exception as e:
        print(f"Game crashed with error: {e}")
        pygame.quit()
        sys.exit()
