# Import modules for the main game file
import pygame
import sys
import constants
import levels
from player import Player

"""
The Adventures of Tyler the Tiger
@author Trevor Pirone
version 1.0 beta
Main game module
"""

"""
Controls
Left arrow key: move left
Right arrow key: move right
Up arrow key: jump
Mouse click: restart/close game (only used on game over and winner screen)
"""

"""
Gameplay
Maneuver your player (Tyler) through the depths of the jungle before the timer
runs out. Avoid making contact with the enemies as they effect the player's
health. Be careful! If Tyler falls off the platforms, he loses a life and the
game restarts at the beginning. If Tyler loses all of his lives, the game ends.
If Tyler's health reaches zero, the game also ends or restarts.
"""

"""
Installation Instructions
Un-zip the file to your desktop.
Run the program.
*NOTE* There is no need for installing tiles or backgrounds. The files
for audio and visuals are located in the same directory as the modules.
"""


def main():
    # Main game
    pygame.init()

    # Sets the height and width of the screen
    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("The Adventures of Tyler the Tiger")
    icon = pygame.image.load("icon.png")
    icon.set_colorkey(constants.GRAY)
    pygame.display.set_icon(icon)

    # Creates an instance of the player
    player = Player()

    # Game attribute variables
    game_over = False
    victory = False
    game_start = False
    help_screen = False
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    # Create all the levels
    level_list = []
    level_list.append(levels.Level_01(player))
    level_list.append(levels.Level_02(player))
    level_list.append(levels.Level_03(player))

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    # Sets the player on the level
    player.rect.x = 120
    player.rect.y = constants.SCREEN_HEIGHT - 68
    player.lose_jump = constants.SCREEN_HEIGHT - 67
    active_sprite_list.add(player)

    # Loop until the user clicks the close button
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Sound effects and background music
    jump_sound = pygame.mixer.Sound("jump.ogg")
    _ = pygame.mixer.music.load("Deep in the Rainforest.ogg")
    pygame.mixer.music.play(-1, 0.0)

    # -------- Main Program Loop -----------
    while not done:

        for event in pygame.event.get():  # User did something
            if event.type == pygame.USEREVENT:
                if game_start is True:
                    if constants.TIME > 0:
                        if victory is True:
                            constants.TIME = constants.TIME
                        else:
                            constants.TIME -= 1

            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
                pygame.mixer.music.stop()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h and game_start is False:
                    help_screen = True
                if event.key == pygame.K_ESCAPE and game_start is False:
                    help_screen = False
                if event.key == pygame.K_SPACE and game_start is False:
                    game_start = True
                if event.key == pygame.K_LEFT and player.rect.x > 120:
                    player.go_left()
                if event.key == pygame.K_RIGHT and player.rect.x > 0:
                    player.go_right()
                if (event.key == pygame.K_UP and
                   player.rect.y < player.lose_jump):
                    player.jump()  # Player is above the platform
                    jump_sound.play()
                    if game_over is True:
                        jump_sound.stop()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

            if event.type == pygame.MOUSEBUTTONDOWN and game_over is True:
                if victory is True:  # Player won the game
                    pygame.quit()
                    sys.exit()
                    break
                elif constants.LIVES <= 1:  # Player has no more lives
                    pygame.quit()
                    sys.exit()
                    break
                else:
                    pygame.mixer_music.play()
                    constants.TIME = 100  # Reset time
                    constants.LIVES = constants.LIVES - 1  # Subtract a life
                    constants.HEALTH = 100
                    main()
                    done = True

        # Update the player
        active_sprite_list.update()

        # Update items in the level
        current_level.update()

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.x >= 500:
            diff = player.rect.x - 500
            player.rect.x = 500
            current_level.shift_world(-diff)

        # If the player gets near the left side, do not shift the world
        if player.rect.x <= 120:
            player.rect.x = 120
            current_level.shift_world(0)

        # If the player gets to the last level, end the game
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            if current_level_no == len(level_list)-1:
                game_over = True
                victory = True
                constants.TIME = constants.TIME
                pygame.mixer.music.stop()

        # If the player gets to the end of the level, go to the next level
            if current_level_no < len(level_list)-1:
                player.rect.x = 120
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
                if constants.HEALTH == 100:
                    constants.SCORE = 500
                else:
                    constants.SCORE = constants.HEALTH*5

        # If the player falls while time remains, end game and reset time
        if player.rect.y == 650 and constants.TIME >= 0:
            game_over = True
            constants.TIME = 0
        else:
            constants.LIVES = constants.LIVES

        # If the time runs out, end the game and reset the time
        if constants.TIME == 0:
            game_over = True
            pygame.mixer.music.stop()
        else:
            constants.LIVES = constants.LIVES

        if constants.HEALTH == 0:
            game_over = True
            pygame.mixer.music.stop()
        else:
            constants.LIVES = constants.LIVES

        # All code to draw goes below this comment
        if game_start is True:  # Draw game
            if game_over is True:  # Game ended
                if victory is True:
                    player.winner_screen(screen)  # Draw the winner screen
                else:
                    player.game_over(screen)  # Draw the game over screen
            else:
                current_level.draw(screen)
                active_sprite_list.draw(screen)
                levels.timer(screen)
                player.lives(screen)
                player.health(screen)
                player.score(screen)
        elif help_screen is True:
            player.help(screen)
        else:
            player.title_screen(screen)
        # All code to draw goes above this comment

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn
        pygame.display.flip()

    # Need this line, so that the game will not hang when a user quits
    pygame.quit()

if __name__ == "__main__":
    main()
