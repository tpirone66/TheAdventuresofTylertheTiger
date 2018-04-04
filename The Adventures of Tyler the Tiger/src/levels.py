"""
This module is used to hold the Level class. The Level represents the world
the player interacts with.
"""

import pygame
import constants
import platforms


class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    # Lists of sprites used in all levels
    platform_list = None
    enemy_list = None

    # Background image
    background = None

    # How far this world has been scrolled horizontally
    world_shift = 0
    level_limit = -1000

    def __init__(self, player):
        """
        Constructor. Pass in a handle to player.
        Needed for when moving platforms collide with the player.
        """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

    # Update everything on this level
    def update(self):
        """ Update everything in this level. """

        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw and shift the background
        screen.fill(constants.WHITE)
        screen.blit(self.background, (self.world_shift // 3, 0))

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    def shift_world(self, shift_x):
        """ When the user moves left/right, we need to scroll everything: """

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x


class Level_01(Level):
    """ Definition for Level 1. """

    def __init__(self, player):
        """ Create Level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("background_01.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -2500

        # Array with type of platform, and x, y location of the platform
        level = [[platforms.SMALL_GRASS_MIDDLE, 0,
                  constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 70,
                  constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 140,
                  constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 210,
                  constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 280,
                  constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 350,
                  constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 420,
                  constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 1680,
                  constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 1750,
                  constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 1820,
                  constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 1890,
                  constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 2170,
                  constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 2240,
                  constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 2310,
                  constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 2380,
                  constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 2940,
                  constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 3010,
                  constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 3080,
                  constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 3430,
                  constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 3500,
                  constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 500, 500],
                 [platforms.SMALL_GRASS_MIDDLE, 570, 500],
                 [platforms.SMALL_GRASS_MIDDLE, 710, 450],
                 [platforms.SMALL_GRASS_MIDDLE, 940, 400],
                 [platforms.SMALL_GRASS_MIDDLE, 1070, 300],
                 [platforms.SMALL_GRASS_MIDDLE, 1140, 300],
                 [platforms.SMALL_GRASS_MIDDLE, 1280, 400],
                 [platforms.SMALL_GRASS_MIDDLE, 1460, 500],
                 [platforms.SMALL_GRASS_MIDDLE, 1740, 300],
                 [platforms.SMALL_GRASS_MIDDLE, 1810, 300],
                 [platforms.SMALL_GRASS_MIDDLE, 1960, 500],
                 [platforms.SMALL_GRASS_MIDDLE, 2000, 200],
                 [platforms.SMALL_GRASS_MIDDLE, 2250, 250],
                 [platforms.SMALL_GRASS_MIDDLE, 2500, 125],
                 [platforms.SMALL_GRASS_MIDDLE, 2570, 550],
                 [platforms.SMALL_GRASS_MIDDLE, 2710, 500],
                 [platforms.SMALL_GRASS_MIDDLE, 2630, 275],
                 [platforms.SMALL_GRASS_MIDDLE, 2850, 375],
                 [platforms.SMALL_GRASS_MIDDLE, 3150, 400],
                 [platforms.SMALL_GRASS_MIDDLE, 3220, 400],
                 [platforms.SMALL_GRASS_MIDDLE, 3290, 400],
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)

        # Add an enemy to the level
        block = platforms.Enemy(platforms.ENEMY_PLATFORM)
        block.rect.x = 260
        block.rect.y = constants.SCREEN_HEIGHT - 110
        block.boundary_right = 340
        block.boundary_left = 180
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.enemy_list.add(block)

        block = platforms.Enemy(platforms.ENEMY_PLATFORM)
        block.rect.x = 1700
        block.rect.y = constants.SCREEN_HEIGHT - 110
        block.boundary_right = 1850
        block.boundary_left = 1700
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.enemy_list.add(block)

        block = platforms.Enemy(platforms.ENEMY_PLATFORM)
        block.rect.x = 2250
        block.rect.y = constants.SCREEN_HEIGHT - 110
        block.boundary_right = 2350
        block.boundary_left = 2250
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.enemy_list.add(block)

        block = platforms.Enemy(platforms.ENEMY_PLATFORM)
        block.rect.x = 3170
        block.rect.y = 310
        block.boundary_right = 3270
        block.boundary_left = 3170
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.enemy_list.add(block)

        # Add a custom moving platform
        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1350
        block.rect.y = 300
        block.boundary_left = 1350
        block.boundary_right = 1600
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 950
        block.rect.y = 500
        block.boundary_left = 950
        block.boundary_right = 1200
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 2020
        block.rect.y = 400
        block.boundary_left = 2020
        block.boundary_right = 2300
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)


class Level_02(Level):
    """ Definition for Level 2. """

    def __init__(self, player):
        """ Create Level 2. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("background_02.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -2500

        # Array with type of platform, and x, y location of the platform.
        level = [[platforms.SMALL_GRASS_MIDDLE, 0,
                 constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 70,
                 constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 140,
                 constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 210,
                 constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 280,
                 constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 350,
                 constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 420,
                 constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 2940,
                 constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 3010,
                 constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 3080,
                 constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 3430,
                 constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 3500,
                 constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 3570,
                 constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 650, 500],
                 [platforms.SMALL_GRASS_MIDDLE, 720, 500],
                 [platforms.SMALL_GRASS_MIDDLE, 1070, 200],
                 [platforms.SMALL_GRASS_MIDDLE, 1140, 200],
                 [platforms.SMALL_GRASS_MIDDLE, 1210, 200],
                 [platforms.SMALL_GRASS_MIDDLE, 1280, 200],
                 [platforms.SMALL_GRASS_MIDDLE, 1740, 300],
                 [platforms.SMALL_GRASS_MIDDLE, 1810, 300],
                 [platforms.SMALL_GRASS_MIDDLE, 1880, 300],
                 [platforms.SMALL_GRASS_MIDDLE, 1950, 300],
                 [platforms.SMALL_GRASS_MIDDLE, 2450, 500],
                 [platforms.SMALL_GRASS_MIDDLE, 2690, 550],
                 [platforms.SMALL_GRASS_MIDDLE, 3150, 450],
                 [platforms.SMALL_GRASS_MIDDLE, 3220, 450],
                 [platforms.SMALL_GRASS_MIDDLE, 3290, 450],
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)

        # Add a custom moving platform
        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 500
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 800
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 500
        block.change_y = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 2250
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 500
        block.change_y = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        # Add an enemy to the level
        block = platforms.Enemy(platforms.ENEMY_PLATFORM)
        block.rect.x = 1100
        block.rect.y = 110
        block.boundary_right = 1200
        block.boundary_left = 1100
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.enemy_list.add(block)

        block = platforms.Enemy(platforms.ENEMY_PLATFORM)
        block.rect.x = 1900
        block.rect.y = 210
        block.boundary_right = 1900
        block.boundary_left = 1800
        block.change_x = -1
        block.player = self.player
        block.level = self
        self.enemy_list.add(block)

        block = platforms.Enemy(platforms.ENEMY_PLATFORM)
        block.rect.x = 2960
        block.rect.y = constants.SCREEN_HEIGHT - 110
        block.boundary_right = 3060
        block.boundary_left = 2960
        block.change_x = -1
        block.player = self.player
        block.level = self
        self.enemy_list.add(block)

        block = platforms.Enemy(platforms.ENEMY_PLATFORM)
        block.rect.x = 260
        block.rect.y = constants.SCREEN_HEIGHT - 110
        block.boundary_right = 340
        block.boundary_left = 180
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.enemy_list.add(block)


class Level_03(Level):
    """ Definition for Level 3. """

    def __init__(self, player):
        """ Create Level 3. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("background_03.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -2500

        # Array with type of platform, and x, y location of the platform
        level = [[platforms.SMALL_GRASS_MIDDLE, 0,
                 constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 70,
                 constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 140,
                 constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 210,
                 constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 280,
                 constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 3290,
                 constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 3470,
                 constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 3540,
                 constants.SCREEN_HEIGHT - 20],
                 [platforms.SMALL_GRASS_MIDDLE, 1200, 300],
                 [platforms.SMALL_GRASS_MIDDLE, 1270, 300],
                 [platforms.SMALL_GRASS_MIDDLE, 1340, 300],
                 [platforms.SMALL_GRASS_MIDDLE, 1410, 300],
                 [platforms.SMALL_GRASS_MIDDLE, 1480, 300],
                 [platforms.SMALL_GRASS_MIDDLE, 1550, 300],
                 [platforms.SMALL_GRASS_MIDDLE, 1620, 300],
                 [platforms.SMALL_GRASS_MIDDLE, 3000, 475],
                 [platforms.SMALL_GRASS_MIDDLE, 3070, 475],
                 [platforms.SMALL_GRASS_MIDDLE, 3140, 475],
                 [platforms.SMALL_GRASS_MIDDLE, 3210, 475],
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)

        # Add a custom moving platform
        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 350
        block.rect.y = 450
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -5
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 450
        block.rect.y = 450
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = 5
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 550
        block.rect.y = 450
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -5
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 650
        block.rect.y = 450
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = 5
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 750
        block.rect.y = 450
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -5
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 850
        block.rect.y = 450
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = 5
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 950
        block.rect.y = 450
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -5
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        # Add an enemy to the level
        block = platforms.Enemy(platforms.ENEMY_PLATFORM)
        block.rect.x = 1320
        block.rect.y = 210
        block.boundary_right = 1480
        block.boundary_left = 1320
        block.change_x = 5
        block.player = self.player
        block.level = self
        self.enemy_list.add(block)

        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1700
        block.rect.y = 400
        block.boundary_left = 1700
        block.boundary_right = 1900
        block.change_x = 5
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 2100
        block.rect.y = 400
        block.boundary_left = 1900
        block.boundary_right = 2100
        block.change_x = -5
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 2100
        block.rect.y = 400
        block.boundary_left = 2100
        block.boundary_right = 2300
        block.change_x = 5
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 2500
        block.rect.y = 400
        block.boundary_left = 2300
        block.boundary_right = 2500
        block.change_x = -5
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 2500
        block.rect.y = 400
        block.boundary_left = 2500
        block.boundary_right = 2700
        block.change_x = 5
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 2900
        block.rect.y = 400
        block.boundary_left = 2700
        block.boundary_right = 2900
        block.change_x = -5
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = platforms.Enemy(platforms.ENEMY_PLATFORM)
        block.rect.x = 3160
        block.rect.y = 385
        block.boundary_right = 3160
        block.boundary_left = 3060
        block.change_x = -5
        block.player = self.player
        block.level = self
        self.enemy_list.add(block)


def timer(screen):
    """ Method to be called for displaying the time on the screen. """

    if constants.GAME_OVER is False:
        font = pygame.font.SysFont("serif", 36)
        text = font.render(
            "Time: " + str(constants.TIME), True, constants.TIGER_ORANGE
        )
        outline = font.render(
            "Time: " + str(constants.TIME), True, constants.BLACK
        )
        pos_x = 10
        pos_y = 10
        screen.blit(outline, [pos_x - 1, pos_y - 1])
        screen.blit(outline, [pos_x - 1, pos_y + 1])
        screen.blit(outline, [pos_x + 1, pos_y - 1])
        screen.blit(outline, [pos_x + 1, pos_y + 1])
        screen.blit(text, [pos_x, pos_y])
