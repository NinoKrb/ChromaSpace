import pygame
import os
import random

class Settings(object):
    window_height = 1000
    window_width = 700

    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "Storage/Images/")
    path_font = os.path.join(path_file, "Storage/Fonts/")
    title = "ChromaSpace - The Game"

    spaceship_size = (75, 104)
    spaceship_speed_x = 8
    spaceship_speed_y = 8
    spaceship_lives = 3
    spaceship_teleports = 3
    spaceship_spawnpoint = (window_height - window_height / 4,window_width // 2 - spaceship_size[0] // 2)

    asteroid_counter_delay = 100
    max_asteroid_counter_delay = 50
    max_asteroid_size_multiplier = 2
    asteroid_default_speed_y = 5
    asteroid_size = (54, 45)

    bonus_size = (35, 35)
    bonus_counter_delay = 400
    bonus_heart_ration = (1, 10)

    point_text = (25, 25)
    click_to_start_alpha_speed = 0.7
    font_color = (70, 108, 255)
    font_color_warning = (255, 70, 70)
    show_no_teleports_counter_delay = 250

    clock = 60


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.update_sprite()
        self.direction = "up"
        self.special_teleport_mask = False
        self.teleport_to_spawnpoint()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update_sprite(self):          # Update the Spaceship sprite
        self.image = pygame.image.load(os.path.join(Settings.path_image, self.filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.spaceship_size)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, direction):             # Move the Spaceship by the current direction
        self.direction = direction
        if self.direction == "up":
            new_pos = self.rect.top - Settings.spaceship_speed_y
            if new_pos >= 0:
                self.rect.top = new_pos

        elif self.direction == "down":
            new_pos = self.rect.top + Settings.spaceship_speed_y
            if new_pos + Settings.spaceship_size[1] <= Settings.window_height:
                self.rect.top = new_pos

        elif self.direction == "left":
            new_pos = self.rect.left - Settings.spaceship_speed_x
            if new_pos >= 0:
                self.rect.left = new_pos

        elif self.direction == "right":
            new_pos = self.rect.left + Settings.spaceship_speed_x
            if new_pos + Settings.spaceship_size[0] <= Settings.window_width:
                self.rect.left = new_pos

        self.update_coords()

    def update_coords(self):    # Update the coords of the Spaceship for backup
        self.y = self.rect.top
        self.x = self.rect.left

    def sync_rect_coords(self):    # Sync the backup coords with the Spaceship rect coords
        self.rect.top = self.y
        self.rect.left = self.x

    # Teleport the spaceship to the default spawnpoint
    def teleport_to_spawnpoint(self):
        self.rect.top = Settings.spaceship_spawnpoint[0]
        self.rect.left = Settings.spaceship_spawnpoint[1]
        self.update_coords()

    # Teleport the spaceship to a custom coordinate
    def teleport_to_coords(self, x, y):
        self.rect.top = y
        self.rect.left = x
        self.update_coords()

    # Bonus Task: Special Teleporting
    # It works by enlarging the spaceship sprite and thus clearing a radius around the actual sprite
    def special_teleport(self):
        if game.teleports - 1 >= 0:
            game.teleports -= 1
            self.update_coords()
            random_x = random.randint(0, int(Settings.window_width - Settings.spaceship_size[0]))
            random_y = random.randint(0, int(Settings.window_height - Settings.spaceship_size[1]))

            self.image = pygame.transform.scale(self.image, (Settings.spaceship_size[0] * 4, Settings.spaceship_size[1] * 4))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)

            self.teleport_to_coords(random_x - (Settings.spaceship_size[0] * 4) // 2, random_y - (Settings.spaceship_size[1] * 4) // 2)
            pygame.sprite.spritecollide(self, game.asteroids, True)

            self.image = pygame.transform.scale(self.image, Settings.spaceship_size)
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)

            self.teleport_to_coords(random_x, random_y)
        else:
            game.show_no_teleports = True
        

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, filename, multiplier):
        super().__init__()
        self.speed = random.uniform(1 * multiplier, 3 * multiplier)
        self.size_multiplier = random.uniform(1, Settings.max_asteroid_size_multiplier)
        self.update_sprite(filename)
        self.rect.left = random.randint(0, int(Settings.window_width - Settings.asteroid_size[0] * self.size_multiplier))
        self.rect.top = 0 - (Settings.asteroid_size[1] * self.size_multiplier)

    def update_sprite(self, filename):          # Update the asteroid sprite
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (Settings.asteroid_size[0] * self.size_multiplier, Settings.asteroid_size[1] * self.size_multiplier))
        self.rect = self.image.get_rect()

    def update(self):
        # Move the asteroid in direction to the bottom
        self.rect.top += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Bonus(pygame.sprite.Sprite):
    def __init__(self, filename, type):
        super().__init__()
        self.type = type
        self.speed = random.randint(1, 4)
        self.update_sprite(filename)
        self.rect.left = random.randint(0, Settings.window_width - Settings.bonus_size[0])
        self.rect.top = 0 - Settings.bonus_size[1]

    def update_sprite(self, filename):          # Update the bonus sprite
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.bonus_size)
        self.rect = self.image.get_rect()

    def update(self):
        # Move the bonus in direction to the bottom
        self.rect.top += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Background(pygame.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert()
        pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Game(object):
    def __init__(self):
        super().__init__()
        pygame.init()
        # Pygame essential settings
        pygame.display.set_caption(Settings.title)

        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.clock = pygame.time.Clock()

        # Define Sprites & Spritegroups
        self.background = Background("background-space.png")
        self.spaceship = Spaceship("spaceship.png")

        self.asteroids = pygame.sprite.Group()
        self.bonuses = pygame.sprite.Group()

        # Set default game values
        self.alpha_counter = 0
        self.alpha_direction = "down"

        self.running = True
        self.collided = False
        self.pause_menu = True
        self.game_over = False

        # Set fonts for the game overlay
        self.font = pygame.font.Font(os.path.join(Settings.path_font, "ChubbyChoo-Regular.ttf"), 30)
        self.overlay_font = pygame.font.Font(os.path.join(Settings.path_font, "ChubbyChoo-Regular.ttf"), 50)

        # Reset the game stats
        self.reset_stats()

    def run(self):  # Main game loop
        while self.running:
            self.clock.tick(Settings.clock)
            if self.game_over == False:
                if self.pause_menu == False:
                    self.watch_for_control_events()
                    self.update()

            self.watch_for_events()
            self.update_overlay()
            self.draw()

    def draw(self):  # Draw all sprites
        self.background.draw(self.screen)
        self.spaceship.draw(self.screen)
        self.asteroids.draw(self.screen)
        self.bonuses.draw(self.screen)
        self.update_overlay()
        pygame.display.flip()

    def update_overlay(self):
        if self.game_over == True or self.pause_menu == True:
            # Set Overlay title
            if self.game_over:
                header_text = "Game Over"
            if self.pause_menu:
                header_text = "Welcome to"

            header_text = self.overlay_font.render(header_text, True, Settings.font_color)
            self.screen.blit(header_text, (Settings.window_width // 2 - header_text.get_rect().centerx, 25))

            # Load Logo
            logo = pygame.image.load(os.path.join(Settings.path_image, "ChromaSpaceLogo.png")).convert_alpha()
            logo = pygame.transform.scale(logo, (604, 118))
            self.screen.blit(logo, ((Settings.window_width // 2 - logo.get_rect().centerx), 75))

            if self.game_over:
                score_text = self.font.render(f"Your score: {self.stats_points}", True, Settings.font_color)
                self.screen.blit(score_text, ((Settings.window_width // 2 -score_text.get_rect().centerx), 75 + logo.get_rect().bottom))

            # Loading "click to start" text
            click_to_start = pygame.image.load(os.path.join(Settings.path_image, "ClickToStart.png")).convert_alpha()
            click_to_start = pygame.transform.scale(click_to_start, (351, 85))

            # Fade Animation for the "click to start" text
            if self.alpha_counter >= 99:
                self.alpha_direction = "down"
            elif self.alpha_counter <= 1:
                self.alpha_direction = "up"

            if self.alpha_direction == "up":
                self.alpha_counter += Settings.click_to_start_alpha_speed
            else:
                self.alpha_counter -= Settings.click_to_start_alpha_speed

            click_to_start.set_alpha(self.alpha_counter)
            self.screen.blit(click_to_start, (Settings.window_width // 2 - click_to_start.get_rect().centerx, Settings.window_height // 2))

        else:
            # Hud/Stats Rendering

            # Render Points
            points = self.font.render(f"{self.stats_points} Points", True, Settings.font_color)
            self.screen.blit(points, Settings.point_text)

            # Render Lives
            lives = self.font.render(f"{self.lives} Lives", True, Settings.font_color)
            self.screen.blit(lives, (Settings.point_text[0], Settings.point_text[1] * 2))

            # Render Teleports
            teleports = self.font.render(f"{self.teleports} Teleports", True, Settings.font_color)
            self.screen.blit(teleports, (Settings.point_text[0], Settings.point_text[1] * 3))

            if self.show_no_teleports == True:
                self.show_no_teleports_counter += 1

                if self.show_no_teleports_counter >= Settings.show_no_teleports_counter_delay:
                    self.show_no_teleports = False
                    self.show_no_teleports_counter = 0

                self.show_no_teleports_text = self.font.render("You have no Teleports left", True, Settings.font_color_warning)
                self.screen.blit(self.show_no_teleports_text, (Settings.window_width // 2 - self.show_no_teleports_text.get_rect().centerx, Settings.window_height - Settings.window_height // 4))



    def update(self):
        # Update the spawn counters
        self.asteroid_counter += 1
        self.bonus_counter += 1

        # Asteroid collision check
        if pygame.sprite.spritecollide(self.spaceship, self.asteroids, False) and self.collided == False:
            for asteroid in self.asteroids:
                if pygame.sprite.collide_mask(self.spaceship, asteroid):
                    self.lives -= 1
                    self.collided = True

                    if self.lives <= 0:
                        self.game_over = True

                    self.spaceship.teleport_to_spawnpoint()
                    self.asteroids.empty()
                    self.bonuses.empty()
                    self.collided = False

         # Bonus collision check
        if pygame.sprite.spritecollide(self.spaceship, self.bonuses, False) and self.collided == False:
            for bonus in self.bonuses:
                if pygame.sprite.collide_mask(self.spaceship, bonus):
                    self.collided = True
                    if bonus.type == "gem":
                        self.stats_points += 10
                    if bonus.type == "heart":
                        self.lives += 1
                    self.bonuses.remove(bonus)
                    self.collided = False

        # Update Asteroids & check window collisions
        for asteroid in self.asteroids:
            asteroid.update()

            if asteroid.rect.top >= Settings.window_height:
                self.asteroids.remove(asteroid)
                self.stats_points += 1

        # Update Bonuss & check window collisions
        for bonus in self.bonuses:
            bonus.update()

            if bonus.rect.top >= Settings.window_height:
                self.bonuses.remove(bonus)

        # Check Asteroid delay
        if self.asteroid_counter >= self.asteroid_counter_delay:
            multiplier = 1 + self.asteroid_counter_speed
            self.asteroids.add(Asteroid("asteroid.png", multiplier))
            self.asteroid_counter = 0

            # Reduce the asteroid spawn delay
            if self.asteroid_counter_delay >= Settings.max_asteroid_counter_delay:
                self.asteroid_counter_delay -= 0.5
                self.asteroid_counter_speed += 0.012

        # Check Bonus delay
        if self.bonus_counter >= Settings.bonus_counter_delay:
            if random.randint(Settings.bonus_heart_ration[0], Settings.bonus_heart_ration[1]) < Settings.bonus_heart_ration[1]:
                self.bonuses.add(Bonus("blue-gem.png", "gem"))
            else:
                self.bonuses.add(Bonus("red-gem.png", "heart"))
            self.bonus_counter = 0

    def reset_stats(self):  # Reset the player stats
        self.stats_points = 0
        self.asteroid_counter = 0
        self.bonus_counter = 0
        self.asteroid_counter_speed = 0
        self.asteroid_counter_delay = Settings.asteroid_counter_delay
        self.lives = Settings.spaceship_lives
        self.teleports = Settings.spaceship_teleports
        self.show_no_teleports = False
        self.show_no_teleports_counter = 0

    def reset_game(self):
        self.reset_stats()
        self.game_over = False

    def watch_for_events(self):  # Check all essential press events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over == True:
                    self.reset_game()

                elif self.pause_menu == True:
                    self.pause_menu = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.pause_menu = not self.pause_menu

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if self.pause_menu == False and self.game_over == False:
                        self.spaceship.special_teleport()

    def watch_for_control_events(self):  # Check for control press events
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w] or pressed[pygame.K_UP]:
            self.spaceship.move("up")

        if pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
            self.spaceship.move("down")

        if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
            self.spaceship.move("right")

        if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
            self.spaceship.move("left")

        if pressed[pygame.K_ESCAPE]:
            self.running = False


if __name__ == '__main__':
    os.environ['SDL_VIDEO_WINDOW_POS'] = '1'
    game = Game()
    game.run()
