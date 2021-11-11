from dataclasses import dataclass
import pygame, pytmx, pyscroll

@dataclass
class Portal:
    from_world: str
    origin_point : str
    target_world: str
    teleport_point: str 


@dataclass
class Map:
    name:  str
    walls : list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]


class MapManager:
    
    def __init__(self,screen, player) -> None:
        self.maps = dict() # "house" -> Map("house", wall, group)
        self.screen = screen
        self.player = player
        self.current_map ="world"
        
        self.register_map("world", portals =[
            Portal(from_world="world", origin_point="enter_house", target_world="house", teleport_point="spawn_house"),
            Portal(from_world="world", origin_point="enter_house2", target_world="house2", teleport_point="spawn_house")
        ])
        
        self.register_map("house", portals = [
            Portal(from_world="house", origin_point="exit_house", target_world="world", teleport_point="enter_house_exit")
        ])
        
        self.register_map("house2", portals = [
            Portal(from_world="house2", origin_point="exit_house", target_world="world", teleport_point="exit_house2")
        ])
        
        self.teleport_player("player")
        
    def check_collisions(self):
        # portails
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point. width, point.height)
                
                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)
                    
                    
            
        #colision avec les mur
        for sprite in self.get_group().sprites():
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()
            
        
    
    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()
    
    def register_map(self, name, portals=[]):
      # charger la carte
        tmx_data = pytmx.util_pygame.load_pygame(f"../map/{name}.tmx")  
        map_data = pyscroll.data.TiledMapData(tmx_data) 
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2
        
        
        
        # definir une liste qui stocke les rectangle de collision
        walls = []
        
        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            
        # dessiner le  groupe  de calque
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        group.add(self.player)
        
        #Enregister la nouvelle carte chargée
        self.maps[name] =  Map(name, walls, group, tmx_data, portals)
        
        
    def get_map(self) : return self.maps[self.current_map]
    
    def get_group(self): return self.get_map().group
    
    def get_walls(self): return  self.get_map().walls
    
    def get_object(self, name) : return self.get_map().tmx_data.get_object_by_name(name)
    
    
    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)
        
    def update(self):
        self.get_group().update()
        self.check_collisions()