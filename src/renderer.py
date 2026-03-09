import pygame

class Renderer:
    """Handles Pygame drawing and display logic ONLY."""
    def __init__(self, settings):
        self.settings = settings
        pygame.init()
        self.screen = pygame.display.set_mode((self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT))
        pygame.display.set_caption("God Mode AI Sandbox: Flappy Bird Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

    def draw(self, engine):
        """Takes engine state and draws it entirely visually."""
        self.screen.fill((135, 206, 235))  # Sky blue

        # Draw pipes
        for pipe in engine.pipes:
            pygame.draw.rect(self.screen, (34, 139, 34), pipe.top_rect)    # Forest green
            pygame.draw.rect(self.screen, (34, 139, 34), pipe.bottom_rect)
            
        # Draw bird
        pygame.draw.rect(self.screen, (255, 215, 0), engine.bird.rect)  # Gold/Yellow
        
        # UI overlays
        if not engine.game_over:
            score_surf = self.font.render(f"Score: {engine.score}", True, (255, 255, 255))
            self.screen.blit(score_surf, (10, 10))
        else:
            game_over_surf = self.font.render("Game Over! Space to Restart", True, (255, 0, 0))
            text_rect = game_over_surf.get_rect(center=(self.settings.SCREEN_WIDTH//2, self.settings.SCREEN_HEIGHT//2))
            self.screen.blit(game_over_surf, text_rect)

        pygame.display.flip()
        
    def tick(self):
        """Regulate frame rate based on settings."""
        self.clock.tick(self.settings.FPS)

    def quit(self):
        """Closes renderer."""
        pygame.quit()
