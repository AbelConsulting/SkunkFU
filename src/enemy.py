"""
Enemy character class
"""
import pygame
from config import *
from sprite_loader import sprite_loader, Animation

class Enemy:
    """Base enemy class"""
    
    def __init__(self, x, y, enemy_type="BASIC"):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        
        # Load sprites based on enemy type
        self.load_sprites()
        
        # Set size based on type
        if enemy_type == "BASIC":
            self.width = 48
            self.height = 48
        elif enemy_type == "FLYING":
            self.width = 40
            self.height = 40
        elif enemy_type == "BOSS":
            self.width = 128
            self.height = 128
        else:
            self.width = 50
            self.height = 70
            
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Stats
        self.health = ENEMY_HEALTH
        self.max_health = ENEMY_HEALTH
        self.speed = ENEMY_SPEED
        self.attack_damage = ENEMY_ATTACK_DAMAGE
        self.points = ENEMY_POINTS
        
        # Movement
        self.velocity_x = -self.speed
        self.velocity_y = 0
        self.facing_right = False
        self.patrol_range = 200
        self.start_x = x
        
        # Combat
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_duration = 0.4
        self.attack_cooldown = 1.5
        self.attack_cooldown_timer = 0
        self.attack_range = 60
        self.attack_hitbox = pygame.Rect(0, 0, 50, 40)
        
        # AI state
        self.state = "PATROL"  # PATROL, CHASE, ATTACK
        self.detection_range = 300
        
        # Animation
        self.current_animation = "idle"
        self.animation_timer = 0
    
    def load_sprites(self):
        """Load sprites based on enemy type"""
        prefix = "basic" if self.enemy_type == "BASIC" else "fly" if self.enemy_type == "FLYING" else "boss"
        
        try:
            if self.enemy_type == "BASIC":
                self.sprites = {
                    "idle": sprite_loader.load_sprite(f"enemies/{prefix}_idle.png", (48, 48)),
                    "walk": sprite_loader.load_sprite(f"enemies/{prefix}_walk.png", (48, 48)),
                    "attack": sprite_loader.load_sprite(f"enemies/{prefix}_attack.png", (48, 48)),
                    "hurt": sprite_loader.load_sprite(f"enemies/{prefix}_hurt.png", (48, 48))
                }
            elif self.enemy_type == "FLYING":
                self.sprites = {
                    "idle": sprite_loader.load_sprite(f"enemies/{prefix}_idle.png", (40, 40)),
                    "move": sprite_loader.load_sprite(f"enemies/{prefix}_move.png", (40, 40)),
                    "attack": sprite_loader.load_sprite(f"enemies/{prefix}_attack.png", (40, 40))
                }
            elif self.enemy_type == "BOSS":
                self.sprites = {
                    "idle": sprite_loader.load_sprite(f"enemies/{prefix}_idle.png", (128, 128)),
                    "walk": sprite_loader.load_sprite(f"enemies/{prefix}_walk.png", (128, 128)),
                    "attack1": sprite_loader.load_sprite(f"enemies/{prefix}_attack1.png", (128, 128)),
                    "attack2": sprite_loader.load_sprite(f"enemies/{prefix}_attack2.png", (128, 128)),
                    "special": sprite_loader.load_sprite(f"enemies/{prefix}_special.png", (128, 128))
                }
            print(f"✓ Loaded {self.enemy_type} enemy sprites")
        except Exception as e:
            print(f"Error loading enemy sprites: {e}")
            # Fallback to colored rectangles
            self.sprites = None
    
    def update(self, dt, level, player):
        """Update enemy behavior"""
        # Check player distance
        distance_to_player = abs(self.x - player.x)
        
        # AI state machine
        if distance_to_player < self.attack_range and abs(self.y - player.y) < 50:
            self.state = "ATTACK"
        elif distance_to_player < self.detection_range:
            self.state = "CHASE"
        else:
            self.state = "PATROL"
        
        # Behavior based on state
        if self.state == "PATROL":
            self.patrol(dt)
        elif self.state == "CHASE":
            self.chase(dt, player)
        elif self.state == "ATTACK":
            self.attack_player(dt, player)
        
        # Apply gravity
        self.velocity_y += GRAVITY * dt
        if self.velocity_y > MAX_FALL_SPEED:
            self.velocity_y = MAX_FALL_SPEED
        
        # Update position
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        
        # Ground collision (simplified)
        if self.y >= 500:
            self.y = 500
            self.velocity_y = 0
        
        # Update rect
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # Update attack
        if self.is_attacking:
            self.attack_timer -= dt
            if self.attack_timer <= 0:
                self.is_attacking = False
        
        if self.attack_cooldown_timer > 0:
            self.attack_cooldown_timer -= dt
        
        # Update attack hitbox
        if self.is_attacking:
            if self.facing_right:
                self.attack_hitbox.x = self.rect.right
            else:
                self.attack_hitbox.x = self.rect.left - self.attack_hitbox.width
            self.attack_hitbox.y = self.rect.y + 20
        
        # Update animation state
        self.update_animation_state(dt)
    
    def update_animation_state(self, dt):
        """Update which animation to show"""
        if self.is_attacking:
            self.current_animation = "attack"
        elif abs(self.velocity_x) > 0:
            self.current_animation = "walk" if self.enemy_type != "FLYING" else "move"
        else:
            self.current_animation = "idle"
    
    def patrol(self, dt):
        """Patrol back and forth"""
        # Turn around at patrol boundaries
        if self.x <= self.start_x - self.patrol_range:
            self.velocity_x = self.speed
            self.facing_right = True
        elif self.x >= self.start_x + self.patrol_range:
            self.velocity_x = -self.speed
            self.facing_right = False
    
    def chase(self, dt, player):
        """Chase the player"""
        if player.x > self.x:
            self.velocity_x = self.speed
            self.facing_right = True
        else:
            self.velocity_x = -self.speed
            self.facing_right = False
    
    def attack_player(self, dt, player):
        """Attack the player"""
        self.velocity_x = 0
        
        if self.attack_cooldown_timer <= 0:
            self.is_attacking = True
            self.attack_timer = self.attack_duration
            self.attack_cooldown_timer = self.attack_cooldown
    
    def take_damage(self, damage):
        """Take damage"""
        self.health -= damage
    
    def render(self, screen, camera_x):
        """Render the enemy"""
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y)
        
        # Try to render sprite
        if self.sprites and self.current_animation in self.sprites:
            sprite = self.sprites[self.current_animation]
            
            # Flip sprite if facing left
            if not self.facing_right:
                sprite = pygame.transform.flip(sprite, True, False)
            
            # Center sprite on enemy position
            sprite_rect = sprite.get_rect()
            sprite_rect.center = (screen_x + self.width // 2, screen_y + self.height // 2)
            screen.blit(sprite, sprite_rect)
        else:
            # Fallback to colored rectangles
            color = RED if self.state == "ATTACK" else YELLOW if self.state == "CHASE" else GRAY
            pygame.draw.rect(screen, color, (screen_x, screen_y, self.width, self.height))
        
        # Health bar
        health_ratio = self.health / self.max_health
        bar_width = max(self.width, 50)
        bar_x = screen_x + (self.width - bar_width) // 2
        pygame.draw.rect(screen, RED, (bar_x, screen_y - 10, bar_width, 5))
        pygame.draw.rect(screen, GREEN, (bar_x, screen_y - 10, int(bar_width * health_ratio), 5))
        
        # Attack hitbox when attacking (debug)
        if self.is_attacking and False:  # Set to True to see hitboxes
            hitbox_screen_x = int(self.attack_hitbox.x - camera_x)
            pygame.draw.rect(screen, RED,
                           (hitbox_screen_x, self.attack_hitbox.y,
                            self.attack_hitbox.width, self.attack_hitbox.height), 2)
