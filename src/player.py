"""
Player character class
"""
import pygame
from config import *
from sprite_loader import sprite_loader

class Player:
    """Player character with combat and platforming abilities"""
    
    def __init__(self, x, y):
        # Position and movement
        self.x = x
        self.y = y
        self.width = 64
        self.height = 64
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Character stats (Ninja Skunk)
        self.name = CHARACTER["name"]
        self.max_health = CHARACTER["health"]
        self.health = self.max_health
        self.speed = CHARACTER["speed"]
        self.jump_force = CHARACTER["jump_force"]
        self.attack_damage = CHARACTER["attack_damage"]
        self.special_ability = CHARACTER["special_ability"]
        self.color = CHARACTER["color"]
        
        # Load sprites
        self.load_sprites()
        
        # Movement state
        self.velocity_x = 0
        self.velocity_y = 0
        self.target_velocity_x = 0
        self.acceleration = 2500  # How fast we reach target speed
        self.friction = 1800  # How fast we slow down
        self.facing_right = True
        self.on_ground = False
        
        # Jump mechanics
        self.coyote_time = 0.15  # Time after leaving ground you can still jump
        self.coyote_timer = 0
        self.jump_buffer_time = 0.1  # Time before landing jump is buffered
        self.jump_buffer_timer = 0
        
        # Combat state
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_duration = 0.3
        self.attack_cooldown = 0.3  # Reduced for faster combos
        self.attack_cooldown_timer = 0
        self.attack_hitbox = pygame.Rect(0, 0, 60, 40)
        
        # Combo system
        self.combo_count = 0
        self.combo_window = 0.4  # Time to continue combo
        self.combo_timer = 0
        self.max_combo = 3
        
        # Hit feedback
        self.hit_stun_timer = 0
        self.invulnerable_timer = 0
        self.invulnerable_duration = 0.5
        
        # Animation state
        self.animation_state = "IDLE"  # IDLE, WALK, JUMP, ATTACK, HURT
        self.animation_frame = 0
        self.animation_timer = 0
        
        # Input
        self.keys = pygame.key.get_pressed()
    
    def load_sprites(self):
        """Load Ninja Skunk sprites"""
        print("Loading Ninja Skunk sprites...")
        try:
            self.sprites = {
                "idle": sprite_loader.load_sprite("characters/ninja_idle.png", (64, 64)),
                "walk": sprite_loader.load_sprite("characters/ninja_walk.png", (64, 64)),
                "jump": sprite_loader.load_sprite("characters/ninja_jump.png", (64, 64)),
                "attack": sprite_loader.load_sprite("characters/ninja_attack.png", (64, 64)),
                "shadow_strike": sprite_loader.load_sprite("characters/ninja_shadow_strike.png", (64, 64)),
                "hurt": sprite_loader.load_sprite("characters/ninja_hurt.png", (64, 64))
            }
            print(f"✓ Loaded {len(self.sprites)} Ninja Skunk sprites")
        except Exception as e:
            print(f"Warning: Could not load player sprites: {e}")
            self.sprites = None
    
    def handle_event(self, event):
        """Handle player input events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Jump buffering - remember jump input
                self.jump_buffer_timer = self.jump_buffer_time
            elif event.key == pygame.K_x:
                self.attack()
            elif event.key == pygame.K_z:
                self.special_attack()
    
    def update(self, dt, level):
        """Update player state"""
        self.keys = pygame.key.get_pressed()
        
        # Update timers
        if self.coyote_timer > 0:
            self.coyote_timer -= dt
        if self.jump_buffer_timer > 0:
            self.jump_buffer_timer -= dt
        if self.combo_timer > 0:
            self.combo_timer -= dt
        else:
            self.combo_count = 0  # Reset combo if timer expires
        if self.hit_stun_timer > 0:
            self.hit_stun_timer -= dt
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= dt
        
        # Determine target velocity based on input (no movement during hit stun)
        self.target_velocity_x = 0
        if self.hit_stun_timer <= 0:
            if self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]:
                self.target_velocity_x = -self.speed
                self.facing_right = False
            if self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d]:
                self.target_velocity_x = self.speed
                self.facing_right = True
        
        # Smooth acceleration/deceleration
        if self.target_velocity_x != 0:
            # Accelerate towards target
            if abs(self.velocity_x) < abs(self.target_velocity_x):
                self.velocity_x += (self.target_velocity_x / abs(self.target_velocity_x)) * self.acceleration * dt
                # Clamp to target
                if abs(self.velocity_x) > abs(self.target_velocity_x):
                    self.velocity_x = self.target_velocity_x
            else:
                # Already at or above target, match it
                self.velocity_x = self.target_velocity_x
        else:
            # Apply friction when no input
            if abs(self.velocity_x) > 0:
                friction_amount = self.friction * dt
                if abs(self.velocity_x) <= friction_amount:
                    self.velocity_x = 0
                else:
                    self.velocity_x -= (self.velocity_x / abs(self.velocity_x)) * friction_amount
        
        # Check if we just left the ground (for coyote time)
        was_on_ground = self.on_ground
        
        # Apply gravity
        self.velocity_y += GRAVITY * dt
        if self.velocity_y > MAX_FALL_SPEED:
            self.velocity_y = MAX_FALL_SPEED
        
        # Update position
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        
        # Collision with ground
        if self.y >= 500:  # Temporary ground level
            self.y = 500
            self.velocity_y = 0
            self.on_ground = True
        else:
            self.on_ground = False
        
        # Update coyote timer
        if was_on_ground and not self.on_ground:
            self.coyote_timer = self.coyote_time
        elif self.on_ground:
            self.coyote_timer = 0
        
        # Handle jump buffering - try to jump if we buffered a jump and just landed
        if self.jump_buffer_timer > 0 and (self.on_ground or self.coyote_timer > 0):
            self.jump()
            self.jump_buffer_timer = 0
        
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
        self.update_animation_state()
    
    def update_animation_state(self):
        """Update current animation state"""
        if self.is_attacking:
            self.animation_state = "ATTACK"
        elif not self.on_ground:
            self.animation_state = "JUMP"
        elif self.velocity_x != 0:
            self.animation_state = "WALK"
        else:
            self.animation_state = "IDLE"
    
    def jump(self):
        """Make the player jump"""
        if self.on_ground or self.coyote_timer > 0:
            self.velocity_y = -self.jump_force
            self.on_ground = False
            self.coyote_timer = 0  # Used up coyote time
    
    def attack(self):
        """Perform basic attack with combo system"""
        if self.attack_cooldown_timer <= 0 and not self.is_attacking:
            self.is_attacking = True
            self.attack_timer = self.attack_duration
            self.attack_cooldown_timer = self.attack_cooldown
            
            # Combo system
            if self.combo_timer > 0 and self.combo_count < self.max_combo:
                self.combo_count += 1
            else:
                self.combo_count = 1
            self.combo_timer = self.combo_window
            
            # Scale damage with combo
            combo_multiplier = 1 + (self.combo_count - 1) * 0.2
            self.current_attack_damage = int(self.attack_damage * combo_multiplier)
    
    def special_attack(self):
        """Perform Shadow Strike - fast dash attack"""
        if not self.is_attacking and self.on_ground:
            self.is_attacking = True
            self.attack_timer = self.attack_duration
            self.attack_cooldown_timer = self.attack_cooldown
            
            # Dash forward
            dash_distance = 150
            if self.facing_right:
                self.x += dash_distance
            else:
                self.x -= dash_distance
            
            # Larger hitbox for special
            self.attack_hitbox.width = 80
            self.attack_hitbox.height = 60
    
    def take_damage(self, damage):
        """Take damage from enemy"""
        if self.invulnerable_timer <= 0:  # Only take damage if not invulnerable
            self.health -= damage
            if self.health < 0:
                self.health = 0
            
            # Apply hit stun and invulnerability
            self.hit_stun_timer = 0.2
            self.invulnerable_timer = self.invulnerable_duration
            
            # Knockback
            self.velocity_x = -200 if self.facing_right else 200
            self.velocity_y = -300
    
    def reset(self):
        """Reset player to starting state"""
        self.x = 100
        self.y = 500
        self.health = self.max_health
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_attacking = False
    
    def render(self, screen, camera_x):
        """Render the player"""
        # Calculate screen position
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y)
        
        # Determine which sprite to show
        sprite_key = "idle"
        if self.is_attacking:
            sprite_key = "shadow_strike" if self.attack_hitbox.width > 60 else "attack"
        elif not self.on_ground:
            sprite_key = "jump"
        elif abs(self.velocity_x) > 0:
            sprite_key = "walk"
        
        # Try to render sprite
        if self.sprites and sprite_key in self.sprites:
            sprite = self.sprites[sprite_key]
            
            # Flip sprite if facing left
            if not self.facing_right:
                sprite = pygame.transform.flip(sprite, True, False)
            
            # Center sprite on player position
            sprite_rect = sprite.get_rect()
            sprite_rect.center = (screen_x + self.width // 2, screen_y + self.height // 2)
            screen.blit(sprite, sprite_rect)
        else:
            # Fallback to colored rectangle
            pygame.draw.rect(screen, self.color, (screen_x, screen_y, self.width, self.height))
            
            # Health indicator overlay
            if self.health < 30:
                overlay_color = RED if self.health < 15 else YELLOW
                overlay = pygame.Surface((self.width, self.height))
                overlay.set_alpha(100)
                overlay.fill(overlay_color)
                screen.blit(overlay, (screen_x, screen_y))
        
        # Direction indicator (for placeholder mode)
        if not self.sprites:
            if self.facing_right:
                pygame.draw.circle(screen, BLACK, (screen_x + self.width - 10, screen_y + 20), 5)
            else:
                pygame.draw.circle(screen, BLACK, (screen_x + 10, screen_y + 20), 5)
        
        # Draw attack hitbox (debug - set to True to see hitboxes)
        if self.is_attacking and False:
            hitbox_screen_x = int(self.attack_hitbox.x - camera_x)
            pygame.draw.rect(screen, RED, 
                           (hitbox_screen_x, self.attack_hitbox.y, 
                            self.attack_hitbox.width, self.attack_hitbox.height), 2)
