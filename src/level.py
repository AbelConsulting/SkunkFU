"""
Level class - Handles platforms and level layout
"""
import pygame
from config import *

class Level:
    """Game level with platforms and decorations"""
    
    def __init__(self, screen_width, screen_height):
        self.width = 3000  # Total level width
        self.height = screen_height
        self.platforms = []
        
        # Create platforms
        self.create_platforms()
    
    def create_platforms(self):
        """Create platform layout"""
        # Ground
        self.platforms.append(pygame.Rect(0, 580, self.width, 40))
        
        # Floating platforms
        self.platforms.append(pygame.Rect(300, 480, 200, 20))
        self.platforms.append(pygame.Rect(600, 400, 200, 20))
        self.platforms.append(pygame.Rect(900, 350, 200, 20))
        self.platforms.append(pygame.Rect(1200, 450, 200, 20))
        self.platforms.append(pygame.Rect(1500, 380, 250, 20))
        self.platforms.append(pygame.Rect(1800, 420, 200, 20))
        self.platforms.append(pygame.Rect(2100, 360, 200, 20))
        self.platforms.append(pygame.Rect(2400, 440, 200, 20))
    
    def check_collision(self, rect, velocity_y):
        """Check if rect collides with platforms"""
        for platform in self.platforms:
            if rect.colliderect(platform):
                if velocity_y > 0:  # Falling
                    return True, platform.top
        return False, 0
    
    def render(self, screen, camera_x):
        """Render the level"""
        # Sky background
        screen.fill((100, 180, 255))
        
        # Draw ground and platforms
        for platform in self.platforms:
            screen_x = platform.x - camera_x
            color = (100, 200, 100) if platform.y >= 580 else (139, 69, 19)
            pygame.draw.rect(screen, color, 
                           (screen_x, platform.y, platform.width, platform.height))
            
            # Platform outline
            pygame.draw.rect(screen, BLACK,
                           (screen_x, platform.y, platform.width, platform.height), 2)
