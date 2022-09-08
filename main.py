from game.utils import *
from game.player import Player

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Catch the Ketchup!')
        self.clock = pygame.time.Clock()
        self.fader = Fader()
        self.game_start = False
        self.running = 1
    
    def run(self):
        bg = ParallaxBG(load_texture("title", "bg.png"))
        planet = pygame.transform.scale(load_texture("red_planet.png"), (300, 300)).convert_alpha()
        title = ScaledSprite(load_texture("title", "title.png"))
        title2 = ScaledSprite(load_texture("title", "title2.png"))
        angle = 0

        self.fader.start(3)
        while self.running:
            bg.draw()
            if self.game_start:
                self.player.update_player()
            else:
                blit_rotate_center(SCREEN, planet, (810, 470), angle)
                SCREEN.blit(title.image, (SCREEN_CENTERX - title.image.get_width() / 2, 230 - title.image.get_height() / 2 + 10 * sin(angle / 20)))
                SCREEN.blit(title2.image, (SCREEN_CENTERX - title2.image.get_width() / 2, SCREEN_HEIGHT - 100 - title2.image.get_height() / 2 + 5 * sin(1.5 + angle / 20)))
                angle += 0.5
    
            if (self.fader.fading == False and self.fader.has_ended() and not self.game_start):
                del planet, title, title2, angle
                self.game_start = True
                self.player = Player()
                self.fader.start(1)
            
            self.fader.update()
            self.event_handler()
            pygame.display.update()
            self.clock.tick(FPS)
        pygame.quit()
        exit(0)
    
    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = 0
            else:
                if self.game_start:
                    if self.fader.has_ended() and event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                        self.player.key_handler(event)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.fader.start(3, False)

if __name__ == "__main__":
    Game().run()