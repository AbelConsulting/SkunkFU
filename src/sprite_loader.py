"""
Sprite loader and animation handler
"""
import pygame
import os

class SpriteLoader:
    """Utility class for loading and managing sprites"""
    
    def __init__(self):
        self.sprites = {}
        self.base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sprites")
    
    def load_sprite(self, path, scale=None):
        """Load a single sprite image"""
        try:
            full_path = os.path.join(self.base_path, path)
            image = pygame.image.load(full_path).convert_alpha()
            if scale:
                image = pygame.transform.scale(image, scale)
            return image
        except pygame.error as e:
            print(f"Warning: Could not load sprite {path}: {e}")
            # Return a colored rectangle as fallback
            surf = pygame.Surface((50, 50))
            surf.fill((255, 0, 255))  # Magenta to indicate missing sprite
            return surf
    
    def load_spritesheet(self, path, frame_width, frame_height, num_frames, scale=None):
        """Load a sprite sheet and split it into frames"""
        try:
            full_path = os.path.join(self.base_path, path)
            sheet = pygame.image.load(full_path).convert_alpha()
            frames = []
            
            for i in range(num_frames):
                frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                frame.blit(sheet, (0, 0), (i * frame_width, 0, frame_width, frame_height))
                if scale:
                    frame = pygame.transform.scale(frame, scale)
                frames.append(frame)
            
            return frames
        except pygame.error as e:
            print(f"Warning: Could not load spritesheet {path}: {e}")
            # Return placeholder frames
            surf = pygame.Surface((frame_width, frame_height))
            surf.fill((255, 0, 255))
            return [surf]


class Animation:
    """Handles sprite animation"""
    
    def __init__(self, frames, frame_duration=0.1, loop=True):
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
        self.current_frame = 0
        self.timer = 0
        self.finished = False
    
    def update(self, dt):
        """Update animation"""
        if self.finished and not self.loop:
            return
        
        self.timer += dt
        if self.timer >= self.frame_duration:
            self.timer = 0
            self.current_frame += 1
            
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True
    
    def get_current_frame(self):
        """Get the current frame image"""
        return self.frames[self.current_frame]
    
    def reset(self):
        """Reset animation to start"""
        self.current_frame = 0
        self.timer = 0
        self.finished = False


# Global sprite loader instance
sprite_loader = SpriteLoader()
