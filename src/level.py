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
        # Ground platform (full width)
        self.platforms.append(pygame.Rect(0, 580, self.width, 40))
        
        # Starting area platforms
        self.platforms.append(pygame.Rect(200, 500, 150, 20))
        self.platforms.append(pygame.Rect(400, 420, 180, 20))
        
        # Mid-section with varied heights
        self.platforms.append(pygame.Rect(650, 480, 200, 20))
        self.platforms.append(pygame.Rect(900, 380, 180, 20))
        self.platforms.append(pygame.Rect(1120, 440, 160, 20))
        self.platforms.append(pygame.Rect(1320, 350, 200, 20))
        
        # High platforms section
        self.platforms.append(pygame.Rect(1580, 280, 180, 20))
        self.platforms.append(pygame.Rect(1820, 340, 160, 20))
        
        # Staircase effect
        self.platforms.append(pygame.Rect(2040, 500, 140, 20))
        self.platforms.append(pygame.Rect(2220, 440, 140, 20))
        self.platforms.append(pygame.Rect(2400, 380, 140, 20))
        self.platforms.append(pygame.Rect(2580, 320, 140, 20))
        
        # Final area
        self.platforms.append(pygame.Rect(2760, 400, 240, 20))
    
    def check_collision(self, rect, velocity_y):
        """Check if rect collides with platforms"""
        for platform in self.platforms:
            if rect.colliderect(platform):
                if velocity_y > 0:  # Falling
                    return True, platform.top
        return False, 0
    
    def render(self, screen, camera_x):
        """Render the level"""
        # Sky background with gradient effect
        screen.fill((135, 206, 235))  # Sky blue
        
        # Draw clouds (simple decoration)
        cloud_color = (255, 255, 255, 128)
        
        # Draw platforms
        for platform in self.platforms:
            screen_x = platform.x - camera_x
            
            # Different colors for ground vs floating platforms
            if platform.y >= 580:
                # Ground - grass green
                top_color = (34, 139, 34)
                side_color = (101, 67, 33)
            else:
                # Floating platforms - stone gray
                top_color = (120, 120, 120)
                side_color = (80, 80, 80)
            
            # Draw platform with depth effect
            # Main platform surface
            pygame.draw.rect(screen, top_color,
                           (screen_x, platform.y, platform.width, platform.height))
            
            # Top highlight (lighter)
            highlight_color = tuple(min(255, c + 30) for c in top_color)
            pygame.draw.rect(screen, highlight_color,
                           (screen_x, platform.y, platform.width, 3))
            
            # Side shadow (darker)
            if platform.height > 10:
                pygame.draw.rect(screen, side_color,
                               (screen_x, platform.y + 3, platform.width, platform.height - 3))
            
            # Platform outline
            pygame.draw.rect(screen, BLACK,
                           (screen_x, platform.y, platform.width, platform.height), 2)
