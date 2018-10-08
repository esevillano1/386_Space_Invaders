import pygame


class Menu:
    """Initialize the start up menu for the game."""
    def __init__(self, settings, screen):
        self.screen = screen
        self.settings = settings
        self.text_highlight_color = (0, 255, 0)

    def start_menu(self, play_button, high_scores):
        font = pygame.font.SysFont(None, 192)
        title = font.render("SPACE", True, (255, 255, 255))

        self.screen.fill((0, 0, 0))
        self.screen.blit(title, (self.settings.screen_width/3.75, self.settings.screen_height/24))
        subfont = pygame.font.SysFont(None, 112)
        subtitle = subfont.render("INVADERS", True, self.text_highlight_color)
        self.screen.blit(subtitle, (self.settings.screen_width/3.5, self.settings.screen_height/5))

        points = pygame.font.SysFont(None, 32)

        # Draw the alien types along with how many points are given by each
        self.alien1 = pygame.image.load("images/alien1.png").convert_alpha()
        alien1 = pygame.transform.chop(self.alien1, (64, 64, 64, 64))
        alien1 = pygame.transform.scale(alien1, (128, 128))
        self.screen.blit(alien1, (self.settings.screen_width / 3.05, (self.settings.screen_height * 2.5) / 7))
        alienPoints = points.render("= " + str(self.settings.alien_points[0]) + " PTS", True, (255, 255, 255))
        self.screen.blit(alienPoints, (self.settings.screen_width / 2.25, (self.settings.screen_height * 3.4) / 8))

        self.alien2 = pygame.image.load("images/alien2.png").convert_alpha()
        alien2 = pygame.transform.chop(self.alien2, (64, 64, 64, 64))
        alien2 = pygame.transform.scale(alien2, (128, 128))
        self.screen.blit(alien2, (self.settings.screen_width / 3.1, (self.settings.screen_height * 2.75) / 7))
        alienPoints = points.render("= " + str(self.settings.alien_points[1]) + " PTS", True, (255, 255, 255))
        self.screen.blit(alienPoints, (self.settings.screen_width / 2.25, (self.settings.screen_height * 3.9) / 8))

        self.alien3 = pygame.image.load("images/alien3.png").convert_alpha()
        alien3 = pygame.transform.chop(self.alien3, (64, 64, 64, 64))
        alien3 = pygame.transform.scale(alien3, (128, 128))
        self.screen.blit(alien3, (self.settings.screen_width / 3.21, (self.settings.screen_height * 3.4) / 7))
        alienPoints = points.render("= " + str(self.settings.alien_points[2]) + " PTS", True, (255, 255, 255))
        self.screen.blit(alienPoints, (self.settings.screen_width / 2.25, (self.settings.screen_height * 4.4) / 8))

        self.ufo = pygame.image.load("images/ufo.png").convert_alpha()
        ufo = pygame.transform.scale(self.ufo, (128, 128))
        self.screen.blit(ufo, (self.settings.screen_width / 3.21, (self.settings.screen_height * 3.8) / 7))
        alienPoints = points.render("= ???", True, (255, 255, 255))
        self.screen.blit(alienPoints, (self.settings.screen_width / 2.25, (self.settings.screen_height * 4.95) / 8))

        play_button.draw_button()
        high_scores.draw_button()

    def high_scores(self):
        file = open("text_files/scores.txt", "r")
        line_num = 1
        title_font = pygame.font.SysFont(None, 128)
        title = title_font.render("HIGH SCORES", True, (255, 255, 255))
        self.screen.fill((0, 0, 0))
        self.screen.blit(title, (self.settings.screen_width / 6, self.settings.screen_height / 12))
        for line in file:
            line_font = pygame.font.SysFont(None, 48)
            high_score_line = line_font.render(str(line).strip(), True, (255, 255, 255))
            self.screen.blit(high_score_line, ((self.settings.screen_width * 2.5) / 7, (self.settings.screen_height * (1 + line_num)) / 8))
            line_num += 0.5
        returnToStart = line_font.render("Press Space to return to the start menu...", True, (255, 255, 255))
        self.screen.blit(returnToStart, ((self.settings.screen_width / 7), ((self.settings.screen_height * 7) / 8)))
        file.close()
