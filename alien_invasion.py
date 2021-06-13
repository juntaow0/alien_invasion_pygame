import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self) -> None:
        """initialize the game, and create game resources"""
        pygame.init()
        self.settings = Settings()

        #self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()
            # make the most recently drawn screen visible
            pygame.display.flip()

    def _check_events(self):
        # watch for keyboard and mouse events
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    sys.exit()
                elif event.type==pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type==pygame.KEYUP:
                    self._check_keyup_events(event)
    
    def _check_keydown_events(self,event):
        """respond to key press events"""
        if event.key == pygame.K_RIGHT:
            # move ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key==pygame.K_q:
            sys.exit()
        elif event.key==pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        """respond to key up events"""
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """update bullet position and remove old bullets"""

        # update bullet positions
        self.bullets.update()
        # get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)
        
        # check for any bullet that have hit aliens and remove it
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """respond to bullet-alien collisions"""
        # remove any bullet and alien that have collided
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            # destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()


    def _create_alien(self, alien_number, row_number):
        """create am alien and place it in the row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2*alien_width*alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2*alien_height*row_number
        self.aliens.add(alien)

    def _create_fleet(self):
        """create the fleet of aliens"""
        # create an alien and find the number of aliens in a row
        # space = one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2*alien_width)
        num_aliens_x = available_space_x//(2*alien_width)

        #determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height-3*alien_height-ship_height)
        num_rows = available_space_y//(2*alien_height)

        # create the fleet of aliens
        for row_number in range(num_rows):
            for alien_number in range(num_aliens_x):
                self._create_alien(alien_number, row_number)

    def _check_fleet_edges(self):
        """respond appropriately if any alien have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
        
    def _change_fleet_direction(self):
        """drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1
            
    def _update_aliens(self):
        """update the positions of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()
    
    def _update_screen(self):
        # Redraw screen
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

if __name__ == '__main__':
    # make game instance and run game
    ai = AlienInvasion()
    ai.run_game()