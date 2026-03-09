import pygame

class Bird(pygame.sprite.Sprite):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.rect = pygame.Rect(
            self.settings.BIRD_X,
            self.settings.SCREEN_HEIGHT // 2,
            self.settings.BIRD_WIDTH,
            self.settings.BIRD_HEIGHT
        )
        self.velocity = 0.0

    def flap(self):
        """Applies upward flap strength."""
        self.velocity = self.settings.FLAP_STRENGTH

    def apply_physics(self):
        """Updates physics strictly based on settings."""
        self.velocity += self.settings.GRAVITY
        if self.velocity > self.settings.MAX_VELOCITY:
            self.velocity = self.settings.MAX_VELOCITY
        self.rect.y += int(self.velocity)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, settings, x, gap_y):
        super().__init__()
        self.settings = settings
        self.x = float(x)
        self.gap_y = gap_y
        
        # Top pipe
        self.top_rect = pygame.Rect(
            self.x,
            0,
            self.settings.PIPE_WIDTH,
            self.gap_y
        )
        
        # Bottom pipe
        self.bottom_rect = pygame.Rect(
            self.x,
            self.gap_y + self.settings.PIPE_GAP_SIZE,
            self.settings.PIPE_WIDTH,
            self.settings.SCREEN_HEIGHT - (self.gap_y + self.settings.PIPE_GAP_SIZE)
        )
        self.passed = False

    def apply_physics(self):
        """Moves the pipe strictly based on settings."""
        self.x -= self.settings.PIPE_SPEED
        self.top_rect.x = int(self.x)
        self.bottom_rect.x = int(self.x)
