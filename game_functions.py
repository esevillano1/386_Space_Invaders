import sys
from time import sleep
from random import randint
import pygame
from bullet import Bullet
from alien import Alien


def get_number_aliens_x(si_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = si_settings.screen_width * (1.75/3)
    number_aliens_x = int(available_space_x / alien_width)
    return number_aliens_x


def get_number_rows(si_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (si_settings.screen_height - alien_height - ship_height)/2
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(si_settings, screen, aliens, alien_number, row_number, image, points):
    """Create an alien and place it in the row."""
    # Create an alien and place it in the row.
    alien = Alien(si_settings, screen, image, points)
    alien_width = alien.rect.width
    alien.x = alien_width + 0.5 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = si_settings.screen_height/8 + alien.rect.height + 0.5 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(si_settings, screen, ship, aliens, images):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    # Spacing between each alien is equal to one alien width.
    alien = Alien(si_settings, screen, images[0], si_settings.alien_points[0])
    print(str(alien))
    number_aliens_x = get_number_aliens_x(si_settings, alien.rect.width)
    print("num aliens: " + str(number_aliens_x))
    number_rows = get_number_rows(si_settings, ship.rect.height, alien.rect.height)
    print("num rows: " + str(number_rows))

    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
                create_alien(si_settings, screen, aliens, alien_number, row_number, images[0], si_settings.alien_points[0])

    alien = Alien(si_settings, screen, images[1], si_settings.alien_points[1])
    print(str(alien))
    number_aliens_x = get_number_aliens_x(si_settings, alien.rect.width)
    print("num aliens: " + str(number_aliens_x))
    number_rows = get_number_rows(si_settings, ship.rect.height, alien.rect.height)
    print("num rows: " + str(number_rows))

    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(si_settings, screen, aliens, alien_number, row_number + 2, images[1], si_settings.alien_points[1])

    alien = Alien(si_settings, screen, images[2], si_settings.alien_points[2])
    print(str(alien))
    number_aliens_x = get_number_aliens_x(si_settings, alien.rect.width)
    print("num aliens: " + str(number_aliens_x))
    number_rows = get_number_rows(si_settings, ship.rect.height, alien.rect.height)
    print("num rows: " + str(number_rows))

    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
                create_alien(si_settings, screen, aliens, alien_number, row_number + 4, images[2], si_settings.alien_points[2])


def update_screen(si_settings, screen, stats, sb, ship, aliens, bullets, alienBullets, menu, play_button, high_scores_button):
    # Redraw the screen during each pass through the loop.
    screen.fill(si_settings.bg_color)

    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    for bullet in alienBullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    # Draw the score information.
    sb.show_score()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        if si_settings.high_score_screen:
            menu.high_scores()
        else:
            load_startup_screen(menu, play_button, high_scores_button)

    if stats.game_active and len(aliens) <= 9:
        play_sound("audio/bg_music.wav", -1)

    # Make the most recently drawn screen visible
    pygame.display.flip()


def check_keydown_events(event, si_settings, screen, ship, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        # Move the ship to the right.
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        if si_settings.high_score_screen:
            si_settings.high_score_screen = False
        else:
            play_sound("audio/laser_shot.wav")
            fire_bullet(si_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(si_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < si_settings.bullets_allowed:
        new_bullet = Bullet(si_settings, screen, ship, si_settings.ship_direction)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(si_settings, screen, stats, sb, menu, play_button, high_scores, ship, aliens, bullets, alienBullets, images):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, si_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(si_settings, screen, stats, sb, play_button, ship, aliens, bullets, alienBullets, images, mouse_x, mouse_y)
            check_high_scores(si_settings, menu, high_scores, mouse_x, mouse_y)
        elif event.type == pygame.MOUSEMOTION:
            check_button_hover(pygame.mouse.get_pos(), play_button, high_scores)


def check_button_hover(coord, play_button, high_scores_button):
    """Check if the mouse is hovering over the Play Game or High Scores button."""
    x = coord[0]
    y = coord[1]
    play_x = (play_button.rect.x <= x <= play_button.rect.x + play_button.width)
    play_y = (play_button.rect.y <= y <= play_button.rect.y + play_button.height)
    scores_x = (high_scores_button.rect.x <= x <= high_scores_button.rect.x + high_scores_button.width)
    scores_y = (high_scores_button.rect.y <= y <= high_scores_button.rect.y + high_scores_button.height)
    if play_x and play_y:
        play_button.text_color = (0, 255, 0)
    else:
        play_button.text_color = (255, 255, 255)

    play_button.prep_msg()
    play_button.draw_button()

    if scores_x and scores_y:
        high_scores_button.text_color = (0, 255, 0)
    else:
        high_scores_button.text_color = (255, 255, 255)

    high_scores_button.prep_msg()
    high_scores_button.draw_button()


def check_play_button(si_settings, screen, stats, sb, play_button, ship, aliens, bullets, alienBullets, images, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        si_settings.initialize_dynamic_settings()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        alienBullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(si_settings, screen, ship, aliens, images)
        ship.center_ship()


def check_high_scores(si_settings, menu, high_scores, mouse_x, mouse_y):
    """Load the list of high scores."""
    button_clicked = high_scores.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        menu.high_scores()
        si_settings.high_score_screen = True


def load_startup_screen(menu, play_button, high_scores_button):
    """Load the start menu """
    menu.start_menu(play_button, high_scores_button)


def update_bullets(si_settings, screen, stats, sb, ship, aliens, bullets, alienBullets, images):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()
    alienBullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    for bullet in alienBullets.copy():
        if bullet.rect.top >= si_settings.screen_height:
            alienBullets.remove(bullet)

    check_bullet_collisions(si_settings, screen, stats, sb, ship, aliens, bullets, alienBullets, images)


def check_bullet_collisions(si_settings, screen, stats, sb, ship, aliens, bullets, alienBullets, images):
    """Respond to bullet collisions."""
    # Remove any bullets and aliens that have collided.
    alienBulletCollisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if alienBulletCollisions:
        for aliens in alienBulletCollisions.values():
            for alien in aliens:
                stats.score += alien.alien_points
                sb.prep_score()
        check_high_score(stats, sb)

    for bullet in alienBullets:
        if pygame.sprite.collide_rect(bullet, ship):
            ship_hit(si_settings, screen, stats, sb, ship, aliens, bullets, alienBullets, images)

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        alienBullets.empty()
        si_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(si_settings, screen, ship, aliens, images)


def check_fleet_edges(si_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(si_settings, aliens)
            break


def change_fleet_direction(si_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += si_settings.fleet_drop_speed
    si_settings.fleet_direction *= -1


def ship_hit(si_settings, screen, stats, sb, ship, aliens, bullets, alienBullets, images):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1

        # Animate the ship explosion
        ship_explosion(si_settings, screen, ship)

        # Update scoreboard.
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        alienBullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(si_settings, screen, ship, aliens, images)
        ship.center_ship()

        # Pause.
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(si_settings, screen, stats, sb, ship, aliens, bullets, alienBullets, images):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(si_settings, screen, stats, sb, ship, aliens, bullets, alienBullets, images)
            break


def update_aliens(si_settings, screen, stats, sb, ship, aliens, bullets, alienBullets, images, elapsedTime, ufo):
    """Check if the fleet is at an edge, and update the positions of all aliens in the fleet."""
    check_fleet_edges(si_settings, aliens)
    aliens.update()

    if elapsedTime == 1:
        for alien in aliens:
            if alien.image == alien.image2:
                alien.image = alien.image3
            else:
                alien.image = alien.image2

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(si_settings, screen, stats, sb, ship, aliens, bullets, alienBullets, images)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(si_settings, screen, stats, sb, ship, aliens, bullets, alienBullets, images)

    # Have the ufo move across the screen
    if ufo is not None and ufo[1].x <= si_settings.screen_width:
        ufo_oscillating(si_settings, screen, ufo)


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def fire_back(si_settings, screen, aliens, alienBullets):
    """Timer that tells the aliens when to fire back."""
    for alien in aliens:
        if randint(0, 100) % 2 == 0:
            new_bullet = Bullet(si_settings, screen, alien, si_settings.alien_direction)
            alienBullets.add(new_bullet)


def ship_explosion(si_settings, screen, ship):
    """Animate the ship explosion."""
    ship.image = pygame.image.load("images/ship_explosion.png")
    explosion_rect = ship.rect

    for i in range(0, 7):
        explosionPart = pygame.transform.chop(ship.image, (i * 64, i * 64, 64, 64))
        screen.fill(si_settings.bg_color)
        screen.blit(explosionPart, explosion_rect)


def create_ufo(si_settings):
    ufo = pygame.image.load("images/ufo.png")
    ufo_rect = ufo.get_rect()
    ufo_rect.x = 0
    ufo_rect.y = si_settings.screen_height/7
    return ufo, ufo_rect


def ufo_oscillating(si_settings, screen, ufo):
    ufo[1].x += si_settings.ship_speed_factor * 3
    screen.blit(ufo[0], (ufo[1].x, ufo[1].y))
    play_sound("audio/ufo_oscillating.wav", 10)


def play_sound(audio, loop=0):
    src = pygame.mixer.Sound(audio)
    pygame.mixer.music.load(audio)
    pygame.mixer.music.play(loop)

