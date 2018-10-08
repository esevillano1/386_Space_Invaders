import pygame
from random import randint
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from menu import Menu
import game_functions as gf


def run_game():
    # Initialize game and create a screen object
    pygame.init()

    si_settings = Settings()

    screen = pygame.display.set_mode((si_settings.screen_width, si_settings.screen_height))
    pygame.display.set_caption("Space Invaders")

    # Make the Menu and the Play Game and High Scores buttons.
    menu = Menu(si_settings, screen)
    play_button = Button(si_settings, screen, "PLAY GAME", (si_settings.screen_width * 2.75) / 7, (si_settings.screen_height * 5.25) / 7)
    high_scores_button = Button(si_settings, screen, "HIGH SCORES", (si_settings.screen_width * 2.65) / 7, (si_settings.screen_height * 6) / 7)

    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(si_settings)
    sb = Scoreboard(si_settings, screen, stats)

    # Make a ship, a group of bullets, and a group of aliens
    ship = Ship(si_settings, screen)
    bullets = Group()
    alienBullets = Group()
    aliens = Group()

    images = ["images/alien1.png", "images/alien2.png", "images/alien3.png"]

    random = randint(0, 10)
    ufo_random = randint(0, 10)
    start_ticks = pygame.time.get_ticks()

    # Create the ufo
    ufo = None

    # Create the fleet of aliens.
    gf.create_fleet(si_settings, screen, ship, aliens, images)

    # Load the background music
    # bg_music = pygame.mixer.music("audio/background_music.mp3")

    # Start the main loop for the game
    while True:
        # Watch for keyboard and mouse events.
        gf.check_events(si_settings, screen, stats, sb, menu, play_button, high_scores_button, ship, aliens, bullets, alienBullets, images)

        if stats.game_active:
            seconds = int((pygame.time.get_ticks() - start_ticks) / 1000)
            if seconds - previous_time == random:
                gf.fire_back(si_settings, screen, aliens, alienBullets)
                previous_time = seconds
                random = randint(5, 10)
            if seconds - ufo_previous_time == ufo_random:
                ufo = gf.create_ufo(si_settings)
                ufo_previous_time = seconds
                ufo_random = randint(20, 30)
                print("UFO Random: " + str(ufo_random) + "    Seconds: " + str(seconds) + "   UFO Previous Time: " + str(ufo_previous_time))
            ship.update()
            gf.update_bullets(si_settings, screen, stats, sb, ship, aliens, bullets, alienBullets, images)
            gf.update_aliens(si_settings, screen, stats, sb, ship, aliens, bullets, alienBullets, images, (seconds - previous_time), ufo)
        else:
            previous_time = int(pygame.time.get_ticks() / 1000)
            ufo_previous_time = int(pygame.time.get_ticks() / 1000)

        gf.update_screen(si_settings, screen, stats, sb, ship, aliens, bullets, alienBullets, menu, play_button, high_scores_button)


run_game()
