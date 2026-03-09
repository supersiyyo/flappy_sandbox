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

    def step(self, action=0):
        """Advances physics by one frame. Returns (obs, reward, done, info)."""
        if self.game_over:
            return self._get_observation(), 0, True, {}

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
        
        # Reward is usually 1 for staying alive, plus any score gains (which are handled implicitly if we just survive, or we return 1 per step)
        # Using 1 per step to encourage surviving.
        reward = 1.0 if not self.game_over else -1.0
        
        return self._get_observation(), reward, self.game_over, {"score": self.score}

    def _get_observation(self):
        """Returns [bird_y, bird_velocity, dist_to_next_pipe, next_pipe_gap_y]"""
        bird_y = self.bird.rect.y
        bird_velocity = self.bird.velocity
        
        # Find the closest pipe in front of the bird
        closest_pipe = None
        for pipe in self.pipes:
            if pipe.x + self.settings.PIPE_WIDTH > self.bird.rect.x:
                closest_pipe = pipe
                break
                
        if closest_pipe:
            dist_to_next_pipe = closest_pipe.x - self.bird.rect.x
            next_pipe_gap_y = closest_pipe.gap_y
        else:
            # Fallbacks if no pipe is spawned yet or weird state
            dist_to_next_pipe = self.settings.SCREEN_WIDTH
            next_pipe_gap_y = self.settings.SCREEN_HEIGHT // 2
            
        return [bird_y, bird_velocity, dist_to_next_pipe, next_pipe_gap_y]

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
