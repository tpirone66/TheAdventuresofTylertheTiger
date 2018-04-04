"""
This module is used to hold the Player class. The Player represents the user-
controlled sprite on the screen.
"""
import pygame
import constants
from platforms import MovingPlatform
from spritesheet_functions import SpriteSheet


class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
    controls. """

    # Set speed vector of player
    change_x = 0
    change_y = 0

    # Set the lives of the player
    player_lives = 3

    # Hold the images for the sprite to animate it
    walking_frames_l = []
    walking_frames_r = []

    # Direction the player is facing
    direction = "R"

    # List of sprites we can bump against
    level = None

    def __init__(self):
        """ Constructor function. """

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = SpriteSheet("p1_walk.png")
        # Load all the right facing images into a list
        image = sprite_sheet.get_image(0, 96, 48, 48)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(48, 96, 48, 48)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(96, 96, 48, 48)
        self.walking_frames_r.append(image)

        # Load all the right facing images, then flip them to face left
        image = sprite_sheet.get_image(0, 96, 48, 48)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(48, 96, 48, 48)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(96, 96, 48, 48)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        # Set the image the player starts with
        self.image = self.walking_frames_r[0]

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()

    def update(self):
        """ Move the player. """

        # Gravity
        self.calc_grav()

        # Move left or right
        self.rect.x += self.change_x
        pos = self.rect.x + self.level.world_shift
        if self.direction == "R":
            frame = (pos // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = (pos // 30) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(
            self, self.level.platform_list, False
        )
        for block in block_hit_list:
            if self.change_x > 0:  # Moving right
                # Set our right side to the left side of the item we hit
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite
                self.rect.left = block.rect.right

        # Move up or down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(
            self, self.level.platform_list, False
        )
        for block in block_hit_list:

            # Reset our position based on the top or bottom of the object
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

            if isinstance(block, MovingPlatform):
                self.rect.x += block.change_x

    def calc_grav(self):
        """ Calculate effect of gravity. """

        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .25

        # See if we are on the ground
        ground = constants.SCREEN_HEIGHT - self.rect.height
        if self.rect.y >= ground and self.change_y >= 0:
            self.change_y = 1

    def jump(self):
        """ Called when user hits 'jump' button. """

        self.rect.y += 1
        platform_hit_list = pygame.sprite.spritecollide(
            self, self.level.platform_list, False
        )
        self.rect.y -= 1

        # If it is ok to jump, set our speed upwards
        if (len(platform_hit_list) > 0 or
           self.rect.bottom >= constants.SCREEN_HEIGHT):
            self.change_y = -8

    # Player-controlled movement
    def go_left(self):
        """ Called when the user hits the left arrow. """

        self.change_x = -6
        self.direction = "L"

    def go_right(self):
        """ Called when the user hits the right arrow. """

        self.change_x = 6
        self.direction = "R"

    def stop(self):
        """ Called when the user lets off the keyboard. """

        self.change_x = 0

    def lives(self, screen):
        """ Method to be called for displaying the lives on the screen. """

        if constants.GAME_OVER is False:
            font = pygame.font.SysFont("serif", 36)
            text = font.render(
                "Lives: " + str(constants.LIVES), True, constants.TIGER_ORANGE
            )
            outline = font.render(
                "Lives: " + str(constants.LIVES), True, constants.BLACK
            )
            pos_x = 675
            pos_y = 10
            screen.blit(outline, [pos_x - 1, pos_y - 1])
            screen.blit(outline, [pos_x - 1, pos_y + 1])
            screen.blit(outline, [pos_x + 1, pos_y - 1])
            screen.blit(outline, [pos_x + 1, pos_y + 1])
            screen.blit(text, [pos_x, pos_y])

    def health(self, screen):
        """ Method to be called for displaying the health on the screen. """

        if constants.GAME_OVER is False:
            font = pygame.font.SysFont("serif", 36)
            text = font.render(
                "Health: " + str(constants.HEALTH),
                True,
                constants.TIGER_ORANGE
            )
            outline = font.render(
                "Health: " + str(constants.HEALTH), True, constants.BLACK
            )
            pos_x = 475
            pos_y = 10
            screen.blit(outline, [pos_x - 1, pos_y - 1])
            screen.blit(outline, [pos_x - 1, pos_y + 1])
            screen.blit(outline, [pos_x + 1, pos_y - 1])
            screen.blit(outline, [pos_x + 1, pos_y + 1])
            screen.blit(text, [pos_x, pos_y])

    def score(self, screen):
        """ Method to be called for displaying the score on the screen. """

        if constants.GAME_OVER is False:
            font = pygame.font.SysFont("serif", 36)
            text = font.render(
                "Score: " + str(constants.SCORE), True, constants.TIGER_ORANGE
            )
            outline = font.render(
                "Score: " + str(constants.SCORE), True, constants.BLACK
            )
            pos_x = 225
            pos_y = 10
            screen.blit(outline, [pos_x - 1, pos_y - 1])
            screen.blit(outline, [pos_x - 1, pos_y + 1])
            screen.blit(outline, [pos_x + 1, pos_y - 1])
            screen.blit(outline, [pos_x + 1, pos_y + 1])
            screen.blit(text, [pos_x, pos_y])

    def game_over(self, screen):
        """Method to be called for displaying the game over screen."""
        self.game_over_music = pygame.mixer.music.load("Game Over.ogg")
        screen.fill(constants.WHITE)

        if self.game_over:
            # Draw if the player loses and has lost all of their lives
            if constants.LIVES - 1 == 0:
                self.background = pygame.image.load("game_over.png")
                screen.blit(self.background, [0, 0])
            # Draw if the player loses and has lives remaining
            else:
                self.background = pygame.image.load("mouse_restart.png")
                screen.blit(self.background, [0, 0])

    def winner_screen(self, screen):
        """ Method to be called for displaying the winner screen. """
        screen.fill(constants.WHITE)

        # Player has reached the end of the game
        self.background = pygame.image.load("winner_screen.png")
        font = pygame.font.SysFont("serif", 84)
        score = (
            (constants.TIME*100)+(constants.LIVES*1000)+(constants.HEALTH*10)
        )
        scoretext = font.render(str(score), True, constants.TIGER_ORANGE)
        outlinetext = font.render(str(score), True, constants.BLACK)
        pos_x = (constants.SCREEN_WIDTH // 2) - (scoretext.get_width() // 2)
        pos_y = (constants.SCREEN_HEIGHT // 2) - (scoretext.get_height() // 2)
        outpos_x = (
            (constants.SCREEN_WIDTH // 2) - (outlinetext.get_width() // 2)
        )
        outpos_y = (
            (constants.SCREEN_HEIGHT // 2) - (outlinetext.get_height() // 2)
        )
        screen.blit(self.background, [0, 0])
        screen.blit(outlinetext, [outpos_x + 129, outpos_y + 19])
        screen.blit(outlinetext, [outpos_x + 129, outpos_y + 21])
        screen.blit(outlinetext, [outpos_x + 131, outpos_y + 19])
        screen.blit(outlinetext, [outpos_x + 131, outpos_y + 21])
        screen.blit(scoretext, [pos_x + 130, pos_y + 20])

    def title_screen(self, screen):
        """ Method that draws the title screen. """
        screen.fill(constants.WHITE)

        if constants.LIVES < 3:
            self.background = pygame.image.load("intermission_screen.png")
            font = pygame.font.SysFont("serif", 84)
            text = font.render(
                str(constants.LIVES), True, constants.TIGER_ORANGE
            )
            outline_text = font.render(
                str(constants.LIVES), True, constants.BLACK
            )
            center_x = (constants.SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (
                (constants.SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            )
            pos_x = (
                (constants.SCREEN_WIDTH // 2) -
                (outline_text.get_width() // 2)
            )
            pos_y = (
                (constants.SCREEN_HEIGHT // 2) -
                (outline_text.get_height() // 2)
            )
            screen.blit(self.background, [0, 0])
            screen.blit(outline_text, [pos_x + 49, pos_y - 29])
            screen.blit(outline_text, [pos_x + 49, pos_y - 31])
            screen.blit(outline_text, [pos_x + 51, pos_y - 29])
            screen.blit(outline_text, [pos_x + 51, pos_y - 31])
            screen.blit(text, [center_x + 50, center_y - 30])
        else:
            self.background = pygame.image.load("title_screen.png")
            screen.blit(self.background, [0, 0])

    def help(self, screen):
        """ Method that draws the help screen. """
        screen.fill(constants.WHITE)
        self.background = pygame.image.load("help_screen.png")
        screen.blit(self.background, [0, 0])
