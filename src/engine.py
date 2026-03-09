import random
from .entities import Bird, Pipe

class GameEnvironment:
    """Handles ONLY physics and math, decoupling strict logic from rendering."""
    def __init__(self, settings):
        self.settings = settings
        self.reset()
        
    def reset(self):
        self.bird = Bird(self.settings)
        self.pipes = []
        self.frame_count = 0
        self.score = 0
        self.game_over = False
        self._spawn_pipe()

    def _spawn_pipe(self):
        # Ensure a minimum height for top and bottom pipes
        min_gap_y = 50
        max_gap_y = self.settings.SCREEN_HEIGHT - self.settings.PIPE_GAP_SIZE - 50
        max_gap_y = max(min_gap_y, max_gap_y) 
        gap_y = random.randint(min_gap_y, max_gap_y)
        self.pipes.append(Pipe(self.settings, self.settings.SCREEN_WIDTH, gap_y))

    def update(self, action=0):
        """Advances physics by one frame."""
        if self.game_over:
            return

        # Handle Action (1 = Jump, 0 = Do nothing)
        if action == 1:
            self.bird.flap()

        # Update Bird Movement
        self.bird.apply_physics()

        # Update Pipes
        self.frame_count += 1
        if self.frame_count >= self.settings.PIPE_SPAWN_FREQUENCY:
            self._spawn_pipe()
            self.frame_count = 0

        # Update and score logic
        for pipe in self.pipes:
            pipe.apply_physics()
            
            # Score
            if not pipe.passed and pipe.x + self.settings.PIPE_WIDTH < self.bird.rect.x:
                pipe.passed = True
                self.score += 1

        # Culling
        self.pipes = [pipe for pipe in self.pipes if pipe.x + self.settings.PIPE_WIDTH > 0]

        self._check_collisions()

    def _check_collisions(self):
        """Detects precise bounding box collisions."""
        # Floor & Ceiling Check
        if self.bird.rect.top <= 0 or self.bird.rect.bottom >= self.settings.SCREEN_HEIGHT:
            self.game_over = True
            return

        # AABB Pipe Check
        for pipe in self.pipes:
            if self.bird.rect.colliderect(pipe.top_rect) or self.bird.rect.colliderect(pipe.bottom_rect):
                self.game_over = True
                return
