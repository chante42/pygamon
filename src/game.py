import pygame
from pygame.constants import K_DOWN
import pytmx
import pyscroll
from map import MapManager
from player import Player



class Game:
    def __init__(self) -> None:

        # creer la fenetre du jeux
        self.screen = pygame.display.set_mode((800,600))
        pygame.display.set_caption("Pygamon - Aventure") 
        
        # genere un joureur
        self.player = Player()
        
        self.map_manager = MapManager(self.screen, self.player)
    
        
    def handle_input(self):
        pressed = pygame.key.get_pressed()
        
        if pressed[pygame.K_UP]:
            self.player.move_up()
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
        elif  pressed[pygame.K_LEFT]:
            self.player.move_left()
        elif  pressed[pygame.K_RIGHT]:
            self.player.move_right()
        
    
        
    def update(self):
        self.map_manager.update()
        
                    
            
    def run(self):

        clock = pygame.time.Clock()
        
        # boucle du jeux
        running = True 

        while running: 
            
            self.player.save_location()
            self.handle_input()
            self.update()
            self.map_manager.draw()
            pygame.display.flip()
            
            for event in pygame.event.get() :
                if event.type == pygame.QUIT:
                    running = False 

        clock.tick(40)
        pygame.quit()